#!/usr/bin/env python3
"""
数据初始化脚本
从 FastF1 拉取 2025 赛季主数据并填充数据库
"""

import asyncio
import logging
import sys
import time
from pathlib import Path

# 添加项目根目录到 Python 路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from sqlalchemy.orm import Session

from app.core.database import get_db
from app.services.data_sync_service import DataSyncService

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('data_init_2025.log')
    ]
)
logger = logging.getLogger(__name__)


async def main():
    """主函数"""
    logger.info("🚀 开始初始化 2025 赛季 F1 主数据...")
    start_time = time.time()
    
    try:
        # 获取数据库会话
        db = next(get_db())
        
        # 修复Season模型（如果需要）
        logger.info("🔧 检查并修复数据模型...")
        try:
            from scripts.fix_season_model import fix_season_model
            if fix_season_model():
                logger.info("✅ 数据模型检查完成")
            else:
                logger.warning("⚠️ 数据模型修复跳过")
        except Exception as e:
            logger.warning(f"⚠️ 数据模型检查跳过: {e}")
        
        # 创建数据同步服务
        sync_service = DataSyncService(cache_dir="./cache")
        
        # 初始化 2025 赛季主数据
        logger.info("📊 开始同步基础数据...")
        
        # 1. 同步赛季数据
        logger.info("1️⃣ 同步赛季数据...")
        if sync_service.sync_seasons(db, start_year=2025, end_year=2025):
            logger.info("✅ 赛季数据同步完成")
        else:
            logger.error("❌ 赛季数据同步失败")
            return False
        
        # 2. 同步赛道数据
        logger.info("2️⃣ 同步赛道数据...")
        if sync_service.sync_circuits(db, season=2025):
            logger.info("✅ 赛道数据同步完成")
        else:
            logger.error("❌ 赛道数据同步失败")
            return False
        
        # 3. 同步车手数据
        logger.info("3️⃣ 同步车手数据...")
        if sync_service.sync_drivers(db, season=2025):
            logger.info("✅ 车手数据同步完成")
        else:
            logger.error("❌ 车手数据同步失败")
            return False
        
        # 4. 同步车队数据
        logger.info("4️⃣ 同步车队数据...")
        if sync_service.sync_constructors(db, season=2025):
            logger.info("✅ 车队数据同步完成")
        else:
            logger.error("❌ 车队数据同步失败")
            return False
        
        # 5. 同步积分榜数据
        logger.info("5️⃣ 同步积分榜数据...")
        if sync_service.sync_driver_standings(db, season=2025):
            logger.info("✅ 车手积分榜同步完成")
        else:
            logger.warning("⚠️ 车手积分榜同步跳过")
        
        if sync_service.sync_constructor_standings(db, season=2025):
            logger.info("✅ 车队积分榜同步完成")
        else:
            logger.warning("⚠️ 车队积分榜同步跳过")
        
        # 6. 同步比赛结果数据（前3轮）
        logger.info("6️⃣ 同步比赛结果数据（前3轮）...")
        for round_num in range(1, 4):
            logger.info(f"   同步第 {round_num} 轮比赛结果...")
            if sync_service.sync_race_results(db, season=2025, round_number=round_num):
                logger.info(f"   ✅ 第 {round_num} 轮比赛结果同步完成")
            else:
                logger.warning(f"   ⚠️ 第 {round_num} 轮比赛结果同步跳过")
            
            if sync_service.sync_qualifying_results(db, season=2025, round_number=round_num):
                logger.info(f"   ✅ 第 {round_num} 轮排位赛结果同步完成")
            else:
                logger.warning(f"   ⚠️ 第 {round_num} 轮排位赛结果同步跳过")
        
        elapsed_time = time.time() - start_time
        logger.info(f"🎉 2025 赛季主数据初始化完成！耗时: {elapsed_time:.2f} 秒")
        
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
        from app.models.driver_standing import DriverStanding
        from app.models.constructor_standing import ConstructorStanding
        
        # 统计各表记录数
        seasons_count = db.query(Season).count()
        circuits_count = db.query(Circuit).count()
        races_count = db.query(Race).count()
        drivers_count = db.query(Driver).count()
        constructors_count = db.query(Constructor).count()
        results_count = db.query(Result).count()
        qualifying_results_count = db.query(QualifyingResult).count()
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
        logger.info(f"车手积分榜数量: {driver_standings_count}")
        logger.info(f"车队积分榜数量: {constructor_standings_count}")
        
        # 显示赛季信息
        seasons = db.query(Season).order_by(Season.year).all()
        logger.info("\n🏆 === 赛季信息 ===")
        for season in seasons:
            logger.info(f"{season.year}: {season.name} {'(当前赛季)' if season.is_current else ''}")
        
        # 显示最近的比赛
        recent_races = db.query(Race).order_by(Race.race_date.desc()).limit(5).all()
        logger.info("\n🏁 === 最近的比赛 ===")
        for race in recent_races:
            logger.info(f"{race.race_date.strftime('%Y-%m-%d')}: {race.name}")
        
        # 显示车手信息
        drivers = db.query(Driver).filter_by(is_active=True).limit(10).all()
        logger.info("\n👥 === 活跃车手 (前10名) ===")
        for driver in drivers:
            logger.info(f"{driver.full_name} ({driver.nationality}) - #{driver.number}")
        
        # 显示车队信息
        constructors = db.query(Constructor).filter_by(is_active=True).all()
        logger.info("\n🏎️ === 活跃车队 ===")
        for constructor in constructors:
            logger.info(f"{constructor.name} ({constructor.nationality})")
        
    except Exception as e:
        logger.error(f"显示统计信息时发生错误: {e}")


if __name__ == "__main__":
    success = asyncio.run(main())
    if not success:
        sys.exit(1) 