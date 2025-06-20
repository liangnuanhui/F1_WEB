"""
排位赛结果数据模型
"""
from sqlalchemy import Column, Integer, String, Float, Text, ForeignKey, Index
from sqlalchemy.orm import relationship

from .base import BaseModel


class QualifyingResult(BaseModel):
    """排位赛结果模型"""
    
    # 赛季和比赛信息
    season = Column(Integer, nullable=False, index=True)  # 赛季年份
    round_number = Column(Integer, nullable=False)  # 比赛轮次
    
    # 外键关联
    race_id = Column(Integer, ForeignKey("races.id"), nullable=False)
    driver_id = Column(Integer, ForeignKey("drivers.id"), nullable=False)
    constructor_id = Column(Integer, ForeignKey("constructors.id"), nullable=False)
    
    # 车手信息
    driver_number = Column(Integer, nullable=True)  # 车手号码
    driver_code = Column(String(10), nullable=True)  # 车手代码
    
    # 排位赛成绩
    position = Column(Integer, nullable=True)  # 排位赛名次
    
    # Q1, Q2, Q3 成绩
    q1_time = Column(String(20), nullable=True)  # Q1 时间
    q2_time = Column(String(20), nullable=True)  # Q2 时间
    q3_time = Column(String(20), nullable=True)  # Q3 时间
    
    # 关联关系
    race = relationship("Race", back_populates="qualifying_results")
    driver = relationship("Driver", back_populates="qualifying_results")
    constructor = relationship("Constructor", back_populates="qualifying_results")
    
    # 复合索引
    __table_args__ = (
        Index('idx_qualifying_season_round', 'season', 'round_number'),
        Index('idx_qualifying_season_round_driver', 'season', 'round_number', 'driver_id'),
        Index('idx_qualifying_season_round_constructor', 'season', 'round_number', 'constructor_id'),
    )
    
    def __repr__(self):
        return f"<QualifyingResult(season={self.season}, round={self.round_number}, driver_id={self.driver_id}, position={self.position})>" 