"""
赛道相关的 Pydantic 模式
"""
from typing import Optional, List
from pydantic import BaseModel, Field

from .base import BaseModelSchema


class CircuitBase(BaseModel):
    """赛道基础模式"""
    
    circuit_id: str = Field(..., description="赛道ID")
    circuit_url: Optional[str] = Field(None, description="赛道官网")
    circuit_name: str = Field(..., description="赛道名称")
    lat: Optional[float] = Field(None, description="纬度")
    long: Optional[float] = Field(None, description="经度")
    locality: Optional[str] = Field(None, description="城市/地区")
    country: Optional[str] = Field(None, description="国家")
    length: Optional[float] = Field(None, description="赛道长度")
    corners: Optional[int] = Field(None, description="弯道数")
    lap_record: Optional[str] = Field(None, description="单圈纪录")
    lap_record_driver: Optional[str] = Field(None, description="纪录保持者")
    lap_record_year: Optional[int] = Field(None, description="纪录年份")
    
    # F1官网新增字段
    first_grand_prix: Optional[int] = Field(None, description="首次举办大奖赛年份")
    typical_lap_count: Optional[int] = Field(None, description="典型圈数")
    race_distance: Optional[float] = Field(None, description="比赛距离(公里)")
    circuit_layout_image_url: Optional[str] = Field(None, description="赛道布局图URL")
    circuit_layout_image_path: Optional[str] = Field(None, description="本地存储的布局图路径")
    
    description: Optional[str] = Field(None, description="描述")
    characteristics: Optional[str] = Field(None, description="特点")
    is_active: bool = Field(..., description="是否活跃")


class CircuitCreate(CircuitBase):
    """创建赛道模式"""
    pass


class CircuitUpdate(BaseModel):
    """更新赛道模式"""
    
    name: Optional[str] = Field(default=None, min_length=1, max_length=200, description="赛道名称")
    location: Optional[str] = Field(default=None, min_length=1, max_length=200, description="赛道位置")
    country: Optional[str] = Field(default=None, min_length=1, max_length=100, description="国家")
    length: Optional[float] = Field(default=None, gt=0, description="赛道长度(米)")
    corners: Optional[int] = Field(default=None, ge=0, description="弯道数量")
    lap_record: Optional[str] = Field(default=None, max_length=50, description="单圈记录")
    lap_record_driver: Optional[str] = Field(default=None, max_length=100, description="记录保持者")
    lap_record_year: Optional[int] = Field(default=None, ge=1950, le=2030, description="记录年份")
    
    # F1官网新增字段更新
    first_grand_prix: Optional[int] = Field(default=None, ge=1950, le=2030, description="首次举办大奖赛年份")
    typical_lap_count: Optional[int] = Field(default=None, ge=1, le=100, description="典型圈数")
    race_distance: Optional[float] = Field(default=None, gt=0, description="比赛距离(公里)")
    circuit_layout_image_url: Optional[str] = Field(default=None, description="赛道布局图URL")
    circuit_layout_image_path: Optional[str] = Field(default=None, description="本地存储的布局图路径")
    
    description: Optional[str] = Field(default=None, description="赛道描述")
    characteristics: Optional[str] = Field(default=None, description="赛道特点")


class CircuitResponse(CircuitBase, BaseModelSchema):
    """赛道响应模式"""
    pass


class CircuitListResponse(BaseModel):
    """赛道列表响应模式"""
    
    circuits: List[CircuitResponse] = Field(description="赛道列表")
    total: int = Field(description="总数") 