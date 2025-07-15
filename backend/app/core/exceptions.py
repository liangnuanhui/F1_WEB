"""
统一异常处理器
提供全局异常处理和标准化错误响应
"""
from typing import Union
from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError
import structlog

logger = structlog.get_logger()


class BaseAPIException(Exception):
    """
    API异常基类
    """
    def __init__(self, status_code: int, message: str, detail: str = None):
        self.status_code = status_code
        self.message = message
        self.detail = detail


class DatabaseException(BaseAPIException):
    """
    数据库异常
    """
    def __init__(self, message: str = "数据库操作失败", detail: str = None):
        super().__init__(status_code=500, message=message, detail=detail)


class ValidationException(BaseAPIException):
    """
    数据验证异常
    """
    def __init__(self, message: str = "数据验证失败", detail: str = None):
        super().__init__(status_code=400, message=message, detail=detail)


class NotFoundException(BaseAPIException):
    """
    资源未找到异常
    """
    def __init__(self, message: str = "资源未找到", detail: str = None):
        super().__init__(status_code=404, message=message, detail=detail)


async def http_exception_handler(request: Request, exc: HTTPException):
    """
    HTTP异常处理器
    """
    logger.warning(
        "HTTP异常",
        status_code=exc.status_code,
        detail=exc.detail,
        path=request.url.path
    )
    
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "message": exc.detail,
            "data": None,
            "error_code": exc.status_code
        }
    )


async def base_api_exception_handler(request: Request, exc: BaseAPIException):
    """
    API异常处理器
    """
    logger.error(
        "API异常",
        status_code=exc.status_code,
        message=exc.message,
        detail=exc.detail,
        path=request.url.path
    )
    
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "message": exc.message,
            "data": None,
            "error_code": exc.status_code,
            "detail": exc.detail
        }
    )


async def sqlalchemy_exception_handler(request: Request, exc: SQLAlchemyError):
    """
    SQLAlchemy异常处理器
    """
    logger.error(
        "数据库异常",
        error=str(exc),
        path=request.url.path
    )
    
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "message": "数据库操作失败",
            "data": None,
            "error_code": 500
        }
    )


async def general_exception_handler(request: Request, exc: Exception):
    """
    通用异常处理器
    """
    logger.error(
        "未处理的异常",
        error=str(exc),
        error_type=type(exc).__name__,
        path=request.url.path
    )
    
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "message": "服务器内部错误",
            "data": None,
            "error_code": 500
        }
    )