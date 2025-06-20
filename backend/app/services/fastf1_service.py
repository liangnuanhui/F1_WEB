"""
FastF1 数据服务
用于从 FastF1 库拉取真实的 F1 数据并初始化数据库
"""

import asyncio
import logging
import os
from datetime import datetime
from typing import List, Optional

import fastf1
import pandas as pd
from sqlalchemy.orm import Session

from app.models.circuit import Circuit
from app.models.constructor import Constructor
from app.models.driver import Driver
from app.models.race import Race
from app.models.result import Result
from app.models.season import Season

logger = logging.getLogger(__name__)


class FastF1Service:
    """FastF1 数据服务类"""
    
    def __init__(self, db: Session):
        self.db = db
        # 设置 FastF1 缓存目录（绝对路径，防止相对路径问题）
        cache_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../cache'))
        fastf1.Cache.enable_cache(cache_dir)
        logger.info(f"FastF1 缓存目录设置为: {cache_dir}")
    
    async def initialize_database(self, start_year: int = 2020, end_year: int = 2024):
        """
        初始化数据库，从指定年份范围拉取 F1 数据
        
        Args:
            start_year: 开始年份
            end_year: 结束年份
        """
        logger.info(f"开始初始化数据库，年份范围: {start_year}-{end_year}")
        
        try:
            for year in range(start_year, end_year + 1):
                logger.info(f"正在处理 {year} 赛季数据...")
                await self._process_season(year)
            logger.info("数据库初始化完成！")
        except Exception as e:
            logger.error(f"初始化数据库时发生错误: {e}")
            raise
    
    async def _process_season(self, year: int):
        """处理单个赛季的数据"""
        try:
            # 获取赛季信息
            season = fastf1.get_season(year)
            # 创建或更新赛季记录
            season_record = self._create_or_update_season(year, season)
            # 获取所有比赛
            races = fastf1.get_event_schedule(year)
            for _, race_info in races.iterrows():
                await self._process_race(year, race_info, season_record)
        except Exception as e:
            logger.error(f"处理 {year} 赛季时发生错误: {e}")
    
    def _create_or_update_season(self, year: int, season_data) -> Season:
        """创建或更新赛季记录"""
        existing_season = self.db.query(Season).filter(Season.year == year).first()
        if existing_season:
            logger.info(f"赛季 {year} 已存在，跳过创建")
            return existing_season
        # 创建新赛季记录
        season = Season(
            year=year,
            name=f"Formula 1 World Championship {year}",
            description=f"第 {year} 赛季 F1 世界锦标赛",
            start_date=datetime(year, 1, 1).date(),
            end_date=datetime(year, 12, 31).date(),
            is_current=year == datetime.now().year,  # 动态判断当前赛季
            total_races=0,  # 稍后更新
            completed_races=0,
            is_active=True
        )
        self.db.add(season)
        self.db.commit()
        self.db.refresh(season)
        logger.info(f"创建赛季 {year}")
        return season
    
    async def _process_race(self, year: int, race_info: pd.Series, season: Season):
        """处理单场比赛（字段兼容性处理）"""
        try:
            event_name = race_info.get('EventName') or race_info.get('Event')
            circuit_name = race_info.get('CircuitShortName') or race_info.get('Circuit')
            # 创建或获取赛道
            circuit = self._get_or_create_circuit(circuit_name, race_info)
            # 创建或更新比赛记录
            race = self._create_or_update_race(year, race_info, season, circuit)
            # 获取比赛结果
            await self._process_race_results(year, event_name, race)
        except Exception as e:
            logger.error(f"处理比赛 {race_info.get('EventName', race_info.get('Event', '未知'))} 时发生错误: {e}")
    
    def _get_or_create_circuit(self, circuit_name: str, race_info: pd.Series) -> Circuit:
        """获取或创建赛道记录"""
        if not circuit_name:
            circuit_name = 'Unknown'
        existing_circuit = self.db.query(Circuit).filter(
            Circuit.name.ilike(f"%{circuit_name}%")
        ).first()
        if existing_circuit:
            return existing_circuit
        # 创建新赛道记录
        circuit = Circuit(
            circuit_id=f"circuit_{circuit_name.lower().replace(' ', '_')}",
            name=race_info.get('CircuitFullName', circuit_name),
            location=race_info.get('Location', ''),
            country=race_info.get('Country', ''),
            length=None,  # FastF1 可能没有这些详细信息
            corners=None,
            lap_record=None,
            lap_record_driver=None,
            lap_record_year=None,
            description=f"{circuit_name} 赛道",
            characteristics="",
            is_active=True
        )
        self.db.add(circuit)
        self.db.commit()
        self.db.refresh(circuit)
        logger.info(f"创建赛道: {circuit.name}")
        return circuit
    
    def _create_or_update_race(self, year: int, race_info: pd.Series, season: Season, circuit: Circuit) -> Race:
        """创建或更新比赛记录"""
        event_name = race_info.get('EventName') or race_info.get('Event')
        race_id = f"{year}_{str(event_name).lower().replace(' ', '_')}"
        existing_race = self.db.query(Race).filter(Race.race_id == race_id).first()
        if existing_race:
            return existing_race
        # 解析日期
        race_date = None
        if 'EventDate' in race_info and pd.notna(race_info['EventDate']):
            race_date = pd.to_datetime(race_info['EventDate'])
        # 创建新比赛记录
        race = Race(
            race_id=race_id,
            name=event_name,
            round_number=race_info.get('RoundNumber', 0),
            season_id=season.id,
            circuit_id=circuit.id,
            race_date=race_date or datetime.now(),
            qualifying_date=None,  # FastF1 可能没有这些详细信息
            sprint_date=None,
            status='scheduled',  # 默认为已安排
            is_sprint_weekend=False,  # 需要根据实际情况判断
            description=f"{year} 赛季 {event_name}",
            weather=None,
            temperature=None,
            is_active=True
        )
        self.db.add(race)
        self.db.commit()
        self.db.refresh(race)
        logger.info(f"创建比赛: {race.name}")
        return race
    
    async def _process_race_results(self, year: int, event_name: str, race: Race):
        """处理比赛结果（异步获取 Session，异常捕获更细致）"""
        try:
            # 异步获取 session
            session = await self._get_session_async(year, event_name, 'R')
            try:
                session.load()
            except Exception as e:
                logger.warning(f"加载 {year} {event_name} session 数据失败: {e}")
                return
            if not hasattr(session, 'results') or session.results is None or session.results.empty:
                logger.warning(f"没有找到 {year} {event_name} 的比赛结果")
                return
            # 处理车手和车队
            for _, result in session.results.iterrows():
                await self._process_driver_result(result, race)
        except Exception as e:
            logger.error(f"处理 {year} {event_name} 比赛结果时发生错误: {e}")
    
    async def _get_session_async(self, year: int, event: str, session_type: str):
        """异步获取 FastF1 Session 对象"""
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(
            None, lambda: fastf1.get_session(year, event, session_type)
        )
    
    async def _process_driver_result(self, result: pd.Series, race: Race):
        """处理单个车手的比赛结果"""
        try:
            driver_name = result.get('Driver', '')
            constructor_name = result.get('Constructor', '')
            if not driver_name or not constructor_name:
                return
            # 获取或创建车队
            constructor = self._get_or_create_constructor(constructor_name, race.season_id)
            # 获取或创建车手
            driver = self._get_or_create_driver(driver_name, race.season_id, constructor.id)
            # 创建比赛结果
            self._create_race_result(result, race, driver, constructor)
        except Exception as e:
            logger.error(f"处理车手结果时发生错误: {e}")
    
    def _get_or_create_constructor(self, constructor_name: str, season_id: int) -> Constructor:
        """获取或创建车队记录"""
        if not constructor_name:
            constructor_name = 'Unknown'
        existing_constructor = self.db.query(Constructor).filter(
            Constructor.name.ilike(f"%{constructor_name}%"),
            Constructor.season_id == season_id
        ).first()
        if existing_constructor:
            return existing_constructor
        # 创建新车队记录
        constructor = Constructor(
            constructor_id=f"constructor_{constructor_name.lower().replace(' ', '_')}",
            name=constructor_name,
            nationality="",  # FastF1 可能没有这些详细信息
            season_id=season_id,
            base="",
            team_chief="",
            technical_chief="",
            power_unit="",
            is_active=True,
            championships=0,
            wins=0,
            podiums=0,
            poles=0,
            fastest_laps=0
        )
        self.db.add(constructor)
        self.db.commit()
        self.db.refresh(constructor)
        logger.info(f"创建车队: {constructor.name}")
        return constructor
    
    def _get_or_create_driver(self, driver_name: str, season_id: int, constructor_id: int) -> Driver:
        """获取或创建车手记录"""
        if not driver_name:
            driver_name = 'Unknown'
        existing_driver = self.db.query(Driver).filter(
            Driver.full_name.ilike(f"%{driver_name}%"),
            Driver.season_id == season_id
        ).first()
        if existing_driver:
            return existing_driver
        # 解析车手姓名
        name_parts = driver_name.split()
        first_name = name_parts[0] if len(name_parts) > 0 else ""
        last_name = " ".join(name_parts[1:]) if len(name_parts) > 1 else ""
        # 创建新车手记录
        driver = Driver(
            driver_id=f"driver_{driver_name.lower().replace(' ', '_')}",
            code="",  # FastF1 可能没有这些详细信息
            first_name=first_name,
            last_name=last_name,
            full_name=driver_name,
            date_of_birth=None,
            nationality="",
            number=None,
            season_id=season_id,
            constructor_id=constructor_id,
            is_active=True,
            championships=0,
            wins=0,
            podiums=0,
            poles=0,
            fastest_laps=0
        )
        self.db.add(driver)
        self.db.commit()
        self.db.refresh(driver)
        logger.info(f"创建车手: {driver.full_name}")
        return driver
    
    def _create_race_result(self, result: pd.Series, race: Race, driver: Driver, constructor: Constructor):
        """创建比赛结果记录"""
        # 检查是否已存在结果
        existing_result = self.db.query(Result).filter(
            Result.race_id == race.id,
            Result.driver_id == driver.id
        ).first()
        if existing_result:
            return
        # 解析位置
        position = None
        position_text = result.get('Position', '')
        if pd.notna(position_text) and position_text != 'NC':
            try:
                position = int(position_text)
            except (ValueError, TypeError):
                pass
        # 解析积分
        points = result.get('Points', 0)
        if pd.isna(points):
            points = 0
        # 创建比赛结果记录
        race_result = Result(
            race_id=race.id,
            driver_id=driver.id,
            constructor_id=constructor.id,
            position=position,
            position_text=position_text,
            points=float(points),
            grid_position=result.get('Grid', None),
            qualifying_position=None,
            status=result.get('Status', ''),
            laps_completed=result.get('Laps', None),
            fastest_lap=result.get('FastestLap', None),
            fastest_lap_rank=None,
            finish_time=None,
            gap_to_leader=None,
            gap_to_previous=None,
            penalties="",
            notes="",
            is_active=True
        )
        self.db.add(race_result)
        self.db.commit()
        logger.debug(f"创建比赛结果: {driver.full_name} - 位置 {position_text}")
    
    async def update_current_season(self):
        """更新当前赛季数据"""
        current_year = datetime.now().year
        logger.info(f"更新 {current_year} 赛季数据...")
        await self._process_season(current_year)
    
    async def get_season_summary(self, year: int) -> dict:
        """获取赛季摘要信息"""
        try:
            season = fastf1.get_season(year)
            races = fastf1.get_event_schedule(year)
            return {
                "year": year,
                "total_races": len(races),
                "races": races['EventName'].tolist() if 'EventName' in races.columns else races['Event'].tolist(),
                "circuits": races['CircuitShortName'].unique().tolist() if 'CircuitShortName' in races.columns else races['Circuit'].unique().tolist()
            }
        except Exception as e:
            logger.error(f"获取 {year} 赛季摘要时发生错误: {e}")
            return {} 