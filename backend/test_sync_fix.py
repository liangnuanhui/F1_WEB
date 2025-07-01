#!/usr/bin/env python3
"""
测试2025年比赛后数据更新功能
专注测试5个核心数据：排位赛结果、比赛结果、冲刺赛结果、车手积分榜、车队积分榜
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.core.database import SessionLocal
from app.services.unified_sync_service import UnifiedSyncService

def test_2025_race_data_updates():
    """测试2025年比赛后数据更新功能"""
    db = SessionLocal()
    
    try:
        service = UnifiedSyncService(db)
        
        print("🏎️ 测试2025年比赛后数据更新功能")
        print("="*60)
        
        # 首先确保2025年赛季和比赛日程存在
        print("\n=== 1. 检查2025年赛季数据 ===")
        seasons = service.sync_seasons()
        season_2025 = next((s for s in seasons if s.year == 2025), None)
        if season_2025:
            print(f"✅ 2025年赛季已存在: {season_2025.name}")
        else:
            print("❌ 2025年赛季不存在")
            return
        
        # 同步2025年比赛日程
        print("\n=== 2. 同步2025年比赛日程 ===")
        races = service.sync_races(2025)
        print(f"✅ 成功获取 {len(races)} 场2025年比赛")
        if races:
            for race in races[:3]:  # 只显示前3场
                print(f"   - 第{race.round_number}轮: {race.official_event_name} ({race.event_date})")
        
        print("\n" + "="*60)
        print("🎯 测试比赛后数据更新的5个核心功能:")
        print("="*60)
        
        # 测试1: 排位赛结果更新
        print("\n=== 3. 排位赛结果更新测试 ===")
        try:
            qualifying_success = service.sync_qualifying_results(2025)
            print(f"排位赛结果: {'✅ 成功' if qualifying_success else '⏳ 暂无数据（比赛未进行）'}")
        except Exception as e:
            print(f"排位赛结果: ❌ 失败 - {e}")
        
        # 测试2: 比赛结果更新
        print("\n=== 4. 比赛结果更新测试 ===")
        try:
            race_results_success = service.sync_race_results(2025)
            print(f"比赛结果: {'✅ 成功' if race_results_success else '⏳ 暂无数据（比赛未进行）'}")
        except Exception as e:
            print(f"比赛结果: ❌ 失败 - {e}")
        
        # 测试3: 冲刺赛结果更新
        print("\n=== 5. 冲刺赛结果更新测试 ===")
        try:
            sprint_success = service.sync_sprint_results(2025)
            print(f"冲刺赛结果: {'✅ 成功' if sprint_success else '⏳ 暂无数据（冲刺赛未进行）'}")
        except Exception as e:
            print(f"冲刺赛结果: ❌ 失败 - {e}")
        
        # 测试4: 车手积分榜更新
        print("\n=== 6. 车手积分榜更新测试 ===")
        try:
            driver_success = service.sync_driver_standings(2025)
            print(f"车手积分榜: {'✅ 成功' if driver_success else '⏳ 暂无数据（赛季未开始）'}")
        except Exception as e:
            print(f"车手积分榜: ❌ 失败 - {e}")
        
        # 测试5: 车队积分榜更新
        print("\n=== 7. 车队积分榜更新测试 ===")
        try:
            constructor_success = service.sync_constructor_standings(2025)
            print(f"车队积分榜: {'✅ 成功' if constructor_success else '⏳ 暂无数据（赛季未开始）'}")
        except Exception as e:
            print(f"车队积分榜: ❌ 失败 - {e}")
        
        print("\n" + "="*60)
        print("📝 测试总结:")
        print("- ✅ 表示功能正常工作")
        print("- ⏳ 表示暂无数据（比赛/赛季未开始，这是正常的）")
        print("- ❌ 表示功能有错误需要修复")
        print("\n🎉 2025年比赛后数据更新测试完成！")
        
    except Exception as e:
        print(f"❌ 测试过程中出错: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    test_2025_race_data_updates() 