"""
车手数据模型 - 基于FastF1实际数据结构
"""
from sqlalchemy import Column, String, Integer, Date
from sqlalchemy.orm import relationship

from .base import Base


class Driver(Base):
    """车手模型 - 基于FastF1实际数据结构"""
    __tablename__ = "drivers"
    
    # 使用driver_id作为主键
    driver_id = Column(String(50), primary_key=True, index=True)  # FastF1的driverId
    driver_number = Column(Integer, nullable=True)  # 车手号码
    driver_code = Column(String(10), nullable=True)  # 车手代码
    driver_url = Column(String(500), nullable=True)  # 维基百科链接
    given_name = Column(String(100), nullable=False)  # 名
    family_name = Column(String(100), nullable=False)  # 姓
    date_of_birth = Column(Date, nullable=True)  # 出生日期
    driver_nationality = Column(String(100), nullable=True)  # 国籍
    
    # 关联关系 - 车手可以跨赛季为不同车队效力
    driver_seasons = relationship("DriverSeason", back_populates="driver")
    results = relationship("Result", back_populates="driver")
    qualifying_results = relationship("QualifyingResult", back_populates="driver")
    sprint_results = relationship("SprintResult", back_populates="driver")
    driver_standings = relationship("DriverStanding", back_populates="driver")
    
    def __repr__(self):
        return f"<Driver(driver_id='{self.driver_id}', name='{self.given_name} {self.family_name}')>" 