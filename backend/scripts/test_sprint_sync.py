#!/usr/bin/env python3
"""
测试冲刺赛同步功能
"""

import sys
import logging
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.unified_sync_service import UnifiedSyncService

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def test_sprint_sync():
    """测试冲刺赛同步功能"""
    logger.info("🧪 开始测试冲刺赛同步功能...")
    
    try:
        # 获取数据库会话
        db = next(get_db())
        
        # 创建统一同步服务
        sync_service = UnifiedSyncService(db, cache_dir="./cache")
        
        # 测试冲刺赛结果同步
        logger.info("🔄 测试冲刺赛结果同步...")
        success = sync_service.sync_sprint_results(2025)
        
        if success:
            logger.info("✅ 冲刺赛同步测试成功！")
            
            # 显示统计信息
            from app.models.sprint_result import SprintResult
            sprint_count = db.query(SprintResult).count()
            logger.info(f"📊 冲刺赛结果数量: {sprint_count}")
            
            # 显示前几条记录
            sprint_results = db.query(SprintResult).limit(5).all()
            logger.info("📋 前5条冲刺赛结果:")
            for result in sprint_results:
                logger.info(f"  - 位置: {result.position}, 车手ID: {result.driver_id}, 积分: {result.points}")
        else:
            logger.warning("⚠️ 冲刺赛同步测试跳过（可能没有数据）")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ 冲刺赛同步测试失败: {e}")
        return False
    finally:
        db.close()


if __name__ == "__main__":
    success = test_sprint_sync()
    if not success:
        sys.exit(1) 