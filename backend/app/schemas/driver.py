"""
车手相关的 Pydantic 模式
"""
from datetime import date
from typing import Optional, List
from pydantic import BaseModel, Field

from .base import BaseModelSchema


class DriverBase(BaseModel):
    """车手基础模式"""
    
    driver_id: str = Field(..., min_length=1, max_length=50, description="车手ID")
    code: Optional[str] = Field(default=None, max_length=10, description="车手代码")
    first_name: str = Field(..., min_length=1, max_length=100, description="名")
    last_name: str = Field(..., min_length=1, max_length=100, description="姓")
    full_name: str = Field(..., min_length=1, max_length=200, description="全名")
    date_of_birth: Optional[date] = Field(default=None, description="出生日期")
    nationality: str = Field(..., min_length=1, max_length=100, description="国籍")
    number: Optional[int] = Field(default=None, ge=1, le=99, description="车手号码")
    season_id: int = Field(..., ge=1, description="赛季ID")
    constructor_id: Optional[int] = Field(default=None, ge=1, description="车队ID")
    championships: int = Field(default=0, ge=0, description="世界冠军次数")
    wins: int = Field(default=0, ge=0, description="获胜次数")
    podiums: int = Field(default=0, ge=0, description="领奖台次数")
    poles: int = Field(default=0, ge=0, description="杆位次数")
    fastest_laps: int = Field(default=0, ge=0, description="最快圈速次数")


class DriverCreate(DriverBase):
    """创建车手模式"""
    pass


class DriverUpdate(BaseModel):
    """更新车手模式"""
    
    code: Optional[str] = Field(default=None, max_length=10, description="车手代码")
    first_name: Optional[str] = Field(default=None, min_length=1, max_length=100, description="名")
    last_name: Optional[str] = Field(default=None, min_length=1, max_length=100, description="姓")
    full_name: Optional[str] = Field(default=None, min_length=1, max_length=200, description="全名")
    date_of_birth: Optional[date] = Field(default=None, description="出生日期")
    nationality: Optional[str] = Field(default=None, min_length=1, max_length=100, description="国籍")
    number: Optional[int] = Field(default=None, ge=1, le=99, description="车手号码")
    constructor_id: Optional[int] = Field(default=None, ge=1, description="车队ID")
    championships: Optional[int] = Field(default=None, ge=0, description="世界冠军次数")
    wins: Optional[int] = Field(default=None, ge=0, description="获胜次数")
    podiums: Optional[int] = Field(default=None, ge=0, description="领奖台次数")
    poles: Optional[int] = Field(default=None, ge=0, description="杆位次数")
    fastest_laps: Optional[int] = Field(default=None, ge=0, description="最快圈速次数")


class DriverResponse(DriverBase, BaseModelSchema):
    """车手响应模式"""
    
    # 关联数据
    constructor_name: Optional[str] = Field(default=None, description="车队名称")
    season_year: Optional[int] = Field(default=None, description="赛季年份")


class DriverListResponse(BaseModel):
    """车手列表响应模式"""
    
    drivers: List[DriverResponse] = Field(description="车手列表")
    total: int = Field(description="总数")


class DriverStandingResponse(BaseModel):
    """车手积分榜响应模式"""
    
    position: int = Field(description="排名")
    driver: DriverResponse = Field(description="车手信息")
    points: float = Field(description="积分")
    wins: int = Field(description="获胜次数")
    podiums: int = Field(description="领奖台次数") 