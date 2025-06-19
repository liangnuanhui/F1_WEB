"""
车队相关的 Pydantic 模式
"""
from typing import Optional, List
from pydantic import BaseModel, Field

from .base import BaseModelSchema


class ConstructorBase(BaseModel):
    """车队基础模式"""
    
    constructor_id: str = Field(..., min_length=1, max_length=50, description="车队ID")
    name: str = Field(..., min_length=1, max_length=200, description="车队名称")
    nationality: str = Field(..., min_length=1, max_length=100, description="国籍")
    season_id: int = Field(..., ge=1, description="赛季ID")
    base: Optional[str] = Field(default=None, max_length=200, description="车队基地")
    team_chief: Optional[str] = Field(default=None, max_length=100, description="车队领队")
    technical_chief: Optional[str] = Field(default=None, max_length=100, description="技术总监")
    power_unit: Optional[str] = Field(default=None, max_length=100, description="动力单元")
    championships: int = Field(default=0, ge=0, description="车队冠军次数")
    wins: int = Field(default=0, ge=0, description="获胜次数")
    podiums: int = Field(default=0, ge=0, description="领奖台次数")
    poles: int = Field(default=0, ge=0, description="杆位次数")
    fastest_laps: int = Field(default=0, ge=0, description="最快圈速次数")


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
    championships: Optional[int] = Field(default=None, ge=0, description="车队冠军次数")
    wins: Optional[int] = Field(default=None, ge=0, description="获胜次数")
    podiums: Optional[int] = Field(default=None, ge=0, description="领奖台次数")
    poles: Optional[int] = Field(default=None, ge=0, description="杆位次数")
    fastest_laps: Optional[int] = Field(default=None, ge=0, description="最快圈速次数")


class ConstructorResponse(ConstructorBase, BaseModelSchema):
    """车队响应模式"""
    
    # 关联数据
    season_year: Optional[int] = Field(default=None, description="赛季年份")
    drivers: Optional[List[str]] = Field(default=None, description="车手列表")


class ConstructorListResponse(BaseModel):
    """车队列表响应模式"""
    
    constructors: List[ConstructorResponse] = Field(description="车队列表")
    total: int = Field(description="总数")


class ConstructorStandingResponse(BaseModel):
    """车队积分榜响应模式"""
    
    position: int = Field(description="排名")
    constructor: ConstructorResponse = Field(description="车队信息")
    points: float = Field(description="积分")
    wins: int = Field(description="获胜次数")
    podiums: int = Field(description="领奖台次数") 