"""
车手相关的 API 端点
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.models.driver import Driver
from app.schemas.driver import DriverResponse, DriverListPaginatedResponse
from app.schemas.base import ApiResponse

router = APIRouter()


def _serialize_driver(driver: Driver) -> dict:
    """
    将Driver对象序列化为字典
    统一的数据序列化逻辑，避免重复代码
    """
    return {
        "driver_id": driver.driver_id,
        "number": driver.number,
        "code": driver.code,
        "driver_url": driver.driver_url,
        "forename": driver.forename,
        "surname": driver.surname,
        "date_of_birth": driver.date_of_birth,
        "nationality": driver.nationality,
    }


@router.get("/", response_model=DriverListPaginatedResponse)
async def get_drivers(
    db: Session = Depends(get_db),
    page: int = Query(1, ge=1, description="页码"),
    size: int = Query(20, ge=1, le=100, description="每页数量"),
):
    """
    获取车手列表
    """
    try:
        # 计算偏移量
        offset = (page - 1) * size
        
        # 查询总数
        total = db.query(Driver).count()
        # 查询车手数据
        drivers = db.query(Driver).offset(offset).limit(size).all()
        
        # 使用统一的序列化函数
        driver_list = [_serialize_driver(driver) for driver in drivers]
        
        pages = (total + size - 1) // size
        return {
            "data": driver_list,
            "total": total,
            "page": page,
            "size": size,
            "pages": pages
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取车手列表失败: {str(e)}")


@router.get("/search", response_model=ApiResponse[List[DriverResponse]])
async def search_drivers(
    q: str = Query(..., description="搜索关键词"),
    db: Session = Depends(get_db)
):
    """
    搜索车手
    """
    try:
        # 简单的名称搜索
        drivers = db.query(Driver).filter(
            (Driver.forename.ilike(f"%{q}%")) | 
            (Driver.surname.ilike(f"%{q}%")) |
            (Driver.code.ilike(f"%{q}%"))
        ).limit(10).all()
        
        # 使用统一的序列化函数
        driver_list = [_serialize_driver(driver) for driver in drivers]
        
        return ApiResponse(
            success=True,
            message="搜索车手成功",
            data=driver_list
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"搜索车手失败: {str(e)}")


@router.get("/{driver_id}", response_model=ApiResponse[DriverResponse])
async def get_driver(driver_id: str, db: Session = Depends(get_db)):
    """
    根据ID获取车手详情
    """
    try:
        driver = db.query(Driver).filter(Driver.driver_id == driver_id).first()
        
        if not driver:
            raise HTTPException(status_code=404, detail="车手不存在")
        
        # 使用统一的序列化函数
        driver_data = _serialize_driver(driver)
        
        return ApiResponse(
            success=True,
            message="获取车手详情成功",
            data=driver_data
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取车手详情失败: {str(e)}") 