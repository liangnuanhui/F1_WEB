"""
比赛相关的 Pydantic 模式
"""
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field

from .base import BaseModelSchema


class RaceBase(BaseModel):
    """比赛基础模式"""
    
    race_id: str = Field(..., min_length=1, max_length=50, description="比赛ID")
    name: str = Field(..., min_length=1, max_length=200, description="比赛名称")
    round_number: int = Field(..., ge=1, description="比赛轮次")
    season_id: int = Field(..., ge=1, description="赛季ID")
    circuit_id: int = Field(..., ge=1, description="赛道ID")
    race_date: datetime = Field(..., description="比赛日期")
    qualifying_date: Optional[datetime] = Field(default=None, description="排位赛日期")
    sprint_date: Optional[datetime] = Field(default=None, description="冲刺赛日期")
    status: str = Field(default="scheduled", description="比赛状态")
    is_sprint_weekend: bool = Field(default=False, description="是否为冲刺赛周末")
    description: Optional[str] = Field(default=None, description="比赛描述")
    weather: Optional[str] = Field(default=None, max_length=100, description="天气")
    temperature: Optional[int] = Field(default=None, ge=-50, le=100, description="温度(摄氏度)")


class RaceCreate(RaceBase):
    """创建比赛模式"""
    pass


class RaceUpdate(BaseModel):
    """更新比赛模式"""
    
    name: Optional[str] = Field(default=None, min_length=1, max_length=200, description="比赛名称")
    round_number: Optional[int] = Field(default=None, ge=1, description="比赛轮次")
    race_date: Optional[datetime] = Field(default=None, description="比赛日期")
    qualifying_date: Optional[datetime] = Field(default=None, description="排位赛日期")
    sprint_date: Optional[datetime] = Field(default=None, description="冲刺赛日期")
    status: Optional[str] = Field(default=None, description="比赛状态")
    is_sprint_weekend: Optional[bool] = Field(default=None, description="是否为冲刺赛周末")
    description: Optional[str] = Field(default=None, description="比赛描述")
    weather: Optional[str] = Field(default=None, max_length=100, description="天气")
    temperature: Optional[int] = Field(default=None, ge=-50, le=100, description="温度(摄氏度)")


class RaceResponse(RaceBase, BaseModelSchema):
    """比赛响应模式"""
    
    # 关联数据
    season_name: Optional[str] = Field(default=None, description="赛季名称")
    circuit_name: Optional[str] = Field(default=None, description="赛道名称")
    circuit_country: Optional[str] = Field(default=None, description="赛道国家")


class RaceListResponse(BaseModel):
    """比赛列表响应模式"""
    
    races: List[RaceResponse] = Field(description="比赛列表")
    total: int = Field(description="总数")
    next_race: Optional[RaceResponse] = Field(default=None, description="下一场比赛") 