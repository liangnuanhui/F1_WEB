"""
赛季数据模型 - 基于FastF1实际数据结构
"""
from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import relationship

from .base import Base


class Season(Base):
    """赛季模型 - 基于FastF1实际数据结构"""
    __tablename__ = "seasons"
    
    # 使用自增ID作为主键
    id = Column(Integer, primary_key=True, index=True)
    year = Column(Integer, unique=True, nullable=False, index=True)  # 2023, 2024, 2025
    name = Column(String(100), nullable=False)  # "2025 Formula 1 World Championship"
    description = Column(String, nullable=True)  # 赛季描述
    start_date = Column(Date, nullable=True)  # 赛季开始日期
    end_date = Column(Date, nullable=True)  # 赛季结束日期
    
    # 关联关系
    races = relationship("Race", back_populates="season")
    driver_standings = relationship("DriverStanding", back_populates="season")
    constructor_standings = relationship("ConstructorStanding", back_populates="season")
    driver_seasons = relationship("DriverSeason", back_populates="season")
    
    def __repr__(self):
        return f"<Season(year={self.year}, name='{self.name}')>" 