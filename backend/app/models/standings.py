"""
积分榜数据模型
"""
from sqlalchemy import Column, Integer, String, Float, Text, ForeignKey, Index
from sqlalchemy.orm import relationship

from .base import BaseModel


class DriverStanding(BaseModel):
    """车手积分榜模型 - 只保存最新积分榜"""
    
    # 赛季信息
    season = Column(Integer, nullable=False, index=True)  # 赛季年份
    
    # 外键关联
    driver_id = Column(Integer, ForeignKey("drivers.id"), nullable=False)
    constructor_id = Column(Integer, ForeignKey("constructors.id"), nullable=False)
    
    # 积分榜信息
    position = Column(Integer, nullable=True)  # 积分榜位置
    position_text = Column(String(10), nullable=True)  # 位置文本
    points = Column(Float, default=0, nullable=False)  # 总积分
    wins = Column(Integer, default=0, nullable=False)  # 获胜次数
    
    # 关联关系
    driver = relationship("Driver", back_populates="driver_standings")
    constructor = relationship("Constructor", back_populates="driver_standings")
    
    # 复合索引
    __table_args__ = (
        Index('idx_driver_standing_season', 'season'),
        Index('idx_driver_standing_season_driver', 'season', 'driver_id'),
        Index('idx_driver_standing_season_constructor', 'season', 'constructor_id'),
    )
    
    def __repr__(self):
        return f"<DriverStanding(season={self.season}, driver_id={self.driver_id}, position={self.position})>"


class ConstructorStanding(BaseModel):
    """车队积分榜模型 - 只保存最新积分榜"""
    
    # 赛季信息
    season = Column(Integer, nullable=False, index=True)  # 赛季年份
    
    # 外键关联
    constructor_id = Column(Integer, ForeignKey("constructors.id"), nullable=False)
    
    # 积分榜信息
    position = Column(Integer, nullable=True)  # 积分榜位置
    position_text = Column(String(10), nullable=True)  # 位置文本
    points = Column(Float, default=0, nullable=False)  # 总积分
    wins = Column(Integer, default=0, nullable=False)  # 获胜次数
    
    # 关联关系
    constructor = relationship("Constructor", back_populates="constructor_standings")
    
    # 复合索引
    __table_args__ = (
        Index('idx_constructor_standing_season', 'season'),
        Index('idx_constructor_standing_season_constructor', 'season', 'constructor_id'),
    )
    
    def __repr__(self):
        return f"<ConstructorStanding(season={self.season}, constructor_id={self.constructor_id}, position={self.position})>" 