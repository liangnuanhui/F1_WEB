"""
API v1 路由注册
"""
from fastapi import APIRouter

from .endpoints import circuits, drivers, data_init, standings, seasons, races, constructors

api_router = APIRouter()

# 注册各个模块的路由
api_router.include_router(circuits.router, prefix="/circuits", tags=["circuits"])
api_router.include_router(drivers.router, prefix="/drivers", tags=["drivers"])
api_router.include_router(data_init.router, prefix="/data-init", tags=["data-init"])
api_router.include_router(standings.router, prefix="/standings", tags=["standings"])
api_router.include_router(seasons.router, prefix="/seasons", tags=["seasons"])
api_router.include_router(races.router, prefix="/races", tags=["races"])
api_router.include_router(constructors.router, prefix="/constructors", tags=["constructors"]) 