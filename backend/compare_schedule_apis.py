#!/usr/bin/env python3
"""
对比 fastf1.get_event_schedule 和 ergast.get_race_schedule 的数据差异
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

def compare_schedule_apis():
    """对比两种API的数据差异"""
    try:
        import fastf1
        from fastf1.ergast import Ergast
        
        logger.info("🔍 对比比赛日程API...")
        
        # 启用缓存
        fastf1.Cache.enable_cache('./cache')
        ergast = Ergast()
        
        # 1. 获取 FastF1 的比赛日程
        logger.info("📊 1. 获取 FastF1 比赛日程...")
        try:
            fastf1_schedule = fastf1.get_event_schedule(2025)
            logger.info(f"✅ FastF1 日程获取成功，共{len(fastf1_schedule)}条记录")
            logger.info(f"📋 FastF1 日程列名: {list(fastf1_schedule.columns)}")
            
            # 显示前几场比赛的详细信息
            logger.info("📋 FastF1 日程详情（前5场）:")
            for idx, event in fastf1_schedule.head().iterrows():
                logger.info(f"   {event.get('EventName', 'N/A')} - {event.get('EventDate', 'N/A')}")
                logger.info(f"     轮次: {event.get('RoundNumber', 'N/A')}, 赛道: {event.get('CircuitShortName', 'N/A')}")
                logger.info(f"     包含session: {event.get('Sessions', 'N/A')}")
        except Exception as e:
            logger.error(f"❌ FastF1 日程获取失败: {e}")
            fastf1_schedule = pd.DataFrame()
        
        # 2. 获取 Ergast 的比赛日程
        logger.info("📊 2. 获取 Ergast 比赛日程...")
        try:
            ergast_schedule = ergast.get_race_schedule(season=2025)
            logger.info(f"✅ Ergast 日程获取成功，共{len(ergast_schedule)}条记录")
            logger.info(f"📋 Ergast 日程列名: {list(ergast_schedule.columns)}")
            
            # 显示前几场比赛的详细信息
            logger.info("📋 Ergast 日程详情（前5场）:")
            for idx, race in ergast_schedule.head().iterrows():
                logger.info(f"   {race.get('raceName', 'N/A')} - {race.get('date', 'N/A')}")
                logger.info(f"     轮次: {race.get('round', 'N/A')}, 赛道: {race.get('circuitId', 'N/A')}")
        except Exception as e:
            logger.error(f"❌ Ergast 日程获取失败: {e}")
            ergast_schedule = pd.DataFrame()
        
        # 3. 数据对比分析
        logger.info("📊 3. 数据对比分析...")
        
        if not fastf1_schedule.empty and not ergast_schedule.empty:
            logger.info(f"📈 数据量对比: FastF1({len(fastf1_schedule)}) vs Ergast({len(ergast_schedule)})")
            
            # 检查比赛数量是否一致
            if len(fastf1_schedule) == len(ergast_schedule):
                logger.info("✅ 比赛数量一致")
            else:
                logger.warning(f"⚠️ 比赛数量不一致: FastF1({len(fastf1_schedule)}) vs Ergast({len(ergast_schedule)})")
            
            # 对比比赛名称
            fastf1_races = set(fastf1_schedule['EventName'].dropna())
            ergast_races = set(ergast_schedule['raceName'].dropna())
            
            logger.info(f"🏁 FastF1 比赛: {len(fastf1_races)}场")
            logger.info(f"🏁 Ergast 比赛: {len(ergast_races)}场")
            
            # 找出差异
            only_fastf1 = fastf1_races - ergast_races
            only_ergast = ergast_races - fastf1_races
            
            if only_fastf1:
                logger.info(f"🔍 仅在 FastF1 中: {only_fastf1}")
            if only_ergast:
                logger.info(f"🔍 仅在 Ergast 中: {only_ergast}")
            
            # 检查共同比赛
            common_races = fastf1_races & ergast_races
            logger.info(f"✅ 共同比赛: {len(common_races)}场")
        
        # 4. 数据完整性分析
        logger.info("📊 4. 数据完整性分析...")
        
        if not fastf1_schedule.empty:
            logger.info("📋 FastF1 数据完整性:")
            for col in fastf1_schedule.columns:
                non_null_count = fastf1_schedule[col].notna().sum()
                logger.info(f"   {col}: {non_null_count}/{len(fastf1_schedule)} ({non_null_count/len(fastf1_schedule)*100:.1f}%)")
        
        if not ergast_schedule.empty:
            logger.info("📋 Ergast 数据完整性:")
            for col in ergast_schedule.columns:
                non_null_count = ergast_schedule[col].notna().sum()
                logger.info(f"   {col}: {non_null_count}/{len(ergast_schedule)} ({non_null_count/len(ergast_schedule)*100:.1f}%)")
        
        # 5. 使用建议
        logger.info("💡 5. 使用建议:")
        logger.info("   - FastF1: 适合需要详细session信息、练习赛、排位赛等")
        logger.info("   - Ergast: 适合只需要正赛基本信息、历史数据查询等")
        logger.info("   - 建议: 根据具体需求选择合适的API，可以结合使用")
        
        logger.info("✅ 对比分析完成")
        
    except Exception as e:
        logger.error(f"❌ 对比分析失败: {e}")

if __name__ == "__main__":
    compare_schedule_apis() 