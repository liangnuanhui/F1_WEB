#!/usr/bin/env python3
"""
测试 Ergast API 的正确使用
"""

import sys
import os
import logging
import pandas as pd

# 添加项目根目录到 Python 路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def test_ergast_api():
    """测试 Ergast API 的正确使用"""
    try:
        import fastf1
        from fastf1.ergast import Ergast
        
        logger.info("🔍 测试 Ergast API...")
        
        # 启用缓存
        fastf1.Cache.enable_cache('./cache')
        ergast = Ergast()
        
        # 1. 测试获取可用赛季列表
        logger.info("📊 1. 获取可用赛季列表...")
        seasons = ergast.get_seasons()
        logger.info(f"✅ 可用赛季数量: {len(seasons)}")
        logger.info(f"📅 赛季范围: {seasons['season'].min()} - {seasons['season'].max()}")
        
        # 检查2025赛季是否在可用列表中
        season_2025_available = 2025 in seasons['season'].values
        logger.info(f"🔍 2025赛季是否可用: {season_2025_available}")
        
        # 2. 测试获取2025赛季比赛日程
        logger.info("🏁 2. 获取2025赛季比赛日程...")
        try:
            race_schedule_2025 = ergast.get_race_schedule(season=2025)
            if not race_schedule_2025.empty:
                logger.info(f"✅ 2025赛季比赛日程获取成功，共{len(race_schedule_2025)}场比赛")
                logger.info("📋 比赛列表:")
                for _, race in race_schedule_2025.iterrows():
                    logger.info(f"   第{race.get('round', 'N/A')}轮: {race.get('raceName', 'N/A')} - {race.get('date', 'N/A')}")
            else:
                logger.warning("⚠️ 2025赛季比赛日程为空")
        except Exception as e:
            logger.error(f"❌ 获取2025赛季比赛日程失败: {e}")
        
        # 3. 测试获取2024赛季比赛日程（作为对比）
        logger.info("🏁 3. 获取2024赛季比赛日程（对比）...")
        try:
            race_schedule_2024 = ergast.get_race_schedule(season=2024)
            if not race_schedule_2024.empty:
                logger.info(f"✅ 2024赛季比赛日程获取成功，共{len(race_schedule_2024)}场比赛")
            else:
                logger.warning("⚠️ 2024赛季比赛日程为空")
        except Exception as e:
            logger.error(f"❌ 获取2024赛季比赛日程失败: {e}")
        
        # 4. 测试获取车手信息
        logger.info("👤 4. 获取2025赛季车手信息...")
        try:
            drivers_2025 = ergast.get_driver_info(season=2025)
            if not drivers_2025.empty:
                logger.info(f"✅ 2025赛季车手信息获取成功，共{len(drivers_2025)}名车手")
            else:
                logger.warning("⚠️ 2025赛季车手信息为空")
        except Exception as e:
            logger.error(f"❌ 获取2025赛季车手信息失败: {e}")
        
        # 5. 测试获取车队信息
        logger.info("🏎️ 5. 获取2025赛季车队信息...")
        try:
            constructors_2025 = ergast.get_constructor_info(season=2025)
            if not constructors_2025.empty:
                logger.info(f"✅ 2025赛季车队信息获取成功，共{len(constructors_2025)}支车队")
            else:
                logger.warning("⚠️ 2025赛季车队信息为空")
        except Exception as e:
            logger.error(f"❌ 获取2025赛季车队信息失败: {e}")
        
        logger.info("✅ 测试完成")
        
    except Exception as e:
        logger.error(f"❌ 测试失败: {e}")

if __name__ == "__main__":
    test_ergast_api() 