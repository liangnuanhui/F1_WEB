#!/usr/bin/env python3
"""
最终冲刺赛同步测试
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

def test_sprint_sync_final():
    logger.info("🧪 开始最终冲刺赛同步测试...")
    
    try:
        db = next(get_db())
        sync_service = UnifiedSyncService(db, cache_dir="./cache")
        
        # 1. 重新同步比赛数据（设置is_sprint字段）
        logger.info("🔄 步骤1: 重新同步比赛数据...")
        races = sync_service.sync_races(2025)
        logger.info(f"✅ 同步了 {len(races)} 场比赛")
        
        # 2. 检查冲刺赛标识
        from app.models.race import Race
        sprint_races = db.query(Race).filter(
            Race.season_id == 2025,
            Race.is_sprint == True
        ).all()
        logger.info(f"📊 找到 {len(sprint_races)} 场冲刺赛:")
        for race in sprint_races:
            logger.info(f"  - 第{race.round_number}轮: {race.official_event_name} (格式: {race.event_format})")
        
        # 3. 同步冲刺赛结果
        logger.info("🔄 步骤2: 同步冲刺赛结果...")
        success = sync_service.sync_sprint_results(2025)
        
        if success:
            logger.info("✅ 冲刺赛结果同步成功！")
            
            # 显示统计信息
            from app.models.sprint_result import SprintResult
            sprint_count = db.query(SprintResult).count()
            logger.info(f"📊 冲刺赛结果总数: {sprint_count}")
            
            # 显示前3条记录
            sprint_results = db.query(SprintResult).limit(3).all()
            logger.info("📋 前3条冲刺赛结果:")
            for result in sprint_results:
                logger.info(f"  - 位置: {result.position}, 车手ID: {result.driver_id}, 积分: {result.points}")
        else:
            logger.warning("⚠️ 冲刺赛结果同步失败")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ 测试失败: {e}")
        return False
    finally:
        db.close()

if __name__ == "__main__":
    test_sprint_sync_final() 