#!/usr/bin/env python3
"""
调试race表查询问题
"""

import sys
from pathlib import Path
import logging

project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.race import Race
from app.models.season import Season

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def debug_race_query():
    """调试race表查询问题"""
    logger.info("🔍 调试race表查询问题...")
    
    try:
        db = next(get_db())
        
        # 1. 检查所有比赛记录
        all_races = db.query(Race).all()
        logger.info(f"📊 数据库中总共有 {len(all_races)} 场比赛")
        
        # 2. 检查所有赛季
        all_seasons = db.query(Season).all()
        logger.info(f"📊 数据库中总共有 {len(all_seasons)} 个赛季")
        for season in all_seasons:
            logger.info(f"  - 赛季 {season.year} (ID: {season.id})")
        
        # 3. 检查2025赛季是否存在
        season_2025 = db.query(Season).filter(Season.year == 2025).first()
        if season_2025:
            logger.info(f"✅ 找到2025赛季 (ID: {season_2025.id})")
        else:
            logger.error("❌ 没有找到2025赛季")
            return False
        
        # 4. 检查2025赛季的比赛
        races_2025 = db.query(Race).filter(Race.season_id == 2025).all()
        logger.info(f"📊 2025赛季有 {len(races_2025)} 场比赛")
        
        # 5. 检查season_id字段的值
        unique_season_ids = db.query(Race.season_id).distinct().all()
        logger.info(f"📊 race表中的season_id值: {[sid[0] for sid in unique_season_ids]}")
        
        # 6. 显示前5场比赛的详细信息
        logger.info("📋 前5场比赛的详细信息:")
        for i, race in enumerate(races_2025[:5]):
            logger.info(f"  {i+1}. 第{race.round_number}轮: {race.official_event_name}")
            logger.info(f"      season_id: {race.season_id}")
            logger.info(f"      event_format: {race.event_format}")
            logger.info(f"      is_sprint: {race.is_sprint}")
        
        # 7. 检查冲刺赛格式的比赛
        sprint_format_races = db.query(Race).filter(
            Race.event_format == 'sprint_qualifying'
        ).all()
        logger.info(f"📊 冲刺赛格式的比赛: {len(sprint_format_races)} 场")
        for race in sprint_format_races:
            logger.info(f"  - 第{race.round_number}轮: {race.official_event_name} (season_id: {race.season_id}, is_sprint: {race.is_sprint})")
        
        # 8. 检查标记为冲刺赛的比赛
        sprint_races = db.query(Race).filter(Race.is_sprint == True).all()
        logger.info(f"📊 标记为冲刺赛的比赛: {len(sprint_races)} 场")
        for race in sprint_races:
            logger.info(f"  - 第{race.round_number}轮: {race.official_event_name} (season_id: {race.season_id}, 格式: {race.event_format})")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ 调试失败: {e}", exc_info=True)
        return False
    finally:
        db.close()

if __name__ == "__main__":
    debug_race_query() 