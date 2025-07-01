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
    },
    
    # 队列配置
    task_default_queue="default",
    task_queues=(
        Queue("default"),
        Queue("data_sync", routing_key="data_sync"),
        Queue("scheduler", routing_key="scheduler"),
    ),
    
    # 重试配置
    task_default_retry_delay=60,
    task_max_retries=3,
    
    # 结果过期时间
    result_expires=86400,  # 24小时
    
    # Beat 调度器配置
    beat_schedule={
        # 每天检查一次是否有需要调度的比赛（F1比赛最频繁也就一周一次）
        "check-race-schedules": {
            "task": "app.tasks.scheduler.check_race_schedules",
            "schedule": 86400.0,  # 每24小时（1天）
        },
        # 每6小时清理过期的调度任务
        "cleanup-expired-schedules": {
            "task": "app.tasks.scheduler.cleanup_expired_schedules", 
            "schedule": 21600.0,  # 每6小时
        },
    },
)

# 自动发现任务
celery_app.autodiscover_tasks() 