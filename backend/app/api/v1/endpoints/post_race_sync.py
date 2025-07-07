"""
比赛后数据同步 API 端点
提供比赛后数据同步的管理和监控接口
"""

from typing import List, Dict, Any, Optional
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from pydantic import BaseModel
import logging

from ....core.database import get_db
from ....services.post_race_sync_service import PostRaceSyncService, PostRaceSchedule, SyncStatus
from ....tasks.post_race_tasks import (
    schedule_race_post_sync, 
    execute_post_race_sync,
    monitor_pending_syncs,
    cleanup_expired_schedules,
    batch_schedule_upcoming_races
)
from ....models import Race, Season

router = APIRouter()
logger = logging.getLogger(__name__)


class ScheduleRequest(BaseModel):
    """同步计划请求模型"""
    retry_intervals: Optional[List[int]] = None


@router.post("/{season_year}/{race_round}/schedule")
async def schedule_post_race_sync(
    season_year: int,
    race_round: int,
    request: ScheduleRequest = ScheduleRequest(),
    background_tasks: BackgroundTasks = BackgroundTasks(),
    db: Session = Depends(get_db)
):
    """
    为指定比赛安排赛后数据同步计划
    
    Args:
        season_year: 赛季年份
        race_round: 比赛轮次
        request: 同步计划请求，包含retry_intervals等参数
    """
    try:
        # 验证比赛存在
        race = db.query(Race).join(Season).filter(
            Season.year == season_year,
            Race.round_number == race_round
        ).first()
        
        if not race:
            raise HTTPException(
                status_code=404, 
                detail=f"未找到 {season_year} 赛季第 {race_round} 轮比赛"
            )
        
        # 检查是否已有同步计划
        sync_service = PostRaceSyncService(db, cache_dir="./cache")
        existing_schedule = sync_service.get_schedule(season_year, race_round)
        
        if existing_schedule:
            return {
                "message": "同步计划已存在",
                "existing_schedule": {
                    "race_name": existing_schedule.race_name,
                    "race_end_time": existing_schedule.race_end_time.isoformat(),
                    "attempts_count": len(existing_schedule.attempts),
                    "is_completed": existing_schedule.is_completed,
                    "success_rate": existing_schedule.success_rate
                }
            }
        
        # 直接创建同步计划（同步执行）
        retry_intervals = request.retry_intervals
        if retry_intervals is None:
            retry_intervals = [6, 12, 24]
        
        # 直接调用同步服务创建计划
        schedule = sync_service.schedule_post_race_sync(
            race=race,
            retry_intervals=retry_intervals
        )
        
        return {
            "message": f"已成功安排 {race.official_event_name} 的赛后同步计划",
            "season_year": season_year,
            "race_round": race_round,
            "race_name": race.official_event_name,
            "retry_intervals": retry_intervals,
            "status": "scheduled",
            "schedule_id": f"{season_year}:{race_round}",
            "attempts_count": len(schedule.attempts)
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"安排赛后同步计划失败: {e}")
        raise HTTPException(status_code=500, detail=f"安排同步计划失败: {str(e)}")


