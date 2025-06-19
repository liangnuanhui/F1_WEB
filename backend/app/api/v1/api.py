"""
API v1 路由注册
"""
from fastapi import APIRouter

from .endpoints import seasons, circuits

api_router = APIRouter()

# 注册各个模块的路由
api_router.include_router(seasons.router, prefix="/seasons", tags=["seasons"])
api_router.include_router(circuits.router, prefix="/circuits", tags=["circuits"]) 