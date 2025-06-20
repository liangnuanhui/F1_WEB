"""
数据同步服务
使用统一的 FastF1 数据提供者
"""
import logging
from typing import Optional, List, Dict, Any
from datetime import datetime
import pandas as pd
from sqlalchemy.orm import Session as DBSession

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
        logger.info("初始化数据同步服务，使用 FastF1 数据提供者")
    
    def sync_seasons(self, db: DBSession, start_year: int = None, end_year: int = None) -> bool:
        """同步赛季数据"""
        try:
            logger.info(f"开始同步赛季数据 (年份范围: {start_year}-{end_year})...")
            
            # 获取赛季数据
            seasons_data = self.provider.get_seasons(start_year, end_year)
            
            if seasons_data.empty:
                logger.warning("没有获取到赛季数据")
                return False
            
            for _, row in seasons_data.iterrows():
                season_year = row['season']
                
                # 检查是否已存在
                existing_season = db.query(Season).filter_by(year=season_year).first()
                if not existing_season:
                    season = Season(
                        year=season_year,
                        name=row.get('name', f"{season_year} Formula 1 World Championship"),
                        is_active=season_year == self.current_season
                    )
                    db.add(season)
                    logger.info(f"添加赛季: {season_year}")
            
            db.commit()
            logger.info("赛季数据同步完成")
            return True
            
        except Exception as e:
            logger.error(f"同步赛季数据失败: {e}")
            db.rollback()
            return False
    
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
            logger.info("车队数据同步完成")
            return True
            
        except Exception as e:
            logger.error(f"同步车队数据失败: {e}")
            db.rollback()
            return False
    
    def sync_race_results(self, db: DBSession, season: int, round_number: int = None) -> bool:
        """同步比赛结果数据"""
        try:
            logger.info(f"开始同步比赛结果数据 (赛季: {season}, 轮次: {round_number or 'all'})...")
            
            # 获取比赛结果数据
            results_data = self.provider.get_race_results(season=season, round_number=round_number)
            
            if results_data.empty:
                logger.warning("没有获取到比赛结果数据")
                return False
            
            # 删除该轮次的旧数据（幂等操作）
            if round_number:
                db.query(Result).filter_by(season=season, round_number=round_number).delete()
            else:
                db.query(Result).filter_by(season=season).delete()
            
            for _, row in results_data.iterrows():
                # 获取或创建车手
                driver = self._get_or_create_driver(db, row)
                if not driver:
                    continue
                
                # 获取或创建车队
                constructor = self._get_or_create_constructor(db, row)
                if not constructor:
                    continue
                
                # 获取或创建比赛
                race = self._get_or_create_race(db, row)
                if not race:
                    continue
                
                # 创建比赛结果
                result = Result(
                    race_id=race.id,
                    driver_id=driver.id,
                    constructor_id=constructor.id,
                    position=row.get('position'),
                    position_text=row.get('positionText', ''),
                    points=row.get('points', 0),
                    grid_position=row.get('grid'),
                    status=row.get('status', ''),
                    laps_completed=row.get('laps'),
                    fastest_lap=row.get('fastestLap'),
                    is_active=True
                )
                db.add(result)
            
            db.commit()
            logger.info("比赛结果数据同步完成")
            return True
            
        except Exception as e:
            logger.error(f"同步比赛结果数据失败: {e}")
            db.rollback()
            return False
    
    def sync_qualifying_results(self, db: DBSession, season: int, round_number: int = None) -> bool:
        """同步排位赛结果数据"""
        try:
            logger.info(f"开始同步排位赛结果数据 (赛季: {season}, 轮次: {round_number or 'all'})...")
            
            # 获取排位赛结果数据
            qualifying_data = self.provider.get_qualifying_results(season=season, round_number=round_number)
            
            if qualifying_data.empty:
                logger.warning("没有获取到排位赛结果数据")
                return False
            
            # 删除该轮次的旧数据（幂等操作）
            if round_number:
                db.query(QualifyingResult).filter_by(season=season, round_number=round_number).delete()
            else:
                db.query(QualifyingResult).filter_by(season=season).delete()
            
            for _, row in qualifying_data.iterrows():
                # 获取或创建车手
                driver = self._get_or_create_driver(db, row)
                if not driver:
                    continue
                
                # 获取或创建车队
                constructor = self._get_or_create_constructor(db, row)
                if not constructor:
                    continue
                
                # 创建排位赛结果
                qualifying_result = QualifyingResult(
                    season=season,
                    round_number=row.get('round', round_number),
                    driver_number=row.get('driverNumber'),
                    driver_code=row.get('driverCode', ''),
                    position=row.get('position'),
                    q1_time=row.get('Q1'),
                    q2_time=row.get('Q2'),
                    q3_time=row.get('Q3')
                )
                db.add(qualifying_result)
            
            db.commit()
            logger.info("排位赛结果数据同步完成")
            return True
            
        except Exception as e:
            logger.error(f"同步排位赛结果数据失败: {e}")
            db.rollback()
            return False
    
    def sync_driver_standings(self, db: DBSession, season: int, round_number: int = None) -> bool:
        """同步车手积分榜数据"""
        try:
            logger.info(f"开始同步车手积分榜数据 (赛季: {season}, 轮次: {round_number or 'all'})...")
            
            # 获取车手积分榜数据
            standings_data = self.provider.get_driver_standings(season=season, round_number=round_number)
            
            if standings_data.empty:
                logger.warning("没有获取到车手积分榜数据")
                return False
            
            # 删除该轮次的旧数据（幂等操作）
            if round_number:
                db.query(DriverStanding).filter_by(season=season, round_number=round_number).delete()
            else:
                db.query(DriverStanding).filter_by(season=season).delete()
            
            for _, row in standings_data.iterrows():
                standing = DriverStanding(
                    season=season,
                    round_number=row.get('round', round_number),
                    position=row.get('position'),
                    position_text=row.get('positionText', ''),
                    points=row.get('points', 0),
                    wins=row.get('wins', 0)
                )
                db.add(standing)
            
            db.commit()
            logger.info("车手积分榜数据同步完成")
            return True
            
        except Exception as e:
            logger.error(f"同步车手积分榜数据失败: {e}")
            db.rollback()
            return False
    
    def sync_constructor_standings(self, db: DBSession, season: int, round_number: int = None) -> bool:
        """同步车队积分榜数据"""
        try:
            logger.info(f"开始同步车队积分榜数据 (赛季: {season}, 轮次: {round_number or 'all'})...")
            
            # 获取车队积分榜数据
            standings_data = self.provider.get_constructor_standings(season=season, round_number=round_number)
            
            if standings_data.empty:
                logger.warning("没有获取到车队积分榜数据")
                return False
            
            # 删除该轮次的旧数据（幂等操作）
            if round_number:
                db.query(ConstructorStanding).filter_by(season=season, round_number=round_number).delete()
            else:
                db.query(ConstructorStanding).filter_by(season=season).delete()
            
            for _, row in standings_data.iterrows():
                standing = ConstructorStanding(
                    season=season,
                    round_number=row.get('round', round_number),
                    position=row.get('position'),
                    position_text=row.get('positionText', ''),
                    points=row.get('points', 0),
                    wins=row.get('wins', 0)
                )
                db.add(standing)
            
            db.commit()
            logger.info("车队积分榜数据同步完成")
            return True
            
        except Exception as e:
            logger.error(f"同步车队积分榜数据失败: {e}")
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
    
    def _get_or_create_race(self, db: DBSession, row: pd.Series) -> Optional[Race]:
        """获取或创建比赛"""
        season = row.get('season')
        round_number = row.get('round')
        
        if not season or not round_number:
            return None
        
        race = db.query(Race).filter_by(season_id=season, round_number=round_number).first()
        if not race:
            # 创建新比赛
            race = Race(
                season_id=season,
                round_number=round_number,
                name=row.get('raceName', f'Race {round_number}'),
                is_active=True
            )
            db.add(race)
            db.flush()  # 获取ID但不提交
        
        return race
    
    def sync_all_data(self, db: DBSession, season: int = None, start_year: int = None, end_year: int = None) -> bool:
        """同步所有数据"""
        try:
            logger.info(f"开始同步所有数据 (赛季: {season}, 年份范围: {start_year}-{end_year})...")
            
            success = True
            
            # 同步基础数据
            if season:
                success &= self.sync_circuits(db, season)
                success &= self.sync_drivers(db, season)
                success &= self.sync_constructors(db, season)
                success &= self.sync_race_results(db, season)
                success &= self.sync_qualifying_results(db, season)
                success &= self.sync_driver_standings(db, season)
                success &= self.sync_constructor_standings(db, season)
            else:
                # 同步历史数据
                if start_year and end_year:
                    success &= self.sync_seasons(db, start_year, end_year)
                    for year in range(start_year, end_year + 1):
                        success &= self.sync_circuits(db, year)
                        success &= self.sync_drivers(db, year)
                        success &= self.sync_constructors(db, year)
                        success &= self.sync_race_results(db, year)
                        success &= self.sync_qualifying_results(db, year)
                        success &= self.sync_driver_standings(db, year)
                        success &= self.sync_constructor_standings(db, year)
            
            if success:
                logger.info("所有数据同步完成")
            else:
                logger.warning("部分数据同步失败")
            
            return success
            
        except Exception as e:
            logger.error(f"同步所有数据时发生错误: {e}")
            return False 