#!/usr/bin/env python3
"""
完整数据同步脚本
使用统一同步服务同步所有F1数据
"""

import sys
import os
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
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('unified_sync.log')
    ]
)

logger = logging.getLogger(__name__)


def main():
    """主函数"""
    logger.info("🚀 开始完整数据同步...")
    
    try:
        # 获取数据库会话
        db = next(get_db())
        
        # 创建统一同步服务
        sync_service = UnifiedSyncService(db, cache_dir="./cache")
        
        # 同步所有数据
        # 使用服务中定义的目标赛季，或者可以自定义
        sync_service.sync_all_data()  # 使用默认的 TARGET_SEASONS = [2023, 2024, 2025]
        
        # 或者只同步特定赛季（可选）
        # sync_service.sync_all_data(target_seasons=[2025])  # 只同步2025赛季
        # sync_service.sync_all_data(target_seasons=[2024, 2025])  # 同步2024-2025赛季
        
        logger.info("✅ 完整数据同步完成！")
        
    except Exception as e:
        logger.error(f"❌ 数据同步失败: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    main() 