"""
积分榜 API 端点
提供车手和车队积分榜数据
"""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import desc

from app.api.deps import get_db
from app.models import DriverStanding, ConstructorStanding, Driver, Constructor
from app.schemas.standings import (
    DriverStandingResponse, 
    ConstructorStandingResponse,
    DriverStandingList,
    ConstructorStandingList
)

router = APIRouter()


@router.get("/drivers", response_model=DriverStandingList)
def get_driver_standings(
    season: int = Query(..., description="赛季年份"),
    limit: int = Query(20, ge=1, le=100, description="返回记录数量限制"),
    offset: int = Query(0, ge=0, description="偏移量"),
    db: Session = Depends(get_db)
):
    """
    获取车手积分榜
    
    Args:
        season: 赛季年份
        limit: 返回记录数量限制
        offset: 偏移量
    
    Returns:
        车手积分榜列表
    """
    try:
        # 构建查询
        query = db.query(DriverStanding).filter(DriverStanding.season == season)
        
        # 按位置排序
        query = query.order_by(DriverStanding.position.asc())
        
        # 分页
        total = query.count()
        standings = query.offset(offset).limit(limit).all()
        
        # 转换为响应格式
        standings_data = []
        for standing in standings:
            # 获取关联的车手和车队信息
            driver = db.query(Driver).filter(Driver.id == standing.driver_id).first()
            constructor = db.query(Constructor).filter(Constructor.id == standing.constructor_id).first()
            
            standings_data.append(DriverStandingResponse(
                id=standing.id,
                season=standing.season,
                round_number=None,  # 不再有轮次信息
                position=standing.position,
                position_text=standing.position_text,
                points=standing.points,
                wins=standing.wins,
                driver_id=standing.driver_id,
                driver_name=driver.full_name if driver else "Unknown",
                driver_code=driver.code if driver else "",
                constructor_id=standing.constructor_id,
                constructor_name=constructor.name if constructor else "Unknown",
                created_at=standing.created_at,
                updated_at=standing.updated_at
            ))
        
        return DriverStandingList(
            items=standings_data,
            total=total,
            limit=limit,
            offset=offset,
            season=season,
            round_number=None  # 不再有轮次信息
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取车手积分榜失败: {str(e)}")


@router.get("/constructors", response_model=ConstructorStandingList)
def get_constructor_standings(
    season: int = Query(..., description="赛季年份"),
    limit: int = Query(20, ge=1, le=100, description="返回记录数量限制"),
    offset: int = Query(0, ge=0, description="偏移量"),
    db: Session = Depends(get_db)
):
    """
    获取车队积分榜
    
    Args:
        season: 赛季年份
        limit: 返回记录数量限制
        offset: 偏移量
    
    Returns:
        车队积分榜列表
    """
    try:
        # 构建查询
        query = db.query(ConstructorStanding).filter(ConstructorStanding.season == season)
        
        # 按位置排序
        query = query.order_by(ConstructorStanding.position.asc())
        
        # 分页
        total = query.count()
        standings = query.offset(offset).limit(limit).all()
        
        # 转换为响应格式
        standings_data = []
        for standing in standings:
            # 获取关联的车队信息
            constructor = db.query(Constructor).filter(Constructor.id == standing.constructor_id).first()
            
            standings_data.append(ConstructorStandingResponse(
                id=standing.id,
                season=standing.season,
                round_number=None,  # 不再有轮次信息
                position=standing.position,
                position_text=standing.position_text,
                points=standing.points,
                wins=standing.wins,
                constructor_id=standing.constructor_id,
                constructor_name=constructor.name if constructor else "Unknown",
                constructor_nationality=constructor.nationality if constructor else "",
                created_at=standing.created_at,
                updated_at=standing.updated_at
            ))
        
        return ConstructorStandingList(
            items=standings_data,
            total=total,
            limit=limit,
            offset=offset,
            season=season,
            round_number=None  # 不再有轮次信息
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取车队积分榜失败: {str(e)}")


@router.get("/drivers/{driver_id}")
def get_driver_standing_history(
    driver_id: int,
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
        driver = db.query(Driver).filter(Driver.id == driver_id).first()
        if not driver:
            raise HTTPException(status_code=404, detail="车手不存在")
        
        # 构建查询
        query = db.query(DriverStanding).filter(DriverStanding.driver_id == driver_id)
        
        if season:
            query = query.filter(DriverStanding.season == season)
        
        # 按赛季排序
        query = query.order_by(desc(DriverStanding.season))
        
        # 分页
        total = query.count()
        standings = query.offset(offset).limit(limit).all()
        
        # 转换为响应格式
        standings_data = []
        for standing in standings:
            constructor = db.query(Constructor).filter(Constructor.id == standing.constructor_id).first()
            
            standings_data.append(DriverStandingResponse(
                id=standing.id,
                season=standing.season,
                position=standing.position,
                position_text=standing.position_text,
                points=standing.points,
                wins=standing.wins,
                driver_id=standing.driver_id,
                driver_name=driver.full_name,
                driver_code=driver.code,
                constructor_id=standing.constructor_id,
                constructor_name=constructor.name if constructor else "Unknown",
                created_at=standing.created_at,
                updated_at=standing.updated_at
            ))
        
        return {
            "driver": {
                "id": driver.id,
                "name": driver.full_name,
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


@router.get("/constructors/{constructor_id}")
def get_constructor_standing_history(
    constructor_id: int,
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
        constructor = db.query(Constructor).filter(Constructor.id == constructor_id).first()
        if not constructor:
            raise HTTPException(status_code=404, detail="车队不存在")
        
        # 构建查询
        query = db.query(ConstructorStanding).filter(ConstructorStanding.constructor_id == constructor_id)
        
        if season:
            query = query.filter(ConstructorStanding.season == season)
        
        # 按赛季排序
        query = query.order_by(desc(ConstructorStanding.season))
        
        # 分页
        total = query.count()
        standings = query.offset(offset).limit(limit).all()
        
        # 转换为响应格式
        standings_data = []
        for standing in standings:
            standings_data.append(ConstructorStandingResponse(
                id=standing.id,
                season=standing.season,
                position=standing.position,
                position_text=standing.position_text,
                points=standing.points,
                wins=standing.wins,
                constructor_id=standing.constructor_id,
                constructor_name=constructor.name,
                constructor_nationality=constructor.nationality,
                created_at=standing.created_at,
                updated_at=standing.updated_at
            ))
        
        return {
            "constructor": {
                "id": constructor.id,
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