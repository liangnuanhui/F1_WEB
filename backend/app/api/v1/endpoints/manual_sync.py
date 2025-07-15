"""
手动数据更新API端点
替代Celery定时任务的手动触发方案
"""
from fastapi import APIRouter, HTTPException, BackgroundTasks
from app.core.database import get_db
from app.services.unified_sync_service import UnifiedSyncService
from sqlalchemy.orm import Session
from fastapi import Depends
import asyncio
from typing import Dict, Any

router = APIRouter()

@router.post("/sync/all")
async def sync_all_data(
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """
    手动触发全量数据同步
    替代Celery定时任务
    """
    try:
        # 在后台任务中执行数据同步
        background_tasks.add_task(run_full_sync, db)
        return {
            "message": "数据同步已开始",
            "status": "started",
            "note": "同步将在后台进行，请稍后检查数据"
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"启动数据同步失败: {str(e)}"
        )

@router.post("/sync/season/{year}")
async def sync_season_data(
    year: int,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """
    手动触发特定年份数据同步
    """
    try:
        background_tasks.add_task(run_season_sync, year, db)
        return {
            "message": f"开始同步{year}年数据",
            "status": "started",
            "year": year
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"启动{year}年数据同步失败: {str(e)}"
        )

@router.post("/sync/standings")
async def sync_standings_data(
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """
    手动触发积分榜数据同步
    """
    try:
        background_tasks.add_task(run_standings_sync, db)
        return {
            "message": "积分榜数据同步已开始",
            "status": "started"
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"启动积分榜数据同步失败: {str(e)}"
        )

@router.get("/sync/status")
async def get_sync_status():
    """
    检查数据同步状态
    """
    return {
        "message": "手动数据同步API",
        "endpoints": {
            "sync_all": "POST /api/v1/manual/sync/all - 全量数据同步",
            "sync_season": "POST /api/v1/manual/sync/season/{year} - 特定年份同步",
            "sync_standings": "POST /api/v1/manual/sync/standings - 积分榜同步"
        },
        "note": "这些端点替代了Celery定时任务，需要手动触发数据更新"
    }

# 后台任务函数
async def run_full_sync(db: Session):
    """执行全量数据同步"""
    try:
        sync_service = UnifiedSyncService(db)
        
        # 同步基础数据
        await sync_service.sync_drivers()
        await sync_service.sync_constructors()
        await sync_service.sync_circuits()
        await sync_service.sync_races()
        
        # 同步积分榜
        await sync_service.sync_driver_standings()
        await sync_service.sync_constructor_standings()
        
        print("✅ 全量数据同步完成")
    except Exception as e:
        print(f"❌ 全量数据同步失败: {str(e)}")

async def run_season_sync(year: int, db: Session):
    """执行特定年份数据同步"""
    try:
        sync_service = UnifiedSyncService(db)
        await sync_service.sync_season_data(year)
        print(f"✅ {year}年数据同步完成")
    except Exception as e:
        print(f"❌ {year}年数据同步失败: {str(e)}")

async def run_standings_sync(db: Session):
    """执行积分榜数据同步"""
    try:
        sync_service = UnifiedSyncService(db)
        await sync_service.sync_driver_standings()
        await sync_service.sync_constructor_standings()
        print("✅ 积分榜数据同步完成")
    except Exception as e:
        print(f"❌ 积分榜数据同步失败: {str(e)}")