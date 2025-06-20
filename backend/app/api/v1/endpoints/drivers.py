"""
车手相关的 API 端点
"""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from ....api.deps import get_db
from ....models import Driver, Constructor, Season
from ....schemas import (
    DriverResponse,
    DriverListResponse,
    DriverCreate,
    DriverUpdate,
    DataResponse,
    PaginationParams
)

router = APIRouter()


@router.get("/", response_model=DataResponse[List[DriverResponse]])
async def get_drivers(
    db: Session = Depends(get_db),
    pagination: PaginationParams = Depends(),
    season_id: Optional[int] = Query(None, description="赛季ID"),
    constructor_id: Optional[int] = Query(None, description="车队ID"),
    nationality: Optional[str] = Query(None, description="国籍"),
    is_active: Optional[bool] = Query(None, description="是否激活")
):
    """
    获取车手列表
    """
    query = db.query(Driver)
    if season_id:
        query = query.filter(Driver.season_id == season_id)
    if constructor_id:
        query = query.filter(Driver.constructor_id == constructor_id)
    if nationality:
        query = query.filter(Driver.nationality.ilike(f"%{nationality}%"))
    if is_active is not None:
        query = query.filter(Driver.is_active == is_active)
    # 排序
    if pagination.sort_by:
        sort_column = getattr(Driver, pagination.sort_by, Driver.full_name)
        if pagination.sort_order == "desc":
            sort_column = sort_column.desc()
        query = query.order_by(sort_column)
    else:
        query = query.order_by(Driver.full_name)
    # 分页
    total = query.count()
    drivers = query.offset((pagination.page - 1) * pagination.size).limit(pagination.size).all()
    return DataResponse(
        data=[DriverResponse.from_orm(driver) for driver in drivers],
        total=total,
        page=pagination.page,
        size=pagination.size
    )


@router.get("/{driver_id}", response_model=DriverResponse)
async def get_driver(driver_id: int, db: Session = Depends(get_db)):
    """
    根据ID获取车手详情
    """
    driver = db.query(Driver).filter(Driver.id == driver_id).first()
    if not driver:
        raise HTTPException(status_code=404, detail="车手不存在")
    return DriverResponse.from_orm(driver)


@router.post("/", response_model=DriverResponse)
async def create_driver(driver: DriverCreate, db: Session = Depends(get_db)):
    """
    创建新车手
    """
    # 检查 driver_id 是否唯一
    existing = db.query(Driver).filter(Driver.driver_id == driver.driver_id).first()
    if existing:
        raise HTTPException(status_code=400, detail="车手ID已存在")
    # 检查赛季和车队是否存在
    season = db.query(Season).filter(Season.id == driver.season_id).first()
    if not season:
        raise HTTPException(status_code=400, detail="赛季不存在")
    if driver.constructor_id:
        constructor = db.query(Constructor).filter(Constructor.id == driver.constructor_id).first()
        if not constructor:
            raise HTTPException(status_code=400, detail="车队不存在")
    db_driver = Driver(**driver.dict())
    db.add(db_driver)
    db.commit()
    db.refresh(db_driver)
    return DriverResponse.from_orm(db_driver)


@router.put("/{driver_id}", response_model=DriverResponse)
async def update_driver(driver_id: int, driver_update: DriverUpdate, db: Session = Depends(get_db)):
    """
    更新车手信息
    """
    db_driver = db.query(Driver).filter(Driver.id == driver_id).first()
    if not db_driver:
        raise HTTPException(status_code=404, detail="车手不存在")
    update_data = driver_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_driver, field, value)
    db.commit()
    db.refresh(db_driver)
    return DriverResponse.from_orm(db_driver)


@router.delete("/{driver_id}")
async def delete_driver(driver_id: int, db: Session = Depends(get_db)):
    """
    删除车手
    """
    db_driver = db.query(Driver).filter(Driver.id == driver_id).first()
    if not db_driver:
        raise HTTPException(status_code=404, detail="车手不存在")
    db.delete(db_driver)
    db.commit()
    return {"message": "车手删除成功"} 