"""
比赛数据调度器管理 API
"""

import logging
from typing import Dict, Any, List, Optional
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.tasks.scheduler import RaceScheduler, schedule_post_race_updates
from app.tasks.data_sync import sync_all_post_race_data_task
from app.models import Race, Season

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/schedules", response_model=Dict[str, Any])
async def get_race_schedules(db: Session = Depends(get_db)):
    """
    获取所有已调度的比赛数据更新任务
    """
    try:
        scheduler = RaceScheduler()
        scheduled_races = scheduler.get_scheduled_races()
        
        return {
            "message": "获取调度列表成功",
            "total": len(scheduled_races),
            "schedules": scheduled_races,
            "retrieved_at": datetime.utcnow().isoformat(),
        }
        
    except Exception as e:
        logger.error(f"获取调度列表时发生错误: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"获取调度列表失败: {str(e)}"
        )


@router.post("/schedule/season/{season_year}", response_model=Dict[str, Any])
async def schedule_season_updates(
    season_year: int,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """
    为指定赛季的所有比赛安排数据更新任务
    """
    try:
        # 验证赛季是否存在
        season = db.query(Season).filter(Season.year == season_year).first()
        if not season:
            raise HTTPException(
                status_code=404,
                detail=f"赛季 {season_year} 不存在"
            )
        
        # 在后台执行调度任务
        background_tasks.add_task(
            schedule_post_race_updates.delay,
            season_year
        )
        
        return {
            "message": f"已开始为 {season_year} 赛季安排数据更新任务",
            "season_year": season_year,
            "status": "background_task_started",
            "scheduled_at": datetime.utcnow().isoformat(),
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"安排赛季调度时发生错误: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"安排赛季调度失败: {str(e)}"
        )


@router.post("/schedule/race/{season_year}/{race_round}", response_model=Dict[str, Any])
async def schedule_race_update(
    season_year: int,
    race_round: int,
    db: Session = Depends(get_db)
):
    """
    为指定比赛安排数据更新任务
    """
    try:
        # 查找比赛
        race = db.query(Race).join(Season).filter(
            Season.year == season_year,
            Race.round_number == race_round
        ).first()
        
        if not race:
            raise HTTPException(
                status_code=404,
                detail=f"未找到 {season_year} 赛季第 {race_round} 轮比赛"
            )
        
        # 创建调度器并安排任务
        scheduler = RaceScheduler()
        success = scheduler.schedule_post_race_update(race)
        
        if success:
            return {
                "message": f"已安排 {season_year} 赛季第 {race_round} 轮比赛的数据更新任务",
                "season_year": season_year,
                "race_round": race_round,
                "race_name": race.official_event_name,
                "status": "scheduled",
                "scheduled_at": datetime.utcnow().isoformat(),
            }
        else:
            raise HTTPException(
                status_code=500,
                detail="安排比赛调度失败"
            )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"安排比赛调度时发生错误: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"安排比赛调度失败: {str(e)}"
        )


@router.delete("/schedule/race/{season_year}/{race_round}", response_model=Dict[str, Any])
async def cancel_race_schedule(
    season_year: int,
    race_round: int,
    db: Session = Depends(get_db)
):
    """
    取消指定比赛的数据更新任务
    """
    try:
        # 验证比赛是否存在
        race = db.query(Race).join(Season).filter(
            Season.year == season_year,
            Race.round_number == race_round
        ).first()
        
        if not race:
            raise HTTPException(
                status_code=404,
                detail=f"未找到 {season_year} 赛季第 {race_round} 轮比赛"
            )
        
        # 取消调度
        scheduler = RaceScheduler()
        success = scheduler.cancel_race_schedule(season_year, race_round)
        
        if success:
            return {
                "message": f"已取消 {season_year} 赛季第 {race_round} 轮比赛的调度",
                "season_year": season_year,
                "race_round": race_round,
                "race_name": race.official_event_name,
                "status": "cancelled",
                "cancelled_at": datetime.utcnow().isoformat(),
            }
        else:
            return {
                "message": f"{season_year} 赛季第 {race_round} 轮比赛未找到调度记录",
                "season_year": season_year,
                "race_round": race_round,
                "status": "not_found",
            }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"取消比赛调度时发生错误: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"取消比赛调度失败: {str(e)}"
        )


