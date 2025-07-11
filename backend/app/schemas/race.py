"""
比赛相关的 Pydantic 模式
"""
from datetime import datetime, date
from typing import Optional, List
from pydantic import BaseModel, Field

from .base import BaseModelSchema
from .circuit import CircuitResponse


class RaceBase(BaseModel):
    """比赛基础模式"""
    
    id: int = Field(..., description="比赛ID")
    season_id: int = Field(..., description="赛季ID")
    circuit_id: str = Field(..., description="赛道ID")
    round_number: int = Field(..., description="轮次")
    country: Optional[str] = Field(None, description="国家")
    location: Optional[str] = Field(None, description="地点")
    official_event_name: str = Field(..., description="官方赛事名称")
    event_date: Optional[date] = Field(None, description="比赛日期")
    event_format: Optional[str] = Field(None, description="比赛格式")
    is_sprint: bool = Field(..., description="是否冲刺赛")
    
    # 会话信息
    session1: Optional[str] = Field(None, description="第一节名称")
    session1_date: Optional[datetime] = Field(None, description="第一节时间")
    session2: Optional[str] = Field(None, description="第二节名称")
    session2_date: Optional[datetime] = Field(None, description="第二节时间")
    session3: Optional[str] = Field(None, description="第三节名称")
    session3_date: Optional[datetime] = Field(None, description="第三节时间")
    session4: Optional[str] = Field(None, description="第四节名称")
    session4_date: Optional[datetime] = Field(None, description="第四节时间")
    session5: Optional[str] = Field(None, description="第五节名称")
    session5_date: Optional[datetime] = Field(None, description="第五节时间")
    season_name: Optional[str] = Field(None, description="赛季名称")
    circuit_name: Optional[str] = Field(None, description="赛道名称")
    circuit_country: Optional[str] = Field(None, description="赛道国家")


class RaceCreate(RaceBase):
    """创建比赛模式"""
    pass


class RaceUpdate(BaseModel):
    """更新比赛模式"""
    
    round_number: Optional[int] = Field(default=None, ge=1, description="比赛轮次")
    country: Optional[str] = Field(default=None, max_length=100, description="国家")
    location: Optional[str] = Field(default=None, max_length=100, description="地点")
    official_event_name: Optional[str] = Field(default=None, min_length=1, max_length=200, description="官方名称")
    event_date: Optional[date] = Field(default=None, description="比赛日期")
    event_format: Optional[str] = Field(default=None, max_length=50, description="比赛格式")
    is_sprint: Optional[bool] = Field(default=None, description="是否有冲刺赛")


class RaceResponse(RaceBase, BaseModelSchema):
    """比赛响应模式"""
    
    # 关联数据
    season_name: Optional[str] = Field(default=None, description="赛季名称")
    circuit_name: Optional[str] = Field(default=None, description="赛道名称")
    circuit_country: Optional[str] = Field(default=None, description="赛道国家")
    circuit: Optional[CircuitResponse] = Field(default=None, description="完整赛道信息")


class RaceListResponse(BaseModel):
    """比赛列表响应模式"""
    
    races: List[RaceResponse] = Field(description="比赛列表")
    total: int = Field(description="总数")
    next_race: Optional[RaceResponse] = Field(default=None, description="下一场比赛") 