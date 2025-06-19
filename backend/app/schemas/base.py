"""
基础响应模式
包含通用的响应结构
"""
from datetime import datetime
from typing import Any, Optional, Generic, TypeVar
from pydantic import BaseModel, Field

# 泛型类型变量
T = TypeVar('T')


class BaseResponse(BaseModel):
    """基础响应模式"""
    
    success: bool = Field(default=True, description="请求是否成功")
    message: str = Field(default="操作成功", description="响应消息")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="响应时间")


class DataResponse(BaseResponse, Generic[T]):
    """数据响应模式"""
    
    data: Optional[T] = Field(default=None, description="响应数据")
    total: Optional[int] = Field(default=None, description="数据总数")
    page: Optional[int] = Field(default=None, description="当前页码")
    size: Optional[int] = Field(default=None, description="每页大小")


class ErrorResponse(BaseResponse):
    """错误响应模式"""
    
    success: bool = Field(default=False, description="请求是否成功")
    error_code: Optional[str] = Field(default=None, description="错误代码")
    error_details: Optional[Any] = Field(default=None, description="错误详情")


class PaginationParams(BaseModel):
    """分页参数"""
    
    page: int = Field(default=1, ge=1, description="页码")
    size: int = Field(default=20, ge=1, le=100, description="每页大小")
    sort_by: Optional[str] = Field(default=None, description="排序字段")
    sort_order: Optional[str] = Field(default="asc", description="排序方向 (asc/desc)")


class BaseModelSchema(BaseModel):
    """基础模型模式"""
    
    id: int = Field(description="记录ID")
    created_at: datetime = Field(description="创建时间")
    updated_at: datetime = Field(description="更新时间")
    is_active: bool = Field(description="是否激活")
    
    class Config:
        from_attributes = True 