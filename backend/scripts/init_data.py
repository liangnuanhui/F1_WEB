#!/usr/bin/env python3
"""
数据初始化脚本
使用统一同步服务初始化F1数据
支持动态年份
"""

import asyncio
import logging
import sys
import time
from datetime import datetime
from pathlib import Path

# 添加项目根目录到 Python 路径
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
        logging.StreamHandler(),
        logging.FileHandler('data_init_unified.log')
    ]
)
logger = logging.getLogger(__name__)


def get_current_year():
    """获取当前年份"""
    return datetime.now().year


async def main():
    """主函数"""
    current_year = get_current_year()
    logger.info(f"🚀 开始初始化F1数据 (当前年份: {current_year})...")
    start_time = time.time()
    
    try:
        # 获取数据库会话
        db = next(get_db())
        
        # 创建统一同步服务
        sync_service = UnifiedSyncService(db, cache_dir="./cache")
        
        # 初始化基础数据
        logger.info("📊 开始同步基础数据...")
        
        # 1. 同步赛季数据
        logger.info("1️⃣ 同步赛季数据...")
        seasons = sync_service.sync_seasons()
        logger.info(f"✅ 赛季数据同步完成，共 {len(seasons)} 个赛季")
        
        # 2. 同步赛道数据
        logger.info("2️⃣ 同步赛道数据...")
        circuits = sync_service.sync_circuits()
        logger.info(f"✅ 赛道数据同步完成，共 {len(circuits)} 个赛道")
        
        # 3. 同步车队数据
        logger.info("3️⃣ 同步车队数据...")
        constructors = sync_service.sync_constructors()
        logger.info(f"✅ 车队数据同步完成，共 {len(constructors)} 个车队")
        
        # 4. 同步车手数据
        logger.info("4️⃣ 同步车手数据...")
        drivers = sync_service.sync_drivers()
        logger.info(f"✅ 车手数据同步完成，共 {len(drivers)} 个车手")
        
        # 5. 同步比赛数据（当前赛季）
        logger.info(f"5️⃣ 同步比赛数据 ({current_year}赛季)...")
        races = sync_service.sync_races(current_year)
        logger.info(f"✅ 比赛数据同步完成，共 {len(races)} 场比赛")
        
        # 6. 同步积分榜数据（当前赛季）
        logger.info(f"6️⃣ 同步积分榜数据 ({current_year}赛季)...")
        if sync_service.sync_driver_standings(current_year):
            logger.info("✅ 车手积分榜同步完成")
        else:
            logger.warning("⚠️ 车手积分榜同步跳过")
        
        if sync_service.sync_constructor_standings(current_year):
            logger.info("✅ 车队积分榜同步完成")
        else:
            logger.warning("⚠️ 车队积分榜同步跳过")
        
        # 7. 同步比赛结果数据（前3轮）
        logger.info(f"7️⃣ 同步比赛结果数据 ({current_year}赛季，前3轮)...")
        for round_num in range(1, 4):
            logger.info(f"   同步第 {round_num} 轮比赛结果...")
            if sync_service.sync_race_results(current_year):
                logger.info(f"   ✅ 第 {round_num} 轮比赛结果同步完成")
            else:
                logger.warning(f"   ⚠️ 第 {round_num} 轮比赛结果同步跳过")
            
            if sync_service.sync_qualifying_results(current_year):
                logger.info(f"   ✅ 第 {round_num} 轮排位赛结果同步完成")
            else:
                logger.warning(f"   ⚠️ 第 {round_num} 轮排位赛结果同步跳过")
        
        # 8. 同步冲刺赛结果数据（当前赛季）
        logger.info(f"8️⃣ 同步冲刺赛结果数据 ({current_year}赛季)...")
        if sync_service.sync_sprint_results(current_year):
            logger.info("✅ 冲刺赛结果同步完成")
        else:
            logger.warning("⚠️ 冲刺赛结果同步跳过")
        
        elapsed_time = time.time() - start_time
        logger.info(f"🎉 F1数据初始化完成！耗时: {elapsed_time:.2f} 秒")
        
        # 显示统计信息
        await show_statistics(db)
        
        return True
        
    except Exception as e:
        logger.error(f"❌ 初始化数据时发生错误: {e}")
        return False
    finally:
        db.close()


async def show_statistics(db: Session):
    """显示数据库统计信息"""
    try:
        from app.models.season import Season
        from app.models.circuit import Circuit
        from app.models.race import Race
        from app.models.driver import Driver
        from app.models.constructor import Constructor
        from app.models.result import Result
        from app.models.qualifying_result import QualifyingResult
        from app.models.sprint_result import SprintResult
        from app.models.standings import DriverStanding, ConstructorStanding
        
        # 统计各表记录数
        seasons_count = db.query(Season).count()
        circuits_count = db.query(Circuit).count()
        races_count = db.query(Race).count()
        drivers_count = db.query(Driver).count()
        constructors_count = db.query(Constructor).count()
        results_count = db.query(Result).count()
        qualifying_results_count = db.query(QualifyingResult).count()
        sprint_results_count = db.query(SprintResult).count()
        driver_standings_count = db.query(DriverStanding).count()
        constructor_standings_count = db.query(ConstructorStanding).count()
        
        logger.info("📈 === 数据库统计信息 ===")
        logger.info(f"赛季数量: {seasons_count}")
        logger.info(f"赛道数量: {circuits_count}")
        logger.info(f"比赛数量: {races_count}")
        logger.info(f"车手数量: {drivers_count}")
        logger.info(f"车队数量: {constructors_count}")
        logger.info(f"比赛结果数量: {results_count}")
        logger.info(f"排位赛结果数量: {qualifying_results_count}")
        logger.info(f"冲刺赛结果数量: {sprint_results_count}")
        logger.info(f"车手积分榜数量: {driver_standings_count}")
        logger.info(f"车队积分榜数量: {constructor_standings_count}")
        
        # 显示赛季信息
        seasons = db.query(Season).order_by(Season.year).all()
        logger.info("\n🏆 === 赛季信息 ===")
        for season in seasons:
            logger.info(f"{season.year}: {season.name} {'(当前赛季)' if season.is_current else ''}")
        
        # 显示最近的比赛
        recent_races = db.query(Race).order_by(Race.event_date.desc()).limit(5).all()
        logger.info("\n🏁 === 最近的比赛 ===")
        for race in recent_races:
            logger.info(f"{race.event_date.strftime('%Y-%m-%d')}: {race.official_event_name}")
        
        # 显示车手信息
        drivers = db.query(Driver).limit(10).all()
        logger.info("\n👥 === 车手信息 (前10名) ===")
        for driver in drivers:
            logger.info(f"{driver.given_name} {driver.family_name} ({driver.driver_nationality}) - #{driver.driver_number}")
        
        # 显示车队信息
        constructors = db.query(Constructor).all()
        logger.info("\n🏎️ === 车队信息 ===")
        for constructor in constructors:
            logger.info(f"{constructor.constructor_name} ({constructor.constructor_nationality})")
        
    except Exception as e:
        logger.error(f"显示统计信息时发生错误: {e}")


if __name__ == "__main__":
    success = asyncio.run(main())
    if not success:
        sys.exit(1) 