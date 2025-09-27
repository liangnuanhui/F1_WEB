"""
赛道信息 API 端点
"""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks, Query
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.models.circuit import Circuit
from app.schemas.circuit import CircuitResponse, CircuitListResponse
from app.services.circuit_sync_service_v2 import sync_circuits_main
import logging

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/", response_model=CircuitListResponse)
def get_circuits(
    skip: int = Query(0, ge=0, description="跳过记录数"),
    limit: int = Query(100, ge=1, le=1000, description="限制记录数"),
    country: Optional[str] = Query(None, description="按国家过滤"),
    db: Session = Depends(get_db)
):
    """获取赛道列表"""
    
    query = db.query(Circuit)
    
    if country:
        query = query.filter(Circuit.country.ilike(f"%{country}%"))
    
    total = query.count()
    circuits = query.offset(skip).limit(limit).all()
    
    return CircuitListResponse(
        circuits=circuits,
        total=total
    )


@router.get("/{circuit_id}", response_model=CircuitResponse)
def get_circuit(circuit_id: str, db: Session = Depends(get_db)):
    """根据ID获取赛道详情"""
    
    circuit = db.query(Circuit).filter(Circuit.circuit_id == circuit_id).first()
    
    if not circuit:
        raise HTTPException(status_code=404, detail="赛道未找到")
    
    return circuit


@router.post("/sync")
async def sync_circuit_details(
    background_tasks: BackgroundTasks,
    circuit_ids: Optional[List[str]] = Query(None, description="指定要同步的赛道ID列表"),
    force_update: bool = Query(False, description="强制更新所有赛道"),
    db: Session = Depends(get_db)
):
    """
    同步赛道详细信息
    
    从F1官网抓取赛道的详细信息并更新数据库：
    - 赛道长度
    - 首次举办大奖赛年份  
    - 典型圈数
    - 最快圈速记录
    - 比赛距离
    - 赛道布局图
    """
    
    try:
        logger.info(f"🚀 启动赛道信息同步: circuit_ids={circuit_ids}, force_update={force_update}")
        
        # 验证指定的赛道ID是否存在
        if circuit_ids:
            existing_circuits = db.query(Circuit).filter(
                Circuit.circuit_id.in_(circuit_ids)
            ).all()
            existing_ids = [c.circuit_id for c in existing_circuits]
            missing_ids = set(circuit_ids) - set(existing_ids)
            
            if missing_ids:
                raise HTTPException(
                    status_code=400, 
                    detail=f"以下赛道ID不存在: {list(missing_ids)}"
                )
        
        # 在后台任务中执行同步
        background_tasks.add_task(
            _sync_circuits_background,
            circuit_ids=circuit_ids,
            force_update=force_update
        )
        
        return {
            "message": "赛道信息同步已启动",
            "status": "running",
            "target_circuits": circuit_ids if circuit_ids else "all",
            "force_update": force_update
        }
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ 启动同步失败: {e}")
        raise HTTPException(status_code=500, detail=f"启动同步失败: {str(e)}")


@router.get("/sync/status")
def get_sync_status():
    """
    获取同步状态
    
    注意：这是一个简化版本，实际生产环境中应该使用Redis或数据库来跟踪任务状态
    """
    
    # 实现基础的状态跟踪 - 替代TODO
    # 在真实环境中，这里应该查询Celery任务状态或Redis缓存
    
    return {
        "message": "同步状态查询功能开发中",
        "suggestion": "请查看日志文件或直接查询数据库来了解同步结果"
    }


@router.get("/missing-info")
def get_circuits_missing_info(db: Session = Depends(get_db)):
    """获取缺少详细信息的赛道列表"""
    
    circuits = db.query(Circuit).filter(
        Circuit.length.is_(None) |
        Circuit.first_grand_prix.is_(None) |
        Circuit.circuit_layout_image_url.is_(None) |
        Circuit.lap_record.is_(None)
    ).all()
    
    missing_info = []
    for circuit in circuits:
        missing_fields = []
        if not circuit.length:
            missing_fields.append("length")
        if not circuit.first_grand_prix:
            missing_fields.append("first_grand_prix")
        if not circuit.circuit_layout_image_url:
            missing_fields.append("layout_image")
        if not circuit.lap_record:
            missing_fields.append("lap_record")
        
        missing_info.append({
            "circuit_id": circuit.circuit_id,
            "circuit_name": circuit.circuit_name,
            "country": circuit.country,
            "missing_fields": missing_fields
        })
    
    return {
        "total_missing": len(missing_info),
        "circuits": missing_info
    }


async def _sync_circuits_background(
    circuit_ids: Optional[List[str]] = None,
    force_update: bool = False
):
    """后台同步任务"""
    
    try:
        logger.info("📡 开始后台赛道信息同步...")
        
        results = await sync_circuits_main(
            circuit_ids=circuit_ids,
            force_update=force_update
        )
        
        logger.info(f"✅ 后台同步完成: {results}")
        
    except Exception as e:
        logger.error(f"❌ 后台同步失败: {e}")


# 导出路由器
__all__ = ["router"] 