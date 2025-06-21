"""
数据同步服务
使用统一的 FastF1 数据提供者
"""
import logging
from typing import Optional, List, Dict, Any
from datetime import datetime
import pandas as pd
from sqlalchemy.orm import Session as DBSession
import time

# 添加FastF1的频率限制错误处理
try:
    from fastf1.req import RateLimitExceededError
except ImportError:
    # 如果导入失败，创建一个占位符异常类
    class RateLimitExceededError(Exception):
        pass

from app.models import (
    Season, Circuit, Race, Driver, Constructor, 
    Result, QualifyingResult, SprintResult,
    DriverStanding, ConstructorStanding
)
from app.core.database import get_db
from app.services.data_provider import DataProviderFactory, DataProvider

logger = logging.getLogger(__name__)


class DataSyncService:
    """数据同步服务"""
    
    def __init__(self, cache_dir: str = None):
        """
        初始化数据同步服务
        
        Args:
            cache_dir: FastF1 缓存目录
        """
        self.provider = DataProviderFactory.get_provider('fastf1', cache_dir=cache_dir)
        self.current_season = 2025  # 当前主赛季
        self.rate_limit_delays = {
            'basic': 0.5,      # 基础数据延迟
            'results': 1.0,    # 比赛结果延迟
            'standings': 1.5,  # 积分榜延迟
            'session': 2.0     # 会话数据延迟
        }
        logger.info("初始化数据同步服务，使用 FastF1 数据提供者（带频率限制处理）")
    
    def _handle_rate_limit_error(self, func, *args, max_retries=3, base_delay=1.0, **kwargs):
        """处理API频率限制错误的通用方法"""
        for attempt in range(max_retries):
            try:
                return func(*args, **kwargs)
            except RateLimitExceededError as e:
                if attempt < max_retries - 1:
                    delay = base_delay * (2 ** attempt)  # 指数退避
                    logger.warning(f"遇到API频率限制，等待 {delay} 秒后重试 (尝试 {attempt + 1}/{max_retries})")
                    time.sleep(delay)
                else:
                    logger.error(f"达到最大重试次数，停止尝试: {e}")
                    raise
            except Exception as e:
                # 对于其他错误，不重试
                logger.error(f"执行函数时出错: {e}")
                raise
        
        return None
    
    def _smart_delay(self, data_type: str = 'basic'):
        """智能延迟，根据数据类型调整延迟时间"""
        delay = self.rate_limit_delays.get(data_type, 1.0)
        time.sleep(delay)
    
    def sync_circuits(self, db: DBSession, season: int = None) -> bool:
        """同步赛道数据"""
        try:
            logger.info(f"开始同步赛道数据 (赛季: {season or 'all'})...")
            
            # 获取赛道数据
            circuits_data = self.provider.get_circuits(season=season)
            
            if circuits_data.empty:
                logger.warning("没有获取到赛道数据")
                return False
            
            for _, row in circuits_data.iterrows():
                circuit_id = row['circuitId']
                
                # 检查是否已存在
                existing_circuit = db.query(Circuit).filter_by(circuit_id=circuit_id).first()
                if not existing_circuit:
                    circuit = Circuit(
                        circuit_id=circuit_id,
                        name=row['circuitName'],
                        country=row.get('country', ''),
                        locality=row.get('locality', ''),
                        latitude=row.get('lat'),
                        longitude=row.get('long')
                    )
                    db.add(circuit)
                    logger.info(f"添加赛道: {row['circuitName']}")
            
            db.commit()
            self._smart_delay('basic')
            logger.info("赛道数据同步完成")
            return True
            
        except Exception as e:
            logger.error(f"同步赛道数据失败: {e}")
            db.rollback()
            return False
    
    def sync_drivers(self, db: DBSession, season: int = None) -> bool:
        """同步车手数据"""
        try:
            logger.info(f"开始同步车手数据 (赛季: {season or 'all'})...")
            
            # 获取车手数据
            drivers_data = self.provider.get_drivers(season=season)
            
            if drivers_data.empty:
                logger.warning("没有获取到车手数据")
                return False
            
            for _, row in drivers_data.iterrows():
                driver_id = row['driverId']
                
                # 检查是否已存在
                existing_driver = db.query(Driver).filter_by(driver_id=driver_id).first()
                if not existing_driver:
                    # 解析姓名
                    first_name = row.get('givenName', '')
                    last_name = row.get('familyName', '')
                    full_name = f"{first_name} {last_name}".strip()
                    
                    driver = Driver(
                        driver_id=driver_id,
                        code=row.get('code', ''),
                        first_name=first_name,
                        last_name=last_name,
                        full_name=full_name,
                        date_of_birth=row.get('dateOfBirth'),
                        nationality=row.get('nationality', ''),
                        number=row.get('driverNumber'),
                        season_id=season,
                        constructor_id=None,  # 稍后关联
                        is_active=True
                    )
                    db.add(driver)
                    logger.info(f"添加车手: {full_name}")
            
            db.commit()
            self._smart_delay('basic')
            logger.info("车手数据同步完成")
            return True
            
        except Exception as e:
            logger.error(f"同步车手数据失败: {e}")
            db.rollback()
            return False
    
    def sync_constructors(self, db: DBSession, season: int = None) -> bool:
        """同步车队数据"""
        try:
            logger.info(f"开始同步车队数据 (赛季: {season or 'all'})...")
            
            # 获取车队数据
            constructors_data = self.provider.get_constructors(season=season)
            
            if constructors_data.empty:
                logger.warning("没有获取到车队数据")
                return False
            
            for _, row in constructors_data.iterrows():
                constructor_id = row['constructorId']
                
                # 检查是否已存在
                existing_constructor = db.query(Constructor).filter_by(constructor_id=constructor_id).first()
                if not existing_constructor:
                    constructor = Constructor(
                        constructor_id=constructor_id,
                        name=row['constructorName'],
                        nationality=row.get('constructorNationality', ''),
                        season_id=season,
                        is_active=True
                    )
                    db.add(constructor)
                    logger.info(f"添加车队: {row['constructorName']}")
            
            db.commit()
            self._smart_delay('basic')
            logger.info("车队数据同步完成")
            return True
            
        except Exception as e:
            logger.error(f"同步车队数据失败: {e}")
            db.rollback()
            return False
    
    def sync_race_results(self, db: DBSession, season: int, round_number: int = None) -> bool:
        """同步比赛结果数据 (增加延迟和分批处理)"""
        try:
            logger.info(f"开始同步比赛结果数据 (赛季: {season}, 轮次: {round_number or 'all'})...")
            
            rounds_to_sync = self._get_rounds_to_sync(season, round_number)
            if not rounds_to_sync:
                return True # No rounds to sync, not an error

            for current_round in rounds_to_sync:
                logger.info(f"  同步第 {current_round} 轮比赛结果...")
                
                # 检查是否已有数据，避免重复同步
                existing_results = db.query(Result).filter_by(season=season, round_number=current_round).count()
                if existing_results > 0:
                    logger.info(f"  第 {current_round} 轮比赛结果已存在，跳过")
                    continue
                
                results_data = self.provider.get_race_results(season=season, round_number=current_round)
                
                if results_data.empty:
                    logger.warning(f"  没有获取到 {season} 赛季第 {current_round} 轮的比赛结果数据")
                    self._smart_delay('results')
                    continue

                for _, row in results_data.iterrows():
                    driver = self._get_or_create_driver(db, row)
                    constructor = self._get_or_create_constructor(db, row)
                    race = self._get_or_create_race(db, season, current_round, row)
                    
                    if not all([driver, constructor, race]):
                        continue

                    result = Result(
                        race_id=race.id,
                        driver_id=driver.id,
                        constructor_id=constructor.id,
                        season=season,
                        round_number=current_round,
                        position=row.get('position'),
                        position_text=str(row.get('positionText', '')),
                        points=row.get('points', 0),
                        grid_position=row.get('grid'),
                        status=row.get('status', ''),
                        laps_completed=row.get('laps'),
                        fastest_lap=row.get('fastestLap'),
                        is_active=True
                    )
                    db.add(result)
                
                db.commit()
                self._smart_delay('results')
            
            logger.info("比赛结果数据同步完成")
            return True
            
        except Exception as e:
            logger.error(f"同步比赛结果数据失败: {e}", exc_info=True)
            db.rollback()
            return False
    
    def sync_qualifying_results(self, db: DBSession, season: int, round_number: int = None) -> bool:
        """同步排位赛结果数据 (增加延迟和分批处理)"""
        try:
            logger.info(f"开始同步排位赛结果数据 (赛季: {season}, 轮次: {round_number or 'all'})...")
            
            rounds_to_sync = self._get_rounds_to_sync(season, round_number)
            if not rounds_to_sync:
                return True

            for current_round in rounds_to_sync:
                logger.info(f"  同步第 {current_round} 轮排位赛结果...")
                
                # 检查是否已有数据，避免重复同步
                existing_results = db.query(QualifyingResult).filter_by(season=season, round_number=current_round).count()
                if existing_results > 0:
                    logger.info(f"  第 {current_round} 轮排位赛结果已存在，跳过")
                    continue

                qualifying_data = self.provider.get_qualifying_results(season=season, round_number=current_round)
                
                if qualifying_data.empty:
                    logger.warning(f"  没有获取到 {season} 赛季第 {current_round} 轮的排位赛结果数据")
                    self._smart_delay('results')
                    continue
                
                for _, row in qualifying_data.iterrows():
                    driver = self._get_or_create_driver(db, row)
                    constructor = self._get_or_create_constructor(db, row)
                    race = self._get_or_create_race(db, season, current_round, row)

                    if not all([driver, constructor, race]):
                        continue
                        
                    qualifying_result = QualifyingResult(
                        race_id=race.id,
                        driver_id=driver.id,
                        constructor_id=constructor.id,
                        season=season,
                        round_number=current_round,
                        position=row.get('position'),
                        q1_time=str(row.get('Q1', '')),
                        q2_time=str(row.get('Q2', '')),
                        q3_time=str(row.get('Q3', ''))
                    )
                    db.add(qualifying_result)
                
                db.commit()
                self._smart_delay('results')
            
            logger.info("排位赛结果数据同步完成")
            return True
            
        except Exception as e:
            logger.error(f"同步排位赛结果数据失败: {e}", exc_info=True)
            db.rollback()
            return False
    
    def sync_driver_standings(self, db: DBSession, season: int, round_number: int = None) -> bool:
        """同步车手积分榜数据 (增加延迟和分批处理)"""
        try:
            logger.info(f"开始同步车手积分榜数据 (赛季: {season}, 轮次: {round_number or 'all'})...")
            
            rounds_to_sync = self._get_rounds_to_sync(season, round_number)
            if not rounds_to_sync:
                return True

            for current_round in rounds_to_sync:
                logger.info(f"  同步第 {current_round} 轮车手积分榜...")
                
                # 检查是否已有数据，避免重复同步
                existing_standings = db.query(DriverStanding).filter_by(season=season, round_number=current_round).count()
                if existing_standings > 0:
                    logger.info(f"  第 {current_round} 轮车手积分榜已存在，跳过")
                    continue
                
                standings_data = self.provider.get_driver_standings(season=season, round_number=current_round)
                
                if standings_data.empty:
                    logger.warning(f"  没有获取到 {season} 赛季第 {current_round} 轮的车手积分榜数据")
                    self._smart_delay('standings')
                    continue
                
                for _, row in standings_data.iterrows():
                    driver = self._get_or_create_driver(db, row)
                    constructor = self._get_or_create_constructor(db, row)
                    
                    if not all([driver, constructor]):
                        continue

                    standing = DriverStanding(
                        season=season,
                        round_number=current_round,
                        driver_id=driver.id,
                        constructor_id=constructor.id,
                        position=row.get('position'),
                        position_text=str(row.get('positionText', '')),
                        points=row.get('points', 0),
                        wins=row.get('wins', 0)
                    )
                    db.add(standing)

                db.commit()
                self._smart_delay('standings')
            
            logger.info("车手积分榜数据同步完成")
            return True
            
        except Exception as e:
            logger.error(f"同步车手积分榜数据失败: {e}", exc_info=True)
            db.rollback()
            return False
    
    def sync_constructor_standings(self, db: DBSession, season: int, round_number: int = None) -> bool:
        """同步车队积分榜数据 (增加延迟和分批处理)"""
        try:
            logger.info(f"开始同步车队积分榜数据 (赛季: {season}, 轮次: {round_number or 'all'})...")
            
            rounds_to_sync = self._get_rounds_to_sync(season, round_number)
            if not rounds_to_sync:
                return True

            for current_round in rounds_to_sync:
                logger.info(f"  同步第 {current_round} 轮车队积分榜...")
                
                # 检查是否已有数据，避免重复同步
                existing_standings = db.query(ConstructorStanding).filter_by(season=season, round_number=current_round).count()
                if existing_standings > 0:
                    logger.info(f"  第 {current_round} 轮车队积分榜已存在，跳过")
                    continue

                standings_data = self.provider.get_constructor_standings(season=season, round_number=current_round)
                
                if standings_data.empty:
                    logger.warning(f"  没有获取到 {season} 赛季第 {current_round} 轮的车队积分榜数据")
                    self._smart_delay('standings')
                    continue
                
                for _, row in standings_data.iterrows():
                    constructor = self._get_or_create_constructor(db, row)
                    if not constructor:
                        continue

                    standing = ConstructorStanding(
                        season=season,
                        round_number=current_round,
                        constructor_id=constructor.id,
                        position=row.get('position'),
                        position_text=str(row.get('positionText', '')),
                        points=row.get('points', 0),
                        wins=row.get('wins', 0)
                    )
                    db.add(standing)
                
                db.commit()
                self._smart_delay('standings')
            
            logger.info("车队积分榜数据同步完成")
            return True
            
        except Exception as e:
            logger.error(f"同步车队积分榜数据失败: {e}", exc_info=True)
            db.rollback()
            return False
    
    def _get_or_create_driver(self, db: DBSession, row: pd.Series) -> Optional[Driver]:
        """获取或创建车手"""
        driver_id = row.get('driverId')
        if not driver_id:
            return None
        
        driver = db.query(Driver).filter_by(driver_id=driver_id).first()
        if not driver:
            # 创建新车手
            first_name = row.get('givenName', '')
            last_name = row.get('familyName', '')
            full_name = f"{first_name} {last_name}".strip()
            
            driver = Driver(
                driver_id=driver_id,
                code=row.get('code', ''),
                first_name=first_name,
                last_name=last_name,
                full_name=full_name,
                date_of_birth=row.get('dateOfBirth'),
                nationality=row.get('nationality', ''),
                number=row.get('driverNumber'),
                is_active=True
            )
            db.add(driver)
            db.flush()  # 获取ID但不提交
        
        return driver
    
    def _get_or_create_constructor(self, db: DBSession, row: pd.Series) -> Optional[Constructor]:
        """获取或创建车队"""
        constructor_id = row.get('constructorId')
        if not constructor_id:
            return None
        
        constructor = db.query(Constructor).filter_by(constructor_id=constructor_id).first()
        if not constructor:
            # 创建新车队
            constructor = Constructor(
                constructor_id=constructor_id,
                name=row.get('constructorName', ''),
                nationality=row.get('constructorNationality', ''),
                is_active=True
            )
            db.add(constructor)
            db.flush()  # 获取ID但不提交
        
        return constructor
    
    def _get_or_create_race(self, db: DBSession, season_year: int, round_num: int, row: pd.Series) -> Optional[Race]:
        """获取或创建比赛"""
        race = db.query(Race).filter_by(season_year=season_year, round_number=round_num).first()
        if not race:
            # Create new race
            circuit_name = row.get('circuitId', f'round_{round_num}')
            circuit = db.query(Circuit).filter(Circuit.circuit_id == circuit_name).first()
            if not circuit:
                circuit = Circuit(circuit_id=circuit_name, name=row.get('circuitName', 'Unknown'))
                db.add(circuit)
                db.flush()

            race = Race(
                season_year=season_year,
                round_number=round_num,
                name=row.get('raceName', f'Round {round_num}'),
                circuit_id=circuit.id,
                is_active=True
            )
            db.add(race)
            db.flush()
        return race
    
    def _get_rounds_to_sync(self, season: int, round_number: Optional[int]) -> List[int]:
        """获取需要同步的轮次列表 - 优化处理 FastF1 数据"""
        if round_number:
            return [round_number]
        
        try:
            logger.info(f"🔍 获取 {season} 赛季比赛日程以确定轮次...")
            races = self.provider.get_races(season=season)
            
            if races.empty:
                logger.warning(f"无法获取 {season} 赛季的比赛日程，无法确定轮次")
                return []
            
            # 确保 RoundNumber 是整数类型
            races['RoundNumber'] = pd.to_numeric(races['RoundNumber'], errors='coerce').dropna().astype(int)
            
            # 过滤掉季前测试（RoundNumber = 0）
            actual_races = races[races['RoundNumber'] > 0]
            
            if actual_races.empty:
                logger.warning(f"{season} 赛季没有实际比赛数据")
                return []
            
            num_rounds = actual_races['RoundNumber'].max()
            rounds_list = list(range(1, num_rounds + 1))
            
            logger.info(f"📊 {season} 赛季共有 {num_rounds} 轮比赛")
            logger.info(f"🏁 轮次列表: {rounds_list}")
            
            return rounds_list
            
        except Exception as e:
            logger.error(f"❌ 获取轮次列表失败: {e}")
            return []
    
    def sync_all_data(self, db: DBSession, season: int = None, start_year: int = None, end_year: int = None) -> bool:
        """同步所有数据"""
        try:
            logger.info(f"🚀 开始同步所有数据 (赛季: {season}, 年份范围: {start_year}-{end_year})...")
            
            success = True
            
            # 同步基础数据
            if season:
                logger.info(f"📊 同步 {season} 赛季数据...")
                success &= self.sync_circuits(db, season)
                success &= self.sync_drivers(db, season)
                success &= self.sync_constructors(db, season)
                success &= self.sync_races(db, season)
                success &= self.sync_race_results(db, season)
                success &= self.sync_qualifying_results(db, season)
                success &= self.sync_driver_standings(db, season)
                success &= self.sync_constructor_standings(db, season)
            else:
                # 同步历史数据
                if start_year and end_year:
                    logger.info(f"📊 同步历史数据 ({start_year}-{end_year})...")
                    for year in range(start_year, end_year + 1):
                        logger.info(f"📅 同步 {year} 赛季...")
                        success &= self.sync_circuits(db, year)
                        success &= self.sync_drivers(db, year)
                        success &= self.sync_constructors(db, year)
                        success &= self.sync_races(db, year)
                        success &= self.sync_race_results(db, year)
                        success &= self.sync_qualifying_results(db, year)
                        success &= self.sync_driver_standings(db, year)
                        success &= self.sync_constructor_standings(db, year)
            
            if success:
                logger.info("✅ 所有数据同步完成")
            else:
                logger.warning("⚠️ 部分数据同步失败")
            
            return success
            
        except Exception as e:
            logger.error(f"❌ 同步所有数据时发生错误: {e}")
            return False
    
    def sync_races(self, db: DBSession, season: int) -> bool:
        """同步比赛数据 - 使用 FastF1 获取的详细日程"""
        try:
            logger.info(f"🏁 开始同步 {season} 赛季比赛数据...")
            
            # 自动创建赛季（如果不存在）
            season_obj = db.query(Season).filter(Season.year == season).first()
            if not season_obj:
                logger.info(f"赛季 {season} 在数据库中不存在，将自动创建。")
                season_obj = Season(year=season, name=f"{season} Formula 1 Season")
                db.add(season_obj)
                db.flush()  # 使用 flush 以便后续操作可以引用此赛季
                logger.info(f"✅ 赛季 {season} 已创建。")

            # 获取比赛日程（使用 FastF1 获取最全面的数据）
            races_data = self.provider.get_races(season=season)
            
            if races_data.empty:
                logger.warning(f"没有获取到 {season} 赛季的比赛数据")
                return False
            
            logger.info(f"📊 获取到 {len(races_data)} 场比赛数据")
            
            # 过滤掉季前测试（RoundNumber = 0）
            actual_races = races_data[races_data['RoundNumber'] > 0]
            logger.info(f"🏁 实际比赛场数: {len(actual_races)}场（排除季前测试）")
            
            for _, row in actual_races.iterrows():
                round_number = row.get('RoundNumber')
                event_name = row.get('EventName', '')
                official_name = row.get('OfficialEventName', '')
                country = row.get('Country', '')
                location = row.get('Location', '')
                event_date = row.get('EventDate')
                event_format = row.get('EventFormat', 'conventional')
                
                # 检查是否已存在
                existing_race = db.query(Race).filter_by(
                    season_year=season, 
                    round_number=round_number
                ).first()
                
                if not existing_race:
                    # 获取或创建赛道
                    circuit_name = f"{country}_{location}".replace(' ', '_').lower()
                    circuit = db.query(Circuit).filter_by(circuit_id=circuit_name).first()
                    
                    if not circuit:
                        circuit = Circuit(
                            circuit_id=circuit_name,
                            name=f"{location} Circuit",
                            country=country,
                            locality=location
                        )
                        db.add(circuit)
                        db.flush()
                    
                    # 创建比赛记录
                    race = Race(
                        season_year=season,
                        round_number=round_number,
                        name=event_name,
                        official_name=official_name,
                        circuit_id=circuit.id,
                        event_date=event_date,
                        event_format=event_format,
                        is_active=True
                    )
                    db.add(race)
                    logger.info(f"✅ 添加比赛: 第{round_number}轮 - {event_name} ({event_format})")
                else:
                    # 更新现有比赛信息
                    existing_race.name = event_name
                    existing_race.official_name = official_name
                    existing_race.event_date = event_date
                    existing_race.event_format = event_format
                    logger.info(f"🔄 更新比赛: 第{round_number}轮 - {event_name}")
            
            db.commit()
            self._smart_delay('basic')
            logger.info(f"✅ {season} 赛季比赛数据同步完成")
            return True
            
        except Exception as e:
            logger.error(f"❌ 同步比赛数据失败: {e}")
            db.rollback()
            return False 