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
    nationality: Optional[str] = Field(None, description="国籍")
    constructor_id: Optional[str] = Field(None, description="所属车队ID")
    constructor_name: Optional[str] = Field(None, description="所属车队名称")

class DriverStandingResponse(DriverStandingBase):
    pass

class ConstructorStandingBase(BaseModel):
    position: int = Field(..., description="排名")
    points: float = Field(..., description="积分")
    wins: int = Field(..., description="胜场")
    constructor_id: str = Field(..., description="车队ID")
    constructor_name: str = Field(..., description="车队名称")
    nationality: Optional[str] = Field(None, description="国籍")

class ConstructorStandingResponse(ConstructorStandingBase):
    pass

class DriverStandingList(BaseModel):
    standings: List[DriverStandingResponse] = Field(description="车手积分榜")
    total: int = Field(description="总数")

class ConstructorStandingList(BaseModel):
    standings: List[ConstructorStandingResponse] = Field(description="车队积分榜")
    total: int = Field(description="总数")

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