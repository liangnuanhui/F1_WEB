#!/usr/bin/env python3
"""
只测试车手积分榜同步
"""

import sys
import os
import logging
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent
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


def test_driver_standings_only():
    """只测试车手积分榜同步"""
    logger.info("🧪 开始测试车手积分榜同步...")
    
    try:
        # 获取数据库会话
        db = next(get_db())
        
        # 创建统一同步服务
        sync_service = UnifiedSyncService(db, cache_dir="./cache")
        
        # 只同步车手积分榜
        success = sync_service.sync_driver_standings(2025)
        
        if success:
            logger.info("✅ 车手积分榜同步成功")
        else:
            logger.error("❌ 车手积分榜同步失败")
        
    except Exception as e:
        logger.error(f"❌ 测试失败: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    test_driver_standings_only() 