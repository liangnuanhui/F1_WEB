#!/usr/bin/env python3
"""
F1 数据自动调度系统演示脚本

演示如何设置和使用自动调度系统
"""

import sys
import time
from pathlib import Path
from datetime import datetime, timedelta

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from app.core.database import get_db
from app.tasks.scheduler import RaceScheduler
from app.models import Race, Season


def demo_scheduler_workflow():
    """演示调度器完整工作流程"""
    
    print("=" * 60)
    print("🏎️  F1 数据自动调度系统演示")
    print("=" * 60)
    
    # 1. 初始化调度器
    print("\n1️⃣ 初始化调度器...")
    scheduler = RaceScheduler()
    print(f"   ✅ 调度器初始化完成")
    print(f"   📦 Redis 前缀: {scheduler.schedule_key_prefix}")
    print(f"   ⏰ 延迟时间: {scheduler.post_race_delay_hours} 小时")
    
    # 2. 检查系统状态
    print("\n2️⃣ 检查系统状态...")
    try:
        # 测试 Redis 连接
        scheduler.redis_client.ping()
        print("   ✅ Redis 连接正常")
        
        # 测试数据库连接
        db = next(get_db())
        race_count = db.query(Race).count()
        print(f"   ✅ 数据库连接正常，共有 {race_count} 场比赛")
        
        # 检查现有调度
        existing_schedules = scheduler.get_scheduled_races()
        print(f"   📊 当前已有 {len(existing_schedules)} 个调度任务")
        
        db.close()
        
    except Exception as e:
        print(f"   ❌ 系统检查失败: {e}")
        return False
    
    # 3. 演示调度创建
    print("\n3️⃣ 演示调度创建...")
    demo_season = 2025
    demo_round = 1
    
    try:
        # 查找演示比赛
        db = next(get_db())
        demo_race = db.query(Race).join(Season).filter(
            Season.year == demo_season,
            Race.round_number == demo_round
        ).first()
        
        if demo_race:
            print(f"   🏁 找到演示比赛: {demo_race.official_event_name}")
            
            # 清理之前的调度（如果存在）
            scheduler.cancel_race_schedule(demo_season, demo_round)
            
            # 创建新调度
            success = scheduler.schedule_post_race_update(demo_race)
            if success:
                print("   ✅ 演示调度创建成功")
            else:
                print("   ❌ 演示调度创建失败")
        else:
            print(f"   ⚠️ 未找到 {demo_season} 赛季第 {demo_round} 轮比赛")
        
        db.close()
        
    except Exception as e:
        print(f"   ❌ 调度创建演示失败: {e}")
    
    # 4. 演示调度查询
    print("\n4️⃣ 演示调度查询...")
    try:
        scheduled_races = scheduler.get_scheduled_races()
        print(f"   📋 查询到 {len(scheduled_races)} 个调度任务")
        
        if scheduled_races:
            print("   📝 调度详情:")
            for i, schedule in enumerate(scheduled_races[:3], 1):  # 只显示前3个
                race_name = schedule.get('race_name', 'Unknown')[:50]
                update_time = schedule.get('update_time', 'Unknown')
                print(f"      {i}. {race_name} -> {update_time}")
            
            if len(scheduled_races) > 3:
                print(f"      ... 还有 {len(scheduled_races) - 3} 个调度")
        
    except Exception as e:
        print(f"   ❌ 调度查询演示失败: {e}")
    
    # 5. 演示时间计算
    print("\n5️⃣ 演示时间计算...")
    try:
        db = next(get_db())
        upcoming_races = db.query(Race).join(Season).filter(
            Race.session5_date.isnot(None)
        ).order_by(Race.session5_date).limit(3).all()
        
        print("   🕒 时间计算示例:")
        for race in upcoming_races:
            race_end_time = scheduler._get_race_end_time(race)
            if race_end_time:
                update_time = race_end_time + timedelta(hours=scheduler.post_race_delay_hours)
                print(f"      🏁 {race.official_event_name[:40]}...")
                print(f"         比赛时间: {race.session5_date}")
                print(f"         预计结束: {race_end_time}")
                print(f"         更新时间: {update_time}")
                print()
        
        db.close()
        
    except Exception as e:
        print(f"   ❌ 时间计算演示失败: {e}")
    
    # 6. 清理演示调度
    print("\n6️⃣ 清理演示调度...")
    try:
        success = scheduler.cancel_race_schedule(demo_season, demo_round)
        if success:
            print("   ✅ 演示调度已清理")
        else:
            print("   ℹ️ 没有需要清理的演示调度")
    except Exception as e:
        print(f"   ❌ 清理演示调度失败: {e}")
    
    # 7. 总结和建议
    print("\n7️⃣ 系统使用建议...")
    print("   💡 启动调度系统:")
    print("      python scripts/start_scheduler.py")
    print()
    print("   💡 为当前赛季安排调度:")
    print("      python scripts/schedule_current_season.py")
    print()
    print("   💡 监控系统状态:")
    print("      访问 http://localhost:5555/flower")
    print()
    print("   💡 API 管理:")
    print("      GET  /api/v1/scheduler/status")
    print("      GET  /api/v1/scheduler/schedules")
    print("      POST /api/v1/scheduler/schedule/season/2025")
    
    print("\n" + "=" * 60)
    print("🎉 演示完成！调度系统已准备就绪")
    print("=" * 60)
    
    return True


