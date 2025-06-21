"""
比赛结果数据模型 - 基于FastF1实际数据结构
"""
from sqlalchemy import Column, String, Integer, Float, BigInteger, ForeignKey
from sqlalchemy.orm import relationship

from .base import Base


class Result(Base):
    """比赛结果模型 - 基于FastF1实际数据结构"""
    __tablename__ = "results"
    
    # 使用自增ID作为主键
    id = Column(Integer, primary_key=True, index=True)
    
    # 外键关联
    race_id = Column(Integer, ForeignKey("races.id"), nullable=False)
    driver_id = Column(String(50), ForeignKey("drivers.driver_id"), nullable=False)
    constructor_id = Column(String(50), ForeignKey("constructors.constructor_id"), nullable=False)
    
    # FastF1实际字段名
    number = Column(Integer, nullable=True)  # 车手号码
    position = Column(Integer, nullable=True)  # 名次
    position_text = Column(String(10), nullable=True)  # 名次文本
    points = Column(Float, nullable=True)  # 积分
    grid = Column(Integer, nullable=True)  # 发车位置
    laps = Column(Integer, nullable=True)  # 完成圈数
    status = Column(String(50), nullable=True)  # 状态
    
    # 时间信息
    total_race_time_millis = Column(BigInteger, nullable=True)  # 总时间(毫秒)
    total_race_time = Column(String(100), nullable=True)  # 总时间字符串
    fastest_lap_rank = Column(Integer, nullable=True)  # 最快圈排名
    fastest_lap_number = Column(Integer, nullable=True)  # 最快圈圈数
    fastest_lap_time = Column(String(100), nullable=True)  # 最快圈时间
    
    # 关联关系
    race = relationship("Race", back_populates="results")
    driver = relationship("Driver", back_populates="results")
    constructor = relationship("Constructor", back_populates="results")
    
    def __repr__(self):
        return f"<Result(race_id={self.race_id}, driver_id='{self.driver_id}', position={self.position})>" 