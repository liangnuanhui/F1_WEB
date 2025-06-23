#!/usr/bin/env python3
"""
检查数据库的当前状态
"""

import sys
from pathlib import Path
import logging

project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.season import Season
from app.models.race import Race
from app.models.circuit import Circuit

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def check_database_state():
    """检查数据库的当前状态"""
    logger.info("🔍 检查数据库的当前状态...")
    
    try:
        db = next(get_db())
        
        # 1. 检查赛季数据
        seasons = db.query(Season).all()
        logger.info(f"📊 数据库中共有 {len(seasons)} 个赛季:")
        for season in seasons:
            logger.info(f"  - ID: {season.id}, 年份: {season.year}, 名称: {season.name}")
        
        # 2. 检查2025赛季
        season_2025 = db.query(Season).filter(Season.year == 2025).first()
        if season_2025:
            logger.info(f"✅ 找到2025赛季: ID={season_2025.id}")
        else:
            logger.error("❌ 未找到2025赛季")
            return False
        
        # 3. 检查比赛数据
        races_2025 = db.query(Race).filter(Race.season_id == season_2025.id).all()
        logger.info(f"📊 2025赛季共有 {len(races_2025)} 场比赛:")
        
        if len(races_2025) == 0:
            logger.warning("⚠️ 2025赛季没有比赛数据")
            
            # 检查是否有其他赛季的比赛数据
            all_races = db.query(Race).all()
            logger.info(f"📊 数据库中总共有 {len(all_races)} 场比赛")
            
            if len(all_races) > 0:
                logger.info("📊 其他赛季的比赛:")
                for race in all_races:
                    logger.info(f"  - 赛季ID: {race.season_id}, 轮次: {race.round_number}, 名称: {race.official_event_name}")
        else:
            for race in races_2025:
                logger.info(f"  - 第{race.round_number}轮: {race.official_event_name}")
                logger.info(f"    格式: {race.event_format}, is_sprint: {race.is_sprint}")
        
        # 4. 检查赛道数据
        circuits = db.query(Circuit).all()
        logger.info(f"📊 数据库中共有 {len(circuits)} 个赛道")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ 检查失败: {e}")
        return False
    finally:
        db.close()

if __name__ == "__main__":
    check_database_state() 