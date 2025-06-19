"""
FastAPI 主应用
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
import structlog

from .core.config import settings
from .core.database import init_db
from .core.redis import init_redis

# 配置结构化日志
structlog.configure(
    processors=[
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
        structlog.processors.JSONRenderer()
    ],
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
    wrapper_class=structlog.stdlib.BoundLogger,
    cache_logger_on_first_use=True,
)

logger = structlog.get_logger()

# 创建FastAPI应用实例
app = FastAPI(
    title=settings.project_name,
    version=settings.app_version,
    description="F1赛事数据网站后端API",
    docs_url="/docs" if settings.debug else None,
    redoc_url="/redoc" if settings.debug else None,
)

# 添加CORS中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.backend_cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 添加可信主机中间件
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["*"] if settings.debug else ["localhost", "127.0.0.1"]
)


@app.on_event("startup")
async def startup_event():
    """应用启动事件"""
    logger.info("🚀 启动F1 Web后端服务")
    
    # 初始化数据库
    try:
        init_db()
        logger.info("✅ 数据库初始化成功")
    except Exception as e:
        logger.error(f"❌ 数据库初始化失败: {e}")
    
    # 初始化Redis
    try:
        init_redis()
        logger.info("✅ Redis初始化成功")
    except Exception as e:
        logger.error(f"❌ Redis初始化失败: {e}")


@app.on_event("shutdown")
async def shutdown_event():
    """应用关闭事件"""
    logger.info("🛑 关闭F1 Web后端服务")


@app.get("/")
async def root():
    """根路径"""
    return {
        "message": "F1赛事数据网站API",
        "version": settings.app_version,
        "status": "running"
    }


@app.get("/health")
async def health_check():
    """健康检查"""
    return {
        "status": "healthy",
        "version": settings.app_version,
        "environment": settings.environment
    }


# 导入API路由
# from .api.v1.endpoints import schedule, races, drivers, constructors, circuits, results, standings

# 注册API路由
# app.include_router(schedule.router, prefix=settings.api_v1_str, tags=["schedule"])
# app.include_router(races.router, prefix=settings.api_v1_str, tags=["races"])
# app.include_router(drivers.router, prefix=settings.api_v1_str, tags=["drivers"])
# app.include_router(constructors.router, prefix=settings.api_v1_str, tags=["constructors"])
# app.include_router(circuits.router, prefix=settings.api_v1_str, tags=["circuits"])
# app.include_router(results.router, prefix=settings.api_v1_str, tags=["results"])
# app.include_router(standings.router, prefix=settings.api_v1_str, tags=["standings"])


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.backend_host,
        port=settings.backend_port,
        reload=settings.debug,
        log_level=settings.log_level.lower()
    ) 