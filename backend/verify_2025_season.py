#!/usr/bin/env python3
"""
验证2025赛季数据完整性
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

def verify_2025_season():
    """验证2025赛季数据完整性"""
    logger.info("🔍 验证2025赛季数据完整性...")
    
    try:
        db = next(get_db())
        
        # 1. 获取2025赛季
        season_2025 = db.query(Season).filter(Season.year == 2025).first()
        if not season_2025:
            logger.error("❌ 未找到2025赛季")
            return False
        
        logger.info(f"✅ 找到2025赛季: ID={season_2025.id}")
        
        # 2. 获取所有比赛
        all_races = db.query(Race).filter(Race.season_id == season_2025.id).order_by(Race.round_number).all()
        
        logger.info(f"📊 2025赛季共有 {len(all_races)} 场比赛")
        
        # 3. 按类型统计
        conventional_count = 0
        sprint_count = 0
        testing_count = 0
        
        logger.info("📊 比赛详情:")
        for race in all_races:
            logger.info(f"  - 第{race.round_number}轮: {race.official_event_name}")
            logger.info(f"    格式: {race.event_format}, is_sprint: {race.is_sprint}")
            
            if race.event_format == 'conventional':
                conventional_count += 1
            elif race.event_format == 'sprint_qualifying':
                sprint_count += 1
                if not race.is_sprint:
                    logger.warning(f"⚠️  冲刺赛is_sprint字段错误: 第{race.round_number}轮")
            elif race.event_format == 'testing':
                testing_count += 1
        
        # 4. 验证统计
        logger.info("📊 统计结果:")
        logger.info(f"  - 常规比赛: {conventional_count}场")
        logger.info(f"  - 冲刺赛: {sprint_count}场")
        logger.info(f"  - 季前测试: {testing_count}场")
        logger.info(f"  - 总计: {conventional_count + sprint_count + testing_count}场")
        
        # 5. 验证冲刺赛
        sprint_races = db.query(Race).filter(
            Race.season_id == season_2025.id,
            Race.is_sprint == True
        ).order_by(Race.round_number).all()
        
        logger.info(f"📊 冲刺赛验证: 找到 {len(sprint_races)} 场冲刺赛")
        for race in sprint_races:
            logger.info(f"  - 第{race.round_number}轮: {race.official_event_name}")
        
        # 6. 验证季前测试
        testing_race = db.query(Race).filter(
            Race.season_id == season_2025.id,
            Race.round_number == 0
        ).first()
        
        if testing_race:
            logger.info(f"✅ 季前测试验证通过: 第{testing_race.round_number}轮 {testing_race.official_event_name}")
        else:
            logger.warning("⚠️  未找到季前测试")
        
        # 7. 数据完整性检查
        expected_total = 25  # 0-24轮，共25场
        actual_total = len(all_races)
        
        if actual_total == expected_total:
            logger.info(f"✅ 数据完整性验证通过: 期望 {expected_total} 场，实际 {actual_total} 场")
        else:
            logger.warning(f"⚠️  数据完整性验证失败: 期望 {expected_total} 场，实际 {actual_total} 场")
        
        # 8. 冲刺赛数量验证
        expected_sprints = 6
        actual_sprints = len(sprint_races)
        
        if actual_sprints == expected_sprints:
            logger.info(f"✅ 冲刺赛数量验证通过: 期望 {expected_sprints} 场，实际 {actual_sprints} 场")
        else:
            logger.warning(f"⚠️  冲刺赛数量验证失败: 期望 {expected_sprints} 场，实际 {actual_sprints} 场")
        
        logger.info("🎉 2025赛季数据验证完成！")
        return True
        
    except Exception as e:
        logger.error(f"❌ 验证失败: {e}")
        return False
    finally:
        db.close()

if __name__ == "__main__":
    verify_2025_season() 