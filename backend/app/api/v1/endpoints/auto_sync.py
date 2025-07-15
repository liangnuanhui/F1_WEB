"""
自动同步管理 API 端点
提供完全自动化的比赛数据同步管理接口
"""

from typing import Dict, Any, Optional
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.tasks.auto_scheduler import AutoRaceScheduler, auto_schedule_all_races
from app.schemas.base import ApiResponse

router = APIRouter()


@router.post("/setup-season/{season_year}")
async def setup_season_auto_sync(
    season_year: int,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """
    一键设置整个赛季的完全自动化同步
    用户只需要运行一次这个API
    """
    try:
        # 异步执行安排任务
        task = auto_schedule_all_races.delay(season_year)
        
        return ApiResponse(
            success=True,
            message=f"已开始为 {season_year} 赛季设置完全自动化同步",
            data={
                "season_year": season_year,
                "task_id": task.id,
                "status": "设置中，请稍后检查状态",
                "auto_retry_hours": [6, 12, 24, 30, 36, 42, 48]
            }
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"设置自动同步失败: {str(e)}"
        )


@router.get("/status/{season_year}")
async def get_season_auto_sync_status(
    season_year: int,
    db: Session = Depends(get_db)
):
    """
    获取整个赛季的自动同步状态
    """
    try:
        scheduler = AutoRaceScheduler()
        
        # 获取赛季所有比赛的状态
        from app.models import Race, Season
        races = db.query(Race).join(Season).filter(
            Season.year == season_year
        ).all()
        
        total_races = len(races)
        scheduled_races = 0
        pending_tasks = 0
        completed_tasks = 0
        
        race_details = []
        
        for race in races:
            status = scheduler.get_auto_sync_status(season_year, race.round_number)
            
            if status["success"]:
                scheduled_races += 1
                schedule_data = status["data"]
                
                race_pending = 0
                race_completed = 0
                
                for task in schedule_data["scheduled_tasks"]:
                    if task["status"] == "scheduled":
                        race_pending += 1
                        pending_tasks += 1
                    elif task["status"] in ["executed", "completed"]:
                        race_completed += 1
                        completed_tasks += 1
                
                race_details.append({
                    "round": race.round_number,
                    "name": race.official_event_name,
                    "status": "scheduled",
                    "pending_tasks": race_pending,
                    "completed_tasks": race_completed
                })
            else:
                race_details.append({
                    "round": race.round_number,
                    "name": race.official_event_name,
                    "status": "not_scheduled"
                })
        
        return ApiResponse(
            success=True,
            message=f"{season_year} 赛季自动同步状态",
            data={
                "season_year": season_year,
                "total_races": total_races,
                "scheduled_races": scheduled_races,
                "pending_tasks": pending_tasks,
                "completed_tasks": completed_tasks,
                "race_details": race_details
            }
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"获取状态失败: {str(e)}"
        )


@router.get("/race-status/{season_year}/{race_round}")
async def get_race_auto_sync_status(
    season_year: int,
    race_round: int
):
    """
    获取单场比赛的自动同步状态
    """
    try:
        scheduler = AutoRaceScheduler()
        status = scheduler.get_auto_sync_status(season_year, race_round)
        
        if status["success"]:
            return ApiResponse(
                success=True,
                message=f"{season_year} 赛季第 {race_round} 轮自动同步状态",
                data=status["data"]
            )
        else:
            return ApiResponse(
                success=False,
                message=status["error"],
                data=None
            )
            
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"获取比赛状态失败: {str(e)}"
        )


@router.delete("/cancel/{season_year}/{race_round}")
async def cancel_race_auto_sync(
    season_year: int,
    race_round: int
):
    """
    取消单场比赛的自动同步
    """
    try:
        scheduler = AutoRaceScheduler()
        result = scheduler.cancel_auto_sync(season_year, race_round)
        
        if result["success"]:
            return ApiResponse(
                success=True,
                message=f"已取消 {season_year} 赛季第 {race_round} 轮的自动同步",
                data=result
            )
        else:
            return ApiResponse(
                success=False,
                message=result["error"],
                data=None
            )
            
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"取消自动同步失败: {str(e)}"
        )