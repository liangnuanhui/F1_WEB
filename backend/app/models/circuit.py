"""
赛道数据模型 - 基于FastF1实际数据结构
"""
from sqlalchemy import Column, Integer, String, Float, Text, Boolean
from sqlalchemy.orm import relationship

from .base import Base


class Circuit(Base):
    """赛道模型 - 基于FastF1实际数据结构"""
    __tablename__ = "circuits"
    
    # 使用circuit_id作为主键
    circuit_id = Column(String(50), primary_key=True, index=True)  # FastF1的circuitId
    circuit_url = Column(String(500), nullable=True)  # 维基百科链接
    circuit_name = Column(String(200), nullable=False)  # 赛道名称
    lat = Column(Float, nullable=True)  # 纬度
    long = Column(Float, nullable=True)  # 经度
    locality = Column(String(100), nullable=True)  # 城市
    country = Column(String(100), nullable=True)  # 国家
    
    # 赛道规格
    length = Column(Float, nullable=True)  # 赛道长度(米)
    corners = Column(Integer, nullable=True)  # 弯道数量
    lap_record = Column(String(50), nullable=True)  # 单圈记录
    lap_record_driver = Column(String(100), nullable=True)  # 记录保持者
    lap_record_year = Column(Integer, nullable=True)  # 记录年份
    
    # 赛道特点
    description = Column(Text, nullable=True)
    characteristics = Column(Text, nullable=True)  # 赛道特点
    is_active = Column(Boolean, default=True, nullable=False)
    
    # 关联关系
    races = relationship("Race", back_populates="circuit")
    
    def __repr__(self):
        return f"<Circuit(circuit_id='{self.circuit_id}', name='{self.circuit_name}')>" 