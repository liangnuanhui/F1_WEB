#!/usr/bin/env python3
"""
测试完整赛季的比赛结果同步功能
"""

import sys
import logging
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from app.core.database import get_db
from app.services.unified_sync_service import UnifiedSyncService
from app.models.result import Result
from app.models.season import Season

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def test_full_race_results_sync():
    """测试完整赛季的比赛结果同步功能"""
    season_year = 2025
    logger.info(f"🧪 开始测试 {season_year} 赛季完整的比赛结果同步...")
    
    db = next(get_db())
    sync_service = UnifiedSyncService(db, cache_dir="./cache")
    
    try:
        # 调用核心同步函数
        success = sync_service.sync_race_results(season_year)
        
        if success:
            logger.info("✅ 比赛结果同步函数执行成功！")
            
            # 验证数据库中的记录总数
            season = db.query(Season).filter(Season.year == season_year).first()
            if season:
                race_ids = [race.id for race in season.races]
                final_count = db.query(Result).filter(Result.race_id.in_(race_ids)).count()
                logger.info(f"📊 数据库中最终为 {season_year} 赛季存储了 {final_count} 条比赛结果记录")
                
                if final_count > 0:
                    logger.info("📋 抽样检查第一条记录:")
                    first_res = db.query(Result).order_by(Result.id).first()
                    logger.info(f"  - Race ID: {first_res.race_id}, Driver: {first_res.driver_id}, Position: {first_res.position}, Points: {first_res.points}")
                    
                    logger.info("📋 抽样检查最后一条记录:")
                    last_res = db.query(Result).order_by(Result.id.desc()).first()
                    logger.info(f"  - Race ID: {last_res.race_id}, Driver: {last_res.driver_id}, Position: {last_res.position}, Points: {last_res.points}")
            else:
                logger.error(f"❌ 无法在数据库中找到 {season_year} 赛季进行验证")

        else:
            logger.error("❌ 比赛结果同步函数执行失败")

    except Exception as e:
        logger.error(f"❌ 测试脚本执行失败: {e}", exc_info=True)
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    test_full_race_results_sync() 