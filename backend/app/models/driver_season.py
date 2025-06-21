"""
车手赛季关联模型 - 处理车手跨赛季为不同车队效力的关系
"""
from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship

from .base import Base


class DriverSeason(Base):
    """车手赛季关联模型"""
    __tablename__ = "driver_seasons"
    
    # 使用自增ID作为主键
    id = Column(Integer, primary_key=True, index=True)
    
    # 外键关联
    driver_id = Column(String(50), ForeignKey("drivers.driver_id"), nullable=False)
    constructor_id = Column(String(50), ForeignKey("constructors.constructor_id"), nullable=False)
    season_id = Column(Integer, ForeignKey("seasons.id"), nullable=False)
    
    # 关联关系
    driver = relationship("Driver", back_populates="driver_seasons")
    constructor = relationship("Constructor", back_populates="driver_seasons")
    season = relationship("Season", back_populates="driver_seasons")
    
    def __repr__(self):
        return f"<DriverSeason(driver_id='{self.driver_id}', constructor_id='{self.constructor_id}', season_id={self.season_id})>" 