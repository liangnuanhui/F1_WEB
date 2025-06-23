#!/usr/bin/env python3
"""
测试排位赛同步功能（前10轮）
"""

import sys
import logging
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from app.core.database import get_db
from app.services.unified_sync_service import UnifiedSyncService
from app.models.qualifying_result import QualifyingResult
from app.models.race import Race
from app.models.season import Season

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def test_qualifying_sync_partial():
    """测试部分赛季的排位赛同步功能"""
    logger.info("🧪 开始测试部分赛季（前10轮）的排位赛同步...")
    
    db = next(get_db())
    sync_service = UnifiedSyncService(db, cache_dir="./cache")
    season_year = 2025
    
    try:
        # 我们需要一个自定义的、只同步前10轮的函数
        # 为了不修改主服务代码，我们在这里实现这个逻辑
        
        logger.info(f"🏁 开始同步 {season_year} 赛季前10轮排位赛结果...")
        
        season = db.query(Season).filter(Season.year == season_year).first()
        if not season:
            logger.error(f"❌ 赛季 {season_year} 不存在")
            return
        
        # 获取前10轮比赛
        races_to_sync = db.query(Race).filter(
            Race.season_id == season.id,
            Race.round_number <= 10,
            Race.round_number > 0  # 排除季前测试
        ).order_by(Race.round_number).all()
        
        races_by_round = {r.round_number: r for r in races_to_sync}
        race_ids = [r.id for r in races_to_sync]
        
        logger.info(f"🎯 目标比赛轮次: {sorted(list(races_by_round.keys()))}")
        
        # 清除旧数据
        if race_ids:
            db.query(QualifyingResult).filter(QualifyingResult.race_id.in_(race_ids)).delete()
            db.commit()
            logger.info(f"🧹 清除了前10轮比赛的旧排位赛结果")

        total_synced = 0
        # 逐轮同步
        for round_num, race in races_by_round.items():
            logger.info(f"🔄 同步第 {round_num} 轮: {race.official_event_name}")
            qualifying_df = sync_service._handle_api_call(
                sync_service.ergast.get_qualifying_results,
                season=season_year,
                round=round_num
            )

            if qualifying_df is None or qualifying_df.empty:
                logger.warning(f"  - ⚠️ 第 {round_num} 轮没有排位赛数据")
                continue
            
            for _, row in qualifying_df.iterrows():
                driver = sync_service._get_or_create_driver_from_result(row)
                constructor = sync_service._get_or_create_constructor_from_result(row)
                if not driver or not constructor:
                    continue

                qualifying_result = QualifyingResult(
                    race_id=race.id,
                    driver_id=driver.driver_id,
                    constructor_id=constructor.constructor_id,
                    number=row.get('number'),
                    position=row.get('position'),
                    q1_time=str(row.get('q1', '')),
                    q2_time=str(row.get('q2', '')),
                    q3_time=str(row.get('q3', ''))
                )
                db.add(qualifying_result)
                total_synced += 1

            db.commit()
            logger.info(f"  - ✅ 第 {round_num} 轮同步了 {len(qualifying_df)} 条记录")

        logger.info(f"✅ 排位赛同步测试完成，共同步 {total_synced} 条记录")
        
        # 验证结果
        final_count = db.query(QualifyingResult).filter(QualifyingResult.race_id.in_(race_ids)).count()
        logger.info(f"📊 数据库中最终存储了 {final_count} 条记录")

        if final_count > 0:
            logger.info("📋 抽样检查第一条记录:")
            first_res = db.query(QualifyingResult).first()
            logger.info(f"  - Race ID: {first_res.race_id}, Driver: {first_res.driver_id}, Position: {first_res.position}, Q3: {first_res.q3_time}")

    except Exception as e:
        logger.error(f"❌ 测试失败: {e}", exc_info=True)
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    test_qualifying_sync_partial() 