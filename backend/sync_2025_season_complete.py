#!/usr/bin/env python3
"""
完整同步2025赛季数据（包含第0轮季前测试）
"""

import sys
from pathlib import Path
import logging

project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

import fastf1
import pandas as pd
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.unified_sync_service import UnifiedSyncService

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def analyze_event_schedule():
    """分析2025赛季安排数据"""
    logger.info("📊 分析2025赛季安排数据...")
    
    try:
        # 获取2025年赛季安排
        event_schedule = fastf1.get_event_schedule(year=2025)
        events_df = pd.DataFrame(event_schedule)
        
        logger.info(f"📊 数据形状: {events_df.shape}")
        logger.info(f"📊 记录数量: {len(events_df)}")
        
        # 检查EventFormat统计
        if 'EventFormat' in events_df.columns:
            format_counts = events_df['EventFormat'].value_counts()
            logger.info("📊 EventFormat统计:")
            for format_type, count in format_counts.items():
                logger.info(f"  - {format_type}: {count}场")
        
        # 显示所有比赛信息
        logger.info("📊 完整比赛安排:")
        for _, row in events_df.iterrows():
            logger.info(f"  - 第{row['RoundNumber']}轮: {row['OfficialEventName']} (格式: {row['EventFormat']})")
        
        return events_df
        
    except Exception as e:
        logger.error(f"❌ 分析赛季安排失败: {e}")
        return None

def sync_complete_season():
    """同步完整的2025赛季数据"""
    logger.info("🔄 开始同步完整的2025赛季数据...")
    
    try:
        db = next(get_db())
        sync_service = UnifiedSyncService(db, cache_dir="./cache")
        
        # 1. 分析赛季安排
        events_df = analyze_event_schedule()
        if events_df is None:
            return False
        
        # 2. 同步比赛数据（包含季前测试）
        logger.info("🔄 同步2025赛季比赛数据（包含季前测试）...")
        races = sync_service.sync_races(2025)
        logger.info(f"✅ 同步了 {len(races)} 场比赛")
        
        # 3. 验证同步结果
        from app.models.race import Race
        all_races = db.query(Race).filter(
            Race.season_id == 2025
        ).order_by(Race.round_number).all()
        
        logger.info(f"📊 数据库中共有 {len(all_races)} 场比赛:")
        for race in all_races:
            logger.info(f"  - 第{race.round_number}轮: {race.official_event_name} (格式: {race.event_format})")
        
        # 4. 特别验证第0轮季前测试
        testing_race = db.query(Race).filter(
            Race.season_id == 2025,
            Race.round_number == 0
        ).first()
        
        if testing_race:
            logger.info(f"✅ 成功同步季前测试: {testing_race.official_event_name}")
        else:
            logger.warning("⚠️ 未找到第0轮季前测试")
        
        # 5. 验证冲刺赛
        sprint_races = db.query(Race).filter(
            Race.season_id == 2025,
            Race.is_sprint == True
        ).order_by(Race.round_number).all()
        
        logger.info(f"📊 冲刺赛数量: {len(sprint_races)}")
        for race in sprint_races:
            logger.info(f"  - 第{race.round_number}轮: {race.official_event_name}")
        
        # 6. 验证常规比赛
        conventional_races = db.query(Race).filter(
            Race.season_id == 2025,
            Race.is_sprint == False
        ).order_by(Race.round_number).all()
        
        logger.info(f"📊 常规比赛数量: {len(conventional_races)}")
        
        # 7. 数据完整性检查
        expected_count = len(events_df)
        actual_count = len(all_races)
        
        if actual_count == expected_count:
            logger.info(f"✅ 数据完整性验证通过: 期望 {expected_count} 场，实际 {actual_count} 场")
        else:
            logger.warning(f"⚠️ 数据完整性验证失败: 期望 {expected_count} 场，实际 {actual_count} 场")
        
        logger.info("✅ 完整赛季同步完成")
        return True
        
    except Exception as e:
        logger.error(f"❌ 同步失败: {e}")
        return False
    finally:
        db.close()

def main():
    """主函数"""
    logger.info("🚀 开始2025赛季完整数据同步流程...")
    
    success = sync_complete_season()
    
    if success:
        logger.info("🎉 2025赛季数据同步成功完成！")
    else:
        logger.error("💥 2025赛季数据同步失败！")
    
    return success

if __name__ == "__main__":
    main() 