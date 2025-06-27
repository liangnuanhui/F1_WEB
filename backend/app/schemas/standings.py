"""
积分榜相关的 Pydantic 模式
"""
from typing import Optional, List
from pydantic import BaseModel, Field


class DriverStandingBase(BaseModel):
    position: int = Field(..., description="排名")
    points: float = Field(..., description="积分")
    wins: int = Field(..., description="胜场")
    driver_id: str = Field(..., description="车手ID")
    driver_name: str = Field(..., description="车手姓名")
    nationality: str = Field(..., description="国籍")
    constructor_id: str = Field(..., description="所属车队ID")
    constructor_name: str = Field(..., description="所属车队名称")

    class Config:
        from_attributes = True


class ConstructorStandingBase(BaseModel):
    position: int = Field(..., description="排名")
    points: float = Field(..., description="积分")
    wins: int = Field(..., description="胜场")
    constructor_id: str = Field(..., description="车队ID")
    constructor_name: str = Field(..., description="车队名称")
    nationality: str = Field(..., description="国籍")
    constructor_url: Optional[str] = Field(None, description="车队维基百科链接")

    class Config:
        from_attributes = True


class DriverStandingList(BaseModel):
    standings: List[DriverStandingBase]
    total: int


class ConstructorStandingList(BaseModel):
    standings: List[ConstructorStandingBase]
    total: int


class DriverStandingResponse(DriverStandingBase):
    pass


class ConstructorStandingResponse(ConstructorStandingBase):
    pass


class StandingHistoryResponse(BaseModel):
    """积分榜历史响应模式"""
    id: int
    season_id: int
    position: Optional[int] = None
    points: float
    wins: int
    driver_id: str
    constructor_id: str
    driver_name: str
    driver_code: str
    constructor_name: str


# Properties to return to client
class ConstructorStanding(ConstructorStandingBase):
    constructor_id: str
    constructor_name: str
    constructor_url: str | None = None

    class Config:
        orm_mode = True


class ConstructorStandingsResponse(BaseModel):
    pass 