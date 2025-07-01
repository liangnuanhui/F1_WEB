#!/usr/bin/env python3
"""
比赛后数据更新系统演示
演示如何在比赛结束后自动更新5个核心数据
"""
import sys
import os
from datetime import datetime, timedelta, timezone
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.core.database import SessionLocal
from app.tasks.scheduler import RaceScheduler
from app.tasks.data_sync import sync_post_race_data

def demo_post_race_system():
    """演示比赛后数据更新系统"""
    print("🏎️ F1 比赛后数据更新系统演示")
    print("="*60)
    
    db = SessionLocal()
    
    try:
        scheduler = RaceScheduler(db)
        
        # 模拟比赛场景：奥地利大奖赛
        print("\n📅 场景设置:")
        print("比赛: 2025年奥地利大奖赛")
        print("比赛时间: 6月29日21:00 (北京时间)")
        print("预期结束: 6月29日23:00 (北京时间)")
        print("数据更新时间: 6月30日02:00、05:00、11:00 (北京时间)")
        
        # 转换为UTC时间 (北京时间-8小时)
        race_end_time_utc = datetime(2025, 6, 29, 15, 0, 0, tzinfo=timezone.utc)  # 北京时间23:00 = UTC 15:00
        race_id = "2025_round_10_austria"
        
        print(f"\n⏰ 比赛结束时间 (UTC): {race_end_time_utc}")
        
        # 1. 安排比赛后数据更新
        print("\n" + "="*60)
        print("🚀 安排比赛后数据更新...")
        
        result = scheduler.schedule_post_race_updates(
            race_id=race_id,
            race_end_time=race_end_time_utc,
            season_year=2025
        )
        
        if result["success"]:
            print(f"✅ 更新调度成功: {result['summary']}")
            print("\n📋 调度详情:")
            for task in result["scheduled_tasks"]:
                print(f"   - {task['hours_after_race']}小时后: {task['update_time']} ({task['status']})")
        else:
            print(f"❌ 调度失败: {result['error']}")
            return
        
        # 2. 查看调度信息
        print("\n" + "="*60)
        print("📋 查看调度信息...")
        
        schedule_info = scheduler.get_post_race_schedule(race_id)
        if schedule_info["success"]:
            data = schedule_info["data"]
            print(f"✅ 调度信息获取成功")
            print(f"   比赛ID: {data['race_id']}")
            print(f"   比赛结束时间: {data['race_end_time']}")
            print(f"   赛季: {data['season_year']}")
            print(f"   调度任务数: {len(data['scheduled_tasks'])}")
        else:
            print(f"❌ 获取调度信息失败: {schedule_info['error']}")
        
        # 3. 手动测试数据同步
        print("\n" + "="*60)
        print("🧪 手动测试比赛后数据同步...")
        print("(模拟比赛结束后的数据更新)")
        
        try:
            # 直接调用同步函数（同步方式，用于演示）
            sync_result = sync_post_race_data(season_year=2025)
            
            if sync_result and sync_result.get("success"):
                print(f"✅ 数据同步测试成功: {sync_result['summary']}")
                print("📊 同步结果:")
                for data_type, success in sync_result["results"].items():
                    status = "✅ 成功" if success else "⏳ 暂无数据"
                    print(f"   - {data_type}: {status}")
            else:
                print(f"❌ 数据同步测试失败")
                if sync_result:
                    print(f"   错误: {sync_result.get('error', '未知错误')}")
                    
        except Exception as e:
            print(f"❌ 数据同步测试出错: {e}")
        
        # 4. 演示取消调度
        print("\n" + "="*60)
        print("🗑️ 演示取消调度...")
        
        choice = input("是否取消此次演示调度? (y/N): ").lower().strip()
        if choice == 'y':
            cancel_result = scheduler.cancel_post_race_schedule(race_id)
            if cancel_result["success"]:
                print(f"✅ 调度已取消: {cancel_result['message']}")
            else:
                print(f"❌ 取消失败: {cancel_result['error']}")
        else:
            print("📌 调度保持活跃状态")
        
        print("\n" + "="*60)
        print("🎉 比赛后数据更新系统演示完成！")
        print("\n📝 系统特点:")
        print("• 比赛结束后自动在3个时间点更新数据")
        print("• 专注更新5个核心数据类型")
        print("• 支持手动触发和取消调度")
        print("• 基于2025年F1赛季")
        print("• 适应源数据更新延迟的情况")
        
    except Exception as e:
        print(f"❌ 演示过程中出错: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    demo_post_race_system() 