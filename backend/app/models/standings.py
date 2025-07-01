"""
积分榜数据模型 - 基于FastF1实际数据结构
"""
from sqlalchemy import Column, Integer, String, Float, ForeignKey, Index
from sqlalchemy.orm import relationship

from .base import Base


class DriverStanding(Base):
    """车手积分榜模型 - 基于FastF1实际数据结构"""
    __tablename__ = "driver_standings"
    
    # 使用自增ID作为主键
    id = Column(Integer, primary_key=True, index=True)
    
    # 外键关联
    season_id = Column(Integer, ForeignKey("seasons.id"), nullable=False)
    driver_id = Column(String(50), ForeignKey("drivers.driver_id"), nullable=False)
    constructor_id = Column(String(50), ForeignKey("constructors.constructor_id"), nullable=False)
    
    # 积分榜信息 - 匹配 FastF1 字段
    position = Column(Integer, nullable=True)  # 积分榜位置
    position_text = Column(String(10), nullable=True)  # 位置文本（如"1"、"DNF"等）
    points = Column(Float, default=0, nullable=False)  # 总积分
    wins = Column(Integer, default=0, nullable=False)  # 获胜次数
    
    # 关联关系
    season = relationship("Season", back_populates="driver_standings")
    driver = relationship("Driver", back_populates="driver_standings")
    constructor = relationship("Constructor", back_populates="driver_standings")
    
    # 复合索引
    __table_args__ = (
        Index('idx_driver_standing_season', 'season_id'),
        Index('idx_driver_standing_season_driver', 'season_id', 'driver_id'),
        Index('idx_driver_standing_season_constructor', 'season_id', 'constructor_id'),
    )
    
    def __repr__(self):
        return f"<DriverStanding(season_id={self.season_id}, driver_id='{self.driver_id}', position={self.position})>"


class ConstructorStanding(Base):
    """车队积分榜模型 - 基于FastF1实际数据结构"""
    __tablename__ = "constructor_standings"
    
    # 使用自增ID作为主键
    id = Column(Integer, primary_key=True, index=True)
    
    # 外键关联
    season_id = Column(Integer, ForeignKey("seasons.id"), nullable=False)
    constructor_id = Column(String(50), ForeignKey("constructors.constructor_id"), nullable=False)
    
    # 积分榜信息 - 匹配 FastF1 字段
    position = Column(Integer, nullable=True)  # 积分榜位置
    position_text = Column(String(10), nullable=True)  # 位置文本（如"1"、"DNF"等）
    points = Column(Float, default=0, nullable=False)  # 总积分
    wins = Column(Integer, default=0, nullable=False)  # 获胜次数
    
    # 关联关系
    season = relationship("Season", back_populates="constructor_standings")
    constructor = relationship("Constructor", back_populates="constructor_standings")
    
    # 复合索引
    __table_args__ = (
        Index('idx_constructor_standing_season', 'season_id'),
        Index('idx_constructor_standing_season_constructor', 'season_id', 'constructor_id'),
    )
    
    def __repr__(self):
        return f"<ConstructorStanding(season_id={self.season_id}, constructor_id='{self.constructor_id}', position={self.position})>" 