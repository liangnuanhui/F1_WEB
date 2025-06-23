#!/usr/bin/env python3
"""
检查数据库中的冲刺赛状态
"""

import sys
from pathlib import Path
import logging

project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.race import Race

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def check_sprint_races():
    """检查数据库中的冲刺赛状态"""
    logger.info("🔍 检查数据库中的冲刺赛状态...")
    
    try:
        db = next(get_db())
        
        # 1. 检查所有2025赛季的比赛
        all_races = db.query(Race).filter(
            Race.season_id == 2025
        ).order_by(Race.round_number).all()
        
        logger.info(f"📊 2025赛季总共有 {len(all_races)} 场比赛")
        
        # 2. 检查冲刺赛格式的比赛
        sprint_format_races = db.query(Race).filter(
            Race.season_id == 2025,
            Race.event_format == 'sprint_qualifying'
        ).order_by(Race.round_number).all()
        
        logger.info(f"📊 冲刺赛格式的比赛: {len(sprint_format_races)} 场")
        for race in sprint_format_races:
            logger.info(f"  - 第{race.round_number}轮: {race.official_event_name} (is_sprint: {race.is_sprint})")
        
        # 3. 检查标记为冲刺赛的比赛
        sprint_races = db.query(Race).filter(
            Race.season_id == 2025,
            Race.is_sprint == True
        ).order_by(Race.round_number).all()
        
        logger.info(f"📊 标记为冲刺赛的比赛: {len(sprint_races)} 场")
        for race in sprint_races:
            logger.info(f"  - 第{race.round_number}轮: {race.official_event_name} (格式: {race.event_format})")
        
        # 4. 检查不匹配的情况
        logger.info("🔍 检查不匹配的情况...")
        
        # 格式是冲刺赛但is_sprint为False的
        format_sprint_but_not_marked = db.query(Race).filter(
            Race.season_id == 2025,
            Race.event_format == 'sprint_qualifying',
            Race.is_sprint == False
        ).all()
        
        if format_sprint_but_not_marked:
            logger.warning(f"⚠️ 格式是冲刺赛但is_sprint为False的比赛: {len(format_sprint_but_not_marked)} 场")
            for race in format_sprint_but_not_marked:
                logger.warning(f"  - 第{race.round_number}轮: {race.official_event_name}")
        
        # is_sprint为True但格式不是冲刺赛的
        marked_sprint_but_not_format = db.query(Race).filter(
            Race.season_id == 2025,
            Race.event_format != 'sprint_qualifying',
            Race.is_sprint == True
        ).all()
        
        if marked_sprint_but_not_format:
            logger.warning(f"⚠️ is_sprint为True但格式不是冲刺赛的比赛: {len(marked_sprint_but_not_format)} 场")
            for race in marked_sprint_but_not_format:
                logger.warning(f"  - 第{race.round_number}轮: {race.official_event_name} (格式: {race.event_format})")
        
        # 5. 显示所有比赛的基本信息
        logger.info("📋 所有2025赛季比赛:")
        for race in all_races:
            logger.info(f"  - 第{race.round_number}轮: {race.official_event_name} (格式: {race.event_format}, is_sprint: {race.is_sprint})")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ 检查失败: {e}", exc_info=True)
        return False
    finally:
        db.close()

if __name__ == "__main__":
    check_sprint_races() 