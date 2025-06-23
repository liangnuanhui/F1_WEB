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
                
                # 如果是 ErgastMultiResponse，需要处理分页和多个 DataFrame
                if hasattr(result, 'content') and hasattr(result, 'get_next_result_page'):
                    all_dataframes = []
                    current_response = result
                    
                    page_num = 1
                    while current_response is not None:
                        logger.info(f"📄 正在处理API响应第 {page_num} 页...")
                        if hasattr(current_response, 'content') and current_response.content:
                            # 关键修复：从 description 中提取 round，并添加到每个 DataFrame
                            for idx, result_df in enumerate(current_response.content):
                                if idx < len(current_response.description):
                                    race_info = current_response.description.iloc[idx]
                                    round_num = int(race_info['round'])
                                    
                                    df_copy = result_df.copy()
                                    df_copy['round'] = round_num
                                    all_dataframes.append(df_copy)
                                else:
                                    logger.warning(f"⚠️ 无法为第 {idx} 个结果DataFrame找到描述信息")

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
        """同步赛道数据"""
        logger.info("🔄 开始同步赛道数据...")
        
        try:
            # 获取2025赛季的赛道数据作为基础
            circuits_df = self._handle_api_call(self.ergast.get_circuits, season=2025)
            
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
                    logger.info(f"✅ 赛道 {row['circuitName']} 已存在，跳过")
                    circuits.append(existing)
                    continue
                
                # 创建新赛道
                circuit = Circuit(
                    circuit_id=row['circuitId'],
                    circuit_url=row['circuitUrl'],
                    circuit_name=row['circuitName'],
                    lat=row['lat'],
                    long=row['long'],
                    locality=row['locality'],
                    country=row['country']
                )
                
                self.db.add(circuit)
                circuits.append(circuit)
                logger.info(f"✅ 创建赛道 {row['circuitName']}")
            
            self.db.commit()
            logger.info(f"✅ 赛道数据同步完成，共 {len(circuits)} 个赛道")
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
        """同步比赛数据"""
        logger.info(f"🔄 开始同步 {season_year} 赛季比赛数据...")
        
        try:
            # 获取赛季
            season = self.db.query(Season).filter(Season.year == season_year).first()
            if not season:
                raise ValueError(f"赛季 {season_year} 不存在")
            
            # 获取FastF1的比赛日程
            races_df = self._handle_api_call(fastf1.get_event_schedule, season_year)
            
            if races_df is None or races_df.empty:
                logger.warning(f"没有获取到 {season_year} 赛季的比赛数据")
                return []
            
            logger.info(f"📊 FastF1返回 {len(races_df)} 场比赛")
            
            # 获取所有赛道用于匹配
            all_circuits = {circuit.circuit_name: circuit for circuit in self.db.query(Circuit).all()}
            logger.info(f"📊 数据库中有 {len(all_circuits)} 个赛道")
            
            # FastF1地点名称到数据库赛道名称的映射
            location_to_circuit_mapping = {
                'Melbourne': 'Albert Park Grand Prix Circuit',
                'Sakhir': 'Bahrain International Circuit',
                'Shanghai': 'Shanghai International Circuit',
                'Suzuka': 'Suzuka Circuit',
                'Jeddah': 'Jeddah Corniche Circuit',
                'Miami': 'Miami International Autodrome',
                'Imola': 'Autodromo Enzo e Dino Ferrari',
                'Monaco': 'Circuit de Monaco',
                'Barcelona': 'Circuit de Barcelona-Catalunya',
                'Montréal': 'Circuit Gilles Villeneuve',
                'Spielberg': 'Red Bull Ring',
                'Silverstone': 'Silverstone Circuit',
                'Spa-Francorchamps': 'Circuit de Spa-Francorchamps',
                'Budapest': 'Hungaroring',
                'Zandvoort': 'Circuit Park Zandvoort',
                'Monza': 'Autodromo Nazionale di Monza',
                'Baku': 'Baku City Circuit',
                'Marina Bay': 'Marina Bay Street Circuit',
                'Austin': 'Circuit of the Americas',
                'Mexico City': 'Autódromo Hermanos Rodríguez',
                'São Paulo': 'Autódromo José Carlos Pace',
                'Las Vegas': 'Las Vegas Strip Street Circuit',
                'Lusail': 'Losail International Circuit',
                'Yas Island': 'Yas Marina Circuit'
            }
            
            races = []
            skipped_count = 0
            
            for _, row in races_df.iterrows():
                # 检查是否已存在
                existing = self.db.query(Race).filter(
                    Race.season_id == season.id,
                    Race.round_number == row['RoundNumber']
                ).first()
                
                if existing:
                    logger.info(f"✅ 比赛 {row['OfficialEventName']} 已存在，跳过")
                    races.append(existing)
                    continue
                
                # 查找对应的赛道 - 使用映射表
                circuit = None
                location = str(row['Location']) if pd.notna(row['Location']) else ''
                
                # 使用映射表查找
                if location in location_to_circuit_mapping:
                    circuit_name = location_to_circuit_mapping[location]
                    if circuit_name in all_circuits:
                        circuit = all_circuits[circuit_name]
                    else:
                        logger.warning(f"⚠️  映射的赛道名称不存在: {circuit_name}")
                else:
                    logger.warning(f"⚠️  未找到地点映射: {location}")
                
                if not circuit:
                    logger.warning(f"⚠️  未找到赛道: {location} (比赛: {row['OfficialEventName']})")
                    skipped_count += 1
                    continue
                
                # 处理比赛日期
                event_date = None
                if pd.notna(row['EventDate']):
                    try:
                        event_date = pd.to_datetime(row['EventDate']).date()
                    except:
                        logger.warning(f"⚠️  无法解析比赛日期: {row['EventDate']}")
                        event_date = datetime(season_year, 3, 1).date()
                else:
                    event_date = datetime(season_year, 3, 1).date()
                
                # 处理会话日期，将NaT转换为None
                def handle_session_date(date_value):
                    if pd.isna(date_value) or pd.isna(pd.to_datetime(date_value, errors='coerce')):
                        return None
                    try:
                        return pd.to_datetime(date_value)
                    except:
                        return None
                
                # 创建新比赛
                race = Race(
                    season_id=season.id,
                    circuit_id=circuit.circuit_id,
                    round_number=row['RoundNumber'],
                    country=row['Country'],
                    location=row['Location'],
                    official_event_name=row['OfficialEventName'],
                    event_date=event_date,
                    event_format=row['EventFormat'],
                    # 根据EventFormat设置is_sprint
                    is_sprint=row['EventFormat'] == 'sprint_qualifying',
                    session1=row.get('Session1'),
                    session1_date=handle_session_date(row.get('Session1Date')),
                    session2=row.get('Session2'),
                    session2_date=handle_session_date(row.get('Session2Date')),
                    session3=row.get('Session3'),
                    session3_date=handle_session_date(row.get('Session3Date')),
                    session4=row.get('Session4'),
                    session4_date=handle_session_date(row.get('Session4Date')),
                    session5=row.get('Session5'),
                    session5_date=handle_session_date(row.get('Session5Date'))
                )
                
                # 添加冲刺赛识别日志
                if row['EventFormat'] == 'sprint_qualifying':
                    logger.info(f"🏁 识别冲刺赛: 第{row['RoundNumber']}轮 {row['OfficialEventName']}")
                
                self.db.add(race)
                races.append(race)
                logger.info(f"✅ 创建比赛 第{row['RoundNumber']}轮: {row['OfficialEventName']} - {location}")
            
            self.db.commit()
            logger.info(f"✅ {season_year} 赛季比赛数据同步完成，共 {len(races)} 场比赛，跳过 {skipped_count} 场")
            return races
            
        except Exception as e:
            logger.error(f"❌ 比赛数据同步失败: {e}")
            self.db.rollback()
            raise
    
    def sync_race_results(self, season_year: int) -> bool:
        """同步比赛结果，并创建 DriverSeason 记录"""
        logger.info(f"🔄 开始同步 {season_year} 赛季的比赛结果...")
        
        try:
            season = self.db.query(Season).filter(Season.year == season_year).first()
            if not season:
                logger.error(f"❌ 赛季 {season_year} 不存在，无法同步比赛结果")
                return False

            races = self.db.query(Race).filter(Race.season_id == season.id).order_by(Race.round_number).all()
            if not races:
                logger.warning(f"⚠️ 赛季 {season_year} 没有比赛，跳过结果同步")
                return True

            logger.info(f"赛季 {season_year} 共有 {len(races)} 场比赛，开始同步结果...")

            for race in races:
                logger.info(f"  🔄 同步比赛: {race.official_event_name} (Round {race.round_number})")
                self._smart_delay('results')

                # 检查此比赛是否已有结果数据，避免重复处理
                existing_result_count = self.db.query(Result).filter(Result.race_id == race.id).count()
                if existing_result_count > 0:
                    logger.info(f"    - 比赛 {race.official_event_name} 已有 {existing_result_count} 条结果，跳过")
                    continue

                # 获取比赛结果
                results_df = self._handle_api_call(
                    self.ergast.get_race_results,
                    season=season_year,
                    round=race.round_number
                )
                
                if results_df is None or results_df.empty:
                    logger.warning(f"    - 比赛 {race.official_event_name} API未返回结果数据，跳过")
                    continue
                
                results_added_count = 0
                for _, row in results_df.iterrows():
                    # 获取车手和车队
                    driver = self._get_or_create_driver_from_result(row)
                    constructor = self._get_or_create_constructor_from_result(row)
                    
                    if not driver or not constructor:
                        logger.warning("    - 无法获取或创建车手/车队实体，跳过此条结果")
                        continue
                        
                    # 检查并创建 DriverSeason 记录
                    existing_driver_season = self.db.query(DriverSeason).filter_by(
                        driver_id=driver.driver_id,
                        constructor_id=constructor.constructor_id,
                        season_id=season.id
                    ).first()

                    if not existing_driver_season:
                        driver_season = DriverSeason(
                            driver_id=driver.driver_id,
                            constructor_id=constructor.constructor_id,
                            season_id=season.id
                        )
                        self.db.add(driver_season)
                        logger.info(f"      -> 新增 DriverSeason: {driver.given_name} {driver.family_name} 为 {constructor.constructor_name} ({season.year})")

                    # 创建比赛结果记录
                    result = Result(
                        race_id=race.id,
                        driver_id=driver.driver_id,
                        constructor_id=constructor.constructor_id,
                        number=row.get('number'),
                        position=row.get('position'),
                        position_text=row.get('positionText'),
                        points=row.get('points'),
                        grid=row.get('grid'),
                        laps=row.get('laps'),
                        status=row.get('status'),
                        total_race_time=row.get('totalRaceTime'),
                        total_race_time_millis=row.get('totalRaceTimeMillis'),
                        fastest_lap_rank=row.get('fastestLapRank'),
                        fastest_lap_number=row.get('fastestLapNumber'),
                        fastest_lap_time=row.get('fastestLapTime')
                    )
                    self.db.add(result)
                    results_added_count += 1

                if results_added_count > 0:
                    logger.info(f"    - 为比赛 {race.official_event_name} 添加了 {results_added_count} 条新结果")
                
                self.db.commit() # 在处理完一场比赛的所有结果后提交

            logger.info(f"✅ {season_year} 赛季比赛结果同步完成")
            return True
            
        except Exception as e:
            logger.error(f"❌ 同步 {season_year} 赛季比赛结果时发生严重错误: {e}", exc_info=True)
            self.db.rollback()
            return False
    
    def sync_qualifying_results(self, season_year: int) -> bool:
        """同步排位赛结果数据，并正确处理分页"""
        logger.info(f"🏁 开始同步 {season_year} 赛季排位赛结果...")
        
        try:
            season = self.db.query(Season).filter(Season.year == season_year).first()
            if not season:
                logger.error(f"❌ 赛季 {season_year} 不存在，无法同步排位赛结果")
                return False

            # 1. 获取所有比赛的排位赛结果，支持分页
            all_qualifying_results_df = self._handle_api_call(
                self.ergast.get_qualifying_results, 
                season=season_year
            )

            if all_qualifying_results_df is None or all_qualifying_results_df.empty:
                logger.warning(f"没有获取到 {season_year} 赛季的排位赛结果数据")
                return True # 没有数据也算成功

            logger.info(f"📊 成功从API获取 {len(all_qualifying_results_df)} 条排位赛记录")

            # 2. 准备数据库数据
            races_db = self.db.query(Race).filter(Race.season_id == season.id).all()
            races_by_round = {race.round_number: race for race in races_db}
            
            # 3. 清除旧数据
            race_ids = [race.id for race in races_db]
            if race_ids:
                self.db.query(QualifyingResult).filter(QualifyingResult.race_id.in_(race_ids)).delete()
                logger.info(f"🧹 清除了赛季 {season_year} 的旧排位赛结果")
            
            total_results = 0
            
            # 按轮次分组处理数据
            for round_number, group_df in all_qualifying_results_df.groupby('round'):
                race = races_by_round.get(round_number)
                if not race:
                    logger.warning(f"⚠️ 找不到第 {round_number} 轮比赛，跳过该轮排位赛结果")
                    continue
                
                logger.info(f"🔄 处理第 {round_number} 轮排位赛: {race.official_event_name} ({len(group_df)}条记录)")

                for _, row in group_df.iterrows():
                    driver = self._get_or_create_driver_from_result(row)
                    constructor = self._get_or_create_constructor_from_result(row)
                    
                    if not driver or not constructor:
                        logger.warning(f"⚠️ 无法获取车手或车队信息，跳过记录: {row.get('driverId')}")
                        continue
                    
                    # 使用我们之前定义的 safe_* 函数来处理潜在的 None 或 NaN 值
                    def safe_str(value):
                        if pd.isna(value) or value is None: return None
                        return str(value)

                    qualifying_result = QualifyingResult(
                        race_id=race.id,
                        driver_id=driver.driver_id,
                        constructor_id=constructor.constructor_id,
                        number=row.get('number'),
                        position=row.get('position'),
                        q1_time=safe_str(row.get('q1')),
                        q2_time=safe_str(row.get('q2')),
                        q3_time=safe_str(row.get('q3'))
                    )
                    
                    self.db.add(qualifying_result)
                    total_results += 1
            
            self.db.commit()
            logger.info(f"✅ {season_year} 赛季排位赛结果同步完成，共 {total_results} 条记录")
            return True
            
        except Exception as e:
            logger.error(f"❌ 排位赛结果同步失败: {e}", exc_info=True)
            self.db.rollback()
            return False
    
    def sync_sprint_results(self, season_year: int) -> bool:
        """同步冲刺赛结果数据，并正确处理分页"""
        logger.info(f"🏁 开始同步 {season_year} 赛季冲刺赛结果...")
        
        try:
            # 获取赛季对象
            season = self.db.query(Season).filter(Season.year == season_year).first()
            if not season:
                logger.error(f"❌ 赛季 {season_year} 不存在，无法同步冲刺赛结果")
                return False
            
            # 1. 获取所有冲刺赛结果页面，并按轮次组织数据
            all_sprints_by_round = {}  # {round_number: [df_page1, df_page2, ...]}
            
            try:
                current_response = self.ergast.get_sprint_results(season=season_year)
                logger.info("📡 成功从 API 获取第一页冲刺赛数据")
            except Exception as e:
                logger.error(f"❌ 调用API获取冲刺赛数据失败: {e}", exc_info=True)
                return False

            page_num = 1
            while current_response:
                logger.info(f"📄 处理第 {page_num} 页API响应...")
                
                if hasattr(current_response, 'content') and current_response.content:
                    logger.info(f"  - 页面包含 {len(current_response.content)} 个冲刺赛事件的DataFrame")
                    for idx, result_df in enumerate(current_response.content):
                        if idx < len(current_response.description):
                            race_info = current_response.description.iloc[idx]
                            round_number = int(race_info['round'])
                            if round_number not in all_sprints_by_round:
                                all_sprints_by_round[round_number] = []
                            all_sprints_by_round[round_number].append(result_df)
                            logger.info(f"    - 提取到第 {round_number} 轮的数据")
                        else:
                            logger.warning(f"  - ⚠️ 无法为第 {idx} 个结果DataFrame找到描述信息")
                else:
                    logger.info("  - 页面没有 'content' 或内容为空")

                # 尝试获取下一页
                try:
                    if hasattr(current_response, 'is_complete') and current_response.is_complete:
                        logger.info("✅ API响应已包含所有结果，无需翻页")
                        break
                    
                    logger.info("  - 尝试获取下一页...")
                    current_response = current_response.get_next_result_page()
                    page_num += 1
                except ValueError:
                    logger.info("✅ 已到达最后一页")
                    break
                except Exception as e:
                    logger.warning(f"⚠️ 获取下一页数据时出错: {e}")
                    break

            # 2. 准备数据库数据
            sprint_races_db = self.db.query(Race).filter(
                Race.season_id == season.id,
                Race.is_sprint == True
            ).all()
            races_by_round = {race.round_number: race for race in sprint_races_db}
            logger.info(f"📊 数据库中找到 {len(races_by_round)} 场冲刺赛: {sorted(list(races_by_round.keys()))}")
            
            # 3. 清除旧数据
            race_ids = [race.id for race in sprint_races_db]
            if race_ids:
                self.db.query(SprintResult).filter(SprintResult.race_id.in_(race_ids)).delete()
                logger.info(f"🧹 清除了赛季 {season_year} 的旧冲刺赛结果")

            total_results = 0
            sprint_count = 0

            # 4. 处理收集到的所有数据
            for round_number, dfs in all_sprints_by_round.items():
                race = races_by_round.get(round_number)
                if not race:
                    logger.warning(f"⚠️ 第 {round_number} 轮的冲刺赛在数据库中未找到，跳过")
                    continue
                
                # 合并该轮次的所有DataFrame
                sprint_df = pd.concat(dfs, ignore_index=True)
                
                logger.info(f"🔄 处理第 {round_number} 轮冲刺赛: {race.official_event_name} ({len(sprint_df)}条记录)")
                sprint_count += 1
                
                for _, row in sprint_df.iterrows():
                    driver = self._get_or_create_driver_from_result(row)
                    constructor = self._get_or_create_constructor_from_result(row)
                    
                    if not driver or not constructor:
                        logger.warning(f"⚠️ 无法获取车手或车队信息，跳过记录: {row.get('driverId')}")
                        continue
                    
                    def safe_int(value):
                        if pd.isna(value) or value is None: return None
                        try: return int(float(value))
                        except (ValueError, TypeError): return None
                    
                    def safe_float(value):
                        if pd.isna(value) or value is None: return 0.0
                        try: return float(value)
                        except (ValueError, TypeError): return 0.0
                    
                    def safe_str(value):
                        if pd.isna(value) or value is None: return ''
                        try: return str(value)
                        except: return ''
                    
                    sprint_result = SprintResult(
                        race_id=race.id,
                        driver_id=driver.driver_id,
                        constructor_id=constructor.constructor_id,
                        number=safe_int(row.get('number')),
                        position=safe_int(row.get('position')),
                        position_text=safe_str(row.get('positionText')),
                        points=safe_float(row.get('points')),
                        grid=safe_int(row.get('grid')),
                        status=safe_str(row.get('status')),
                        laps=safe_int(row.get('laps')),
                        fastest_lap_time=safe_str(row.get('fastestLapTime')),
                        fastest_lap_rank=safe_int(row.get('fastestLapRank')),
                        fastest_lap_number=safe_int(row.get('fastestLapNumber')),
                        total_race_time=safe_str(row.get('totalRaceTime')),
                        total_race_time_millis=safe_int(row.get('totalRaceTimeMillis'))
                    )
                    
                    self.db.add(sprint_result)
                    total_results += 1
                
                logger.info(f"  ✅ 第 {race.round_number} 轮冲刺赛结果处理完成")

            self.db.commit()
            self._smart_delay('results')
            logger.info(f"✅ {season_year} 赛季冲刺赛结果同步完成，共 {sprint_count} 场冲刺赛，{total_results} 条记录")
            return True
            
        except Exception as e:
            logger.error(f"❌ 冲刺赛结果同步失败: {e}", exc_info=True)
            self.db.rollback()
            return False
    
    def sync_driver_standings(self, season_year: int) -> bool:
        """同步车手积分榜数据"""
        logger.info(f"🏆 开始同步 {season_year} 赛季车手积分榜...")
        
        try:
            # 获取赛季对象
            season = self.db.query(Season).filter(Season.year == season_year).first()
            if not season:
                logger.error(f"❌ 赛季 {season_year} 不存在，无法同步积分榜")
                return False
            
            # 获取车手积分榜数据
            standings_df = self._handle_api_call(
                self.ergast.get_driver_standings, 
                season=season_year
            )
            
            if standings_df is None or standings_df.empty:
                logger.warning(f"没有获取到 {season_year} 赛季的车手积分榜数据")
                return False
            
            logger.info(f"📊 获取到车手积分榜数据，共 {len(standings_df)} 条记录")
            logger.info(f"📊 数据列名: {list(standings_df.columns)}")
            if len(standings_df) > 0:
                logger.info(f"📊 第一条记录: {standings_df.iloc[0].to_dict()}")
            
            # 清除该赛季的旧积分榜数据
            self.db.query(DriverStanding).filter(DriverStanding.season_id == season.id).delete()
            
            total_standings = 0
            skipped_count = 0
            
            for _, row in standings_df.iterrows():
                # 获取车手和车队
                driver = self._get_or_create_driver_from_result(row)
                constructor = self._get_or_create_constructor_from_result(row)
                
                if not driver:
                    logger.warning(f"⚠️  无法获取车手: {row.get('driverId', 'unknown')}")
                    skipped_count += 1
                    continue
                    
                if not constructor:
                    logger.warning(f"⚠️  无法获取车队: {row.get('constructorId', 'unknown')}")
                    skipped_count += 1
                    continue
                
                # 创建车手积分榜记录
                standing = DriverStanding(
                    season_id=season.id,
                    driver_id=driver.driver_id,
                    constructor_id=constructor.constructor_id,
                    position=row.get('position'),
                    points=row.get('points', 0),
                    wins=row.get('wins', 0)
                )
                
                self.db.add(standing)
                total_standings += 1
            
            self.db.commit()
            self._smart_delay('standings')
            logger.info(f"✅ {season_year} 赛季车手积分榜同步完成，共 {total_standings} 条记录，跳过 {skipped_count} 条")
            return True
            
        except Exception as e:
            logger.error(f"❌ 车手积分榜同步失败: {e}")
            self.db.rollback()
            return False
    
    def sync_constructor_standings(self, season_year: int) -> bool:
        """同步车队积分榜数据"""
        logger.info(f"🏆 开始同步 {season_year} 赛季车队积分榜...")
        
        try:
            # 获取赛季对象
            season = self.db.query(Season).filter(Season.year == season_year).first()
            if not season:
                logger.error(f"❌ 赛季 {season_year} 不存在，无法同步积分榜")
                return False
            
            # 获取车队积分榜数据
            standings_df = self._handle_api_call(
                self.ergast.get_constructor_standings, 
                season=season_year
            )
            
            if standings_df is None or standings_df.empty:
                logger.warning(f"没有获取到 {season_year} 赛季的车队积分榜数据")
                return False
            
            # 清除该赛季的旧积分榜数据
            self.db.query(ConstructorStanding).filter(ConstructorStanding.season_id == season.id).delete()
            
            total_standings = 0
            
            for _, row in standings_df.iterrows():
                # 获取车队
                constructor = self._get_or_create_constructor_from_result(row)
                
                if not constructor:
                    continue
                
                # 创建车队积分榜记录
                standing = ConstructorStanding(
                    season_id=season.id,
                    constructor_id=constructor.constructor_id,
                    position=row.get('position'),
                    points=row.get('points', 0),
                    wins=row.get('wins', 0)
                )
                
                self.db.add(standing)
                total_standings += 1
            
            self.db.commit()
            self._smart_delay('standings')
            logger.info(f"✅ {season_year} 赛季车队积分榜同步完成，共 {total_standings} 条记录")
            return True
            
        except Exception as e:
            logger.error(f"❌ 车队积分榜同步失败: {e}")
            self.db.rollback()
            return False
    
    def _get_or_create_driver_from_result(self, row: pd.Series) -> Optional[Driver]:
        """从比赛结果数据中获取或创建车手"""
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
            self.db.flush()
        
        return driver
    
    def _get_or_create_constructor_from_result(self, row: pd.Series) -> Optional[Constructor]:
        """从比赛结果数据中获取或创建车队"""
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
            self.db.flush()
        
        return constructor
    
    def sync_all_data(self, target_seasons: Optional[List[int]] = None):
        """同步所有数据"""
        if target_seasons is None:
            target_seasons = TARGET_SEASONS
        
        logger.info(f"🚀 开始同步所有数据，目标赛季: {target_seasons}")
        
        try:
            # 1. 同步基础数据
            logger.info("📋 第一步：同步基础数据...")
            self.sync_seasons()
            self.sync_circuits()
            self.sync_constructors()
            self.sync_drivers()
            
            # 2. 同步比赛和结果数据
            for season_year in target_seasons:
                logger.info(f"📊 第二步：同步 {season_year} 赛季数据...")
                
                # 同步比赛数据
                self.sync_races(season_year)
                
                # 同步比赛结果
                self.sync_race_results(season_year)
                
                # 同步排位赛结果
                self.sync_qualifying_results(season_year)
                
                # 同步冲刺赛结果
                self.sync_sprint_results(season_year)
                
                # 同步积分榜
                self.sync_driver_standings(season_year)
                self.sync_constructor_standings(season_year)
            
            logger.info("✅ 所有数据同步完成！")
            
        except Exception as e:
            logger.error(f"❌ 数据同步失败: {e}")
            raise 