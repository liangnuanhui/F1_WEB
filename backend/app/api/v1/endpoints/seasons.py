"""
赛季相关的 API 端点
"""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from ....api.deps import get_db
from ....models import Season
from ....schemas import (
    SeasonResponse,
    SeasonListResponse,
    SeasonCreate,
    SeasonUpdate,
    DataResponse,
    PaginationParams
)

router = APIRouter()


@router.get("/", response_model=DataResponse[List[SeasonResponse]])
async def get_seasons(
    db: Session = Depends(get_db),
    pagination: PaginationParams = Depends(),
    year: Optional[int] = Query(None, description="赛季年份"),
    is_current: Optional[bool] = Query(None, description="是否为当前赛季")
):
    """
    获取赛季列表
    """
    query = db.query(Season)
    
    # 应用过滤条件
    if year is not None:
        query = query.filter(Season.year == year)
    if is_current is not None:
        query = query.filter(Season.is_current == is_current)
    
    # 应用排序
    if pagination.sort_by:
        sort_column = getattr(Season, pagination.sort_by, Season.year)
        if pagination.sort_order == "desc":
            sort_column = sort_column.desc()
        query = query.order_by(sort_column)
    else:
        query = query.order_by(Season.year.desc())
    
    # 应用分页
    total = query.count()
    seasons = query.offset((pagination.page - 1) * pagination.size).limit(pagination.size).all()
    
    return DataResponse(
        data=[SeasonResponse.from_orm(season) for season in seasons],
        total=total,
        page=pagination.page,
        size=pagination.size
    )


@router.get("/current", response_model=SeasonResponse)
async def get_current_season(db: Session = Depends(get_db)):
    """
    获取当前赛季
    """
    season = db.query(Season).filter(Season.is_current == True).first()
    if not season:
        raise HTTPException(status_code=404, detail="未找到当前赛季")
    
    return SeasonResponse.from_orm(season)


@router.get("/{season_id}", response_model=SeasonResponse)
async def get_season(season_id: int, db: Session = Depends(get_db)):
    """
    根据ID获取赛季详情
    """
    season = db.query(Season).filter(Season.id == season_id).first()
    if not season:
        raise HTTPException(status_code=404, detail="赛季不存在")
    
    return SeasonResponse.from_orm(season)


@router.get("/year/{year}", response_model=SeasonResponse)
async def get_season_by_year(year: int, db: Session = Depends(get_db)):
    """
    根据年份获取赛季
    """
    season = db.query(Season).filter(Season.year == year).first()
    if not season:
        raise HTTPException(status_code=404, detail=f"{year}赛季不存在")
    
    return SeasonResponse.from_orm(season)


@router.post("/", response_model=SeasonResponse)
async def create_season(season: SeasonCreate, db: Session = Depends(get_db)):
    """
    创建新赛季
    """
    # 检查年份是否已存在
    existing_season = db.query(Season).filter(Season.year == season.year).first()
    if existing_season:
        raise HTTPException(status_code=400, detail=f"{season.year}赛季已存在")
    
    db_season = Season(**season.dict())
    db.add(db_season)
    db.commit()
    db.refresh(db_season)
    
    return SeasonResponse.from_orm(db_season)


@router.put("/{season_id}", response_model=SeasonResponse)
async def update_season(
    season_id: int,
    season_update: SeasonUpdate,
    db: Session = Depends(get_db)
):
    """
    更新赛季信息
    """
    db_season = db.query(Season).filter(Season.id == season_id).first()
    if not db_season:
        raise HTTPException(status_code=404, detail="赛季不存在")
    
    # 更新字段
    update_data = season_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_season, field, value)
    
    db.commit()
    db.refresh(db_season)
    
    return SeasonResponse.from_orm(db_season)


@router.delete("/{season_id}")
async def delete_season(season_id: int, db: Session = Depends(get_db)):
    """
    删除赛季
    """
    db_season = db.query(Season).filter(Season.id == season_id).first()
    if not db_season:
        raise HTTPException(status_code=404, detail="赛季不存在")
    
    db.delete(db_season)
    db.commit()
    
    return {"message": "赛季删除成功"} 