#!/usr/bin/env python3
"""
测试 Ergast API 分页机制
验证比赛结果数据的分页问题
"""

import sys
import os
import logging

# 添加项目根目录到 Python 路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_ergast_pagination():
    """测试 Ergast 分页机制"""
    try:
        import fastf1
        from fastf1.ergast import Ergast
        
        logger.info("🔍 测试 Ergast 分页机制...")
        
        # 启用缓存
        fastf1.Cache.enable_cache('./cache')
        ergast = Ergast()
        
        # 测试比赛结果分页
        logger.info("🏁 测试比赛结果分页...")
        
        # 获取第一页（默认）
        results_page1 = ergast.get_race_results(season=2025)
        logger.info(f"📊 第1页结果: {len(results_page1.content) if hasattr(results_page1, 'content') else 0} 个数据集")
        logger.info(f"📏 是否完整: {getattr(results_page1, 'is_complete', 'Unknown')}")
        logger.info(f"📊 总结果数: {getattr(results_page1, 'total_results', 'Unknown')}")
        
        # 如果第一页不完整，获取下一页
        if hasattr(results_page1, 'is_complete') and not results_page1.is_complete:
            logger.info("📄 获取下一页数据...")
            results_page2 = results_page1.get_next_result_page()
            logger.info(f"📊 第2页结果: {len(results_page2.content) if hasattr(results_page2, 'content') else 0} 个数据集")
            logger.info(f"📏 是否完整: {getattr(results_page2, 'is_complete', 'Unknown')}")
        
        # 尝试使用更大的 limit
        logger.info("📄 尝试使用更大的 limit...")
        results_large = ergast.get_race_results(season=2025, limit=50)
        logger.info(f"📊 大limit结果: {len(results_large.content) if hasattr(results_large, 'content') else 0} 个数据集")
        logger.info(f"📏 是否完整: {getattr(results_large, 'is_complete', 'Unknown')}")
        
        # 检查具体的数据内容
        if hasattr(results_page1, 'content') and results_page1.content:
            logger.info("📋 检查数据内容:")
            for idx, df in enumerate(results_page1.content):
                logger.info(f"   数据集 {idx + 1}: {df.shape}")
                if not df.empty and 'round' in df.columns:
                    rounds = df['round'].unique()
                    logger.info(f"   包含轮次: {list(rounds)}")
        
        logger.info("✅ 测试完成")
        
    except Exception as e:
        logger.error(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_ergast_pagination() 