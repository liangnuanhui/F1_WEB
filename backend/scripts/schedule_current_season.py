#!/usr/bin/env python3
"""
为当前赛季的所有比赛安排自动数据更新调度

使用方法:
python scripts/schedule_current_season.py [--year=2025] [--force]
"""

import sys
import argparse
from pathlib import Path
from datetime import datetime

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from app.core.database import get_db
from app.tasks.scheduler import RaceScheduler
from app.models import Race, Season


def schedule_season_races(season_year: int, force: bool = False):
    """为指定赛季安排所有比赛的调度"""
    
    print(f"🏎️  为 {season_year} 赛季安排比赛数据自动更新")
    print("=" * 50)
    
    try:
        # 获取数据库会话
        db = next(get_db())
        
        # 验证赛季是否存在
        season = db.query(Season).filter(Season.year == season_year).first()
        if not season:
            print(f"❌ 赛季 {season_year} 不存在")
            return False
        
        # 获取该赛季的所有比赛
        races = db.query(Race).filter(Race.season_id == season.id).order_by(Race.round_number).all()
        
        if not races:
            print(f"❌ {season_year} 赛季没有比赛数据")
            return False
        
        print(f"📊 找到 {len(races)} 场比赛")
        
        # 创建调度器
        scheduler = RaceScheduler()
        
        # 统计变量
        scheduled_count = 0
        skipped_count = 0
        error_count = 0
        
        # 为每场比赛安排调度
        for race in races:
            try:
                print(f"\n🏁 处理第 {race.round_number} 轮: {race.official_event_name}")
                
                # 检查是否已经有调度
                schedule_key = scheduler._get_schedule_key(season_year, race.round_number)
                
                if scheduler.redis_client.exists(schedule_key) and not force:
                    print(f"   ⏭️ 已存在调度，跳过")
                    skipped_count += 1
                    continue
                
                # 如果强制模式，先取消现有调度
                if force and scheduler.redis_client.exists(schedule_key):
                    print(f"   🗑️ 强制模式：取消现有调度")
                    scheduler.cancel_race_schedule(season_year, race.round_number)
                
                # 创建新调度
                if scheduler.schedule_post_race_update(race):
                    print(f"   ✅ 调度创建成功")
                    scheduled_count += 1
                else:
                    print(f"   ❌ 调度创建失败")
                    error_count += 1
                    
            except Exception as e:
                print(f"   ❌ 处理比赛时发生错误: {e}")
                error_count += 1
        
        # 显示结果汇总
        print("\n" + "=" * 50)
        print("📈 调度结果汇总")
        print("=" * 50)
        print(f"🎯 总比赛数: {len(races)}")
        print(f"✅ 新建调度: {scheduled_count}")
        print(f"⏭️ 跳过已存在: {skipped_count}")
        print(f"❌ 失败数量: {error_count}")
        
        if error_count == 0:
            print(f"\n🎉 {season_year} 赛季调度安排完成！")
            
            # 显示监控信息
            print(f"\n💡 监控和管理:")
            print(f"   - Flower 面板: http://localhost:5555/flower")
            print(f"   - API 状态: GET /api/v1/scheduler/status")
            print(f"   - 调度列表: GET /api/v1/scheduler/schedules")
            
        else:
            print(f"\n⚠️ 调度完成，但有 {error_count} 个错误")
            
        db.close()
        return error_count == 0
        
    except Exception as e:
        print(f"❌ 调度过程发生错误: {e}")
        return False


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description="为 F1 赛季安排自动数据更新调度")
    parser.add_argument(
        "--year", 
        type=int, 
        default=datetime.now().year,
        help="指定赛季年份 (默认: 当前年份)"
    )
    parser.add_argument(
        "--force", 
        action="store_true",
        help="强制覆盖已存在的调度"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true", 
        help="仅显示将要安排的调度，不实际创建"
    )
    
    args = parser.parse_args()
    
    print("🔧 配置信息:")
    print(f"   - 赛季年份: {args.year}")
    print(f"   - 强制模式: {'是' if args.force else '否'}")
    print(f"   - 试运行: {'是' if args.dry_run else '否'}")
    
    if args.dry_run:
        print("\n🧪 试运行模式 - 仅显示调度信息")
        show_season_schedule_info(args.year)
    else:
        # 确认操作
        if args.force:
            confirm = input(f"\n⚠️ 确认要强制重新安排 {args.year} 赛季的所有调度吗？ (y/N): ")
            if confirm.lower() != 'y':
                print("❌ 操作已取消")
                return 1
        
        success = schedule_season_races(args.year, args.force)
        return 0 if success else 1


def show_season_schedule_info(season_year: int):
    """显示赛季调度信息（试运行模式）"""
    try:
        db = next(get_db())
        
        # 获取赛季比赛
        season = db.query(Season).filter(Season.year == season_year).first()
        if not season:
            print(f"❌ 赛季 {season_year} 不存在")
            return
        
        races = db.query(Race).filter(Race.season_id == season.id).order_by(Race.round_number).all()
        
        if not races:
            print(f"❌ {season_year} 赛季没有比赛数据")
            return
        
        scheduler = RaceScheduler()
        
        print(f"\n📅 {season_year} 赛季比赛调度预览:")
        print("-" * 80)
        
        for race in races:
                                      # 计算预计更新时间
             race_end_time = scheduler._get_race_end_time(race)
             if race_end_time:
                 from datetime import timedelta
                 update_time = race_end_time + timedelta(hours=scheduler.post_race_delay_hours)
                 update_time_str = update_time.strftime("%Y-%m-%d %H:%M:%S UTC")
             else:
                 update_time_str = "无法计算"
            
            # 检查是否已有调度
            schedule_key = scheduler._get_schedule_key(season_year, race.round_number)
            status = "已调度" if scheduler.redis_client.exists(schedule_key) else "未调度"
            
            print(f"第{race.round_number:2d}轮 | {race.official_event_name:<50} | {update_time_str} | {status}")
        
        db.close()
        
    except Exception as e:
        print(f"❌ 获取调度信息时发生错误: {e}")


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code) 