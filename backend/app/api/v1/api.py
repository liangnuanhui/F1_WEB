"""
API v1 路由汇总
"""

from fastapi import APIRouter

from .endpoints import (
    seasons,
    circuits,
    constructors,
    drivers,
    races,
    standings,
    data_init,
    scheduler,  # 新增调度器端点
    post_race_sync,  # 比赛后数据同步端点
)

api_router = APIRouter()

# 注册各个模块的路由
api_router.include_router(circuits.router, prefix="/circuits", tags=["circuits"])
api_router.include_router(drivers.router, prefix="/drivers", tags=["drivers"])
api_router.include_router(data_init.router, prefix="/data", tags=["data-initialization"])
api_router.include_router(standings.router, prefix="/standings", tags=["standings"])
api_router.include_router(seasons.router, prefix="/seasons", tags=["seasons"])
api_router.include_router(races.router, prefix="/races", tags=["races"])
api_router.include_router(constructors.router, prefix="/constructors", tags=["constructors"])
api_router.include_router(scheduler.router, prefix="/scheduler", tags=["scheduler"])  # 新增
api_router.include_router(post_race_sync.router, prefix="/post-race-sync", tags=["post-race-sync"])  # 比赛后同步 