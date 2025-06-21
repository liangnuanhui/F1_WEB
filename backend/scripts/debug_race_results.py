#!/usr/bin/env python3
"""
调试比赛结果数据获取问题
分析为什么只有2个数据集而不是预期的10个
"""

import sys
import os
import logging
import pandas as pd
from datetime import datetime

# 添加项目根目录到 Python 路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def debug_race_results():
    """调试比赛结果数据"""
    try:
        import fastf1
        from fastf1.ergast import Ergast
        
        logger.info("🔍 开始调试比赛结果数据...")
        
        # 启用缓存
        fastf1.Cache.enable_cache('./cache')
        ergast = Ergast()
        
        # 1. 检查2025赛季比赛日程
        logger.info("📅 1. 检查2025赛季比赛日程...")
        try:
            races_schedule = ergast.get_race_schedule(season=2025)
            logger.info(f"📊 2025赛季总比赛数: {len(races_schedule)}")
            logger.info(f"📋 比赛列表:")
            for _, race in races_schedule.iterrows():
                logger.info(f"   第{race['round']}轮: {race['raceName']} - {race['raceDate']}")
        except Exception as e:
            logger.error(f"❌ 获取比赛日程失败: {e}")
        
        # 2. 检查比赛结果数据（使用分页）
        logger.info("🏁 2. 检查比赛结果数据...")
        try:
            # 获取所有比赛结果（不使用分页限制）
            all_results = ergast.get_race_results(season=2025)
            
            logger.info(f"📊 比赛结果数据类型: {type(all_results)}")
            logger.info(f"📏 是否完整: {getattr(all_results, 'is_complete', 'Unknown')}")
            logger.info(f"📊 总结果数: {getattr(all_results, 'total_results', 'Unknown')}")
            
            if hasattr(all_results, 'content') and all_results.content:
                logger.info(f"📋 数据集数量: {len(all_results.content)}")
                
                for idx, result_df in enumerate(all_results.content):
                    logger.info(f"\n📊 第 {idx + 1} 个数据集:")
                    logger.info(f"   数据形状: {result_df.shape}")
                    logger.info(f"   列名: {list(result_df.columns)}")
                    
                    if not result_df.empty:
                        # 检查轮次信息
                        if 'round' in result_df.columns:
                            rounds = result_df['round'].unique()
                            logger.info(f"   包含轮次: {list(rounds)}")
                        
                        # 检查比赛名称
                        if 'raceName' in result_df.columns:
                            race_names = result_df['raceName'].unique()
                            logger.info(f"   比赛名称: {list(race_names)}")
                        
                        # 显示前几行数据
                        logger.info(f"   示例数据:")
                        logger.info(result_df.head(2).to_string())
            else:
                logger.warning("⚠️ 没有比赛结果数据")
                
        except Exception as e:
            logger.error(f"❌ 获取比赛结果失败: {e}")
            import traceback
            traceback.print_exc()
        
        # 3. 检查排位赛结果数据
        logger.info("🏁 3. 检查排位赛结果数据...")
        try:
            qualifying_results = ergast.get_qualifying_results(season=2025)
            
            logger.info(f"📊 排位赛结果数据类型: {type(qualifying_results)}")
            logger.info(f"📏 是否完整: {getattr(qualifying_results, 'is_complete', 'Unknown')}")
            logger.info(f"📊 总结果数: {getattr(qualifying_results, 'total_results', 'Unknown')}")
            
            if hasattr(qualifying_results, 'content') and qualifying_results.content:
                logger.info(f"📋 数据集数量: {len(qualifying_results.content)}")
                
                for idx, result_df in enumerate(qualifying_results.content):
                    logger.info(f"\n📊 第 {idx + 1} 个数据集:")
                    logger.info(f"   数据形状: {result_df.shape}")
                    
                    if not result_df.empty:
                        # 检查轮次信息
                        if 'round' in result_df.columns:
                            rounds = result_df['round'].unique()
                            logger.info(f"   包含轮次: {list(rounds)}")
            else:
                logger.warning("⚠️ 没有排位赛结果数据")
                
        except Exception as e:
            logger.error(f"❌ 获取排位赛结果失败: {e}")
        
        # 4. 检查冲刺赛结果数据
        logger.info("🏁 4. 检查冲刺赛结果数据...")
        try:
            sprint_results = ergast.get_sprint_results(season=2025)
            
            logger.info(f"📊 冲刺赛结果数据类型: {type(sprint_results)}")
            logger.info(f"📏 是否完整: {getattr(sprint_results, 'is_complete', 'Unknown')}")
            logger.info(f"📊 总结果数: {getattr(sprint_results, 'total_results', 'Unknown')}")
            
            if hasattr(sprint_results, 'content') and sprint_results.content:
                logger.info(f"📋 数据集数量: {len(sprint_results.content)}")
                
                for idx, result_df in enumerate(sprint_results.content):
                    logger.info(f"\n📊 第 {idx + 1} 个数据集:")
                    logger.info(f"   数据形状: {result_df.shape}")
                    
                    if not result_df.empty:
                        # 检查轮次信息
                        if 'round' in result_df.columns:
                            rounds = result_df['round'].unique()
                            logger.info(f"   包含轮次: {list(rounds)}")
            else:
                logger.warning("⚠️ 没有冲刺赛结果数据")
                
        except Exception as e:
            logger.error(f"❌ 获取冲刺赛结果失败: {e}")
        
        # 5. 尝试获取特定轮次的数据
        logger.info("🏁 5. 尝试获取特定轮次的数据...")
        try:
            # 尝试获取第1轮比赛结果
            round1_results = ergast.get_race_results(season=2025, round=1)
            logger.info(f"📊 第1轮比赛结果: {type(round1_results)}")
            if hasattr(round1_results, 'content') and round1_results.content:
                logger.info(f"   数据形状: {round1_results.content[0].shape if round1_results.content else 'Empty'}")
            else:
                logger.info("   没有数据")
                
            # 尝试获取第10轮比赛结果
            round10_results = ergast.get_race_results(season=2025, round=10)
            logger.info(f"📊 第10轮比赛结果: {type(round10_results)}")
            if hasattr(round10_results, 'content') and round10_results.content:
                logger.info(f"   数据形状: {round10_results.content[0].shape if round10_results.content else 'Empty'}")
            else:
                logger.info("   没有数据")
                
        except Exception as e:
            logger.error(f"❌ 获取特定轮次数据失败: {e}")
        
        logger.info("✅ 调试完成")
        
    except Exception as e:
        logger.error(f"❌ 调试失败: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    debug_race_results() 