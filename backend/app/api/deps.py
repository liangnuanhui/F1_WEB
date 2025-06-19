"""
API 依赖注入
包含数据库会话、Redis 连接等依赖
"""
from typing import Generator
from sqlalchemy.orm import Session

from ..core.database import SessionLocal
from ..core.redis import get_redis


def get_db() -> Generator[Session, None, None]:
    """
    获取数据库会话
    使用依赖注入模式
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_redis_client():
    """
    获取 Redis 客户端
    """
    return get_redis() 