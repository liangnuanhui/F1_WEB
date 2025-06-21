"""
比赛数据模型 - 基于FastF1实际数据结构
"""
from sqlalchemy import Column, String, Integer, Date, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from .base import Base


class Race(Base):
    """比赛模型 - 基于FastF1实际数据结构"""
    __tablename__ = "races"
    
    # 使用自增ID作为主键
    id = Column(Integer, primary_key=True, index=True)
    
    # 外键关联
    season_id = Column(Integer, ForeignKey("seasons.id"), nullable=False)
    circuit_id = Column(String(50), ForeignKey("circuits.circuit_id"), nullable=False)
    
    # FastF1实际字段名
    round_number = Column(Integer, nullable=False)  # 轮次
    country = Column(String(100), nullable=True)  # 国家
    location = Column(String(100), nullable=True)  # 地点
    official_event_name = Column(String(200), nullable=False)  # 官方名称
    event_date = Column(Date, nullable=True)  # 比赛日期
    event_format = Column(String(50), nullable=True)  # 比赛格式
    
    # 会话信息
    session1 = Column(String(100), nullable=True)  # 第一节
    session1_date = Column(DateTime, nullable=True)  # 第一节日期
    session2 = Column(String(100), nullable=True)  # 第二节
    session2_date = Column(DateTime, nullable=True)  # 第二节日期
    session3 = Column(String(100), nullable=True)  # 第三节
    session3_date = Column(DateTime, nullable=True)  # 第三节日期
    session4 = Column(String(100), nullable=True)  # 第四节
    session4_date = Column(DateTime, nullable=True)  # 第四节日期
    session5 = Column(String(100), nullable=True)  # 第五节
    session5_date = Column(DateTime, nullable=True)  # 第五节日期
    
    # 关联关系
    season = relationship("Season", back_populates="races")
    circuit = relationship("Circuit", back_populates="races")
    results = relationship("Result", back_populates="race")
    qualifying_results = relationship("QualifyingResult", back_populates="race")
    sprint_results = relationship("SprintResult", back_populates="race")
    
    def __repr__(self):
        return f"<Race(round={self.round_number}, name='{self.official_event_name}', date={self.event_date})>" 