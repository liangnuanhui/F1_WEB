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
from app.models.season import Season  # 导入 Season 模型
from app.schemas.standings import DriverStandingResponse, ConstructorStandingResponse, StandingHistoryResponse
from app.schemas.base import ApiResponse

router = APIRouter()


@router.get("/drivers", response_model=ApiResponse[List[DriverStandingResponse]])
def get_driver_standings(
    db: Session = Depends(get_db),
    season_id: Optional[int] = Query(None, description="赛季ID (优先)"),
    year: Optional[int] = Query(None, description="赛季年份"),
):
    """
    获取车手积分榜.
    可通过 season_id 或 year 查询.
    如果两者都未提供, 则返回当前活跃赛季的数据.
    """
    try:
        final_season_id = season_id
        if final_season_id is None:
            query_year = year
            if query_year is None:
                # 默认逻辑：按年份降序查找最新的赛季
                active_season = db.query(Season).order_by(Season.year.desc()).first()
                if not active_season:
                    raise HTTPException(status_code=404, detail="未找到任何赛季")
                final_season_id = active_season.id
            else:
                season = db.query(Season).filter(Season.year == query_year).first()
                if not season:
                    return ApiResponse(
                        success=True, message=f"未找到 {query_year} 赛季", data=[]
                    )
                final_season_id = season.id

        if final_season_id is None:
            raise HTTPException(
                status_code=400, detail="无法确定赛季，请提供 season_id 或 year"
            )

        standings = (
            db.query(DriverStanding)
            .options(
                joinedload(DriverStanding.driver),
                joinedload(DriverStanding.constructor),
            )
            .filter(DriverStanding.season_id == final_season_id)
            .order_by(DriverStanding.position.asc())
            .all()
        )

        result = [
            DriverStandingResponse(
                position=s.position,
                points=s.points,
                wins=s.wins,
                driver_id=s.driver.driver_id,
                driver_name=f"{s.driver.forename} {s.driver.surname}",
                nationality=s.driver.nationality,
                constructor_id=s.constructor.constructor_id,
                constructor_name=s.constructor.name,
            )
            for s in standings
            if s.driver and s.constructor
        ]

        return ApiResponse(success=True, message="获取车手积分榜成功", data=result)

    except HTTPException:
        raise
    except Exception as e:
        # For debugging purposes, you might want to log the error
        # import logging
        # logging.exception("Error fetching driver standings")
        raise HTTPException(
            status_code=500, detail=f"获取车手积分榜失败: An unexpected error occurred."
        )


@router.get("/constructors", response_model=ApiResponse[List[ConstructorStandingResponse]])
def get_constructor_standings(
    db: Session = Depends(get_db),
    season_id: Optional[int] = Query(None, description="赛季ID (优先)"),
    year: Optional[int] = Query(None, description="赛季年份"),
):
    """
    获取车队积分榜.
    可通过 season_id 或 year 查询.
    如果两者都未提供, 则返回当前活跃赛季的数据.
    """
    try:
        final_season_id = season_id
        if final_season_id is None:
            query_year = year
            if query_year is None:
                # 默认逻辑：按年份降序查找最新的赛季
                active_season = db.query(Season).order_by(Season.year.desc()).first()
                if not active_season:
                    raise HTTPException(status_code=404, detail="未找到任何赛季")
                final_season_id = active_season.id
            else:
                season = db.query(Season).filter(Season.year == query_year).first()
                if not season:
                    return ApiResponse(
                        success=True, message=f"未找到 {query_year} 赛季", data=[]
                    )
                final_season_id = season.id

        if final_season_id is None:
            raise HTTPException(
                status_code=400, detail="无法确定赛季，请提供 season_id 或 year"
            )

        standings = (
            db.query(ConstructorStanding)
            .options(joinedload(ConstructorStanding.constructor))
            .filter(ConstructorStanding.season_id == final_season_id)
            .order_by(ConstructorStanding.position.asc())
            .all()
        )

        result = [
            ConstructorStandingResponse(
                position=s.position,
                points=s.points,
                wins=s.wins,
                constructor_id=s.constructor.constructor_id,
                constructor_name=s.constructor.name,
                nationality=s.constructor.nationality,
            )
            for s in standings
            if s.constructor
        ]

        return ApiResponse(success=True, message="获取车队积分榜成功", data=result)

    except HTTPException:
        raise
    except Exception as e:
        # import logging
        # logging.exception("Error fetching constructor standings")
        raise HTTPException(
            status_code=500, detail=f"获取车队积分榜失败: An unexpected error occurred."
        )


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