#!/usr/bin/env python3
"""
安全数据同步脚本
包含API频率限制处理和批量数据处理
"""

import sys
import logging
import argparse
import time
from pathlib import Path

# 添加项目根目录到 Python 路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from app.core.database import get_db
from app.services.data_sync_service import DataSyncService

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('data_sync.log')
    ]
)
logger = logging.getLogger(__name__)


def safe_sync_basic_data(sync_service: DataSyncService, db, season: int = None):
    """安全同步基础数据（包括积分榜）"""
    logger.info("=== 开始同步基础数据（包括积分榜） ===")
    
    try:
        # 1. 同步赛季数据
        logger.info("1. 同步赛季数据...")
        if sync_service.sync_seasons(db, start_year=2020, end_year=2025):
            logger.info("✓ 赛季数据同步完成")
        else:
            logger.error("✗ 赛季数据同步失败")
            return False
        
        time.sleep(1)  # 基础延迟
        
        # 2. 同步赛道数据
        logger.info("2. 同步赛道数据...")
        if sync_service.sync_circuits(db, season=season):
            logger.info("✓ 赛道数据同步完成")
        else:
            logger.error("✗ 赛道数据同步失败")
            return False
        
        time.sleep(1)
        
        # 3. 同步车手数据
        logger.info("3. 同步车手数据...")
        if sync_service.sync_drivers(db, season=season):
            logger.info("✓ 车手数据同步完成")
        else:
            logger.error("✗ 车手数据同步失败")
            return False
        
        time.sleep(1)
        
        # 4. 同步车队数据
        logger.info("4. 同步车队数据...")
        if sync_service.sync_constructors(db, season=season):
            logger.info("✓ 车队数据同步完成")
        else:
            logger.error("✗ 车队数据同步失败")
            return False
        
        time.sleep(2)
        
        # 5. 同步车手积分榜（基础数据，API调用少）
        logger.info("5. 同步车手积分榜...")
        if sync_service.sync_driver_standings(db, season):
            logger.info("✓ 车手积分榜同步完成")
        else:
            logger.warning("⚠ 车手积分榜同步跳过")
        
        time.sleep(2)
        
        # 6. 同步车队积分榜（基础数据，API调用少）
        logger.info("6. 同步车队积分榜...")
        if sync_service.sync_constructor_standings(db, season):
            logger.info("✓ 车队积分榜同步完成")
        else:
            logger.warning("⚠ 车队积分榜同步跳过")
        
        logger.info("=== 基础数据（含积分榜）同步完成 ===")
        return True
        
    except Exception as e:
        logger.error(f"同步基础数据时出错: {e}")
        return False


def safe_sync_session_data(sync_service: DataSyncService, db, season: int, max_rounds: int = 3):
    """安全同步会话数据（比赛结果、排位赛结果）- 容易触发API限制"""
    logger.info(f"=== 开始同步会话数据 (最多 {max_rounds} 轮) ===")
    logger.warning("⚠️  注意：会话数据同步可能触发API限制，将谨慎处理")
    
    try:
        success_count = 0
        
        for round_num in range(1, max_rounds + 1):
            logger.info(f"--- 同步第 {round_num} 轮会话数据 ---")
            
            try:
                # 同步比赛结果（使用Ergast API，较安全）
                logger.info(f"同步第 {round_num} 轮比赛结果...")
                if sync_service.sync_race_results(db, season, round_num):
                    logger.info(f"✓ 第 {round_num} 轮比赛结果同步完成")
                    success_count += 1
                else:
                    logger.warning(f"⚠ 第 {round_num} 轮比赛结果同步跳过")
                
                time.sleep(3)  # 增加轮次间延迟
                
                # 同步排位赛结果（使用Ergast API，较安全）
                logger.info(f"同步第 {round_num} 轮排位赛结果...")
                if sync_service.sync_qualifying_results(db, season, round_num):
                    logger.info(f"✓ 第 {round_num} 轮排位赛结果同步完成")
                else:
                    logger.warning(f"⚠ 第 {round_num} 轮排位赛结果同步跳过")
                
                time.sleep(3)  # 每轮完成后延迟
                
            except Exception as e:
                logger.error(f"同步第 {round_num} 轮会话数据时出错: {e}")
                continue
        
        logger.info(f"=== 会话数据同步完成，成功同步 {success_count}/{max_rounds} 轮 ===")
        return success_count > 0
        
    except Exception as e:
        logger.error(f"同步会话数据时出错: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(description="安全的F1数据同步脚本")
    parser.add_argument("--season", type=int, default=2024, help="赛季年份 (默认: 2024)")
    parser.add_argument("--max-rounds", type=int, default=3, help="最大同步轮次数 (默认: 3)")
    parser.add_argument("--basic-only", action="store_true", help="只同步基础数据（含积分榜）")
    parser.add_argument("--cache-dir", type=str, help="FastF1缓存目录")
    
    args = parser.parse_args()
    
    logger.info(f"开始安全数据同步 - 赛季: {args.season}")
    
    try:
        # 初始化数据同步服务
        sync_service = DataSyncService(cache_dir=args.cache_dir)
        
        # 获取数据库连接
        db = next(get_db())
        
        try:
            # 1. 同步基础数据（包括积分榜）
            if not safe_sync_basic_data(sync_service, db, args.season):
                logger.error("基础数据同步失败，停止执行")
                return False
            
            # 2. 如果不是仅基础数据模式，同步会话数据
            if not args.basic_only:
                time.sleep(5)  # 基础数据和会话数据间的缓冲时间
                logger.info("💡 提示：现在开始同步会话数据，如遇API限制会自动重试")
                if not safe_sync_session_data(sync_service, db, args.season, args.max_rounds):
                    logger.warning("会话数据同步部分失败，但基础数据已成功")
            
            logger.info("🎉 数据同步任务完成！")
            return True
            
        finally:
            db.close()
            
    except Exception as e:
        logger.error(f"数据同步失败: {e}")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 