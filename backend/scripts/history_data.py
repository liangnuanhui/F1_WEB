#!/usr/bin/env python3
"""
历史数据实时拉取脚本
使用统一的 FastF1 数据提供者
"""

import argparse
import logging
import sys

from app.core.database import get_db
from app.services.data_sync_service import DataSyncService

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def sync_historical_data(start_year: int = 1950, end_year: int = 2024, cache_dir: str = None):
    """同步历史赛季数据"""
    logger.info(f"开始同步历史赛季数据 ({start_year}-{end_year})...")
    
    db = next(get_db())
    sync_service = DataSyncService(cache_dir=cache_dir)
    
    try:
        # 使用新的同步方法
        success = sync_service.sync_all_data(db, start_year=start_year, end_year=end_year)
        
        if success:
            logger.info("历史赛季数据同步完成！")
        else:
            logger.warning("部分历史数据同步失败")
        
    except Exception as e:
        logger.error(f"同步历史数据时发生错误: {e}")
        db.rollback()
    finally:
        db.close()


def sync_season_data(season: int, cache_dir: str = None):
    """同步指定赛季数据"""
    logger.info(f"开始同步 {season} 赛季数据...")
    
    db = next(get_db())
    sync_service = DataSyncService(cache_dir=cache_dir)
    
    try:
        # 使用新的同步方法
        success = sync_service.sync_all_data(db, season=season)
        
        if success:
            logger.info(f"{season} 赛季数据同步完成！")
        else:
            logger.warning(f"{season} 赛季部分数据同步失败")
        
    except Exception as e:
        logger.error(f"同步 {season} 赛季数据时发生错误: {e}")
        db.rollback()
    finally:
        db.close()


def main():
    parser = argparse.ArgumentParser(description='F1 历史数据同步工具')
    parser.add_argument('mode', choices=['all', 'season'], help='同步模式: all(年份范围) 或 season(单赛季)')
    parser.add_argument('--start-year', type=int, default=1950, help='开始年份 (默认: 1950)')
    parser.add_argument('--end-year', type=int, default=2024, help='结束年份 (默认: 2024)')
    parser.add_argument('--season', type=int, help='指定赛季 (仅在 mode=season 时使用)')
    parser.add_argument('--cache-dir', help='FastF1 缓存目录')
    
    args = parser.parse_args()
    
    if args.mode == 'all':
        sync_historical_data(args.start_year, args.end_year, args.cache_dir)
    elif args.mode == 'season':
        if not args.season:
            logger.error("season 模式需要指定 --season 参数")
            sys.exit(1)
        sync_season_data(args.season, args.cache_dir)


if __name__ == '__main__':
    main() 