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
from app.models.result import Result
from app.models.driver import Driver

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
            # 包含完整的circuit对象
            "circuit": {
                "circuit_id": race.circuit.circuit_id,
                "circuit_url": race.circuit.circuit_url,
                "circuit_name": race.circuit.circuit_name,
                "lat": race.circuit.lat,
                "long": race.circuit.long,
                "locality": race.circuit.locality,
                "country": race.circuit.country,
                "length": race.circuit.length,
                "corners": race.circuit.corners,
                "lap_record": race.circuit.lap_record,
                "lap_record_driver": race.circuit.lap_record_driver,
                "lap_record_year": race.circuit.lap_record_year,
                "first_grand_prix": race.circuit.first_grand_prix,
                "typical_lap_count": race.circuit.typical_lap_count,
                "race_distance": race.circuit.race_distance,
                "circuit_layout_image_url": race.circuit.circuit_layout_image_url,
                "circuit_layout_image_path": race.circuit.circuit_layout_image_path,
                "description": race.circuit.description,
                "characteristics": race.circuit.characteristics,
                "is_active": race.circuit.is_active,
            } if race.circuit else None,
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


@router.get("/{race_id}/podium", response_model=ApiResponse[list])
def get_race_podium(race_id: int, db: Session = Depends(get_db)):
    """
    获取指定比赛的前三名结果
    """
    try:
        # 查询前三名结果
        podium_results = (
            db.query(Result, Driver)
            .join(Driver, Result.driver_id == Driver.driver_id)
            .filter(Result.race_id == race_id, Result.position.in_([1, 2, 3]))
            .order_by(Result.position.asc())
            .all()
        )
        podium_list = []
        base_time = None
        for result, driver in podium_results:
            # 计算展示用成绩
            if result.position == 1:
                # 第一名显示总用时
                if result.total_race_time:
                    # 只取时:分:秒.毫秒
                    t = str(result.total_race_time)
                    if t.startswith("0 days "):
                        t = t[7:]
                    result_time = t.split(".")[0]
                else:
                    result_time = "-"
                base_time = result.total_race_time_millis
            else:
                # 其他名次显示与第一名的差值
                if base_time and result.total_race_time_millis:
                    diff = int(result.total_race_time_millis) - int(base_time)
                    sec = diff // 1000
                    ms = diff % 1000
                    result_time = f"+{sec // 60}:{sec % 60:02d}.{ms:03d}"
                else:
                    result_time = "-"
            podium_list.append({
                "position": result.position,
                "driver_id": driver.driver_id,
                "driver_code": driver.code or "",
                "driver_name": f"{driver.forename} {driver.surname}",
                "result_time": result_time
            })
        return ApiResponse(success=True, message="获取比赛前三名成功", data=podium_list)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取比赛前三名失败: {str(e)}") 