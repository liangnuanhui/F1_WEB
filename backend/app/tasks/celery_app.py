"""
Celery 应用配置
"""

from celery import Celery
from kombu import Queue

from ..core.config import settings

# 创建 Celery 应用
celery_app = Celery(
    "f1_web_tasks",
    broker=settings.celery_broker_url,
    backend=settings.celery_result_backend,
    include=[
        "app.tasks.data_sync",
        "app.tasks.scheduler",
        "app.tasks.post_race_tasks",  # 添加比赛后同步任务模块
    ]
)

# Celery 配置
celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
    task_time_limit=3600,  # 1小时超时
    task_soft_time_limit=3300,  # 55分钟软超时
    worker_prefetch_multiplier=1,
    worker_max_tasks_per_child=1000,
    
    # 任务路由
    task_routes={
        "app.tasks.data_sync.*": {"queue": "data_sync"},
        "app.tasks.scheduler.*": {"queue": "scheduler"},
        "app.tasks.post_race_tasks.*": {"queue": "post_race_sync"},  # 比赛后同步任务路由
    },
    
    # 队列配置
    task_default_queue="default",
    task_queues=(
        Queue("default"),
        Queue("data_sync", routing_key="data_sync"),
        Queue("scheduler", routing_key="scheduler"),
        # 新增比赛后同步专用队列
        Queue("post_race_sync", routing_key="post_race_sync"),
        Queue("post_race_scheduler", routing_key="post_race_scheduler"),
        Queue("post_race_monitor", routing_key="post_race_monitor"),
        Queue("post_race_cleanup", routing_key="post_race_cleanup"),
        Queue("post_race_batch", routing_key="post_race_batch"),
    ),
    
    # 重试配置
    task_default_retry_delay=60,
    task_max_retries=3,
    
    # 结果过期时间
    result_expires=86400,  # 24小时
    
    # Beat 调度器配置
    beat_schedule={
        # 原有的调度任务
        "check-race-schedules": {
            "task": "app.tasks.scheduler.check_race_schedules",
            "schedule": 86400.0,  # 每24小时（1天）
        },
        "cleanup-expired-schedules": {
            "task": "app.tasks.scheduler.cleanup_expired_schedules", 
            "schedule": 21600.0,  # 每6小时
        },
        
        # 新增的比赛后同步定期任务
        "hourly-monitor-post-race-syncs": {
            "task": "hourly_monitor_post_race_syncs",
            "schedule": 3600.0,  # 每小时监控待执行的同步任务
        },
        "daily-cleanup-expired-schedules": {
            "task": "daily_cleanup_expired_schedules",
            "schedule": 86400.0,  # 每天清理过期的同步计划
        },
        "weekly-batch-schedule-races": {
            "task": "weekly_batch_schedule_races",
            "schedule": 604800.0,  # 每周批量安排即将到来的比赛
        },
    },
)

# 自动发现任务
celery_app.autodiscover_tasks() 