"""
赛季数据模型
"""
from sqlalchemy import Column, Integer, String, Date, Text, Boolean
from sqlalchemy.orm import relationship

from .base import BaseModel


class Season(BaseModel):
    """赛季模型"""
    
    # 赛季信息
    year = Column(Integer, nullable=False, unique=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    
    # 赛季时间
    start_date = Column(Date, nullable=True)
    end_date = Column(Date, nullable=True)
    
    # 赛季状态
    is_current = Column(Boolean, default=False, nullable=False)
    total_races = Column(Integer, default=0, nullable=False)
    completed_races = Column(Integer, default=0, nullable=False)
    
    # 关联关系
    races = relationship("Race", back_populates="season")
    drivers = relationship("Driver", back_populates="season")
    constructors = relationship("Constructor", back_populates="season")
    
    def __repr__(self):
        return f"<Season(year={self.year}, name='{self.name}')>" 