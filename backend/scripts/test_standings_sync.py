import logging
import sys
import os

# 将项目根目录添加到 Python 路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from app.core.database import SessionLocal
from app.services.unified_sync_service import UnifiedSyncService

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def test_sync_standings():
    """测试同步车手和车队积分榜数据"""
    logging.info("🚀 开始测试积分榜同步...")
    
    db = SessionLocal()
    sync_service = UnifiedSyncService(db=db, cache_dir="cache")
    
    season_to_sync = 2025
    
    try:
        # 1. 同步车手积分榜
        logging.info(f"--- 同步 {season_to_sync} 赛季车手积分榜 ---")
        driver_success = sync_service.sync_driver_standings(season_to_sync)
        if driver_success:
            logging.info(f"✅ {season_to_sync} 赛季车手积分榜同步成功。")
        else:
            logging.error(f"❌ {season_to_sync} 赛季车手积分榜同步失败。")

        # 2. 同步车队积分榜
        logging.info(f"--- 同步 {season_to_sync} 赛季车队积分榜 ---")
        constructor_success = sync_service.sync_constructor_standings(season_to_sync)
        if constructor_success:
            logging.info(f"✅ {season_to_sync} 赛季车队积分榜同步成功。")
        else:
            logging.error(f"❌ {season_to_sync} 赛季车队积分榜同步失败。")

    except Exception as e:
        logging.error(f"一个意外的错误发生: {e}", exc_info=True)
    finally:
        db.close()
        logging.info("🏁 积分榜同步测试完成。")

if __name__ == "__main__":
    test_sync_standings() 