"""
比赛结果数据模型
"""
from sqlalchemy import Column, Integer, String, Float, Text, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from .base import BaseModel


class Result(BaseModel):
    """比赛结果模型"""
    
    # 外键关联
    race_id = Column(Integer, ForeignKey("races.id"), nullable=False)
    driver_id = Column(Integer, ForeignKey("drivers.id"), nullable=False)
    constructor_id = Column(Integer, ForeignKey("constructors.id"), nullable=False)
    
    # 比赛成绩
    position = Column(Integer, nullable=True)  # 完赛名次
    position_text = Column(String(10), nullable=True)  # 位置文本 (DNF, DNS等)
    points = Column(Float, default=0, nullable=False)  # 获得积分
    
    # 排位赛成绩
    grid_position = Column(Integer, nullable=True)  # 发车位置
    qualifying_position = Column(Integer, nullable=True)  # 排位赛位置
    
    # 比赛数据
    status = Column(String(50), nullable=True)  # 完赛状态
    laps_completed = Column(Integer, nullable=True)  # 完成圈数
    fastest_lap = Column(String(20), nullable=True)  # 最快圈速
    fastest_lap_rank = Column(Integer, nullable=True)  # 最快圈速排名
    
    # 时间数据
    finish_time = Column(String(50), nullable=True)  # 完赛时间
    gap_to_leader = Column(String(20), nullable=True)  # 与领先者差距
    gap_to_previous = Column(String(20), nullable=True)  # 与前车差距
    
    # 额外信息
    penalties = Column(Text, nullable=True)  # 处罚信息
    notes = Column(Text, nullable=True)  # 备注
    
    # 关联关系
    race = relationship("Race", back_populates="results")
    driver = relationship("Driver", back_populates="results")
    constructor = relationship("Constructor", back_populates="results")
    
    def __repr__(self):
        return f"<Result(race_id={self.race_id}, driver_id={self.driver_id}, position={self.position})>" 