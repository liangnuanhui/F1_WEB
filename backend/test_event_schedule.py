#!/usr/bin/env python3
"""
测试获取2025年赛季安排数据
"""

import sys
from pathlib import Path
import logging

project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

import fastf1
import pandas as pd

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def test_event_schedule():
    logger.info("🧪 开始测试获取2025年赛季安排数据...")
    
    # 使用fastf1.get_event_schedule
    event_schedule = fastf1.get_event_schedule(year=2025)
    logger.info(f"📊 返回结果类型: {type(event_schedule)}")
    
    # 检查EventSchedule对象的属性
    logger.info(f"📊 EventSchedule 属性: {dir(event_schedule)}")
    
    # 尝试获取DataFrame
    if hasattr(event_schedule, 'get_events'):
        events_df = event_schedule.get_events()
        logger.info(f"📊 通过get_events()获取数据: {type(events_df)}")
        if hasattr(events_df, 'shape'):
            logger.info(f"📊 数据形状: {events_df.shape}")
            logger.info(f"📊 列名: {list(events_df.columns)}")
            logger.info(f"📊 记录数量: {len(events_df)}")
            
            # 输出完整数据
            logger.info("📊 完整数据:")
            logger.info("=" * 80)
            for idx, row in events_df.iterrows():
                logger.info(f"记录 {idx + 1}:")
                for col in events_df.columns:
                    logger.info(f"  {col}: {row[col]}")
                logger.info("-" * 40)
            logger.info("=" * 80)
    
    # 尝试直接访问DataFrame
    if hasattr(event_schedule, 'events'):
        events_df = event_schedule.events
        logger.info(f"📊 通过events属性获取数据: {type(events_df)}")
        if hasattr(events_df, 'shape'):
            logger.info(f"📊 数据形状: {events_df.shape}")
            logger.info(f"📊 列名: {list(events_df.columns)}")
            logger.info(f"📊 记录数量: {len(events_df)}")
            
            # 输出完整数据
            logger.info("📊 完整数据:")
            logger.info("=" * 80)
            for idx, row in events_df.iterrows():
                logger.info(f"记录 {idx + 1}:")
                for col in events_df.columns:
                    logger.info(f"  {col}: {row[col]}")
                logger.info("-" * 40)
            logger.info("=" * 80)
    
    # 尝试转换为DataFrame
    try:
        events_df = pd.DataFrame(event_schedule)
        logger.info(f"📊 转换为DataFrame: {type(events_df)}")
        logger.info(f"📊 数据形状: {events_df.shape}")
        logger.info(f"📊 列名: {list(events_df.columns)}")
    except Exception as e:
        logger.info(f"📊 无法转换为DataFrame: {e}")

if __name__ == "__main__":
    test_event_schedule() 