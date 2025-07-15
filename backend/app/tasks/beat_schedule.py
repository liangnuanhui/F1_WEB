"""
Celery 定期任务配置
实现完全自动化的比赛数据同步
"""

from celery.schedules import crontab
from .celery_app import celery_app
from .auto_scheduler import (
    auto_schedule_all_races,
    check_and_schedule_upcoming_races,
    cleanup_old_schedules
)

# 定期任务调度配置
celery_app.conf.beat_schedule = {
    # 每天凌晨2点检查并安排即将到来的比赛
    'check-upcoming-races': {
        'task': 'app.tasks.auto_scheduler.check_and_schedule_upcoming_races',
        'schedule': crontab(hour=2, minute=0),  # 每天凌晨2点
        'options': {'queue': 'scheduler'}
    },
    
    # 每天凌晨3点清理过期的调度计划
    'cleanup-old-schedules': {
        'task': 'app.tasks.auto_scheduler.cleanup_old_schedules',
        'schedule': crontab(hour=3, minute=0),  # 每天凌晨3点
        'options': {'queue': 'scheduler'}
    },
    
    # 每周日凌晨1点为整个赛季重新安排（保险起见）
    'weekly-full-schedule': {
        'task': 'app.tasks.auto_scheduler.auto_schedule_all_races',
        'schedule': crontab(hour=1, minute=0, day_of_week=0),  # 每周日凌晨1点
        'options': {'queue': 'scheduler'}
    },
    
    # 每月1号检查并安排整个赛季（长期保险）
    'monthly-season-check': {
        'task': 'app.tasks.auto_scheduler.auto_schedule_all_races',
        'schedule': crontab(hour=0, minute=30, day_of_month=1),  # 每月1号凌晨0:30
        'options': {'queue': 'scheduler'}
    }
}

# 设置时区
celery_app.conf.timezone = 'UTC'