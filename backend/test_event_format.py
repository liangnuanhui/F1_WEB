#!/usr/bin/env python3
"""
测试EventFormat字段，了解冲刺赛安排
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

def test_event_format():
    logger.info("🧪 开始测试EventFormat字段...")
    
    # 获取2025年赛季安排
    event_schedule = fastf1.get_event_schedule(year=2025)
    events_df = pd.DataFrame(event_schedule)
    
    logger.info(f"📊 数据形状: {events_df.shape}")
    logger.info(f"📊 列名: {list(events_df.columns)}")
    
    # 查看EventFormat字段的唯一值
    if 'EventFormat' in events_df.columns:
        unique_formats = events_df['EventFormat'].unique()
        logger.info(f"📊 EventFormat唯一值: {unique_formats}")
        
        # 统计每种格式的比赛数量
        format_counts = events_df['EventFormat'].value_counts()
        logger.info(f"📊 EventFormat统计:")
        for format_type, count in format_counts.items():
            logger.info(f"  - {format_type}: {count}场")
        
        # 显示冲刺赛的比赛信息
        sprint_events = events_df[events_df['EventFormat'].str.contains('sprint', case=False, na=False)]
        logger.info(f"📊 冲刺赛比赛 ({len(sprint_events)}场):")
        for _, row in sprint_events.iterrows():
            logger.info(f"  - 第{row['RoundNumber']}轮: {row['OfficialEventName']} ({row['EventFormat']})")
        
        # 显示所有比赛的详细信息
        logger.info("📊 所有比赛详细信息:")
        logger.info("=" * 100)
        for _, row in events_df.iterrows():
            logger.info(f"第{row['RoundNumber']}轮: {row['OfficialEventName']}")
            logger.info(f"  地点: {row['Location']}, {row['Country']}")
            logger.info(f"  日期: {row['EventDate']}")
            logger.info(f"  格式: {row['EventFormat']}")
            logger.info(f"  会话: {row['Session1']}, {row['Session2']}, {row['Session3']}, {row['Session4']}, {row['Session5']}")
            logger.info("-" * 50)
    else:
        logger.error("❌ 没有找到EventFormat字段")

if __name__ == "__main__":
    test_event_format() 