#!/usr/bin/env python3
"""
检查FastF1返回的2025赛季日程数据
"""

import fastf1
import pandas as pd

def main():
    print("🔍 检查FastF1 2025赛季日程数据...")
    print("=" * 80)
    
    try:
        # 获取FastF1的2025赛季日程
        races_df = fastf1.get_event_schedule(2025)
        
        print(f"FastF1返回的比赛数量: {len(races_df)}")
        print("\n完整数据:")
        print(races_df.to_string())
        
        print("\n" + "=" * 80)
        print("按轮次排序:")
        for _, row in races_df.iterrows():
            print(f"第{row['RoundNumber']}轮: {row['OfficialEventName']} - {row['Location']} ({row['Country']})")
            
    except Exception as e:
        print(f"❌ 获取数据失败: {e}")

if __name__ == "__main__":
    main() 