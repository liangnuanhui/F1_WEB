"""
积分榜相关 API 端点
"""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import desc

from app.api.deps import get_db
from app.models.standings import DriverStanding, ConstructorStanding
from app.models.driver import Driver
from app.models.constructor import Constructor
from app.schemas.standings import DriverStandingResponse, ConstructorStandingResponse, StandingHistoryResponse
from app.schemas.base import ApiResponse

router = APIRouter()


@router.get("/drivers", response_model=ApiResponse[List[DriverStandingResponse]])
def get_driver_standings(
    db: Session = Depends(get_db),
    season_id: int = Query(..., description="赛季ID"),
):
    """
    获取车手积分榜
    """
    try:
        standings = db.query(DriverStanding)\
            .options(joinedload(DriverStanding.constructor))\
            .filter(DriverStanding.season_id == season_id)\
            .order_by(DriverStanding.position.asc())\
            .all()
        result = []
        for s in standings:
            # 保险做法：直接查 driver 表，确保 driver_name 一定有值
            driver = db.query(Driver).filter(Driver.driver_id == s.driver_id).first()
            result.append({
                "position": s.position,
                "points": s.points,
                "wins": s.wins,
                "driver_id": s.driver_id,
                "driver_name": f"{driver.forename} {driver.surname}" if driver else "",
                "nationality": driver.nationality if driver else "",
                "constructor_id": s.constructor_id,
                "constructor_name": s.constructor.name if s.constructor else "",
            })
        return ApiResponse(success=True, message="获取车手积分榜成功", data=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取车手积分榜失败: {str(e)}")


@router.get("/constructors", response_model=ApiResponse[List[ConstructorStandingResponse]])
def get_constructor_standings(
    db: Session = Depends(get_db),
    season_id: int = Query(..., description="赛季ID"),
):
    """
    获取车队积分榜
    """
    try:
        standings = db.query(ConstructorStanding).filter(ConstructorStanding.season_id == season_id).order_by(ConstructorStanding.position.asc()).all()
        result = []
        for s in standings:
            result.append({
                "position": s.position,
                "points": s.points,
                "wins": s.wins,
                "constructor_id": s.constructor_id,
                "constructor_name": s.constructor.name if s.constructor else "",
                "nationality": s.constructor.nationality if s.constructor else "",
            })
        return ApiResponse(success=True, message="获取车队积分榜成功", data=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取车队积分榜失败: {str(e)}")


@router.get("/drivers/{driver_id}/history")
def get_driver_standing_history(
    driver_id: str,
    season: Optional[int] = Query(None, description="赛季年份（可选）"),
    limit: int = Query(20, ge=1, le=100, description="返回记录数量限制"),
    offset: int = Query(0, ge=0, description="偏移量"),
    db: Session = Depends(get_db)
):
    """
    获取指定车手的积分榜历史
    
    Args:
        driver_id: 车手ID
        season: 赛季年份（可选）
        limit: 返回记录数量限制
        offset: 偏移量
    
    Returns:
        车手积分榜历史
    """
    try:
        # 验证车手是否存在
        driver = db.query(Driver).filter(Driver.driver_id == driver_id).first()
        if not driver:
            raise HTTPException(status_code=404, detail="车手不存在")
        
        # 构建查询
        query = db.query(DriverStanding).filter(DriverStanding.driver_id == driver_id)
        
        if season:
            query = query.filter(DriverStanding.season_id == season)
        
        # 按赛季排序
        query = query.order_by(desc(DriverStanding.season_id))
        
        # 分页
        total = query.count()
        standings = query.offset(offset).limit(limit).all()
        
        # 转换为响应格式
        standings_data = []
        for standing in standings:
            constructor = db.query(Constructor).filter(Constructor.constructor_id == standing.constructor_id).first()
            
            standings_data.append(StandingHistoryResponse(
                id=standing.id,
                season_id=standing.season_id,
                position=standing.position,
                points=standing.points,
                wins=standing.wins,
                driver_id=standing.driver_id,
                constructor_id=standing.constructor_id,
                driver_name=f"{driver.forename} {driver.surname}",
                driver_code=driver.code or "",
                constructor_name=constructor.name if constructor else "Unknown"
            ))
        
        return {
            "driver": {
                "id": driver.driver_id,
                "name": f"{driver.forename} {driver.surname}",
                "code": driver.code,
                "nationality": driver.nationality
            },
            "standings": standings_data,
            "total": total,
            "limit": limit,
            "offset": offset
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取车手积分榜历史失败: {str(e)}")


@router.get("/constructors/{constructor_id}/history")
def get_constructor_standing_history(
    constructor_id: str,
    season: Optional[int] = Query(None, description="赛季年份（可选）"),
    limit: int = Query(20, ge=1, le=100, description="返回记录数量限制"),
    offset: int = Query(0, ge=0, description="偏移量"),
    db: Session = Depends(get_db)
):
    """
    获取指定车队的积分榜历史
    
    Args:
        constructor_id: 车队ID
        season: 赛季年份（可选）
        limit: 返回记录数量限制
        offset: 偏移量
    
    Returns:
        车队积分榜历史
    """
    try:
        # 验证车队是否存在
        constructor = db.query(Constructor).filter(Constructor.constructor_id == constructor_id).first()
        if not constructor:
            raise HTTPException(status_code=404, detail="车队不存在")
        
        # 构建查询
        query = db.query(ConstructorStanding).filter(ConstructorStanding.constructor_id == constructor_id)
        
        if season:
            query = query.filter(ConstructorStanding.season_id == season)
        
        # 按赛季排序
        query = query.order_by(desc(ConstructorStanding.season_id))
        
        # 分页
        total = query.count()
        standings = query.offset(offset).limit(limit).all()
        
        # 转换为响应格式
        standings_data = []
        for standing in standings:
            standings_data.append(StandingHistoryResponse(
                id=standing.id,
                season_id=standing.season_id,
                position=standing.position,
                points=standing.points,
                wins=standing.wins,
                driver_id="",  # 车队积分榜没有车手ID
                constructor_id=standing.constructor_id,
                driver_name="",  # 车队积分榜没有车手名称
                driver_code="",  # 车队积分榜没有车手代码
                constructor_name=constructor.name
            ))
        
        return {
            "constructor": {
                "id": constructor.constructor_id,
                "name": constructor.name,
                "nationality": constructor.nationality
            },
            "standings": standings_data,
            "total": total,
            "limit": limit,
            "offset": offset
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取车队积分榜历史失败: {str(e)}") 