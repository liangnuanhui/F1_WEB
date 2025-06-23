#!/usr/bin/env python3
"""
完整的冲刺赛同步测试
"""

import sys
from pathlib import Path
import logging

project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.unified_sync_service import UnifiedSyncService

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def test_sprint_sync_complete():
    logger.info("🧪 开始完整冲刺赛同步测试...")
    
    try:
        db = next(get_db())
        sync_service = UnifiedSyncService(db, cache_dir="./cache")
        
        # 1. 检查冲刺赛标识
        from app.models.race import Race
        sprint_races = db.query(Race).filter(
            Race.season_id == 2025,
            Race.is_sprint == True
        ).order_by(Race.round_number).all()
        
        logger.info(f"📊 数据库中找到 {len(sprint_races)} 场冲刺赛:")
        for race in sprint_races:
            logger.info(f"  - 第{race.round_number}轮: {race.official_event_name} (格式: {race.event_format})")
        
        if len(sprint_races) == 0:
            logger.error("❌ 没有找到冲刺赛，请先运行 fix_sprint_races.py")
            return False
        
        # 2. 同步冲刺赛结果
        logger.info("🔄 开始同步冲刺赛结果...")
        success = sync_service.sync_sprint_results(2025)
        
        if success:
            logger.info("✅ 冲刺赛结果同步成功！")
            
            # 显示统计信息
            from app.models.sprint_result import SprintResult
            sprint_count = db.query(SprintResult).count()
            logger.info(f"📊 冲刺赛结果总数: {sprint_count}")
            
            # 按比赛分组显示结果
            for race in sprint_races:
                race_results = db.query(SprintResult).filter(
                    SprintResult.race_id == race.id
                ).order_by(SprintResult.position).all()
                
                logger.info(f"📋 第{race.round_number}轮 {race.official_event_name} ({len(race_results)}条记录):")
                for result in race_results[:5]:  # 只显示前5名
                    logger.info(f"    {result.position}. {result.driver_id} ({result.constructor_id}) - {result.points}分")
                if len(race_results) > 5:
                    logger.info(f"    ... 还有 {len(race_results) - 5} 条记录")
        else:
            logger.warning("⚠️ 冲刺赛结果同步失败")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ 测试失败: {e}")
        return False
    finally:
        db.close()

if __name__ == "__main__":
    test_sprint_sync_complete() 