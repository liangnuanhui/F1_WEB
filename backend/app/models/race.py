"""
比赛数据模型
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from .base import BaseModel


class Race(BaseModel):
    """比赛模型"""
    
    # 比赛基本信息
    race_id = Column(String(50), nullable=False, unique=True, index=True)
    name = Column(String(200), nullable=False)
    round_number = Column(Integer, nullable=False)  # 比赛轮次
    
    # 外键关联
    season_id = Column(Integer, ForeignKey("seasons.id"), nullable=False)
    circuit_id = Column(Integer, ForeignKey("circuits.id"), nullable=False)
    
    # 比赛时间
    race_date = Column(DateTime, nullable=False)
    qualifying_date = Column(DateTime, nullable=True)
    sprint_date = Column(DateTime, nullable=True)
    
    # 比赛状态
    status = Column(String(50), default="scheduled", nullable=False)  # scheduled, ongoing, completed, cancelled
    is_sprint_weekend = Column(Boolean, default=False, nullable=False)
    
    # 比赛信息
    description = Column(Text, nullable=True)
    weather = Column(String(100), nullable=True)
    temperature = Column(Integer, nullable=True)  # 温度(摄氏度)
    
    # 关联关系
    season = relationship("Season", back_populates="races")
    circuit = relationship("Circuit", back_populates="races")
    results = relationship("Result", back_populates="race")
    
    def __repr__(self):
        return f"<Race(name='{self.name}', round={self.round_number}, date={self.race_date})>" 