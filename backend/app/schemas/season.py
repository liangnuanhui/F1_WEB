"""
赛季相关的 Pydantic 模式
"""
from datetime import date
from typing import Optional, List
from pydantic import BaseModel, Field

from .base import BaseModelSchema


class SeasonBase(BaseModel):
    """赛季基础模式"""
    
    year: int = Field(..., ge=1950, le=2030, description="赛季年份")
    name: str = Field(..., min_length=1, max_length=100, description="赛季名称")
    description: Optional[str] = Field(default=None, description="赛季描述")
    start_date: Optional[date] = Field(default=None, description="赛季开始日期")
    end_date: Optional[date] = Field(default=None, description="赛季结束日期")
    is_current: bool = Field(default=False, description="是否为当前赛季")
    total_races: int = Field(default=0, ge=0, description="总比赛数")
    completed_races: int = Field(default=0, ge=0, description="已完成比赛数")


class SeasonCreate(SeasonBase):
    """创建赛季模式"""
    pass


class SeasonUpdate(BaseModel):
    """更新赛季模式"""
    
    name: Optional[str] = Field(default=None, min_length=1, max_length=100, description="赛季名称")
    description: Optional[str] = Field(default=None, description="赛季描述")
    start_date: Optional[date] = Field(default=None, description="赛季开始日期")
    end_date: Optional[date] = Field(default=None, description="赛季结束日期")
    is_current: Optional[bool] = Field(default=None, description="是否为当前赛季")
    total_races: Optional[int] = Field(default=None, ge=0, description="总比赛数")
    completed_races: Optional[int] = Field(default=None, ge=0, description="已完成比赛数")


class SeasonResponse(SeasonBase, BaseModelSchema):
    """赛季响应模式"""
    pass


class SeasonListResponse(BaseModel):
    """赛季列表响应模式"""
    
    seasons: List[SeasonResponse] = Field(description="赛季列表")
    total: int = Field(description="总数")
    current_season: Optional[SeasonResponse] = Field(default=None, description="当前赛季") 