@router.post("/sync/immediate/{season_year}/{race_round}", response_model=Dict[str, Any])
async def sync_race_data_immediate(
    season_year: int,
    race_round: int,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """
    立即同步指定比赛的数据（不等待调度时间）
    """
    try:
        # 验证比赛是否存在
        race = db.query(Race).join(Season).filter(
            Season.year == season_year,
            Race.round_number == race_round
        ).first()
        
        if not race:
            raise HTTPException(
                status_code=404,
                detail=f"未找到 {season_year} 赛季第 {race_round} 轮比赛"
            )
        
        # 在后台立即执行数据同步
        background_tasks.add_task(
            sync_all_post_race_data_task.delay,
            season_year,
            race_round
        )
        
        return {
            "message": f"已开始立即同步 {season_year} 赛季第 {race_round} 轮比赛数据",
            "season_year": season_year,
            "race_round": race_round,
            "race_name": race.official_event_name,
            "status": "immediate_sync_started",
            "started_at": datetime.utcnow().isoformat(),
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"立即同步比赛数据时发生错误: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"立即同步比赛数据失败: {str(e)}"
        )


@router.get("/status", response_model=Dict[str, Any])
async def get_scheduler_status():
    """
    获取调度器系统状态
    """
    try:
        from app.tasks.celery_app import celery_app
        from app.core.redis import get_redis_client
        
        # 检查 Celery 状态
        inspector = celery_app.control.inspect()
        active_tasks = inspector.active()
        scheduled_tasks = inspector.scheduled()
        
        # 检查 Redis 状态
        redis_client = get_redis_client()
        redis_info = redis_client.info()
        
        # 统计调度信息
        scheduler = RaceScheduler()
        scheduled_races = scheduler.get_scheduled_races()
        
        return {
            "scheduler_status": "running",
            "celery": {
                "active_tasks": len(active_tasks) if active_tasks else 0,
                "scheduled_tasks": len(scheduled_tasks) if scheduled_tasks else 0,
                "workers": list(active_tasks.keys()) if active_tasks else [],
            },
            "redis": {
                "connected_clients": redis_info.get("connected_clients", 0),
                "used_memory_human": redis_info.get("used_memory_human", "N/A"),
                "uptime_in_seconds": redis_info.get("uptime_in_seconds", 0),
            },
            "scheduled_races": {
                "total": len(scheduled_races),
                "races": scheduled_races[:5],  # 只返回前5个
            },
            "checked_at": datetime.utcnow().isoformat(),
        }
        
    except Exception as e:
        logger.error(f"获取调度器状态时发生错误: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"获取调度器状态失败: {str(e)}"
        )


@router.post("/post-race-updates/{race_id}")
async def schedule_post_race_updates(
    race_id: str,
    race_end_time: str,
    season_year: int = 2025,
    db: Session = Depends(get_db)
):
    """
    为比赛结束后安排数据更新
    
    Args:
        race_id: 比赛ID (例如: "2025_round_10")
        race_end_time: 比赛结束时间 (ISO格式, UTC)
        season_year: 赛季年份
    """
    try:
        # 解析时间
        race_end_datetime = datetime.fromisoformat(race_end_time.replace('Z', '+00:00'))
        
        scheduler = RaceScheduler(db)
        result = scheduler.schedule_post_race_updates(race_id, race_end_datetime, season_year)
        
        if result["success"]:
            return {
                "success": True,
                "message": "比赛后数据更新已安排",
                "data": result
            }
        else:
            raise HTTPException(status_code=400, detail=result["error"])
            
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"时间格式错误: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"安排失败: {e}")


@router.get("/post-race-updates/{race_id}")
async def get_post_race_schedule(race_id: str, db: Session = Depends(get_db)):
    """获取比赛后更新调度信息"""
    try:
        scheduler = RaceScheduler(db)
        result = scheduler.get_post_race_schedule(race_id)
        
        if result["success"]:
            return {
                "success": True,
                "data": result["data"]
            }
        else:
            raise HTTPException(status_code=404, detail=result["error"])
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取失败: {e}")


@router.delete("/post-race-updates/{race_id}")
async def cancel_post_race_schedule(race_id: str, db: Session = Depends(get_db)):
    """取消比赛后更新调度"""
    try:
        scheduler = RaceScheduler(db)
        result = scheduler.cancel_post_race_schedule(race_id)
        
        if result["success"]:
            return {
                "success": True,
                "message": result["message"],
                "data": {
                    "race_id": result["race_id"],
                    "cancelled_tasks": result["cancelled_tasks"]
                }
            }
        else:
            raise HTTPException(status_code=400, detail=result["error"])
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"取消失败: {e}")


@router.post("/manual-post-race-sync")
async def manual_post_race_sync(
    season_year: int = 2025,
    race_round: int = None,
    db: Session = Depends(get_db)
):
    """
    手动触发比赛后数据同步
    用于测试或紧急情况下的数据更新
    """
    try:
        from ...tasks.data_sync import sync_post_race_data
        
        # 异步执行同步任务
        task_result = sync_post_race_data.delay(season_year, race_round)
        
        return {
            "success": True,
            "message": "比赛后数据同步任务已启动",
            "task_id": task_result.id,
            "season_year": season_year,
            "race_round": race_round
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"同步启动失败: {e}") 