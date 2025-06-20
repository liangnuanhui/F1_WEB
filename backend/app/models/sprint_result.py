"""
冲刺赛结果数据模型
"""
from sqlalchemy import Column, Integer, String, Float, Text, ForeignKey, Index
from sqlalchemy.orm import relationship

from .base import BaseModel


class SprintResult(BaseModel):
    """冲刺赛结果模型"""
    
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
    
    # 冲刺赛成绩
    position = Column(Integer, nullable=True)  # 冲刺赛名次
    position_text = Column(String(10), nullable=True)  # 位置文本 (DNF, DNS等)
    points = Column(Float, default=0, nullable=False)  # 获得积分
    
    # 发车位置
    grid_position = Column(Integer, nullable=True)  # 发车位置
    
    # 比赛数据
    status = Column(String(50), nullable=True)  # 完赛状态
    laps_completed = Column(Integer, nullable=True)  # 完成圈数
    
    # 最快圈速信息
    fastest_lap_time = Column(String(20), nullable=True)  # 最快圈速时间
    fastest_lap_rank = Column(Integer, nullable=True)  # 最快圈速排名
    fastest_lap_number = Column(Integer, nullable=True)  # 最快圈速圈数
    fastest_lap_avg_speed = Column(Float, nullable=True)  # 最快圈速平均速度
    fastest_lap_avg_speed_units = Column(String(10), nullable=True)  # 速度单位
    
    # 时间数据
    total_race_time = Column(String(50), nullable=True)  # 总完赛时间
    total_race_time_millis = Column(Integer, nullable=True)  # 总完赛时间(毫秒)
    
    # 关联关系
    race = relationship("Race", back_populates="sprint_results")
    driver = relationship("Driver", back_populates="sprint_results")
    constructor = relationship("Constructor", back_populates="sprint_results")
    
    # 复合索引
    __table_args__ = (
        Index('idx_sprint_season_round', 'season', 'round_number'),
        Index('idx_sprint_season_round_driver', 'season', 'round_number', 'driver_id'),
        Index('idx_sprint_season_round_constructor', 'season', 'round_number', 'constructor_id'),
    )
    
    def __repr__(self):
        return f"<SprintResult(season={self.season}, round={self.round_number}, driver_id={self.driver_id}, position={self.position})>" 