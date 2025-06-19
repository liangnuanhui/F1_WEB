"""
赛道数据模型
"""
from sqlalchemy import Column, Integer, String, Float, Text, Boolean
from sqlalchemy.orm import relationship

from .base import BaseModel


class Circuit(BaseModel):
    """赛道模型"""
    
    # 赛道基本信息
    circuit_id = Column(String(50), nullable=False, unique=True, index=True)
    name = Column(String(200), nullable=False)
    location = Column(String(200), nullable=False)
    country = Column(String(100), nullable=False)
    
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
        return f"<Circuit(name='{self.name}', country='{self.country}')>" 