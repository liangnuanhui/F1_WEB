#!/usr/bin/env python3
"""
双数据库同步脚本 - 同时同步本地和Render数据库
用于比赛后数据更新
"""
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

def sync_to_database(db_url, db_name):
    """同步数据到指定数据库"""
    logging.info(f"🚀 开始同步数据到 {db_name} 数据库...")
    
    # 临时设置数据库URL
    original_db_url = os.environ.get('DATABASE_URL')
    os.environ['DATABASE_URL'] = db_url
    
    try:
        # 重新创建数据库会话
        from app.core.database import SessionLocal
        db = SessionLocal()
        sync_service = UnifiedSyncService(db=db, cache_dir="cache")
        
        season_to_sync = 2025
        success_count = 0
        
        # 1. 同步车手积分榜
        logging.info(f"--- 同步 {season_to_sync} 赛季车手积分榜到 {db_name} ---")
        if sync_service.sync_driver_standings(season_to_sync):
            logging.info(f"✅ {db_name}: 车手积分榜同步成功")
            success_count += 1
        else:
            logging.error(f"❌ {db_name}: 车手积分榜同步失败")

        # 2. 同步车队积分榜
        logging.info(f"--- 同步 {season_to_sync} 赛季车队积分榜到 {db_name} ---")
        if sync_service.sync_constructor_standings(season_to_sync):
            logging.info(f"✅ {db_name}: 车队积分榜同步成功")
            success_count += 1
        else:
            logging.error(f"❌ {db_name}: 车队积分榜同步失败")

        # 3. 同步比赛结果
        logging.info(f"--- 同步 {season_to_sync} 赛季比赛结果到 {db_name} ---")
        if sync_service.sync_race_results(season_to_sync):
            logging.info(f"✅ {db_name}: 比赛结果同步成功")
            success_count += 1
        else:
            logging.error(f"❌ {db_name}: 比赛结果同步失败")

        # 4. 同步排位赛结果
        logging.info(f"--- 同步 {season_to_sync} 赛季排位赛结果到 {db_name} ---")
        if sync_service.sync_qualifying_results(season_to_sync):
            logging.info(f"✅ {db_name}: 排位赛结果同步成功")
            success_count += 1
        else:
            logging.error(f"❌ {db_name}: 排位赛结果同步失败")

        # 5. 同步冲刺赛结果
        logging.info(f"--- 同步 {season_to_sync} 赛季冲刺赛结果到 {db_name} ---")
        if sync_service.sync_sprint_results(season_to_sync):
            logging.info(f"✅ {db_name}: 冲刺赛结果同步成功")
            success_count += 1
        else:
            logging.error(f"❌ {db_name}: 冲刺赛结果同步失败")

        db.close()
        logging.info(f"🏁 {db_name} 数据库同步完成，成功: {success_count}/5")
        return success_count == 5

    except Exception as e:
        logging.error(f"❌ {db_name} 数据库同步过程中发生错误: {e}", exc_info=True)
        return False
    finally:
        # 恢复原始数据库URL
        if original_db_url:
            os.environ['DATABASE_URL'] = original_db_url
        elif 'DATABASE_URL' in os.environ:
            del os.environ['DATABASE_URL']

def dual_database_sync():
    """执行双数据库同步"""
    logging.info("🎯 开始执行双数据库同步...")
    
    # 数据库配置
    local_db_url = "postgresql://f1_user:f1_password@localhost:5432/f1_web"
    render_db_url = "postgresql://f1_user:2VOxvRBuis4t6KaoERGUTwGgJLQ9kfWo@dpg-d1r32dripnbc73f00tbg-a.oregon-postgres.render.com/f1_web"
    
    results = {}
    
    # 同步到本地数据库
    results['local'] = sync_to_database(local_db_url, "本地")
    
    # 同步到Render数据库
    results['render'] = sync_to_database(render_db_url, "Render")
    
    # 总结结果
    logging.info("=" * 50)
    logging.info("📊 双数据库同步结果总结:")
    logging.info(f"   本地数据库: {'✅ 成功' if results['local'] else '❌ 失败'}")
    logging.info(f"   Render数据库: {'✅ 成功' if results['render'] else '❌ 失败'}")
    
    if results['local'] and results['render']:
        logging.info("🎉 双数据库同步全部成功！")
        return True
    else:
        logging.warning("⚠️ 部分数据库同步失败，请检查日志")
        return False

if __name__ == "__main__":
    dual_database_sync()