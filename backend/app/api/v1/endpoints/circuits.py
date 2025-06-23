"""
赛道相关的 API 端点
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.models.circuit import Circuit
from app.schemas.circuit import CircuitResponse
from app.schemas.base import ApiResponse

router = APIRouter()


@router.get("/", response_model=ApiResponse[List[CircuitResponse]])
async def get_circuits(
    db: Session = Depends(get_db),
    page: int = Query(1, ge=1, description="页码"),
    size: int = Query(20, ge=1, le=100, description="每页数量"),
):
    """
    获取赛道列表
    """
    try:
        offset = (page - 1) * size
        circuits = db.query(Circuit).offset(offset).limit(size).all()
        circuit_list = []
        for circuit in circuits:
            circuit_data = {
                "circuit_id": circuit.circuit_id,
                "circuit_url": circuit.circuit_url,
                "circuit_name": circuit.circuit_name,
                "lat": circuit.lat,
                "long": circuit.long,
                "locality": circuit.locality,
                "country": circuit.country,
                "length": circuit.length,
                "corners": circuit.corners,
                "lap_record": circuit.lap_record,
                "lap_record_driver": circuit.lap_record_driver,
                "lap_record_year": circuit.lap_record_year,
                "description": circuit.description,
                "characteristics": circuit.characteristics,
                "is_active": circuit.is_active,
            }
            circuit_list.append(circuit_data)
        return ApiResponse(
            success=True,
            message="获取赛道列表成功",
            data=circuit_list
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取赛道列表失败: {str(e)}")


@router.get("/{circuit_id}", response_model=ApiResponse[CircuitResponse])
async def get_circuit(circuit_id: str, db: Session = Depends(get_db)):
    """
    根据ID获取赛道详情
    """
    try:
        circuit = db.query(Circuit).filter(Circuit.circuit_id == circuit_id).first()
        if not circuit:
            raise HTTPException(status_code=404, detail="赛道不存在")
        circuit_data = {
            "circuit_id": circuit.circuit_id,
            "circuit_url": circuit.circuit_url,
            "circuit_name": circuit.circuit_name,
            "lat": circuit.lat,
            "long": circuit.long,
            "locality": circuit.locality,
            "country": circuit.country,
            "length": circuit.length,
            "corners": circuit.corners,
            "lap_record": circuit.lap_record,
            "lap_record_driver": circuit.lap_record_driver,
            "lap_record_year": circuit.lap_record_year,
            "description": circuit.description,
            "characteristics": circuit.characteristics,
            "is_active": circuit.is_active,
        }
        return ApiResponse(
            success=True,
            message="获取赛道详情成功",
            data=circuit_data
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取赛道详情失败: {str(e)}") 