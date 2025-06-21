#!/usr/bin/env python3
"""
测试修复后的数据提供者
验证分页功能是否正常工作
"""

import sys
import os
import logging
import pandas as pd
from datetime import datetime

# 添加项目根目录到 Python 路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_fixed_data_provider():
    """测试修复后的数据提供者"""
    try:
        from app.services.data_provider import FastF1Provider
        
        logger.info("🔍 测试修复后的数据提供者...")
        
        # 创建数据提供者实例
        provider = FastF1Provider()
        
        # 测试比赛结果数据
        logger.info("🏁 1. 测试比赛结果数据...")
        try:
            race_results = provider.get_race_results(season=2025)
            logger.info(f"📊 比赛结果数据形状: {race_results.shape}")
            logger.info(f"📋 列名: {list(race_results.columns)}")
            
            if not race_results.empty:
                # 检查轮次信息
                if 'round' in race_results.columns:
                    rounds = race_results['round'].unique()
                    rounds.sort()
                    logger.info(f"🎯 包含轮次: {list(rounds)}")
                    logger.info(f"📊 总轮次数量: {len(rounds)}")
                
                # 检查比赛名称
                if 'raceName' in race_results.columns:
                    race_names = race_results['raceName'].unique()
                    logger.info(f"🏆 比赛名称: {list(race_names)}")
                    logger.info(f"📊 总比赛数量: {len(race_names)}")
                
                # 显示前几行数据
                logger.info(f"📋 示例数据:")
                logger.info(race_results.head(3).to_string())
            else:
                logger.warning("⚠️ 没有比赛结果数据")
                
        except Exception as e:
            logger.error(f"❌ 获取比赛结果失败: {e}")
            import traceback
            traceback.print_exc()
        
        # 测试排位赛结果数据
        logger.info("🏁 2. 测试排位赛结果数据...")
        try:
            qualifying_results = provider.get_qualifying_results(season=2025)
            logger.info(f"📊 排位赛结果数据形状: {qualifying_results.shape}")
            
            if not qualifying_results.empty:
                # 检查轮次信息
                if 'round' in qualifying_results.columns:
                    rounds = qualifying_results['round'].unique()
                    rounds.sort()
                    logger.info(f"🎯 包含轮次: {list(rounds)}")
                    logger.info(f"📊 总轮次数量: {len(rounds)}")
                
                # 检查比赛名称
                if 'raceName' in qualifying_results.columns:
                    race_names = qualifying_results['raceName'].unique()
                    logger.info(f"🏆 比赛名称: {list(race_names)}")
                    logger.info(f"📊 总比赛数量: {len(race_names)}")
            else:
                logger.warning("⚠️ 没有排位赛结果数据")
                
        except Exception as e:
            logger.error(f"❌ 获取排位赛结果失败: {e}")
        
        # 测试冲刺赛结果数据
        logger.info("🏁 3. 测试冲刺赛结果数据...")
        try:
            sprint_results = provider.get_sprint_results(season=2025)
            logger.info(f"📊 冲刺赛结果数据形状: {sprint_results.shape}")
            
            if not sprint_results.empty:
                # 检查轮次信息
                if 'round' in sprint_results.columns:
                    rounds = sprint_results['round'].unique()
                    rounds.sort()
                    logger.info(f"🎯 包含轮次: {list(rounds)}")
                    logger.info(f"📊 总轮次数量: {len(rounds)}")
                
                # 检查比赛名称
                if 'raceName' in sprint_results.columns:
                    race_names = sprint_results['raceName'].unique()
                    logger.info(f"🏆 比赛名称: {list(race_names)}")
                    logger.info(f"📊 总比赛数量: {len(race_names)}")
            else:
                logger.warning("⚠️ 没有冲刺赛结果数据")
                
        except Exception as e:
            logger.error(f"❌ 获取冲刺赛结果失败: {e}")
        
        # 测试特定轮次的数据
        logger.info("🏁 4. 测试特定轮次的数据...")
        try:
            # 测试第1轮比赛结果
            round1_results = provider.get_race_results(season=2025, round_number=1)
            logger.info(f"📊 第1轮比赛结果形状: {round1_results.shape}")
            
            # 测试第10轮比赛结果
            round10_results = provider.get_race_results(season=2025, round_number=10)
            logger.info(f"📊 第10轮比赛结果形状: {round10_results.shape}")
            
        except Exception as e:
            logger.error(f"❌ 获取特定轮次数据失败: {e}")
        
        logger.info("✅ 测试完成")
        
    except Exception as e:
        logger.error(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_fixed_data_provider() 