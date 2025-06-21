#!/usr/bin/env python3
"""
测试车手积分榜数据获取
"""

import sys
import os
import logging
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from fastf1.ergast import Ergast
import pandas as pd

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)


def test_driver_standings():
    """测试车手积分榜数据获取"""
    logger.info("🧪 开始测试车手积分榜数据获取...")
    
    try:
        # 创建 Ergast 实例
        ergast = Ergast()
        
        # 获取2025赛季车手积分榜数据
        logger.info("📡 正在获取2025赛季车手积分榜数据...")
        result = ergast.get_driver_standings(season=2025)
        
        logger.info(f"📊 返回结果类型: {type(result)}")
        
        if hasattr(result, 'content'):
            logger.info(f"📊 content 属性存在，长度: {len(result.content)}")
            for i, df in enumerate(result.content):
                logger.info(f"📊 DataFrame {i}: 形状 {df.shape}, 列名: {list(df.columns)}")
                if not df.empty:
                    logger.info(f"📊 DataFrame {i} 第一条记录: {df.iloc[0].to_dict()}")
        else:
            logger.info("❌ 返回结果没有 content 属性")
            
        if hasattr(result, 'description'):
            logger.info(f"📊 description 属性存在: {result.description}")
            
        # 测试我们的 _handle_api_call 逻辑
        logger.info("🧪 测试 _handle_api_call 逻辑...")
        
        # 模拟 _handle_api_call 的处理逻辑
        if hasattr(result, 'content') and hasattr(result, 'get_next_result_page'):
            all_dataframes = []
            current_response = result
            
            while current_response is not None:
                # 获取当前页的所有 DataFrame (content 属性)
                if hasattr(current_response, 'content') and current_response.content:
                    all_dataframes.extend(current_response.content)
                
                # 尝试获取下一页
                try:
                    current_response = current_response.get_next_result_page()
                except ValueError:
                    # 没有更多页面了
                    break
            
            # 合并所有 DataFrame
            if len(all_dataframes) > 1:
                final_df = pd.concat(all_dataframes, ignore_index=True)
            elif len(all_dataframes) == 1:
                final_df = all_dataframes[0]
            else:
                final_df = None
                
            logger.info(f"📊 处理后的 DataFrame: {type(final_df)}")
            if final_df is not None:
                logger.info(f"📊 最终数据形状: {final_df.shape}")
                logger.info(f"📊 最终数据列名: {list(final_df.columns)}")
                if not final_df.empty:
                    logger.info(f"📊 最终数据第一条记录: {final_df.iloc[0].to_dict()}")
            else:
                logger.info("❌ 最终数据为空")
        
        logger.info("✅ 测试完成")
        
    except Exception as e:
        logger.error(f"❌ 测试失败: {e}")
        raise


if __name__ == "__main__":
    test_driver_standings() 