#!/usr/bin/env python3
"""
智能双数据库同步脚本 - 支持灵活的同步选项
用于比赛后数据更新
"""
import argparse
import logging
import os
import sys
from pathlib import Path

# 将项目根目录添加到 Python 路径
sys.path.append(str(Path(__file__).parent.parent))

from app.core.database import SessionLocal
from app.services.unified_sync_service import UnifiedSyncService

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# 数据库配置
DATABASE_CONFIGS = {
    'local': "postgresql://f1_user:f1_password@localhost:5432/f1_web",
    'render': "postgresql://f1_user:2VOxvRBuis4t6KaoERGUTwGgJLQ9kfWo@dpg-d1r32dripnbc73f00tbg-a.oregon-postgres.render.com/f1_web"
}

SYNC_FUNCTIONS = {
    'standings': {
        'drivers': 'sync_driver_standings',
        'constructors': 'sync_constructor_standings'
    },
    'results': {
        'race': 'sync_race_results',
        'qualifying': 'sync_qualifying_results', 
        'sprint': 'sync_sprint_results'
    }
}

def sync_to_database(db_url, db_name, season_year=2025, data_types=None):
    """同步数据到指定数据库"""
    logging.info(f"🚀 开始同步数据到 {db_name} 数据库...")
    
    if data_types is None:
        data_types = ['drivers', 'constructors', 'race', 'qualifying', 'sprint']
    
    # 临时设置数据库URL
    original_db_url = os.environ.get('DATABASE_URL')
    os.environ['DATABASE_URL'] = db_url
    
    try:
        # 重新创建数据库会话
        from app.core.database import SessionLocal
        db = SessionLocal()
        sync_service = UnifiedSyncService(db=db, cache_dir="cache")
        
        success_count = 0
        total_count = len(data_types)
        
        for data_type in data_types:
            if data_type == 'drivers':
                logging.info(f"--- 同步 {season_year} 赛季车手积分榜到 {db_name} ---")
                if sync_service.sync_driver_standings(season_year):
                    logging.info(f"✅ {db_name}: 车手积分榜同步成功")
                    success_count += 1
                else:
                    logging.error(f"❌ {db_name}: 车手积分榜同步失败")
                    
            elif data_type == 'constructors':
                logging.info(f"--- 同步 {season_year} 赛季车队积分榜到 {db_name} ---")
                if sync_service.sync_constructor_standings(season_year):
                    logging.info(f"✅ {db_name}: 车队积分榜同步成功")
                    success_count += 1
                else:
                    logging.error(f"❌ {db_name}: 车队积分榜同步失败")
                    
            elif data_type == 'race':
                logging.info(f"--- 同步 {season_year} 赛季比赛结果到 {db_name} ---")
                if sync_service.sync_race_results(season_year):
                    logging.info(f"✅ {db_name}: 比赛结果同步成功")
                    success_count += 1
                else:
                    logging.error(f"❌ {db_name}: 比赛结果同步失败")
                    
            elif data_type == 'qualifying':
                logging.info(f"--- 同步 {season_year} 赛季排位赛结果到 {db_name} ---")
                if sync_service.sync_qualifying_results(season_year):
                    logging.info(f"✅ {db_name}: 排位赛结果同步成功")
                    success_count += 1
                else:
                    logging.error(f"❌ {db_name}: 排位赛结果同步失败")
                    
            elif data_type == 'sprint':
                logging.info(f"--- 同步 {season_year} 赛季冲刺赛结果到 {db_name} ---")
                if sync_service.sync_sprint_results(season_year):
                    logging.info(f"✅ {db_name}: 冲刺赛结果同步成功")
                    success_count += 1
                else:
                    logging.error(f"❌ {db_name}: 冲刺赛结果同步失败")

        db.close()
        logging.info(f"🏁 {db_name} 数据库同步完成，成功: {success_count}/{total_count}")
        return success_count == total_count

    except Exception as e:
        logging.error(f"❌ {db_name} 数据库同步过程中发生错误: {e}", exc_info=True)
        return False
    finally:
        # 恢复原始数据库URL
        if original_db_url:
            os.environ['DATABASE_URL'] = original_db_url
        elif 'DATABASE_URL' in os.environ:
            del os.environ['DATABASE_URL']

def main():
    parser = argparse.ArgumentParser(description='F1比赛后双数据库同步工具')
    parser.add_argument('--databases', '-d', 
                        choices=['local', 'render', 'both'], 
                        default='both',
                        help='选择要同步的数据库 (默认: both)')
    parser.add_argument('--season', '-s', 
                        type=int, 
                        default=2025,
                        help='赛季年份 (默认: 2025)')
    parser.add_argument('--data-types', '-t',
                        nargs='+',
                        choices=['drivers', 'constructors', 'race', 'qualifying', 'sprint'],
                        default=['drivers', 'constructors', 'race', 'qualifying', 'sprint'],
                        help='选择要同步的数据类型 (默认: 全部)')
    parser.add_argument('--verbose', '-v',
                        action='store_true',
                        help='显示详细日志')
    
    args = parser.parse_args()
    
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    logging.info("🎯 F1比赛后数据同步开始...")
    logging.info(f"   数据库: {args.databases}")
    logging.info(f"   赛季: {args.season}")
    logging.info(f"   数据类型: {', '.join(args.data_types)}")
    
    results = {}
    
    if args.databases in ['local', 'both']:
        results['local'] = sync_to_database(
            DATABASE_CONFIGS['local'], 
            "本地", 
            args.season, 
            args.data_types
        )
    
    if args.databases in ['render', 'both']:
        results['render'] = sync_to_database(
            DATABASE_CONFIGS['render'], 
            "Render", 
            args.season, 
            args.data_types
        )
    
    # 总结结果
    logging.info("=" * 50)
    logging.info("📊 数据同步结果总结:")
    
    if 'local' in results:
        logging.info(f"   本地数据库: {'✅ 成功' if results['local'] else '❌ 失败'}")
    if 'render' in results:
        logging.info(f"   Render数据库: {'✅ 成功' if results['render'] else '❌ 失败'}")
    
    all_success = all(results.values())
    if all_success:
        logging.info("🎉 数据同步全部成功！")
        return 0
    else:
        logging.warning("⚠️ 部分数据库同步失败，请检查日志")
        return 1

if __name__ == "__main__":
    sys.exit(main())