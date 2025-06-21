#!/usr/bin/env python3
"""
FastF1 数据同步脚本
基于实际数据结构进行数据同步
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
from app.services.fastf1_sync_service import FastF1SyncService

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('fastf1_sync.log')
    ]
)

logger = logging.getLogger(__name__)


def main():
    """主函数"""
    logger.info("🚀 开始FastF1数据同步...")
    
    try:
        # 获取数据库会话
        db = next(get_db())
        
        # 创建同步服务
        sync_service = FastF1SyncService(db)
        
        # 执行数据同步
        sync_service.sync_all_data()
        
        logger.info("✅ FastF1数据同步完成！")
        
    except Exception as e:
        logger.error(f"❌ 数据同步失败: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    main() 