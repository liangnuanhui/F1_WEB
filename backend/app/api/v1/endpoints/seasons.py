"""
赛季相关的API端点
"""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.models.season import Season
from app.schemas.season import SeasonResponse
from app.schemas.base import ApiResponse

router = APIRouter()


@router.get("/", response_model=ApiResponse[List[SeasonResponse]])
def get_seasons(
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0, description="跳过的记录数"),
    limit: int = Query(100, ge=1, le=1000, description="返回的记录数"),
    year: Optional[int] = Query(None, ge=1950, le=2030, description="按年份筛选")
):
    """获取赛季列表"""
    try:
        query = db.query(Season)
        
        if year is not None:
            query = query.filter(Season.year == year)
        
        seasons = query.order_by(Season.year.desc()).offset(skip).limit(limit).all()
        
        # 手动构造返回数据
        season_list = []
        for season in seasons:
            season_data = {
                "id": season.id,
                "year": season.year,
                "name": season.name,
                "description": season.description,
                "start_date": season.start_date,
                "end_date": season.end_date,
            }
            season_list.append(season_data)
        
        return ApiResponse(
            success=True,
            message="获取赛季列表成功",
            data=season_list
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取赛季列表失败: {str(e)}")


@router.get("/active", response_model=ApiResponse[SeasonResponse])
def get_active_season(db: Session = Depends(get_db)):
    """获取当前活跃赛季"""
    try:
        # 获取最新的赛季作为当前活跃赛季
        current_season = db.query(Season).order_by(Season.year.desc()).first()
        
        if not current_season:
            raise HTTPException(status_code=404, detail="未找到当前活跃赛季")
        
        season_data = {
            "id": current_season.id,
            "year": current_season.year,
            "name": current_season.name,
            "description": current_season.description,
            "start_date": current_season.start_date,
            "end_date": current_season.end_date,
        }
        
        return ApiResponse(
            success=True,
            message="获取当前活跃赛季成功",
            data=season_data
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取当前活跃赛季失败: {str(e)}")


@router.get("/year/{year}", response_model=ApiResponse[SeasonResponse])
def get_season_by_year(year: int, db: Session = Depends(get_db)):
    """按年份获取赛季"""
    try:
        season = db.query(Season).filter(Season.year == year).first()
        
        if not season:
            raise HTTPException(status_code=404, detail=f"未找到{year}赛季")
        
        season_data = {
            "id": season.id,
            "year": season.year,
            "name": season.name,
            "description": season.description,
            "start_date": season.start_date,
            "end_date": season.end_date,
        }
        
        return ApiResponse(
            success=True,
            message=f"获取{year}赛季成功",
            data=season_data
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取赛季失败: {str(e)}")


@router.get("/{season_id}", response_model=ApiResponse[SeasonResponse])
def get_season(season_id: int, db: Session = Depends(get_db)):
    """按ID获取赛季"""
    try:
        season = db.query(Season).filter(Season.id == season_id).first()
        
        if not season:
            raise HTTPException(status_code=404, detail=f"未找到ID为{season_id}的赛季")
        
        season_data = {
            "id": season.id,
            "year": season.year,
            "name": season.name,
            "description": season.description,
            "start_date": season.start_date,
            "end_date": season.end_date,
        }
        
        return ApiResponse(
            success=True,
            message="获取赛季成功",
            data=season_data
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取赛季失败: {str(e)}") 