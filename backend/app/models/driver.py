"""
车手数据模型
"""
from sqlalchemy import Column, Integer, String, Date, Text, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from .base import BaseModel


class Driver(BaseModel):
    """车手模型"""
    
    # 车手基本信息
    driver_id = Column(String(50), nullable=False, unique=True, index=True)
    code = Column(String(10), nullable=True)  # 车手代码
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    full_name = Column(String(200), nullable=False)
    
    # 个人信息
    date_of_birth = Column(Date, nullable=True)
    nationality = Column(String(100), nullable=False)
    number = Column(Integer, nullable=True)  # 车手号码
    
    # 外键关联
    season_id = Column(Integer, ForeignKey("seasons.id"), nullable=False)
    constructor_id = Column(Integer, ForeignKey("constructors.id"), nullable=True)
    
    # 车手状态
    is_active = Column(Boolean, default=True, nullable=False)
    
    # 统计信息
    championships = Column(Integer, default=0, nullable=False)  # 世界冠军次数
    wins = Column(Integer, default=0, nullable=False)  # 获胜次数
    podiums = Column(Integer, default=0, nullable=False)  # 领奖台次数
    poles = Column(Integer, default=0, nullable=False)  # 杆位次数
    fastest_laps = Column(Integer, default=0, nullable=False)  # 最快圈速次数
    
    # 关联关系
    season = relationship("Season", back_populates="drivers")
    constructor = relationship("Constructor", back_populates="drivers")
    results = relationship("Result", back_populates="driver")
    qualifying_results = relationship("QualifyingResult", back_populates="driver")
    sprint_results = relationship("SprintResult", back_populates="driver")
    driver_standings = relationship("DriverStanding", back_populates="driver")
    
    def __repr__(self):
        return f"<Driver(name='{self.full_name}', number={self.number})>" 