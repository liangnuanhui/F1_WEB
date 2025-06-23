"""
车队相关 API 端点
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.models.constructor import Constructor
from app.schemas.constructor import ConstructorResponse
from app.schemas.base import ApiResponse

router = APIRouter()


@router.get("/", response_model=ApiResponse[List[ConstructorResponse]])
def get_constructors(
    db: Session = Depends(get_db),
    page: int = Query(1, ge=1, description="页码"),
    size: int = Query(20, ge=1, le=100, description="每页数量"),
):
    """
    获取所有车队
    """
    try:
        offset = (page - 1) * size
        constructors = db.query(Constructor).offset(offset).limit(size).all()
        constructor_list = []
        for constructor in constructors:
            constructor_data = {
                "constructor_id": constructor.constructor_id,
                "constructor_url": constructor.constructor_url,
                "name": constructor.name,
                "nationality": constructor.nationality,
                "season_id": constructor.season_id,
                "base": constructor.base,
                "team_chief": constructor.team_chief,
                "technical_chief": constructor.technical_chief,
                "power_unit": constructor.power_unit,
                "is_active": constructor.is_active,
                "championships": constructor.championships,
                "wins": constructor.wins,
                "podiums": constructor.podiums,
                "poles": constructor.poles,
                "fastest_laps": constructor.fastest_laps,
            }
            constructor_list.append(constructor_data)
        return ApiResponse(
            success=True,
            message="获取车队列表成功",
            data=constructor_list
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取车队列表失败: {str(e)}")


@router.get("/{constructor_id}", response_model=ApiResponse[ConstructorResponse])
def get_constructor(constructor_id: str, db: Session = Depends(get_db)):
    """
    获取单个车队详情
    """
    try:
        constructor = db.query(Constructor).filter(Constructor.constructor_id == constructor_id).first()
        if not constructor:
            raise HTTPException(status_code=404, detail="车队不存在")
        constructor_data = {
            "constructor_id": constructor.constructor_id,
            "constructor_url": constructor.constructor_url,
            "name": constructor.name,
            "nationality": constructor.nationality,
            "season_id": constructor.season_id,
            "base": constructor.base,
            "team_chief": constructor.team_chief,
            "technical_chief": constructor.technical_chief,
            "power_unit": constructor.power_unit,
            "is_active": constructor.is_active,
            "championships": constructor.championships,
            "wins": constructor.wins,
            "podiums": constructor.podiums,
            "poles": constructor.poles,
            "fastest_laps": constructor.fastest_laps,
        }
        return ApiResponse(
            success=True,
            message="获取车队详情成功",
            data=constructor_data
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取车队详情失败: {str(e)}")


@router.get("/search", response_model=ApiResponse[List[ConstructorResponse]])
def search_constructors(
    q: str = Query(..., description="搜索关键词"),
    db: Session = Depends(get_db)
):
    """搜索车队"""
    try:
        # 简单的名称搜索
        constructors = db.query(Constructor).filter(
            Constructor.name.ilike(f"%{q}%")
        ).limit(10).all()
        
        constructor_list = []
        for constructor in constructors:
            constructor_data = {
                "constructor_id": constructor.constructor_id,
                "constructor_url": constructor.constructor_url,
                "name": constructor.name,
                "nationality": constructor.nationality,
                "season_id": constructor.season_id,
                "base": constructor.base,
                "team_chief": constructor.team_chief,
                "technical_chief": constructor.technical_chief,
                "power_unit": constructor.power_unit,
                "is_active": constructor.is_active,
                "championships": constructor.championships,
                "wins": constructor.wins,
                "podiums": constructor.podiums,
                "poles": constructor.poles,
                "fastest_laps": constructor.fastest_laps,
            }
            constructor_list.append(constructor_data)
        
        return ApiResponse(
            success=True,
            message="搜索车队成功",
            data=constructor_list
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"搜索车队失败: {str(e)}") 