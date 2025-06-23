"""
基础数据模型
包含所有模型共用的字段和方法
"""
from datetime import datetime
from sqlalchemy import Column, Integer, DateTime, Boolean
from sqlalchemy.ext.declarative import declared_attr

from ..core.database import Base


class BaseModel(Base):
    """基础模型类"""
    
    __abstract__ = True
    
    # 注意：实际的数据库表中没有这些字段，所以这里不定义
    # 如果需要这些字段，需要通过数据库迁移添加
    
    @declared_attr
    def __tablename__(cls):
        """自动生成表名"""
        return cls.__name__.lower() + 's'
    
    def __repr__(self):
        """字符串表示"""
        return f"<{self.__class__.__name__}(id={getattr(self, 'id', 'N/A')})>"
    
    def to_dict(self):
        """转换为字典"""
        return {
            column.name: getattr(self, column.name)
            for column in self.__table__.columns
        } 