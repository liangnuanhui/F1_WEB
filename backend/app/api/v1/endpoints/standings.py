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
from app.models.driver_season import DriverSeason # 导入 DriverSeason 模型
from app.schemas.standings import DriverStandingResponse, ConstructorStandingResponse, StandingHistoryResponse
from app.schemas.base import ApiResponse

router = APIRouter()

def _get_season_id(db: Session, season_id: Optional[int], year: Optional[int]) -> tuple[int, int]:
    """
    根据传入的 season_id 或 year 确定最终的赛季ID和年份.
    - 如果提供了 season_id, 直接使用.
    - 如果提供了 year, 查询对应的 season_id.
    - 如果都未提供, 获取最新的赛季.
    """
    if season_id:
        season = db.query(Season).filter(Season.id == season_id).first()
        if not season:
            raise HTTPException(status_code=404, detail=f"未找到 ID 为 {season_id} 的赛季")
        return season.id, season.year

    if year:
        season = db.query(Season).filter(Season.year == year).first()
        if not season:
            # 兼容前端：如果某年没有数据，返回空列表而不是404
            raise HTTPException(status_code=200, detail=f"未找到 {year} 赛季")
        return season.id, season.year

    # 默认获取最新赛季
    active_season = db.query(Season).order_by(Season.year.desc()).first()
    if not active_season:
        raise HTTPException(status_code=404, detail="未找到任何赛季")
    return active_season.id, active_season.year


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
        final_season_id, current_year = _get_season_id(db, season_id, year)

        # 1. 获取官方指定车队信息
        official_teams_query = (
            db.query(DriverSeason)
            .options(
                joinedload(DriverSeason.driver),
                joinedload(DriverSeason.constructor)
            )
            .filter(DriverSeason.season_id == final_season_id)
        )
        official_teams_list = official_teams_query.all()
        official_teams_map = {
            item.driver_id: item.constructor for item in official_teams_list
        }


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

        result = []
        for s in standings:
            if not s.driver:
                continue

            # 2. 检查是否有官方指定的车队，并进行覆盖
            final_constructor = official_teams_map.get(s.driver.driver_id, s.constructor)

            if not final_constructor:
                continue

            result.append(DriverStandingResponse(
                position=s.position,
                points=s.points,
                wins=s.wins,
                driver_id=s.driver.driver_id,
                driver_name=f"{s.driver.forename} {s.driver.surname}",
                nationality=s.driver.nationality,
                constructor_id=final_constructor.constructor_id,
                constructor_name=final_constructor.name,
            ))


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
        final_season_id, _ = _get_season_id(db, season_id, year)

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

    except HTTPException as e:
        # 特殊处理 _get_season_id 抛出的 200 "错误"
        if e.status_code == 200:
            return ApiResponse(success=True, message=e.detail, data=[])
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