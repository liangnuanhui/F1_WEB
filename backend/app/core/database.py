"""
数据库连接和会话管理
使用 SQLAlchemy 2.0 异步特性
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from .config import settings

# 创建数据库引擎
engine = create_engine(
    settings.database_url,
    poolclass=StaticPool,
    pool_pre_ping=True,
    echo=settings.debug,
)

# 创建会话工厂
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

# 创建基础模型类
Base = declarative_base()


def get_db():
    """
    获取数据库会话
    使用依赖注入模式
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """
    初始化数据库
    创建所有表
    """
    Base.metadata.create_all(bind=engine) 