def show_system_architecture():
    """显示系统架构图"""
    print("\n🏗️ 系统架构概览:")
    print()
    print("    ┌─────────────┐    ┌──────────────┐    ┌─────────────┐")
    print("    │  比赛时间   │───▶│  Celery Beat │───▶│ 调度检查器  │")
    print("    └─────────────┘    └──────────────┘    └─────────────┘")
    print("                                                  │")
    print("                                                  ▼")
    print("    ┌─────────────┐    ┌──────────────┐    ┌─────────────┐")
    print("    │   Redis     │◀───│ 任务调度器   │◀───│ 时间计算器  │")
    print("    │  (调度存储) │    │ (6小时延迟)  │    │ (结束+6h)   │")
    print("    └─────────────┘    └──────────────┘    └─────────────┘")
    print("                              │")
    print("                              ▼")
    print("    ┌─────────────┐    ┌──────────────┐    ┌─────────────┐")
    print("    │ 数据同步器  │◀───│ Celery Worker│◀───│ 任务队列    │")
    print("    │ (5个任务)   │    │ (多进程执行) │    │ (优先级)    │")
    print("    └─────────────┘    └──────────────┘    └─────────────┘")
    print("           │")
    print("           ▼")
    print("    ┌─────────────┐    ┌──────────────┐    ┌─────────────┐")
    print("    │ FastF1 API  │───▶│  数据处理    │───▶│ PostgreSQL  │")
    print("    │ Ergast API  │    │  (结果/积分) │    │  (存储)     │")
    print("    └─────────────┘    └──────────────┘    └─────────────┘")
    print()


def show_data_flow():
    """显示数据流程"""
    print("\n📊 数据更新流程:")
    print()
    print("  1. 🏁 比赛进行中...")
    print("     │")
    print("  2. ⏰ 比赛结束 + 6小时")
    print("     │")
    print("  3. 🚀 触发数据同步任务")
    print("     │")
    print("  4. 📥 同步比赛结果")
    print("     ├── 正赛结果 (Race Results)")
    print("     ├── 排位赛结果 (Qualifying Results)")
    print("     └── 冲刺赛结果 (Sprint Results, 如适用)")
    print("     │")
    print("  5. 📊 更新积分榜")
    print("     ├── 车手积分榜 (Driver Standings)")
    print("     └── 车队积分榜 (Constructor Standings)")
    print("     │")
    print("  6. ✅ 数据更新完成")
    print("     └── 前端显示最新数据")
    print()


def main():
    """主函数"""
    print("🎯 选择演示内容:")
    print("1. 完整工作流程演示")
    print("2. 系统架构展示")
    print("3. 数据流程展示")
    print("4. 全部内容")
    
    try:
        choice = input("\n请输入选择 (1-4): ").strip()
        
        if choice == "1":
            demo_scheduler_workflow()
        elif choice == "2":
            show_system_architecture()
        elif choice == "3":
            show_data_flow()
        elif choice == "4":
            show_system_architecture()
            show_data_flow()
            demo_scheduler_workflow()
        else:
            print("❌ 无效选择，默认运行完整演示")
            demo_scheduler_workflow()
            
    except KeyboardInterrupt:
        print("\n\n👋 演示已取消")
    except Exception as e:
        print(f"\n❌ 演示过程中发生错误: {e}")


if __name__ == "__main__":
    main() 