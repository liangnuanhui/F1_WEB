#!/usr/bin/env python3
"""
测试冲刺赛结果数据获取
"""

import sys
from pathlib import Path
import logging

project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from fastf1.ergast import Ergast
import pandas as pd

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def test_sprint_results():
    logger.info("🧪 开始测试冲刺赛结果数据获取...")
    ergast = Ergast()
    result = ergast.get_sprint_results(season=2025)
    logger.info(f"📊 返回结果类型: {type(result)}")
    if hasattr(result, 'content'):
        logger.info(f"📊 content 属性存在，长度: {len(result.content)}")
        for i, df in enumerate(result.content):
            logger.info(f"📊 DataFrame {i}: 形状 {df.shape}, 列名: {list(df.columns)}")
            logger.info(f"📊 DataFrame {i} 记录数量: {len(df)}")
            
            # 检查是否有round字段
            if 'round' in df.columns:
                logger.info(f"📊 DataFrame {i} 包含round字段，唯一值: {df['round'].unique()}")
            else:
                logger.info(f"📊 DataFrame {i} 不包含round字段")
            
            # 检查是否有raceId字段
            if 'raceId' in df.columns:
                logger.info(f"📊 DataFrame {i} 包含raceId字段，唯一值: {df['raceId'].unique()}")
            else:
                logger.info(f"📊 DataFrame {i} 不包含raceId字段")
            
            # 检查position字段的分布
            if 'position' in df.columns:
                positions = df['position'].dropna().tolist()
                logger.info(f"📊 DataFrame {i} position字段分布: {positions}")
            
            # 检查driverId字段的唯一值数量
            if 'driverId' in df.columns:
                unique_drivers = df['driverId'].nunique()
                logger.info(f"📊 DataFrame {i} 唯一车手数量: {unique_drivers}")
                logger.info(f"📊 DataFrame {i} 车手列表: {df['driverId'].tolist()}")
            
            logger.info(f"📊 DataFrame {i} 完整数据:")
            logger.info("=" * 80)
            # 输出完整的DataFrame数据
            for idx, row in df.iterrows():
                logger.info(f"记录 {idx + 1}:")
                for col in df.columns:
                    logger.info(f"  {col}: {row[col]}")
                logger.info("-" * 40)
            logger.info("=" * 80)
    else:
        logger.info("❌ 返回结果没有 content 属性")

if __name__ == "__main__":
    test_sprint_results() 