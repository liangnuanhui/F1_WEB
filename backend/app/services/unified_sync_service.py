"""
统一数据同步服务
整合 FastF1 和 Ergast API 数据同步功能
"""

import logging
from typing import List, Optional, Dict, Any
from datetime import datetime
import pandas as pd
import time

from sqlalchemy.orm import Session
from fastf1.ergast import Ergast
import fastf1

from ..models import (
    Season, Circuit, Constructor, Driver, DriverSeason,
    Race, Result, QualifyingResult, SprintResult,
    DriverStanding, ConstructorStanding
)

logger = logging.getLogger(__name__)

# 目标赛季
TARGET_SEASONS = [2023, 2024, 2025]


class UnifiedSyncService:
    """统一数据同步服务"""
    
    def __init__(self, db: Session, cache_dir: Optional[str] = None):
        self.db = db
        self.ergast = Ergast()
        
        # 设置FastF1缓存
        if cache_dir:
            fastf1.Cache.enable_cache(cache_dir)
            logger.info(f"启用 FastF1 缓存目录: {cache_dir}")
        
        # 频率限制配置
        self.delays = {
            'basic': 0.5,      # 基础数据延迟
            'results': 1.0,    # 比赛结果延迟
            'standings': 1.5,  # 积分榜延迟
            'session': 2.0     # 会话数据延迟
        }
        
        logger.info("🚀 初始化统一数据同步服务")
    
    def _smart_delay(self, data_type: str = 'basic'):
        """智能延迟"""
        delay = self.delays.get(data_type, 1.0)
        time.sleep(delay)
    
    def _handle_api_call(self, func, *args, max_retries=3, **kwargs):
        """处理API调用的通用方法，支持分页获取完整数据并添加轮次信息"""
        for attempt in range(max_retries):
            try:
                result = func(*args, **kwargs)
                self._smart_delay('basic')
                
                # 区分并处理 SimpleResponse 和 MultiResponse 的分页
                if hasattr(result, 'get_next_result_page'):
                    all_dataframes = []
                    current_response = result
                    
                    page_num = 1
                    while current_response is not None:
                        logger.info(f"📄 正在处理API响应第 {page_num} 页...")
                        
                        if hasattr(current_response, 'content') and current_response.content is not None and not (isinstance(current_response.content, pd.DataFrame) and current_response.content.empty):
                            # 检查 content 是列表 (MultiResponse) 还是单个 DataFrame (SimpleResponse)
                            if isinstance(current_response.content, list):
                                # MultiResponse: .content 是 DataFrame 列表
                                logger.info(f"  - 检测到 MultiResponse，包含 {len(current_response.content)} 个 DataFrame")
                                for idx, result_df in enumerate(current_response.content):
                                    if idx < len(current_response.description):
                                        race_info = current_response.description.iloc[idx]
                                        # 检查 'round' 是否存在
                                        if 'round' in race_info:
                                            df_copy = result_df.copy()
                                            df_copy['round'] = int(race_info['round'])
                                            all_dataframes.append(df_copy)
                                        else:
                                            all_dataframes.append(result_df) # 没有轮次信息，直接添加
                                    else:
                                        logger.warning(f"⚠️ 无法为第 {idx} 个结果DataFrame找到描述信息")
                            else:
                                # SimpleResponse: .content 是单个 DataFrame
                                logger.info("  - 检测到 SimpleResponse")
                                all_dataframes.append(current_response.content)

                        # 尝试获取下一页
                        try:
                            if hasattr(current_response, 'is_complete') and current_response.is_complete:
                                logger.info("✅ API响应已包含所有结果，无需翻页")
                                break
                            current_response = current_response.get_next_result_page()
                            page_num += 1
                        except ValueError:
                            logger.info("✅ 已到达最后一页")
                            break # 没有更多页面了
                    
                    # 如果有多个 DataFrame，合并它们
                    if all_dataframes:
                        return pd.concat(all_dataframes, ignore_index=True)
                    else:
                        return pd.DataFrame()
                
                # 对于非 ErgastResponseMixin 的对象，或者没有分页需求的对象
                return result

            except Exception as e:
                error_str = str(e).lower()
                if 'rate' in error_str or 'limit' in error_str or '500 calls' in error_str:
                    if attempt < max_retries - 1:
                        delay = 2 ** attempt
                        logger.warning(f"API频率限制，等待 {delay} 秒后重试 ({attempt + 1}/{max_retries})")
                        time.sleep(delay)
                    else:
                        logger.error(f"达到最大重试次数: {e}")
                        raise
                else:
                    logger.error(f"API调用失败: {e}", exc_info=True)
                    raise
        return None
    
    def sync_seasons(self) -> List[Season]:
        """同步赛季数据"""
        logger.info("🔄 开始同步赛季数据...")
        
        seasons = []
        for year in TARGET_SEASONS:
            # 检查是否已存在
            existing = self.db.query(Season).filter(Season.year == year).first()
            if existing:
                logger.info(f"✅ 赛季 {year} 已存在，跳过")
                seasons.append(existing)
                continue
            
            # 创建新赛季
            season = Season(
                year=year,
                name=f"{year} Formula 1 World Championship",
                description=f"第{year}赛季F1世界锦标赛",
                start_date=datetime(year, 3, 1).date(),
                end_date=datetime(year, 11, 30).date(),
                is_current=(year == 2025),
                is_active=True
            )
            
            self.db.add(season)
            seasons.append(season)
            logger.info(f"✅ 创建赛季 {year}")
        
        self.db.commit()
        logger.info(f"✅ 赛季数据同步完成，共 {len(seasons)} 个赛季")
        return seasons
    
    def sync_circuits(self) -> List[Circuit]:
        """同步赛道数据 - 获取所有历史赛道以建立完整名录"""
        logger.info("🔄 开始同步赛道数据...")
        
        try:
            # 获取所有历史赛道数据
            circuits_df = self._handle_api_call(self.ergast.get_circuits)
            
            if circuits_df is None or circuits_df.empty:
                logger.warning("没有获取到赛道数据")
                return []
            
            circuits = []
            for _, row in circuits_df.iterrows():
                # 检查是否已存在
                existing = self.db.query(Circuit).filter(
                    Circuit.circuit_id == row['circuitId']
                ).first()
                
                if existing:
                    # 更新已有赛道的 is_active 状态，但不在这里设为 True
                    circuits.append(existing)
                    continue
                
                # 创建新赛道，is_active 默认为 False
                circuit = Circuit(
                    circuit_id=row['circuitId'],
                    circuit_url=row['circuitUrl'],
                    circuit_name=row['circuitName'],
                    lat=row['lat'],
                    long=row['long'],
                    locality=row['locality'],
                    country=row['country'],
                    is_active=False  # 默认设为非活跃
                )
                
                self.db.add(circuit)
                circuits.append(circuit)
                logger.info(f"✅ 创建新赛道: {row['circuitName']}")
            
            self.db.commit()
            logger.info(f"✅ 赛道数据同步完成，共处理 {len(circuits)} 个赛道")
            return circuits
            
        except Exception as e:
            logger.error(f"❌ 赛道数据同步失败: {e}")
            self.db.rollback()
            raise
    
    def sync_constructors(self) -> List[Constructor]:
        """同步车队数据"""
        logger.info("🔄 开始同步车队数据...")
        
        try:
            # 获取2025赛季的车队数据
            constructors_df = self._handle_api_call(self.ergast.get_constructor_info, season=2025)
            
            if constructors_df is None or constructors_df.empty:
                logger.warning("没有获取到车队数据")
                return []
            
            # 获取2025赛季
            season_2025 = self.db.query(Season).filter(Season.year == 2025).first()
            if not season_2025:
                raise ValueError("2025赛季不存在，请先同步赛季数据")
            
            constructors = []
            for _, row in constructors_df.iterrows():
                # 检查是否已存在
                existing = self.db.query(Constructor).filter(
                    Constructor.constructor_id == row['constructorId']
                ).first()
                
                if existing:
                    logger.info(f"✅ 车队 {row['constructorName']} 已存在，跳过")
                    constructors.append(existing)
                    continue
                
                # 创建新车队
                constructor = Constructor(
                    constructor_id=row['constructorId'],
                    constructor_url=row['constructorUrl'],
                    constructor_name=row['constructorName'],
                    constructor_nationality=row['constructorNationality'],
                    season_id=season_2025.id
                )
                
                self.db.add(constructor)
                constructors.append(constructor)
                logger.info(f"✅ 创建车队 {row['constructorName']}")
            
            self.db.commit()
            logger.info(f"✅ 车队数据同步完成，共 {len(constructors)} 个车队")
            return constructors
            
        except Exception as e:
            logger.error(f"❌ 车队数据同步失败: {e}")
            self.db.rollback()
            raise
    
    def sync_drivers(self) -> List[Driver]:
        """同步车手数据"""
        logger.info("🔄 开始同步车手数据...")
        
        try:
            # 获取2025赛季的车手数据
            drivers_df = self._handle_api_call(self.ergast.get_driver_info, season=2025)
            
            if drivers_df is None or drivers_df.empty:
                logger.warning("没有获取到车手数据")
                return []
            
            drivers = []
            for _, row in drivers_df.iterrows():
                # 检查是否已存在
                existing = self.db.query(Driver).filter(
                    Driver.driver_id == row['driverId']
                ).first()
                
                if existing:
                    logger.info(f"✅ 车手 {row['givenName']} {row['familyName']} 已存在，跳过")
                    drivers.append(existing)
                    continue
                
                # 处理出生日期
                date_of_birth = None
                if pd.notna(row['dateOfBirth']):
                    try:
                        date_of_birth = pd.to_datetime(row['dateOfBirth']).date()
                    except:
                        logger.warning(f"⚠️  无法解析车手 {row['givenName']} {row['familyName']} 的出生日期: {row['dateOfBirth']}")
                
                # 创建新车手
                driver = Driver(
                    driver_id=row['driverId'],
                    driver_number=row['driverNumber'],
                    driver_code=row['driverCode'],
                    driver_url=row['driverUrl'],
                    given_name=row['givenName'],
                    family_name=row['familyName'],
                    date_of_birth=date_of_birth,
                    driver_nationality=row['driverNationality']
                )
                
                self.db.add(driver)
                drivers.append(driver)
                logger.info(f"✅ 创建车手 {row['givenName']} {row['familyName']}")
            
            self.db.commit()
            logger.info(f"✅ 车手数据同步完成，共 {len(drivers)} 个车手")
            return drivers
            
        except Exception as e:
            logger.error(f"❌ 车手数据同步失败: {e}")
            self.db.rollback()
            raise
    
    def sync_races(self, season_year: int) -> List[Race]:
        """同步指定赛季的比赛数据"""
        logger.info(f"🔄 开始同步 {season_year} 赛季的比赛数据...")
        
        # 获取赛季对象
        season = self.db.query(Season).filter(Season.year == season_year).first()
        if not season:
            logger.error(f"❌ 赛季 {season_year} 不存在，无法同步比赛")
            return []

        try:
            # 优先使用 FastF1 获取详细日程
            try:
                logger.info(f"🏎️ 尝试使用 FastF1 获取 {season_year} 赛程...")
                schedule_df = fastf1.get_event_schedule(season_year, include_testing=False)
                if schedule_df.empty:
                    raise ValueError("FastF1 返回空赛程")
                logger.info("✅ FastF1 获取成功")
                source = 'fastf1'
            except Exception as e:
                logger.warning(f"⚠️ FastF1 获取失败 ({e})，降级到 Ergast...")
                schedule_df = self._handle_api_call(self.ergast.get_race_schedule, season=season_year)
                if schedule_df.empty:
                    logger.error(f"❌ Ergast 也无法获取 {season_year} 赛程")
                    return []
                source = 'ergast'

            races = []
            for _, row in schedule_df.iterrows():
                if source == 'fastf1':
                    circuit_id = row['Circuit'].get('circuitId')
                    circuit_name = row['Circuit'].get('circuitName')
                    race_name = row['EventName']
                    round_number = row['RoundNumber']
                    race_date = pd.to_datetime(row['EventDate']).date()
                    
                    # 处理会话时间
                    def handle_session_date(date_value):
                        if pd.isna(date_value):
                            return None
                        # FastF1 的时间可能已经是 datetime 对象
                        if isinstance(date_value, datetime):
                            return date_value
                        return pd.to_datetime(date_value)

                    fp1_date = handle_session_date(row.get('Session1DateUtc'))
                    fp2_date = handle_session_date(row.get('Session2DateUtc'))
                    fp3_date = handle_session_date(row.get('Session3DateUtc'))
                    qualifying_date = handle_session_date(row.get('Session4DateUtc'))
                    sprint_date = handle_session_date(row.get('Session5DateUtc')) if 'Session5DateUtc' in row and row['EventFormat'] == 'sprint' else None
                    race_time = handle_session_date(row.get('EventDate')) # 使用 EventDate 作为比赛时间
                    
                else: # ergast
                    circuit_id = row['Circuit']['circuitId']
                    circuit_name = row['Circuit']['circuitName']
                    race_name = row['raceName']
                    round_number = row['round']
                    race_date = pd.to_datetime(row['date']).date()
                    race_time = pd.to_datetime(f"{row['date']}T{row['time']}") if 'time' in row and row['time'] else pd.to_datetime(row['date'])
                    
                    fp1_date, fp2_date, fp3_date, qualifying_date, sprint_date = None, None, None, None, None

                # 查找赛道，并将其激活
                circuit = self.db.query(Circuit).filter(Circuit.circuit_id == circuit_id).first()
                if not circuit:
                    logger.warning(f"⚠️ 赛道 {circuit_name} (ID: {circuit_id}) 不在数据库中，跳过此比赛")
                    continue
                
                # 激活赛道
                circuit.is_active = True

                # 检查比赛是否已存在
                existing_race = self.db.query(Race).filter(
                    Race.season_id == season.id,
                    Race.round_number == round_number
                ).first()

                if existing_race:
                    # 更新已有比赛信息
                    logger.info(f"  - 更新比赛: 第 {round_number} 轮 - {race_name}")
                    existing_race.race_name = race_name
                    existing_race.circuit_id = circuit.id
                    existing_race.race_date = race_date
                    existing_race.race_time = race_time
                    existing_race.fp1_date = fp1_date
                    existing_race.fp2_date = fp2_date
                    existing_race.fp3_date = fp3_date
                    existing_race.qualifying_date = qualifying_date
                    existing_race.sprint_date = sprint_date
                    existing_race.is_sprint = 'sprint' in row.get('EventFormat', '')
                    races.append(existing_race)
                else:
                    # 创建新比赛
                    logger.info(f"  - 创建比赛: 第 {round_number} 轮 - {race_name}")
                    new_race = Race(
                        season_id=season.id,
                        round_number=round_number,
                        race_name=race_name,
                        circuit_id=circuit.id,
                        race_date=race_date,
                        race_time=race_time,
                        fp1_date=fp1_date,
                        fp2_date=fp2_date,
                        fp3_date=fp3_date,
                        qualifying_date=qualifying_date,
                        sprint_date=sprint_date,
                        is_sprint='sprint' in row.get('EventFormat', '')
                    )
                    self.db.add(new_race)
                    races.append(new_race)

            self.db.commit()
            logger.info(f"✅ {season_year} 赛季比赛数据同步完成，共 {len(races)} 场比赛")
            return races
        except Exception as e:
            logger.error(f"❌ {season_year} 赛季比赛数据同步失败: {e}", exc_info=True)
            self.db.rollback()
            return []
    
    def sync_race_results(self, season_year: int) -> bool:
        """同步指定赛季的比赛结果"""
        logger.info(f"🔄 开始同步 {season_year} 赛季的比赛结果...")
        
        races = self.db.query(Race).join(Season).filter(Season.year == season_year).all()
        if not races:
            logger.warning(f"没有为 {season_year} 赛季找到比赛记录，跳过比赛结果同步")
            return True

        try:
            all_results_df = self._handle_api_call(
                self.ergast.get_race_results,
                season=season_year,
                round=None
            )
            
            if all_results_df is None or all_results_df.empty:
                logger.warning(f"Ergast API 未返回 {season_year} 赛季的比赛结果")
                return True
            
            for round_number, group_df in all_results_df.groupby('round'):
                race = next((r for r in races if r.round_number == round_number), None)
                if not race:
                    logger.warning(f"⚠️ 未找到赛季 {season_year} 第 {round_number} 轮的比赛记录，跳过结果同步")
                    continue
                
                existing_count = self.db.query(Result).filter(Result.race_id == race.id).count()
                if existing_count > 0:
                    logger.info(f"  - 第 {race.round_number} 轮比赛结果已存在 {existing_count} 条，跳过")
                    continue

                logger.info(f"🔄 处理第 {round_number} 轮比赛结果: {race.race_name} ({len(group_df)}条记录)")

                for _, row in group_df.iterrows():
                    driver = self._get_or_create_driver_from_result(row)
                    constructor = self._get_or_create_constructor_from_result(row)
                    
                    if not driver or not constructor:
                        continue

                    def safe_int(value):
                        try: return int(value)
                        except (ValueError, TypeError): return None

                    def safe_float(value):
                        try: return float(value)
                        except (ValueError, TypeError): return None

                    def safe_str(value):
                        return str(value) if pd.notna(value) else None

                    result = Result(
                        race_id=race.id, driver_id=driver.id, constructor_id=constructor.id,
                        number=safe_int(row.get('number')), position=safe_int(row.get('position')),
                        position_text=safe_str(row.get('positionText')), points=safe_float(row.get('points')),
                        grid=safe_int(row.get('grid')), laps=safe_int(row.get('laps')),
                        status=safe_str(row.get('status')), time=safe_str(row.get('time')),
                        fastest_lap=safe_int(row.get('fastestLap')), fastest_lap_time=safe_str(row.get('fastestLapTime')),
                        fastest_lap_speed=safe_float(row.get('fastestLapSpeed'))
                    )
                    self.db.add(result)
            
            self.db.commit()
            logger.info(f"✅ {season_year} 赛季比赛结果同步完成")
            return True
        except Exception as e:
            logger.error(f"❌ 比赛结果同步失败 (赛季: {season_year}): {e}", exc_info=True)
            self.db.rollback()
            return False
    
    def sync_qualifying_results(self, season_year: int) -> bool:
        """同步指定赛季的排位赛结果"""
        logger.info(f"🔄 开始同步 {season_year} 赛季的排位赛结果...")
        
        races = self.db.query(Race).join(Season).filter(Season.year == season_year).all()
        if not races:
            logger.warning(f"没有为 {season_year} 赛季找到比赛记录，跳过排位赛结果同步")
            return True

        try:
            all_results_df = self._handle_api_call(
                self.ergast.get_qualifying_results,
                season=season_year,
                round=None
            )
            
            if all_results_df is None or all_results_df.empty:
                logger.warning(f"Ergast API 未返回 {season_year} 赛季的排位赛结果")
                return True

            for round_number, group_df in all_results_df.groupby('round'):
                race = next((r for r in races if r.round_number == round_number), None)
                if not race:
                    logger.warning(f"⚠️ 未找到赛季 {season_year} 第 {round_number} 轮的比赛记录，跳过排位赛结果同步")
                    continue
                
                existing_count = self.db.query(QualifyingResult).filter(QualifyingResult.race_id == race.id).count()
                if existing_count > 0:
                    logger.info(f"  - 第 {race.round_number} 轮排位赛结果已存在 {existing_count} 条，跳过")
                    continue
                
                logger.info(f"🔄 处理第 {round_number} 轮排位赛: {race.race_name} ({len(group_df)}条记录)")

                for _, row in group_df.iterrows():
                    driver = self._get_or_create_driver_from_result(row)
                    constructor = self._get_or_create_constructor_from_result(row)

                    if not driver or not constructor:
                        continue
                    
                    def safe_str(value):
                        return str(value) if pd.notna(value) else None

                    qualifying_result = QualifyingResult(
                        race_id=race.id, driver_id=driver.id, constructor_id=constructor.id,
                        number=int(row['number']), position=int(row['position']),
                        q1=safe_str(row.get('Q1')), q2=safe_str(row.get('Q2')), q3=safe_str(row.get('Q3'))
                    )
                    self.db.add(qualifying_result)

            self.db.commit()
            logger.info(f"✅ {season_year} 赛季排位赛结果同步完成")
            return True
        except Exception as e:
            logger.error(f"❌ 排位赛结果同步失败 (赛季: {season_year}): {e}", exc_info=True)
            self.db.rollback()
            return False
    
    def sync_sprint_results(self, season_year: int) -> bool:
        """同步指定赛季的冲刺赛结果"""
        logger.info(f"🔄 开始同步 {season_year} 赛季的冲刺赛结果...")

        races_with_sprint = self.db.query(Race).join(Season).filter(Season.year == season_year, Race.is_sprint == True).all()
        if not races_with_sprint:
            logger.info(f"{season_year} 赛季没有冲刺赛，跳过")
            return True

        try:
            all_results_df = self._handle_api_call(
                self.ergast.get_sprint_results,
                season=season_year,
                round=None
            )
            
            if all_results_df is None or all_results_df.empty:
                logger.warning(f"Ergast API 未返回 {season_year} 赛季的冲刺赛结果")
                return True
            
            sprint_rounds = {r.round_number for r in races_with_sprint}
            for round_number, group_df in all_results_df.groupby('round'):
                if round_number not in sprint_rounds:
                    continue

                race = next((r for r in races_with_sprint if r.round_number == round_number), None)
                if not race:
                    continue

                existing_count = self.db.query(SprintResult).filter(SprintResult.race_id == race.id).count()
                if existing_count > 0:
                    logger.info(f"  - 第 {race.round_number} 轮冲刺赛结果已存在 {existing_count} 条，跳过")
                    continue
                
                logger.info(f"🔄 处理第 {round_number} 轮冲刺赛: {race.race_name} ({len(group_df)}条记录)")
                
                for _, row in group_df.iterrows():
                    driver = self._get_or_create_driver_from_result(row)
                    constructor = self._get_or_create_constructor_from_result(row)
                    
                    if not driver or not constructor:
                        continue

                    def safe_int(value):
                        try: return int(value)
                        except (ValueError, TypeError): return None
                    
                    def safe_float(value):
                        try: return float(value)
                        except (ValueError, TypeError): return None

                    def safe_str(value):
                        return str(value) if pd.notna(value) else None

                    sprint_result = SprintResult(
                        race_id=race.id, driver_id=driver.id, constructor_id=constructor.id,
                        number=safe_int(row.get('number')), position=safe_int(row.get('position')),
                        position_text=safe_str(row.get('positionText')), points=safe_float(row.get('points')),
                        grid=safe_int(row.get('grid')), laps=safe_int(row.get('laps')),
                        status=safe_str(row.get('status')), time=safe_str(row.get('time')),
                    )
                    self.db.add(sprint_result)
            
            self.db.commit()
            logger.info(f"✅ {season_year} 赛季冲刺赛结果同步完成")
            return True
        except Exception as e:
            logger.error(f"❌ 冲刺赛结果同步失败 (赛季: {season_year}): {e}", exc_info=True)
            self.db.rollback()
            return False
    
    def sync_driver_standings(self, season_year: int) -> bool:
        """同步指定赛季的车手积分榜"""
        logger.info(f"🔄 开始同步 {season_year} 赛季的车手积分榜...")
        
        try:
            standings_df = self._handle_api_call(
                self.ergast.get_driver_standings,
                season=season_year,
                round=None
            )
            
            if standings_df is None or standings_df.empty:
                logger.warning(f"Ergast API 未返回 {season_year} 赛季的车手积分榜")
                return True

            self.db.query(DriverStanding).filter(DriverStanding.season.has(year=season_year)).delete()
            
            season = self.db.query(Season).filter(Season.year == season_year).first()
            if not season:
                logger.error(f"无法找到赛季 {season_year} 用于同步车手积分榜")
                return False

            for _, row in standings_df.iterrows():
                driver = self._get_or_create_driver_from_result(row)
                constructor = self._get_or_create_constructor_from_result(row)

                if not driver or not constructor:
                    continue

                standing = DriverStanding(
                    season_id=season.id,
                    driver_id=driver.id,
                    constructor_id=constructor.id,
                    round=int(row['round']),
                    position=int(row['position']),
                    position_text=str(row['positionText']),
                    points=float(row['points']),
                    wins=int(row['wins'])
                )
                self.db.add(standing)
            
            self.db.commit()
            logger.info(f"✅ {season_year} 赛季车手积分榜同步完成")
            return True
        except Exception as e:
            logger.error(f"❌ 车手积分榜同步失败 (赛季: {season_year}): {e}", exc_info=True)
            self.db.rollback()
            return False
    
    def sync_constructor_standings(self, season_year: int) -> bool:
        """同步指定赛季的车队积分榜"""
        logger.info(f"🔄 开始同步 {season_year} 赛季的车队积分榜...")
        
        try:
            standings_df = self._handle_api_call(
                self.ergast.get_constructor_standings,
                season=season_year,
                round=None
            )
            
            if standings_df is None or standings_df.empty:
                logger.warning(f"Ergast API 未返回 {season_year} 赛季的车队积分榜")
                return True
            
            self.db.query(ConstructorStanding).filter(ConstructorStanding.season.has(year=season_year)).delete()

            season = self.db.query(Season).filter(Season.year == season_year).first()
            if not season:
                logger.error(f"无法找到赛季 {season_year} 用于同步车队积分榜")
                return False

            for _, row in standings_df.iterrows():
                constructor = self._get_or_create_constructor_from_result(row)
                if not constructor:
                    continue
                
                standing = ConstructorStanding(
                    season_id=season.id,
                    constructor_id=constructor.id,
                    round=int(row['round']),
                    position=int(row['position']),
                    position_text=str(row['positionText']),
                    points=float(row['points']),
                    wins=int(row['wins'])
                )
                self.db.add(standing)

            self.db.commit()
            logger.info(f"✅ {season_year} 赛季车队积分榜同步完成")
            return True
        except Exception as e:
            logger.error(f"❌ 车队积分榜同步失败 (赛季: {season_year}): {e}", exc_info=True)
            self.db.rollback()
            return False
    
    def _get_or_create_driver_from_result(self, row: pd.Series) -> Optional[Driver]:
        """从比赛结果行中获取或创建车手"""
        driver_id = row.get('driverId')
        if not driver_id:
            return None
        
        driver = self.db.query(Driver).filter(Driver.driver_id == driver_id).first()
        if not driver:
            # 创建新车手
            driver = Driver(
                driver_id=driver_id,
                driver_number=row.get('driverNumber'),
                driver_code=row.get('driverCode'),
                driver_url=row.get('driverUrl', ''),
                given_name=row.get('givenName', ''),
                family_name=row.get('familyName', ''),
                date_of_birth=row.get('dateOfBirth'),
                driver_nationality=row.get('nationality', '')
            )
            self.db.add(driver)
            self.db.commit()
        
        return driver
    
    def _get_or_create_constructor_from_result(self, row: pd.Series) -> Optional[Constructor]:
        """从比赛结果行中获取或创建车队"""
        # 尝试多个可能的字段名
        constructor_id = row.get('constructorId') or row.get('constructorIds')
        if not constructor_id:
            return None
        
        # 处理 constructorId 可能是列表的情况（如积分榜数据）
        if isinstance(constructor_id, list):
            if len(constructor_id) > 0:
                constructor_id = constructor_id[0]  # 取第一个车队
            else:
                return None
        
        constructor = self.db.query(Constructor).filter(Constructor.constructor_id == constructor_id).first()
        if not constructor:
            # 获取2025赛季作为默认赛季
            season_2025 = self.db.query(Season).filter(Season.year == 2025).first()
            if not season_2025:
                logger.error("找不到2025赛季记录")
                return None
            
            # 创建新车队
            constructor = Constructor(
                constructor_id=constructor_id,
                constructor_url=row.get('constructorUrl', ''),
                constructor_name=row.get('constructorName', ''),
                constructor_nationality=row.get('constructorNationality', ''),
                season_id=season_2025.id
            )
            self.db.add(constructor)
            self.db.commit()
        
        return constructor
    
    def sync_all_data(self, target_seasons: Optional[List[int]] = None):
        """
        完整数据同步流程
        1. 同步核心静态数据（赛季、赛道、车队、车手）
        2. 遍历指定赛季，同步动态数据（比赛、结果、积分榜）
        """
        if target_seasons is None:
            target_seasons = TARGET_SEASONS
        
        logger.info(f"🚀 统一数据同步流程启动，目标赛季: {target_seasons}")

        try:
            # 步骤 1: 同步核心静态数据
            self.sync_seasons()
            self.sync_circuits()
            self.sync_constructors()
            self.sync_drivers()

            # 步骤 2: 重置所有赛道的 active 状态
            logger.info("🔄 重置所有赛道的激活状态...")
            self.db.query(Circuit).update({"is_active": False})
            self.db.commit()
            
            # 步骤 3: 遍历赛季，同步动态数据
            for year in target_seasons:
                logger.info(f"▶️ 开始处理赛季: {year}")
                
                # 同步比赛日程，这将激活赛道
                self.sync_races(year)
                
                # 同步各类比赛结果和积分榜
                self.sync_race_results(year)
                self.sync_qualifying_results(year)
                self.sync_sprint_results(year)
                self.sync_driver_standings(year)
                self.sync_constructor_standings(year)
                
                logger.info(f"✅ 赛季 {year} 处理完成")

            logger.info("🎉 恭喜！所有指定赛季的数据同步成功！")

        except Exception as e:
            logger.error(f"❌ 统一数据同步流程失败: {e}", exc_info=True)
            self.db.rollback()
        finally:
            self.db.close()
            logger.info("🔒 数据库会话已关闭") 