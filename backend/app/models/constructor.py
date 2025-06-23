"""
车队数据模型 - 基于FastF1实际数据结构
"""
from sqlalchemy import Column, Integer, String, Text, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from .base import Base


class Constructor(Base):
    """车队模型 - 基于FastF1实际数据结构"""
    __tablename__ = "constructors"
    
    # 使用constructor_id作为主键
    constructor_id = Column(String(50), primary_key=True, index=True)  # FastF1的constructorId
    constructor_url = Column(String(500), nullable=True)  # 维基百科链接
    name = Column("constructor_name", String(200), nullable=False)  # 车队名称
    nationality = Column("constructor_nationality", String(100), nullable=True)  # 国籍
    
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
    driver_seasons = relationship("DriverSeason", back_populates="constructor")
    results = relationship("Result", back_populates="constructor")
    qualifying_results = relationship("QualifyingResult", back_populates="constructor")
    sprint_results = relationship("SprintResult", back_populates="constructor")
    driver_standings = relationship("DriverStanding", back_populates="constructor")
    constructor_standings = relationship("ConstructorStanding", back_populates="constructor")
    
    def __repr__(self):
        return f"<Constructor(constructor_id='{self.constructor_id}', name='{self.name}')>" 