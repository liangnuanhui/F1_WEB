"""
比赛相关 API 端点
"""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session, joinedload
from datetime import datetime, date

from app.api.deps import get_db
from app.models.race import Race
from app.models.season import Season
from app.models.circuit import Circuit
from app.schemas.race import RaceResponse
from app.schemas.base import ApiResponse

router = APIRouter()


@router.get("/", response_model=ApiResponse[List[RaceResponse]])
async def get_races(
    season: Optional[int] = Query(None, description="赛季年份"),
    page: int = Query(1, ge=1, description="页码"),
    size: int = Query(20, ge=1, le=100, description="每页数量"),
    db: Session = Depends(get_db),
):
    """
    获取比赛列表
    """
    try:
        query = db.query(Race).options(
            joinedload(Race.season),
            joinedload(Race.circuit)
        )
        
        if season:
            query = query.join(Season).filter(Season.year == season)
        
        # 按日期排序
        query = query.order_by(Race.event_date.asc())
        
        # 分页
        races = query.offset((page - 1) * size).limit(size).all()
        
        # 转换数据，添加关联字段
        race_responses = []
        for race in races:
            race_dict = {
                "id": race.id,
                "season_id": race.season_id,
                "circuit_id": race.circuit_id,
                "round_number": race.round_number,
                "country": race.country,
                "location": race.location,
                "official_event_name": race.official_event_name,
                "event_date": race.event_date,
                "event_format": race.event_format,
                "is_sprint": race.is_sprint,
                "session1": race.session1,
                "session1_date": race.session1_date,
                "session2": race.session2,
                "session2_date": race.session2_date,
                "session3": race.session3,
                "session3_date": race.session3_date,
                "session4": race.session4,
                "session4_date": race.session4_date,
                "session5": race.session5,
                "session5_date": race.session5_date,
                "season_name": race.season.name if race.season else None,
                "circuit_name": race.circuit.circuit_name if race.circuit else None,
                "circuit_country": race.circuit.country if race.circuit else None,
            }
            race_responses.append(race_dict)
        
        return ApiResponse(
            success=True,
            message="获取比赛列表成功",
            data=race_responses
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取比赛列表失败: {str(e)}")


@router.get("/upcoming", response_model=ApiResponse[List[RaceResponse]])
async def get_upcoming_races(
    limit: int = Query(5, ge=1, le=20, description="返回数量"),
    db: Session = Depends(get_db),
):
    """
    获取即将到来的比赛
    """
    try:
        today = date.today()
        
        races = db.query(Race).options(
            joinedload(Race.season),
            joinedload(Race.circuit)
        ).filter(
            Race.event_date >= today
        ).order_by(
            Race.event_date.asc()
        ).limit(limit).all()
        
        # 转换数据
        race_responses = []
        for race in races:
            race_dict = {
                "id": race.id,
                "season_id": race.season_id,
                "circuit_id": race.circuit_id,
                "round_number": race.round_number,
                "country": race.country,
                "location": race.location,
                "official_event_name": race.official_event_name,
                "event_date": race.event_date,
                "event_format": race.event_format,
                "is_sprint": race.is_sprint,
                "session1": race.session1,
                "session1_date": race.session1_date,
                "session2": race.session2,
                "session2_date": race.session2_date,
                "session3": race.session3,
                "session3_date": race.session3_date,
                "session4": race.session4,
                "session4_date": race.session4_date,
                "session5": race.session5,
                "session5_date": race.session5_date,
                "season_name": race.season.name if race.season else None,
                "circuit_name": race.circuit.circuit_name if race.circuit else None,
                "circuit_country": race.circuit.country if race.circuit else None,
            }
            race_responses.append(race_dict)
        
        return ApiResponse(
            success=True,
            message="获取即将到来的比赛成功",
            data=race_responses
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取即将到来的比赛失败: {str(e)}")


@router.get("/{race_id}", response_model=ApiResponse[RaceResponse])
async def get_race(
    race_id: int,
    db: Session = Depends(get_db),
):
    """
    获取单个比赛详情
    """
    try:
        race = db.query(Race).options(
            joinedload(Race.season),
            joinedload(Race.circuit)
        ).filter(Race.id == race_id).first()
        
        if not race:
            raise HTTPException(status_code=404, detail="比赛不存在")
        
        race_dict = {
            "id": race.id,
            "season_id": race.season_id,
            "circuit_id": race.circuit_id,
            "round_number": race.round_number,
            "country": race.country,
            "location": race.location,
            "official_event_name": race.official_event_name,
            "event_date": race.event_date,
            "event_format": race.event_format,
            "is_sprint": race.is_sprint,
            "session1": race.session1,
            "session1_date": race.session1_date,
            "session2": race.session2,
            "session2_date": race.session2_date,
            "session3": race.session3,
            "session3_date": race.session3_date,
            "session4": race.session4,
            "session4_date": race.session4_date,
            "session5": race.session5,
            "session5_date": race.session5_date,
            "season_name": race.season.name if race.season else None,
            "circuit_name": race.circuit.circuit_name if race.circuit else None,
            "circuit_country": race.circuit.country if race.circuit else None,
        }
        
        return ApiResponse(
            success=True,
            message="获取比赛详情成功",
            data=race_dict
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取比赛详情失败: {str(e)}") 