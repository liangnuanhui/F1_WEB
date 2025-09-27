"""
Celery 异步任务模块
"""

from .celery_app import celery_app
from .data_sync import (
    sync_race_results_task,
    sync_qualifying_results_task,
    sync_sprint_results_task,
    sync_driver_standings_task,
    sync_constructor_standings_task,
    sync_all_post_race_data_task
)
from .scheduler import schedule_post_race_updates

__all__ = [
    "celery_app",
    "sync_race_results_task",
    "sync_qualifying_results_task",
    "sync_sprint_results_task",
    "sync_driver_standings_task",
    "sync_constructor_standings_task",
    "sync_all_post_race_data_task",
    "schedule_post_race_updates",
] 