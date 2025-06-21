"""
排位赛结果数据模型 - 基于FastF1实际数据结构
"""
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from .base import Base


class QualifyingResult(Base):
    """排位赛结果模型 - 基于FastF1实际数据结构"""
    __tablename__ = "qualifying_results"
    
    # 使用自增ID作为主键
    id = Column(Integer, primary_key=True, index=True)
    
    # 外键关联
    race_id = Column(Integer, ForeignKey("races.id"), nullable=False)
    driver_id = Column(String(50), ForeignKey("drivers.driver_id"), nullable=False)
    constructor_id = Column(String(50), ForeignKey("constructors.constructor_id"), nullable=False)
    
    # 排位赛成绩
    number = Column(Integer, nullable=True)  # 车手号码
    position = Column(Integer, nullable=True)  # 排位赛名次
    
    # Q1, Q2, Q3 成绩
    q1_time = Column(String(100), nullable=True)  # Q1 时间
    q2_time = Column(String(100), nullable=True)  # Q2 时间
    q3_time = Column(String(100), nullable=True)  # Q3 时间
    
    # 关联关系
    race = relationship("Race", back_populates="qualifying_results")
    driver = relationship("Driver", back_populates="qualifying_results")
    constructor = relationship("Constructor", back_populates="qualifying_results")
    
    def __repr__(self):
        return f"<QualifyingResult(race_id={self.race_id}, driver_id='{self.driver_id}', position={self.position})>" 