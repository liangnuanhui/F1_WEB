#!/usr/bin/env python3
"""
完整数据同步脚本
使用统一同步服务同步所有F1数据
支持动态年份，获取连续三年数据
"""

import sys
import os
import logging
from datetime import datetime
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


def get_continuous_three_years():
    """获取连续三年的年份：前一年、当前年、后一年"""
    current_year = datetime.now().year
    previous_year = current_year - 1
    next_year = current_year + 1
    
    return [previous_year, current_year, next_year]


def main():
    """主函数"""
    # 获取连续三年的年份
    target_seasons = get_continuous_three_years()
    current_year = datetime.now().year
    
    logger.info(f"🚀 开始完整数据同步 (连续三年: {target_seasons[0]}-{target_seasons[1]}-{target_seasons[2]})...")
    logger.info(f"📅 当前年份: {current_year}")
    
    try:
        # 获取数据库会话
        db = next(get_db())
        
        # 创建统一同步服务
        sync_service = UnifiedSyncService(db, cache_dir="./cache")
        
        # 同步连续三年的所有数据
        logger.info(f"🎯 同步目标赛季: {target_seasons}")
        sync_service.sync_all_data(target_seasons=target_seasons)
        
        logger.info(f"✅ 连续三年数据同步完成！")
        logger.info(f"📊 已同步赛季: {target_seasons}")
        
    except Exception as e:
        logger.error(f"❌ 数据同步失败: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    main() 