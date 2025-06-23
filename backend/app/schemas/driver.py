"""
车手相关的 Pydantic 模式
"""
from typing import Optional, List
from pydantic import BaseModel, Field
from datetime import date

from .base import BaseModelSchema


class DriverBase(BaseModel):
    """车手基础模式（与数据库字段完全一致）"""
    driver_id: str = Field(..., description="车手ID")
    number: Optional[int] = Field(None, description="车手号码")
    code: Optional[str] = Field(None, description="车手代码")
    driver_url: Optional[str] = Field(None, description="车手官网")
    forename: str = Field(..., description="名")
    surname: str = Field(..., description="姓")
    date_of_birth: Optional[date] = Field(None, description="出生日期")
    nationality: Optional[str] = Field(None, description="国籍")

    @property
    def full_name(self) -> str:
        return f"{self.forename} {self.surname}"


class DriverCreate(DriverBase):
    """创建车手模式"""
    pass


class DriverUpdate(BaseModel):
    """更新车手模式"""
    number: Optional[int] = Field(None, description="车手号码")
    code: Optional[str] = Field(None, description="车手代码")
    driver_url: Optional[str] = Field(None, description="车手官网")
    forename: Optional[str] = Field(None, description="名")
    surname: Optional[str] = Field(None, description="姓")
    date_of_birth: Optional[str] = Field(None, description="出生日期")
    nationality: Optional[str] = Field(None, description="国籍")


class DriverResponse(DriverBase, BaseModelSchema):
    """车手响应模式（与数据库字段一致，额外提供 full_name）"""
    @property
    def full_name(self) -> str:
        return f"{self.forename} {self.surname}"


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


class DriverListPaginatedResponse(BaseModel):
    data: List[DriverResponse] = Field(description="车手列表")
    total: int = Field(description="总数")
    page: int = Field(description="当前页码")
    size: int = Field(description="每页大小")
    pages: int = Field(description="总页数") 