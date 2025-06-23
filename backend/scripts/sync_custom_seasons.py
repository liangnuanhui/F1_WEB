#!/usr/bin/env python3
"""
自定义赛季数据同步脚本
允许用户选择要同步的赛季
"""

import sys
import os
import logging
import argparse
from pathlib import Path
from datetime import datetime

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
        logging.FileHandler('custom_sync.log')
    ]
)

logger = logging.getLogger(__name__)


def parse_arguments():
    """解析命令行参数"""
    # 获取当前年份
    current_year = datetime.now().year
    previous_year = current_year - 1
    
    parser = argparse.ArgumentParser(description='F1 数据同步工具')
    parser.add_argument(
        '--seasons', 
        nargs='+', 
        type=int, 
        default=[previous_year, current_year],
        help=f'要同步的赛季列表 (默认: {previous_year} {current_year})'
    )
    parser.add_argument(
        '--current-only', 
        action='store_true',
        help=f'只同步当前赛季 ({current_year})'
    )
    parser.add_argument(
        '--recent-only', 
        action='store_true',
        help=f'只同步最近两个赛季 ({previous_year} {current_year})'
    )
    parser.add_argument(
        '--cache-dir', 
        type=str, 
        default='./cache',
        help='FastF1 缓存目录 (默认: ./cache)'
    )
    
    return parser.parse_args()


def main():
    """主函数"""
    args = parse_arguments()
    
    # 获取当前年份和前一年
    current_year = datetime.now().year
    previous_year = current_year - 1
    
    # 确定要同步的赛季
    if args.current_only:
        target_seasons = [current_year]
        logger.info(f"🎯 模式: 只同步当前赛季 ({current_year})")
    elif args.recent_only:
        target_seasons = [previous_year, current_year]
        logger.info(f"🎯 模式: 只同步最近两个赛季 ({previous_year}-{current_year})")
    else:
        target_seasons = args.seasons
        logger.info(f"🎯 模式: 自定义赛季 {target_seasons}")
    
    logger.info(f"🚀 开始同步赛季: {target_seasons}")
    
    try:
        # 获取数据库会话
        db = next(get_db())
        
        # 创建统一同步服务
        sync_service = UnifiedSyncService(db, cache_dir=args.cache_dir)
        
        # 同步指定赛季的数据
        sync_service.sync_all_data(target_seasons=target_seasons)
        
        logger.info(f"✅ 赛季 {target_seasons} 数据同步完成！")
        
    except Exception as e:
        logger.error(f"❌ 数据同步失败: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    main() 