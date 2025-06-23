#!/usr/bin/env python3
"""
修复冲刺赛的is_sprint字段（使用正确的赛季ID）
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

def fix_sprint_races_correct():
    """修复冲刺赛的is_sprint字段（使用正确的赛季ID）"""
    logger.info("🔧 开始修复冲刺赛的is_sprint字段...")
    
    try:
        db = next(get_db())
        
        # 1. 获取2025赛季的ID
        season_2025 = db.query(Season).filter(Season.year == 2025).first()
        if not season_2025:
            logger.error("❌ 未找到2025赛季")
            return False
        
        logger.info(f"✅ 找到2025赛季: ID={season_2025.id}")
        
        # 2. 检查当前状态
        all_races = db.query(Race).filter(Race.season_id == season_2025.id).order_by(Race.round_number).all()
        
        logger.info(f"📊 2025赛季共有 {len(all_races)} 场比赛:")
        for race in all_races:
            logger.info(f"  - 第{race.round_number}轮: {race.official_event_name}")
            logger.info(f"    格式: '{race.event_format}', is_sprint: {race.is_sprint}")
        
        # 3. 找出所有冲刺赛
        sprint_races = db.query(Race).filter(
            Race.season_id == season_2025.id,
            Race.event_format == 'sprint_qualifying'
        ).all()
        
        logger.info(f"📊 找到 {len(sprint_races)} 场冲刺赛:")
        for race in sprint_races:
            logger.info(f"  - 第{race.round_number}轮: {race.official_event_name}")
        
        # 4. 修复is_sprint字段
        fixed_count = 0
        for race in sprint_races:
            if not race.is_sprint:
                race.is_sprint = True
                fixed_count += 1
                logger.info(f"✅ 修复第{race.round_number}轮: {race.official_event_name}")
        
        # 5. 确保非冲刺赛的is_sprint为False
        non_sprint_races = db.query(Race).filter(
            Race.season_id == season_2025.id,
            Race.event_format != 'sprint_qualifying'
        ).all()
        
        for race in non_sprint_races:
            if race.is_sprint:
                race.is_sprint = False
                fixed_count += 1
                logger.info(f"✅ 修复第{race.round_number}轮: {race.official_event_name} (设为非冲刺赛)")
        
        # 6. 提交更改
        if fixed_count > 0:
            db.commit()
            logger.info(f"✅ 修复完成，共修复 {fixed_count} 场比赛")
        else:
            logger.info("✅ 无需修复，所有字段都正确")
        
        # 7. 验证修复结果
        sprint_races_after = db.query(Race).filter(
            Race.season_id == season_2025.id,
            Race.is_sprint == True
        ).order_by(Race.round_number).all()
        
        logger.info(f"📊 修复后的冲刺赛数量: {len(sprint_races_after)}")
        for race in sprint_races_after:
            logger.info(f"  - 第{race.round_number}轮: {race.official_event_name}")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ 修复失败: {e}")
        return False
    finally:
        db.close()

if __name__ == "__main__":
    fix_sprint_races_correct() 