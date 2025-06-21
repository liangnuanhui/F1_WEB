"""
赛季相关的API端点
"""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.models.season import Season
from app.schemas.season import SeasonResponse, SeasonListResponse

router = APIRouter()


@router.get("/", response_model=SeasonListResponse)
def get_seasons(
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0, description="跳过的记录数"),
    limit: int = Query(100, ge=1, le=1000, description="返回的记录数"),
    year: Optional[int] = Query(None, ge=1950, le=2030, description="按年份筛选")
):
    """获取赛季列表"""
    query = db.query(Season)
    
    if year is not None:
        query = query.filter(Season.year == year)
    
    total = query.count()
    seasons = query.order_by(Season.year.desc()).offset(skip).limit(limit).all()
    
    current_season = db.query(Season).filter(Season.is_current == True).first()
    
    return SeasonListResponse(
        seasons=seasons,
        total=total,
        current_season=current_season
    )


@router.get("/current", response_model=SeasonResponse)
def get_current_season(db: Session = Depends(get_db)):
    """获取当前赛季"""
    current_season = db.query(Season).filter(Season.is_current == True).first()
    
    if not current_season:
        raise HTTPException(status_code=404, detail="未找到当前赛季")
    
    return current_season


@router.get("/year/{year}", response_model=SeasonResponse)
def get_season_by_year(year: int, db: Session = Depends(get_db)):
    """按年份获取赛季"""
    season = db.query(Season).filter(Season.year == year).first()
    
    if not season:
        raise HTTPException(status_code=404, detail=f"未找到{year}赛季")
    
    return season


@router.get("/{season_id}", response_model=SeasonResponse)
def get_season(season_id: int, db: Session = Depends(get_db)):
    """按ID获取赛季"""
    season = db.query(Season).filter(Season.id == season_id).first()
    
    if not season:
        raise HTTPException(status_code=404, detail=f"未找到ID为{season_id}的赛季")
    
    return season 