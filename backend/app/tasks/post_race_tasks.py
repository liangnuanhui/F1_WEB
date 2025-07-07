"""
比赛后数据同步 Celery 任务
支持多时间点重试的智能同步机制
"""

import logging
from typing import Dict, Any, List, Tuple, Optional
from datetime import datetime, timezone

from celery import Task
from .celery_app import celery_app
from ..core.database import get_db
from ..services.post_race_sync_service import PostRaceSyncService, SyncStatus
from ..models import Race, Season

logger = logging.getLogger(__name__)


class PostRaceTask(Task):
    """比赛后任务基类"""
    
    def on_success(self, retval, task_id, args, kwargs):
        logger.info(f"✅ 比赛后同步任务 {task_id} 执行成功: {retval}")

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        logger.error(f"❌ 比赛后同步任务 {task_id} 执行失败: {exc}")
        logger.error(f"错误详情: {einfo}")

    def on_retry(self, exc, task_id, args, kwargs, einfo):
        logger.warning(f"🔄 比赛后同步任务 {task_id} 准备重试: {exc}")


@celery_app.task(bind=True, base=PostRaceTask, queue="post_race_sync")
def execute_post_race_sync(
    self, 
    season_year: int, 
    race_round: int, 
    attempt_number: int
) -> Dict[str, Any]:
    """
    执行比赛后数据同步
    
    Args:
        season_year: 赛季年份
        race_round: 比赛轮次
        attempt_number: 尝试次数
    
    Returns:
        Dict[str, Any]: 同步结果
    """
    logger.info(f"🏁 开始执行比赛后数据同步: {season_year} 赛季第 {race_round} 轮 (第 {attempt_number} 次尝试)")
    
    db = None
    try:
        # 获取数据库会话
        db = next(get_db())
        
        # 创建同步服务
        sync_service = PostRaceSyncService(db, cache_dir="./cache")
        
        # 执行同步尝试
        status, results = sync_service.execute_sync_attempt(
            season_year, race_round, attempt_number
        )
        
        result = {
            "task": "execute_post_race_sync",
            "season_year": season_year,
            "race_round": race_round,
            "attempt_number": attempt_number,
            "status": status.value,
            "results": results,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "success": status in [SyncStatus.SUCCESS, SyncStatus.PARTIAL_SUCCESS]
        }
        
        if status == SyncStatus.SUCCESS:
            logger.info(f"🎉 第 {attempt_number} 次同步完全成功!")
        elif status == SyncStatus.PARTIAL_SUCCESS:
            logger.warning(f"⚠️ 第 {attempt_number} 次同步部分成功，详情: {results}")
        else:
            logger.error(f"❌ 第 {attempt_number} 次同步失败")
            
        return result
        
    except Exception as e:
        logger.error(f"❌ 执行比赛后数据同步时发生异常: {e}")
        # 对于比赛后同步，我们一般不重试，因为有多个时间点的尝试机制
        raise
    finally:
        if db:
            db.close()


