"""
赛道相关的 API 端点
"""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from ....api.deps import get_db
from ....models import Circuit
from ....schemas import (
    CircuitResponse,
    CircuitListResponse,
    CircuitCreate,
    CircuitUpdate,
    DataResponse,
    PaginationParams
)

router = APIRouter()


@router.get("/", response_model=DataResponse[List[CircuitResponse]])
async def get_circuits(
    db: Session = Depends(get_db),
    pagination: PaginationParams = Depends(),
    country: Optional[str] = Query(None, description="国家"),
    is_active: Optional[bool] = Query(None, description="是否激活")
):
    """
    获取赛道列表
    """
    query = db.query(Circuit)
    
    # 应用过滤条件
    if country:
        query = query.filter(Circuit.country.ilike(f"%{country}%"))
    if is_active is not None:
        query = query.filter(Circuit.is_active == is_active)
    
    # 应用排序
    if pagination.sort_by:
        sort_column = getattr(Circuit, pagination.sort_by, Circuit.name)
        if pagination.sort_order == "desc":
            sort_column = sort_column.desc()
        query = query.order_by(sort_column)
    else:
        query = query.order_by(Circuit.name)
    
    # 应用分页
    total = query.count()
    circuits = query.offset((pagination.page - 1) * pagination.size).limit(pagination.size).all()
    
    return DataResponse(
        data=[CircuitResponse.from_orm(circuit) for circuit in circuits],
        total=total,
        page=pagination.page,
        size=pagination.size
    )


@router.get("/{circuit_id}", response_model=CircuitResponse)
async def get_circuit(circuit_id: int, db: Session = Depends(get_db)):
    """
    根据ID获取赛道详情
    """
    circuit = db.query(Circuit).filter(Circuit.id == circuit_id).first()
    if not circuit:
        raise HTTPException(status_code=404, detail="赛道不存在")
    
    return CircuitResponse.from_orm(circuit)


@router.get("/by-circuit-id/{circuit_id_str}", response_model=CircuitResponse)
async def get_circuit_by_circuit_id(circuit_id_str: str, db: Session = Depends(get_db)):
    """
    根据赛道ID字符串获取赛道
    """
    circuit = db.query(Circuit).filter(Circuit.circuit_id == circuit_id_str).first()
    if not circuit:
        raise HTTPException(status_code=404, detail="赛道不存在")
    
    return CircuitResponse.from_orm(circuit)


@router.get("/country/{country}", response_model=DataResponse[List[CircuitResponse]])
async def get_circuits_by_country(
    country: str,
    db: Session = Depends(get_db),
    pagination: PaginationParams = Depends()
):
    """
    根据国家获取赛道列表
    """
    query = db.query(Circuit).filter(Circuit.country.ilike(f"%{country}%"))
    
    # 应用排序
    if pagination.sort_by:
        sort_column = getattr(Circuit, pagination.sort_by, Circuit.name)
        if pagination.sort_order == "desc":
            sort_column = sort_column.desc()
        query = query.order_by(sort_column)
    else:
        query = query.order_by(Circuit.name)
    
    # 应用分页
    total = query.count()
    circuits = query.offset((pagination.page - 1) * pagination.size).limit(pagination.size).all()
    
    return DataResponse(
        data=[CircuitResponse.from_orm(circuit) for circuit in circuits],
        total=total,
        page=pagination.page,
        size=pagination.size
    )


@router.post("/", response_model=CircuitResponse)
async def create_circuit(circuit: CircuitCreate, db: Session = Depends(get_db)):
    """
    创建新赛道
    """
    # 检查赛道ID是否已存在
    existing_circuit = db.query(Circuit).filter(Circuit.circuit_id == circuit.circuit_id).first()
    if existing_circuit:
        raise HTTPException(status_code=400, detail="赛道ID已存在")
    
    db_circuit = Circuit(**circuit.dict())
    db.add(db_circuit)
    db.commit()
    db.refresh(db_circuit)
    
    return CircuitResponse.from_orm(db_circuit)


@router.put("/{circuit_id}", response_model=CircuitResponse)
async def update_circuit(
    circuit_id: int,
    circuit_update: CircuitUpdate,
    db: Session = Depends(get_db)
):
    """
    更新赛道信息
    """
    db_circuit = db.query(Circuit).filter(Circuit.id == circuit_id).first()
    if not db_circuit:
        raise HTTPException(status_code=404, detail="赛道不存在")
    
    # 更新字段
    update_data = circuit_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_circuit, field, value)
    
    db.commit()
    db.refresh(db_circuit)
    
    return CircuitResponse.from_orm(db_circuit)


@router.delete("/{circuit_id}")
async def delete_circuit(circuit_id: int, db: Session = Depends(get_db)):
    """
    删除赛道
    """
    db_circuit = db.query(Circuit).filter(Circuit.id == circuit_id).first()
    if not db_circuit:
        raise HTTPException(status_code=404, detail="赛道不存在")
    
    db.delete(db_circuit)
    db.commit()
    
    return {"message": "赛道删除成功"} 