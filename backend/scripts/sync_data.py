#!/usr/bin/env python3
"""
数据同步脚本
使用统一的 FastF1 数据提供者
"""

import argparse
import logging
import sys

from app.core.database import engine, get_db
from app.models import BaseModel
from app.services.data_sync_service import DataSyncService

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

def init_database():
    """初始化数据库表"""
    print("正在创建数据库表...")
    BaseModel.metadata.create_all(bind=engine)
    print("数据库表创建完成！")

def sync_current_season(cache_dir: str = None):
    """同步当前赛季数据"""
    print("正在同步当前赛季数据...")
    
    db = next(get_db())
    sync_service = DataSyncService(cache_dir=cache_dir)
    
    try:
        success = sync_service.sync_all_data(db, season=2025)  # 当前赛季
        if success:
            print("当前赛季数据同步完成！")
        else:
            print("当前赛季数据同步失败")
    except Exception as e:
        print(f"同步当前赛季数据时发生错误: {e}")
        db.rollback()
    finally:
        db.close()

def sync_specific_data(data_type: str, season: int, round_number: int = None, cache_dir: str = None):
    """同步特定类型的数据"""
    print(f"正在同步 {data_type} 数据 (赛季: {season}, 轮次: {round_number or 'all'})...")
    
    db = next(get_db())
    sync_service = DataSyncService(cache_dir=cache_dir)
    
    try:
        success = False
        
        if data_type == 'drivers':
            success = sync_service.sync_drivers(db, season)
        elif data_type == 'constructors':
            success = sync_service.sync_constructors(db, season)
        elif data_type == 'circuits':
            success = sync_service.sync_circuits(db, season)
        elif data_type == 'race_results':
            success = sync_service.sync_race_results(db, season, round_number)
        elif data_type == 'qualifying_results':
            success = sync_service.sync_qualifying_results(db, season, round_number)
        elif data_type == 'driver_standings':
            success = sync_service.sync_driver_standings(db, season, round_number)
        elif data_type == 'constructor_standings':
            success = sync_service.sync_constructor_standings(db, season, round_number)
        else:
            print(f"不支持的数据类型: {data_type}")
            return
        
        if success:
            print(f"{data_type} 数据同步完成！")
        else:
            print(f"{data_type} 数据同步失败")
            
    except Exception as e:
        print(f"同步 {data_type} 数据时发生错误: {e}")
        db.rollback()
    finally:
        db.close()

def main():
    parser = argparse.ArgumentParser(description='F1 数据同步工具')
    parser.add_argument('command', choices=['init', 'current', 'drivers', 'constructors', 'circuits', 
                                          'race_results', 'qualifying_results', 'driver_standings', 'constructor_standings'],
                       help='同步命令')
    parser.add_argument('--season', type=int, default=2025, help='赛季年份 (默认: 2025)')
    parser.add_argument('--round', type=int, help='比赛轮次')
    parser.add_argument('--cache-dir', help='FastF1 缓存目录')
    
    args = parser.parse_args()
    
    if args.command == 'init':
        init_database()
    elif args.command == 'current':
        sync_current_season(args.cache_dir)
    else:
        sync_specific_data(args.command, args.season, args.round, args.cache_dir)

if __name__ == '__main__':
    main() 