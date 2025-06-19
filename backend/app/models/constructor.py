"""
车队数据模型
"""
from sqlalchemy import Column, Integer, String, Text, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from .base import BaseModel


class Constructor(BaseModel):
    """车队模型"""
    
    # 车队基本信息
    constructor_id = Column(String(50), nullable=False, unique=True, index=True)
    name = Column(String(200), nullable=False)
    nationality = Column(String(100), nullable=False)
    
    # 外键关联
    season_id = Column(Integer, ForeignKey("seasons.id"), nullable=False)
    
    # 车队信息
    base = Column(String(200), nullable=True)  # 车队基地
    team_chief = Column(String(100), nullable=True)  # 车队领队
    technical_chief = Column(String(100), nullable=True)  # 技术总监
    power_unit = Column(String(100), nullable=True)  # 动力单元
    
    # 车队状态
    is_active = Column(Boolean, default=True, nullable=False)
    
    # 统计信息
    championships = Column(Integer, default=0, nullable=False)  # 车队冠军次数
    wins = Column(Integer, default=0, nullable=False)  # 获胜次数
    podiums = Column(Integer, default=0, nullable=False)  # 领奖台次数
    poles = Column(Integer, default=0, nullable=False)  # 杆位次数
    fastest_laps = Column(Integer, default=0, nullable=False)  # 最快圈速次数
    
    # 关联关系
    season = relationship("Season", back_populates="constructors")
    drivers = relationship("Driver", back_populates="constructor")
    results = relationship("Result", back_populates="constructor")
    
    def __repr__(self):
        return f"<Constructor(name='{self.name}', nationality='{self.nationality}')>" 