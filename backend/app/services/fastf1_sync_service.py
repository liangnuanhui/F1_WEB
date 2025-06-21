"""
FastF1 数据同步服务 - 基于实际数据结构
"""
import logging
from typing import List, Optional
from datetime import datetime
import pandas as pd

from sqlalchemy.orm import Session
from fastf1.ergast import Ergast

from ..models import (
    Season, Circuit, Constructor, Driver, DriverSeason,
    Race, Result, QualifyingResult, SprintResult,
    DriverStanding, ConstructorStanding
)

logger = logging.getLogger(__name__)

# 目标赛季
TARGET_SEASONS = [2023, 2024, 2025]


class FastF1SyncService:
    """FastF1 数据同步服务"""
    
    def __init__(self, db: Session):
        self.db = db
        self.ergast = Ergast()
    
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
                start_date=datetime(year, 3, 1).date(),  # 大致开始日期
                end_date=datetime(year, 11, 30).date()   # 大致结束日期
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
            circuits_df = self.ergast.get_circuits(season=2025)
            
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
            constructors_df = self.ergast.get_constructor_info(season=2025)
            
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
                    season_id=season_2025.id  # 设置赛季外键
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
            drivers_df = self.ergast.get_driver_info(season=2025)
            
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
    
    def sync_driver_seasons(self) -> List[DriverSeason]:
        """同步车手赛季关联数据"""
        logger.info("🔄 开始同步车手赛季关联数据...")
        
        try:
            driver_seasons = []
            
            # 这里需要从比赛结果中获取车手和车队的关联关系
            # 暂时跳过，等有了比赛数据后再处理
            
            logger.info("✅ 车手赛季关联数据同步完成（暂跳过）")
            return driver_seasons
            
        except Exception as e:
            logger.error(f"❌ 车手赛季关联数据同步失败: {e}")
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
            import fastf1
            races_df = fastf1.get_event_schedule(season_year)
            
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
                # 跳过季前测试（第0轮）
                if row['RoundNumber'] == 0:
                    logger.info(f"⏭️  跳过季前测试: {row['OfficialEventName']}")
                    continue
                
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
                location = row['Location']
                
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
                        # 使用默认日期
                        event_date = datetime(season_year, 3, 1).date()
                else:
                    # 使用默认日期
                    event_date = datetime(season_year, 3, 1).date()
                
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
                    session1=row.get('Session1'),
                    session1_date=row.get('Session1Date'),
                    session2=row.get('Session2'),
                    session2_date=row.get('Session2Date'),
                    session3=row.get('Session3'),
                    session3_date=row.get('Session3Date'),
                    session4=row.get('Session4'),
                    session4_date=row.get('Session4Date'),
                    session5=row.get('Session5'),
                    session5_date=row.get('Session5Date')
                )
                
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
    
    def sync_all_data(self):
        """同步所有数据"""
        logger.info("🚀 开始同步所有FastF1数据...")
        
        try:
            # 1. 同步赛季数据
            self.sync_seasons()
            
            # 2. 同步赛道数据
            self.sync_circuits()
            
            # 3. 同步车队数据
            self.sync_constructors()
            
            # 4. 同步车手数据
            self.sync_drivers()
            
            # 5. 同步车手赛季关联数据
            self.sync_driver_seasons()
            
            # 6. 同步比赛数据（2025赛季）
            self.sync_races(2025)
            
            logger.info("✅ 所有数据同步完成！")
            
        except Exception as e:
            logger.error(f"❌ 数据同步失败: {e}")
            raise 