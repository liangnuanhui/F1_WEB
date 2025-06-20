"""
数据初始化 API 端点
"""

import asyncio
import logging
from typing import Dict, Any

from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.services.fastf1_service import FastF1Service

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/init", response_model=Dict[str, Any])
async def initialize_data(
    start_year: int = 2020,
    end_year: int = 2024,
    background_tasks: BackgroundTasks = None,
    db: Session = Depends(get_db)
):
    """
    初始化数据库，从 FastF1 拉取数据
    
    Args:
        start_year: 开始年份
        end_year: 结束年份
        background_tasks: 后台任务
        db: 数据库会话
    """
    try:
        logger.info(f"开始初始化数据，年份范围: {start_year}-{end_year}")
        
        # 创建 FastF1 服务
        fastf1_service = FastF1Service(db)
        
        # 在后台执行数据初始化
        if background_tasks:
            background_tasks.add_task(
                fastf1_service.initialize_database, 
                start_year, 
                end_year
            )
            return {
                "message": "数据初始化任务已启动",
                "start_year": start_year,
                "end_year": end_year,
                "status": "background"
            }
        else:
            # 同步执行
            await fastf1_service.initialize_database(start_year, end_year)
            return {
                "message": "数据初始化完成",
                "start_year": start_year,
                "end_year": end_year,
                "status": "completed"
            }
            
    except Exception as e:
        logger.error(f"初始化数据时发生错误: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"初始化数据时发生错误: {str(e)}"
        )


@router.post("/update-current", response_model=Dict[str, Any])
async def update_current_season(
    background_tasks: BackgroundTasks = None,
    db: Session = Depends(get_db)
):
    """
    更新当前赛季数据
    """
    try:
        logger.info("开始更新当前赛季数据")
        
        # 创建 FastF1 服务
        fastf1_service = FastF1Service(db)
        
        # 在后台执行更新
        if background_tasks:
            background_tasks.add_task(fastf1_service.update_current_season)
            return {
                "message": "当前赛季数据更新任务已启动",
                "status": "background"
            }
        else:
            # 同步执行
            await fastf1_service.update_current_season()
            return {
                "message": "当前赛季数据更新完成",
                "status": "completed"
            }
            
    except Exception as e:
        logger.error(f"更新当前赛季数据时发生错误: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"更新当前赛季数据时发生错误: {str(e)}"
        )


@router.get("/season-summary/{year}", response_model=Dict[str, Any])
async def get_season_summary(
    year: int,
    db: Session = Depends(get_db)
):
    """
    获取指定赛季的摘要信息
    """
    try:
        logger.info(f"获取 {year} 赛季摘要信息")
        
        # 创建 FastF1 服务
        fastf1_service = FastF1Service(db)
        
        # 获取赛季摘要
        summary = await fastf1_service.get_season_summary(year)
        
        if not summary:
            raise HTTPException(
                status_code=404,
                detail=f"未找到 {year} 赛季的数据"
            )
        
        return summary
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"获取赛季摘要时发生错误: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"获取赛季摘要时发生错误: {str(e)}"
        )


@router.get("/statistics", response_model=Dict[str, Any])
async def get_database_statistics(db: Session = Depends(get_db)):
    """
    获取数据库统计信息
    """
    try:
        from app.models.season import Season
        from app.models.circuit import Circuit
        from app.models.race import Race
        from app.models.driver import Driver
        from app.models.constructor import Constructor
        from app.models.result import Result
        
        # 统计各表记录数
        statistics = {
            "seasons": db.query(Season).count(),
            "circuits": db.query(Circuit).count(),
            "races": db.query(Race).count(),
            "drivers": db.query(Driver).count(),
            "constructors": db.query(Constructor).count(),
            "results": db.query(Result).count(),
        }
        
        # 获取赛季列表
        seasons = db.query(Season).order_by(Season.year).all()
        statistics["season_list"] = [
            {"year": season.year, "name": season.name}
            for season in seasons
        ]
        
        # 获取最近的比赛
        recent_races = db.query(Race).order_by(Race.race_date.desc()).limit(5).all()
        statistics["recent_races"] = [
            {
                "id": race.id,
                "name": race.name,
                "date": race.race_date.strftime("%Y-%m-%d"),
                "circuit_id": race.circuit_id
            }
            for race in recent_races
        ]
        
        return statistics
        
    except Exception as e:
        logger.error(f"获取数据库统计信息时发生错误: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"获取数据库统计信息时发生错误: {str(e)}"
        ) 