@celery_app.task(bind=True, base=PostRaceTask, queue="post_race_scheduler")
def schedule_race_post_sync(
    self, 
    season_year: int, 
    race_round: int,
    retry_intervals: Optional[List[int]] = None
) -> Dict[str, Any]:
    """
    为比赛安排赛后数据同步计划
    
    Args:
        season_year: 赛季年份
        race_round: 比赛轮次  
        retry_intervals: 重试间隔时间（小时），默认[6, 12, 24]
    
    Returns:
        Dict[str, Any]: 调度结果
    """
    logger.info(f"📅 开始安排 {season_year} 赛季第 {race_round} 轮的赛后同步计划")
    
    if retry_intervals is None:
        retry_intervals = [6, 12, 24]
    
    db = None
    try:
        # 获取数据库会话
        db = next(get_db())
        
        # 查找比赛
        race = db.query(Race).join(Season).filter(
            Season.year == season_year,
            Race.round_number == race_round
        ).first()
        
        if not race:
            error_msg = f"未找到 {season_year} 赛季第 {race_round} 轮比赛"
            logger.error(error_msg)
            return {
                "success": False,
                "error": error_msg,
                "timestamp": datetime.now(timezone.utc).isoformat()
            }
        
        # 创建同步服务
        sync_service = PostRaceSyncService(db, cache_dir="./cache")
        
        # 安排同步计划
        schedule = sync_service.schedule_post_race_sync(race, retry_intervals)
        
        # 为每个尝试安排Celery任务
        scheduled_tasks = []
        for attempt in schedule.attempts:
            task = execute_post_race_sync.apply_async(
                args=[season_year, race_round, attempt.attempt_number],
                eta=attempt.scheduled_time.replace(tzinfo=timezone.utc)
            )
            scheduled_tasks.append({
                "attempt_number": attempt.attempt_number,
                "task_id": task.id,
                "scheduled_time": attempt.scheduled_time.isoformat(),
                "eta": attempt.scheduled_time.isoformat()
            })
            
            logger.info(
                f"✅ 已安排第 {attempt.attempt_number} 次同步任务: {task.id}, "
                f"执行时间: {attempt.scheduled_time}"
            )
        
        result = {
            "task": "schedule_race_post_sync",
            "success": True,
            "season_year": season_year,
            "race_round": race_round,
            "race_name": race.official_event_name,
            "race_end_time": schedule.race_end_time.isoformat(),
            "retry_intervals": retry_intervals,
            "scheduled_tasks": scheduled_tasks,
            "total_attempts": len(scheduled_tasks),
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
        
        logger.info(
            f"🎯 {race.official_event_name} 赛后同步计划安排完成\n"
            f"   总尝试次数: {len(scheduled_tasks)}\n"
            f"   时间点: {[t['scheduled_time'] for t in scheduled_tasks]}"
        )
        
        return result
        
    except Exception as e:
        logger.error(f"❌ 安排赛后同步计划时发生异常: {e}")
        return {
            "task": "schedule_race_post_sync",
            "success": False,
            "error": str(e),
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
    finally:
        if db:
            db.close()


@celery_app.task(bind=True, base=PostRaceTask, queue="post_race_monitor")
def monitor_pending_syncs(self) -> Dict[str, Any]:
    """
    监控待执行的同步任务
    检查是否有遗漏的同步任务需要立即执行
    """
    logger.info("🔍 开始监控待执行的同步任务...")
    
    db = None
    try:
        # 获取数据库会话
        db = next(get_db())
        
        # 创建同步服务
        sync_service = PostRaceSyncService(db, cache_dir="./cache")
        
        # 获取待执行的同步任务
        pending_syncs = sync_service.get_pending_syncs()
        
        executed_tasks = []
        for season_year, race_round, attempt_number, scheduled_time in pending_syncs:
            logger.info(
                f"🚨 发现遗漏的同步任务: {season_year} 赛季第 {race_round} 轮 "
                f"(第 {attempt_number} 次尝试) - 原定时间: {scheduled_time}"
            )
            
            # 立即执行同步
            task = execute_post_race_sync.delay(season_year, race_round, attempt_number)
            executed_tasks.append({
                "season_year": season_year,
                "race_round": race_round,
                "attempt_number": attempt_number,
                "original_scheduled_time": scheduled_time.isoformat(),
                "task_id": task.id,
                "executed_at": datetime.now(timezone.utc).isoformat()
            })
        
        result = {
            "task": "monitor_pending_syncs",
            "success": True,
            "pending_count": len(pending_syncs),
            "executed_tasks": executed_tasks,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
        
        if executed_tasks:
            logger.info(f"✅ 立即执行了 {len(executed_tasks)} 个遗漏的同步任务")
        else:
            logger.info("✅ 没有待执行的同步任务")
        
        return result
        
    except Exception as e:
        logger.error(f"❌ 监控待执行同步任务时发生异常: {e}")
        return {
            "task": "monitor_pending_syncs",
            "success": False,
            "error": str(e),
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
    finally:
        if db:
            db.close()


@celery_app.task(bind=True, base=PostRaceTask, queue="post_race_cleanup")
def cleanup_expired_schedules(self) -> Dict[str, Any]:
    """
    清理过期的同步计划
    """
    logger.info("🧹 开始清理过期的同步计划...")
    
    db = None
    try:
        # 获取数据库会话
        db = next(get_db())
        
        # 创建同步服务
        sync_service = PostRaceSyncService(db, cache_dir="./cache")
        
        # 清理过期计划
        cleaned_count = sync_service.cleanup_expired_schedules()
        
        result = {
            "task": "cleanup_expired_schedules",
            "success": True,
            "cleaned_count": cleaned_count,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
        
        logger.info(f"✅ 清理完成，共清理 {cleaned_count} 个过期计划")
        return result
        
    except Exception as e:
        logger.error(f"❌ 清理过期计划时发生异常: {e}")
        return {
            "task": "cleanup_expired_schedules",
            "success": False,
            "error": str(e),
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
    finally:
        if db:
            db.close()


@celery_app.task(bind=True, base=PostRaceTask, queue="post_race_batch")
def batch_schedule_upcoming_races(
    self, 
    season_year: int = 2025,
    days_ahead: int = 7
) -> Dict[str, Any]:
    """
    批量安排即将到来的比赛的赛后同步计划
    
    Args:
        season_year: 赛季年份，默认2025
        days_ahead: 提前几天安排，默认7天
        
    Returns:
        Dict[str, Any]: 批量调度结果
    """
    logger.info(f"📦 开始批量安排 {season_year} 赛季未来 {days_ahead} 天内的比赛后同步计划...")
    
    db = None
    try:
        # 获取数据库会话
        db = next(get_db())
        
        # 创建同步服务
        sync_service = PostRaceSyncService(db, cache_dir="./cache")
        
        # 查找即将到来的比赛
        from datetime import timedelta
        
        now = datetime.now(timezone.utc)
        future_date = now + timedelta(days=days_ahead)
        
        upcoming_races = db.query(Race).join(Season).filter(
            Season.year == season_year,
            Race.event_date >= now.date(),
            Race.event_date <= future_date.date()
        ).all()
        
        scheduled_races = []
        for race in upcoming_races:
            try:
                # 检查是否已经有同步计划
                existing_schedule = sync_service.get_schedule(season_year, race.round_number)
                if existing_schedule:
                    logger.info(f"⏭️ {race.official_event_name} 已有同步计划，跳过")
                    continue
                
                # 安排新的同步计划
                task = schedule_race_post_sync.delay(season_year, race.round_number)
                
                scheduled_races.append({
                    "race_round": race.round_number,
                    "race_name": race.official_event_name,
                    "event_date": race.event_date.isoformat(),
                    "task_id": task.id
                })
                
                logger.info(f"✅ 已安排 {race.official_event_name} 的同步计划: {task.id}")
                
            except Exception as e:
                logger.error(f"❌ 为 {race.official_event_name} 安排同步计划失败: {e}")
                continue
        
        result = {
            "task": "batch_schedule_upcoming_races",
            "success": True,
            "season_year": season_year,
            "days_ahead": days_ahead,
            "upcoming_races_count": len(upcoming_races),
            "scheduled_races_count": len(scheduled_races),
            "scheduled_races": scheduled_races,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
        
        logger.info(
            f"🎯 批量调度完成\n"
            f"   即将到来的比赛: {len(upcoming_races)} 场\n"
            f"   新安排的计划: {len(scheduled_races)} 个"
        )
        
        return result
        
    except Exception as e:
        logger.error(f"❌ 批量安排同步计划时发生异常: {e}")
        return {
            "task": "batch_schedule_upcoming_races",
            "success": False,
            "error": str(e),
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
    finally:
        if db:
            db.close()


# 定期任务：每小时检查一次待执行的同步任务
@celery_app.task(bind=True, name="hourly_monitor_post_race_syncs")
def hourly_monitor_post_race_syncs(self):
    """每小时监控一次比赛后同步任务"""
    return monitor_pending_syncs.delay()


# 定期任务：每天清理一次过期的同步计划
@celery_app.task(bind=True, name="daily_cleanup_expired_schedules")
def daily_cleanup_expired_schedules(self):
    """每天清理一次过期的同步计划"""
    return cleanup_expired_schedules.delay()


# 定期任务：每周批量安排即将到来的比赛
@celery_app.task(bind=True, name="weekly_batch_schedule_races")
def weekly_batch_schedule_races(self):
    """每周批量安排即将到来的比赛的同步计划"""
    return batch_schedule_upcoming_races.delay() 