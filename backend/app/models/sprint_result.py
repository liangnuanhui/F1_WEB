"""
冲刺赛结果数据模型 - 基于FastF1实际数据结构
"""
from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship

from .base import Base


class SprintResult(Base):
    """冲刺赛结果模型 - 基于FastF1实际数据结构"""
    __tablename__ = "sprint_results"
    
    # 使用自增ID作为主键
    id = Column(Integer, primary_key=True, index=True)
    
    # 外键关联
    race_id = Column(Integer, ForeignKey("races.id"), nullable=False)
    driver_id = Column(String(50), ForeignKey("drivers.driver_id"), nullable=False)
    constructor_id = Column(String(50), ForeignKey("constructors.constructor_id"), nullable=False)
    
    # 冲刺赛成绩
    number = Column(Integer, nullable=True)  # 车手号码
    position = Column(Integer, nullable=True)  # 冲刺赛名次
    position_text = Column(String(10), nullable=True)  # 位置文本 (DNF, DNS等)
    points = Column(Float, default=0, nullable=False)  # 获得积分
    
    # 发车位置
    grid = Column(Integer, nullable=True)  # 发车位置
    
    # 比赛数据
    status = Column(String(50), nullable=True)  # 完赛状态
    laps = Column(Integer, nullable=True)  # 完成圈数
    
    # 最快圈速信息
    fastest_lap_time = Column(String(100), nullable=True)  # 最快圈速时间
    fastest_lap_rank = Column(Integer, nullable=True)  # 最快圈速排名
    fastest_lap_number = Column(Integer, nullable=True)  # 最快圈速圈数
    
    # 时间数据
    total_race_time = Column(String(100), nullable=True)  # 总完赛时间
    total_race_time_millis = Column(Integer, nullable=True)  # 总完赛时间(毫秒)
    
    # 关联关系
    race = relationship("Race", back_populates="sprint_results")
    driver = relationship("Driver", back_populates="sprint_results")
    constructor = relationship("Constructor", back_populates="sprint_results")
    
    def __repr__(self):
        return f"<SprintResult(race_id={self.race_id}, driver_id='{self.driver_id}', position={self.position})>" 