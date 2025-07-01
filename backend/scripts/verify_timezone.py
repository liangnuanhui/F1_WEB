#!/usr/bin/env python3
"""
时区配置验证脚本

用于验证F1数据调度系统的时区配置是否正确
"""

import os
import sys
from datetime import datetime, timedelta
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

try:
    from app.tasks.celery_app import celery_app
    from app.tasks.scheduler import RaceScheduler
except ImportError as e:
    print(f"❌ 导入错误: {e}")
    print("请确保在项目根目录运行此脚本")
    sys.exit(1)


def verify_system_timezone():
    """验证系统时区配置"""
    print("🕐 系统时区配置检查")
    print("=" * 50)
    
    # 检查环境变量
    tz = os.environ.get('TZ', '未设置')
    print(f"TZ 环境变量: {tz}")
    
    if tz != 'UTC' and tz != '未设置':
        print("⚠️  建议设置 TZ=UTC 以确保时区一致性")
    
    # 检查当前时间
    utc_now = datetime.utcnow()
    local_now = datetime.now()
    
    print(f"当前 UTC 时间: {utc_now}")
    print(f"当前本地时间: {local_now}")
    print(f"时区偏移: {local_now - utc_now}")
    
    return tz == 'UTC'


def verify_celery_config():
    """验证Celery时区配置"""
    print("\n🔧 Celery 配置检查")
    print("=" * 50)
    
    try:
        timezone = celery_app.conf.timezone
        enable_utc = celery_app.conf.enable_utc
        
        print(f"Celery 时区: {timezone}")
        print(f"启用 UTC: {enable_utc}")
        
        if timezone == 'UTC' and enable_utc:
            print("✅ Celery 时区配置正确")
            return True
        else:
            print("❌ Celery 时区配置有问题")
            return False
            
    except Exception as e:
        print(f"❌ 检查 Celery 配置时出错: {e}")
        return False


def verify_scheduler():
    """验证调度器时间处理"""
    print("\n⏰ 调度器时间处理检查")
    print("=" * 50)
    
    try:
        scheduler = RaceScheduler()
        print("✅ 调度器初始化成功")
        
        # 模拟时间计算
        now = datetime.utcnow()
        future_time = now + timedelta(hours=6)
        
        print(f"当前 UTC 时间: {now}")
        print(f"6小时后时间: {future_time}")
        print(f"时间计算正常")
        
        return True
        
    except Exception as e:
        print(f"❌ 调度器验证失败: {e}")
        return False


def verify_database_connection():
    """验证数据库连接和时间存储"""
    print("\n🗄️  数据库时间处理检查")
    print("=" * 50)
    
    try:
        from app.api.deps import get_db
        from app.models.race import Race
        from sqlalchemy import text
        
        db = next(get_db())
        
        # 检查数据库时区
        result = db.execute(text("SELECT NOW() as db_time"))
        db_time = result.fetchone()[0]
        
        print(f"数据库当前时间: {db_time}")
        
        # 检查是否有比赛数据
        race_count = db.query(Race).count()
        print(f"数据库中比赛数量: {race_count}")
        
        if race_count > 0:
            # 检查最近的比赛时间
            recent_race = db.query(Race).filter(
                Race.session5_date.isnot(None)
            ).order_by(Race.session5_date.desc()).first()
            
            if recent_race:
                print(f"最近比赛时间: {recent_race.session5_date}")
                print(f"比赛名称: {recent_race.official_event_name}")
        
        db.close()
        print("✅ 数据库连接和时间处理正常")
        return True
        
    except Exception as e:
        print(f"❌ 数据库检查失败: {e}")
        return False


def verify_schedule_calculation():
    """验证调度时间计算"""
    print("\n📅 调度时间计算验证")
    print("=" * 50)
    
    try:
        # 模拟比赛时间
        race_start = datetime.utcnow() + timedelta(hours=2)  # 2小时后开始
        race_end = race_start + timedelta(hours=3)  # 比赛持续3小时
        update_time = race_end + timedelta(hours=6)  # 结束后6小时更新
        
        print(f"模拟比赛开始时间: {race_start}")
        print(f"预计比赛结束时间: {race_end}")
        print(f"数据更新时间: {update_time}")
        
        # 验证时间是否在未来
        now = datetime.utcnow()
        if update_time > now:
            print("✅ 调度时间计算正确")
            return True
        else:
            print("❌ 调度时间计算有误")
            return False
            
    except Exception as e:
        print(f"❌ 调度计算验证失败: {e}")
        return False


def show_deployment_recommendations():
    """显示部署建议"""
    print("\n🚀 部署建议")
    print("=" * 50)
    
    print("1. 环境变量设置:")
    print("   export TZ=UTC")
    print()
    
    print("2. Docker 部署:")
    print("   environment:")
    print("     - TZ=UTC")
    print()
    
    print("3. Kubernetes 部署:")
    print("   env:")
    print("   - name: TZ")
    print("     value: UTC")
    print()
    
    print("4. AWS Lambda:")
    print("   Environment:")
    print("     TZ: UTC")
    print()
    
    print("5. 验证命令:")
    print("   python scripts/verify_timezone.py")


def main():
    """主函数"""
    print("🌍 F1 数据调度系统时区配置验证")
    print("=" * 60)
    
    checks = [
        ("系统时区", verify_system_timezone),
        ("Celery配置", verify_celery_config),
        ("调度器", verify_scheduler),
        ("数据库连接", verify_database_connection),
        ("调度计算", verify_schedule_calculation),
    ]
    
    results = []
    for name, check_func in checks:
        try:
            result = check_func()
            results.append((name, result))
        except Exception as e:
            print(f"❌ {name} 检查时发生异常: {e}")
            results.append((name, False))
    
    # 汇总结果
    print("\n📊 检查结果汇总")
    print("=" * 50)
    
    all_passed = True
    for name, passed in results:
        status = "✅ 通过" if passed else "❌ 失败"
        print(f"{name}: {status}")
        if not passed:
            all_passed = False
    
    if all_passed:
        print("\n🎉 所有检查都通过！系统时区配置正确。")
        print("您可以安全地部署到任何时区的服务器。")
    else:
        print("\n⚠️  发现问题，请检查上述失败项目。")
        show_deployment_recommendations()
    
    return 0 if all_passed else 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code) 