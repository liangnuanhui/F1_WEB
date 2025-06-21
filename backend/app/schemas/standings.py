"""
积分榜数据模式
"""
from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, Field


class DriverStandingResponse(BaseModel):
    """车手积分榜响应模式"""
    id: int
    season: int
    position: Optional[int] = None
    position_text: Optional[str] = None
    points: float = Field(..., ge=0)
    wins: int = Field(..., ge=0)
    driver_id: int
    driver_name: str
    driver_code: str
    constructor_id: int
    constructor_name: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ConstructorStandingResponse(BaseModel):
    """车队积分榜响应模式"""
    id: int
    season: int
    position: Optional[int] = None
    position_text: Optional[str] = None
    points: float = Field(..., ge=0)
    wins: int = Field(..., ge=0)
    constructor_id: int
    constructor_name: str
    constructor_nationality: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class DriverStandingList(BaseModel):
    """车手积分榜列表响应模式"""
    items: List[DriverStandingResponse]
    total: int
    limit: int
    offset: int
    season: int


class ConstructorStandingList(BaseModel):
    """车队积分榜列表响应模式"""
    items: List[ConstructorStandingResponse]
    total: int
    limit: int
    offset: int
    season: int 