@router.get("/{season_year}/{race_round}/schedule")
async def get_post_race_schedule(
    season_year: int,
    race_round: int,
    db: Session = Depends(get_db)
):
    """
    获取指定比赛的赛后同步计划
    """
    try:
        sync_service = PostRaceSyncService(db, cache_dir="./cache")
        schedule = sync_service.get_schedule(season_year, race_round)
        
        if not schedule:
            raise HTTPException(
                status_code=404, 
                detail=f"未找到 {season_year} 赛季第 {race_round} 轮的同步计划"
            )
        
        return {
            "schedule": {
                "season_year": schedule.season_year,
                "race_round": schedule.race_round,
                "race_name": schedule.race_name,
                "race_end_time": schedule.race_end_time.isoformat(),
                "created_at": schedule.created_at.isoformat(),
                "is_completed": schedule.is_completed,
                "success_rate": schedule.success_rate,
                "next_pending_attempt": (
                    {
                        "attempt_number": schedule.next_pending_attempt.attempt_number,
                        "scheduled_time": schedule.next_pending_attempt.scheduled_time.isoformat()
                    } if schedule.next_pending_attempt else None
                ),
                "attempts": [
                    {
                        "attempt_number": attempt.attempt_number,
                        "scheduled_time": attempt.scheduled_time.isoformat(),
                        "executed_time": attempt.executed_time.isoformat() if attempt.executed_time else None,
                        "status": attempt.status.value,
                        "results": attempt.results,
                        "error_message": attempt.error_message
                    }
                    for attempt in schedule.attempts
                ]
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"获取赛后同步计划失败: {e}")
        raise HTTPException(status_code=500, detail=f"获取同步计划失败: {str(e)}")


@router.delete("/{season_year}/{race_round}/schedule")
async def cancel_post_race_schedule(
    season_year: int,
    race_round: int,
    db: Session = Depends(get_db)
):
    """
    取消指定比赛的赛后同步计划
    """
    try:
        sync_service = PostRaceSyncService(db, cache_dir="./cache")
        success = sync_service.cancel_schedule(season_year, race_round)
        
        if not success:
            raise HTTPException(
                status_code=404, 
                detail=f"未找到 {season_year} 赛季第 {race_round} 轮的同步计划"
            )
        
        return {
            "message": f"已取消 {season_year} 赛季第 {race_round} 轮的同步计划",
            "season_year": season_year,
            "race_round": race_round
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"取消赛后同步计划失败: {e}")
        raise HTTPException(status_code=500, detail=f"取消同步计划失败: {str(e)}")


@router.post("/{season_year}/{race_round}/execute/{attempt_number}")
async def execute_sync_immediately(
    season_year: int,
    race_round: int,
    attempt_number: int,
    background_tasks: BackgroundTasks = BackgroundTasks(),
    db: Session = Depends(get_db)
):
    """
    立即执行指定的同步尝试
    """
    try:
        # 验证同步计划存在
        sync_service = PostRaceSyncService(db, cache_dir="./cache")
        schedule = sync_service.get_schedule(season_year, race_round)
        
        if not schedule:
            raise HTTPException(
                status_code=404, 
                detail=f"未找到 {season_year} 赛季第 {race_round} 轮的同步计划"
            )
        
        # 验证尝试存在
        attempt = next(
            (a for a in schedule.attempts if a.attempt_number == attempt_number),
            None
        )
        if not attempt:
            raise HTTPException(
                status_code=404, 
                detail=f"未找到第 {attempt_number} 次尝试"
            )
        
        # 使用后台任务立即执行
        background_tasks.add_task(
            execute_post_race_sync.delay,
            season_year, 
            race_round, 
            attempt_number
        )
        
        return {
            "message": f"已开始立即执行第 {attempt_number} 次同步",
            "season_year": season_year,
            "race_round": race_round,
            "attempt_number": attempt_number,
            "race_name": schedule.race_name,
            "status": "executing"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"立即执行同步失败: {e}")
        raise HTTPException(status_code=500, detail=f"立即执行同步失败: {str(e)}")


@router.get("/schedules")
async def get_all_schedules(
    season_year: Optional[int] = None,
    status_filter: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    获取所有同步计划
    
    Args:
        season_year: 按赛季年份过滤
        status_filter: 按状态过滤 (pending/completed/failed)
    """
    try:
        sync_service = PostRaceSyncService(db, cache_dir="./cache")
        schedules = sync_service.get_all_schedules()
        
        # 应用过滤器
        if season_year:
            schedules = [s for s in schedules if s.season_year == season_year]
        
        if status_filter:
            if status_filter.lower() == "pending":
                schedules = [s for s in schedules if not s.is_completed and s.next_pending_attempt]
            elif status_filter.lower() == "completed":
                schedules = [s for s in schedules if s.is_completed]
            elif status_filter.lower() == "failed":
                schedules = [s for s in schedules if not s.is_completed and not s.next_pending_attempt]
        
        result_schedules = []
        for schedule in schedules:
            result_schedules.append({
                "season_year": schedule.season_year,
                "race_round": schedule.race_round,
                "race_name": schedule.race_name,
                "race_end_time": schedule.race_end_time.isoformat(),
                "created_at": schedule.created_at.isoformat(),
                "is_completed": schedule.is_completed,
                "success_rate": schedule.success_rate,
                "attempts_count": len(schedule.attempts),
                "next_pending_attempt": (
                    {
                        "attempt_number": schedule.next_pending_attempt.attempt_number,
                        "scheduled_time": schedule.next_pending_attempt.scheduled_time.isoformat()
                    } if schedule.next_pending_attempt else None
                )
            })
        
        return {
            "total_count": len(result_schedules),
            "schedules": result_schedules
        }
        
    except Exception as e:
        logger.error(f"获取所有同步计划失败: {e}")
        raise HTTPException(status_code=500, detail=f"获取同步计划失败: {str(e)}")


@router.get("/pending")
async def get_pending_syncs(db: Session = Depends(get_db)):
    """
    获取所有待执行的同步任务
    """
    try:
        sync_service = PostRaceSyncService(db, cache_dir="./cache")
        pending_syncs = sync_service.get_pending_syncs()
        
        result_syncs = []
        for season_year, race_round, attempt_number, scheduled_time in pending_syncs:
            result_syncs.append({
                "season_year": season_year,
                "race_round": race_round,
                "attempt_number": attempt_number,
                "scheduled_time": scheduled_time.isoformat()
            })
        
        return {
            "pending_count": len(result_syncs),
            "pending_syncs": result_syncs
        }
        
    except Exception as e:
        logger.error(f"获取待执行同步任务失败: {e}")
        raise HTTPException(status_code=500, detail=f"获取待执行任务失败: {str(e)}")


@router.post("/monitor")
async def trigger_monitor(
    background_tasks: BackgroundTasks = BackgroundTasks()
):
    """
    手动触发监控任务，检查并执行遗漏的同步任务
    """
    try:
        background_tasks.add_task(monitor_pending_syncs.delay)
        
        return {
            "message": "已触发监控任务",
            "status": "monitoring"
        }
        
    except Exception as e:
        logger.error(f"触发监控任务失败: {e}")
        raise HTTPException(status_code=500, detail=f"触发监控失败: {str(e)}")


@router.post("/cleanup")
async def trigger_cleanup(
    background_tasks: BackgroundTasks = BackgroundTasks()
):
    """
    手动触发清理任务，清理过期的同步计划
    """
    try:
        background_tasks.add_task(cleanup_expired_schedules.delay)
        
        return {
            "message": "已触发清理任务",
            "status": "cleaning"
        }
        
    except Exception as e:
        logger.error(f"触发清理任务失败: {e}")
        raise HTTPException(status_code=500, detail=f"触发清理失败: {str(e)}")


@router.post("/batch-schedule")
async def trigger_batch_schedule(
    season_year: int = 2025,
    days_ahead: int = 7,
    background_tasks: BackgroundTasks = BackgroundTasks()
):
    """
    批量安排即将到来的比赛的赛后同步计划
    
    Args:
        season_year: 赛季年份，默认2025
        days_ahead: 提前几天安排，默认7天
    """
    try:
        background_tasks.add_task(
            batch_schedule_upcoming_races.delay,
            season_year,
            days_ahead
        )
        
        return {
            "message": f"已开始批量安排 {season_year} 赛季未来 {days_ahead} 天内的比赛后同步计划",
            "season_year": season_year,
            "days_ahead": days_ahead,
            "status": "scheduling"
        }
        
    except Exception as e:
        logger.error(f"批量安排同步计划失败: {e}")
        raise HTTPException(status_code=500, detail=f"批量安排失败: {str(e)}")


@router.get("/stats")
async def get_sync_stats(
    season_year: Optional[int] = None,
    db: Session = Depends(get_db)
):
    """
    获取同步统计信息
    """
    try:
        sync_service = PostRaceSyncService(db, cache_dir="./cache")
        schedules = sync_service.get_all_schedules()
        
        # 应用季节过滤
        if season_year:
            schedules = [s for s in schedules if s.season_year == season_year]
        
        total_schedules = len(schedules)
        completed_schedules = sum(1 for s in schedules if s.is_completed)
        pending_schedules = sum(1 for s in schedules if not s.is_completed and s.next_pending_attempt)
        failed_schedules = sum(1 for s in schedules if not s.is_completed and not s.next_pending_attempt)
        
        # 计算总体成功率
        if schedules:
            avg_success_rate = sum(s.success_rate for s in schedules) / len(schedules)
        else:
            avg_success_rate = 0.0
        
        # 按数据类型统计成功率
        data_type_stats = {}
        for data_type in PostRaceSyncService.SYNC_DATA_TYPES:
            successes = 0
            total_attempts = 0
            
            for schedule in schedules:
                for attempt in schedule.attempts:
                    if attempt.results and data_type in attempt.results:
                        total_attempts += 1
                        if attempt.results[data_type]:
                            successes += 1
            
            data_type_stats[data_type] = {
                "success_rate": (successes / total_attempts) if total_attempts > 0 else 0.0,
                "total_attempts": total_attempts,
                "successes": successes
            }
        
        return {
            "total_schedules": total_schedules,
            "completed_schedules": completed_schedules,
            "pending_schedules": pending_schedules,
            "failed_schedules": failed_schedules,
            "overall_success_rate": avg_success_rate,
            "data_type_stats": data_type_stats,
            "season_year": season_year
        }
        
    except Exception as e:
        logger.error(f"获取同步统计信息失败: {e}")
        raise HTTPException(status_code=500, detail=f"获取统计信息失败: {str(e)}") 