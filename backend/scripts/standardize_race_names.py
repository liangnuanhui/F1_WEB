#!/usr/bin/env python3
"""
标准化比赛名称脚本
将数据库中的比赛名称统一为简化格式，确保命名一致性
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from dotenv import load_dotenv
import fastf1

from app.models import Race, Season

# 加载环境变量
load_dotenv()

def standardize_race_names():
    """标准化比赛名称"""
    # 获取数据库连接
    database_url = os.getenv('DATABASE_URL', 'postgresql://f1user:f1password@localhost:5432/f1_database')
    engine = create_engine(database_url)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    
    db = SessionLocal()
    
    try:
        print("🔄 开始标准化比赛名称...")
        
        # 获取FastF1的2025赛季标准名称映射
        print("📥 获取FastF1标准比赛名称...")
        fastf1_schedule = fastf1.get_event_schedule(2025)
        
        # 创建标准名称映射
        standard_names = {}
        for _, row in fastf1_schedule.iterrows():
            round_num = row['RoundNumber']
            event_name = row['EventName']
            official_name = row['OfficialEventName']
            standard_names[round_num] = {
                'standard': event_name,
                'official': official_name
            }
        
        print(f"✅ 获取到 {len(standard_names)} 个标准比赛名称")
        
        # 查询需要标准化的比赛
        races_2025 = db.query(Race).join(Season).filter(Season.year == 2025).order_by(Race.round_number).all()
        
        print(f"🔍 检查 {len(races_2025)} 场比赛...")
        
        updated_count = 0
        for race in races_2025:
            round_num = race.round_number
            current_name = race.official_event_name
            
            # 跳过测试赛事（第0轮）
            if round_num == 0:
                continue
                
            if round_num in standard_names:
                standard_name = standard_names[round_num]['standard']
                official_name = standard_names[round_num]['official']
                
                # 如果当前名称不是标准简化名称，则更新
                if current_name != standard_name:
                    print(f"📝 更新第{round_num}轮比赛名称:")
                    print(f"   当前: {current_name}")
                    print(f"   标准: {standard_name}")
                    
                    race.official_event_name = standard_name
                    updated_count += 1
                else:
                    print(f"✅ 第{round_num}轮已是标准格式: {current_name}")
            else:
                print(f"⚠️ 未找到第{round_num}轮的标准名称")
        
        if updated_count > 0:
            db.commit()
            print(f"✅ 已更新 {updated_count} 场比赛的名称")
        else:
            print("✅ 所有比赛名称已是标准格式，无需更新")
            
        # 显示更新后的结果
        print("\n📋 更新后的比赛列表:")
        races_2025 = db.query(Race).join(Season).filter(Season.year == 2025).order_by(Race.round_number).all()
        for race in races_2025:
            print(f"第{race.round_number}轮: {race.official_event_name}")
        
    except Exception as e:
        print(f"❌ 标准化失败: {e}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    standardize_race_names() 