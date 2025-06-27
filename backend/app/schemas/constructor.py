"""
车队相关的 Pydantic 模式
"""
from typing import Optional, List
from pydantic import BaseModel, Field

from .base import BaseModelSchema


class ConstructorBase(BaseModel):
    """车队基础模式（与数据库字段完全一致）"""
    constructor_id: str = Field(..., description="车队ID")
    constructor_url: Optional[str] = Field(None, description="车队官网")
    name: str = Field(..., description="车队名称")
    nationality: Optional[str] = Field(None, description="国籍")
    season_id: int = Field(..., description="赛季ID")
    base: Optional[str] = Field(None, description="基地")
    team_chief: Optional[str] = Field(None, description="领队")
    technical_chief: Optional[str] = Field(None, description="技术总监")
    power_unit: Optional[str] = Field(None, description="动力单元")
    is_active: Optional[bool] = Field(None, description="是否活跃")
    championships: int = Field(..., description="冠军数")
    wins: int = Field(..., description="胜场数")
    podiums: int = Field(..., description="领奖台次数")
    poles: int = Field(..., description="杆位数")
    fastest_laps: int = Field(..., description="最快圈数")


class ConstructorCreate(ConstructorBase):
    """创建车队模式"""
    pass


class ConstructorUpdate(BaseModel):
    """更新车队模式"""
    name: Optional[str] = Field(default=None, min_length=1, max_length=200, description="车队名称")
    nationality: Optional[str] = Field(default=None, min_length=1, max_length=100, description="国籍")
    base: Optional[str] = Field(default=None, max_length=200, description="车队基地")
    team_chief: Optional[str] = Field(default=None, max_length=100, description="车队领队")
    technical_chief: Optional[str] = Field(default=None, max_length=100, description="技术总监")
    power_unit: Optional[str] = Field(default=None, max_length=100, description="动力单元")
    is_active: Optional[bool] = Field(default=None, description="是否活跃")
    championships: Optional[int] = Field(default=None, description="车队冠军次数")
    wins: Optional[int] = Field(default=None, description="获胜次数")
    podiums: Optional[int] = Field(default=None, description="领奖台次数")
    poles: Optional[int] = Field(default=None, description="杆位次数")
    fastest_laps: Optional[int] = Field(default=None, description="最快圈速次数")


class ConstructorResponse(ConstructorBase, BaseModelSchema):
    """车队响应模式（与数据库字段一致）"""
    pass


class ConstructorListResponse(BaseModel):
    """车队列表响应模式"""
    constructors: List[ConstructorResponse] = Field(description="车队列表")
    total: int = Field(description="总数")