"""
FastAPI 主应用
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from sqlalchemy.exc import SQLAlchemyError
import structlog

from .core.config import settings
from .core.database import init_db
from .core.redis import init_redis
from .core.exceptions import (
    BaseAPIException,
    http_exception_handler,
    base_api_exception_handler,
    sqlalchemy_exception_handler,
    general_exception_handler
)

# 导入数据模型以确保数据库表被创建
from .models import Season, Circuit, Race, Driver, Constructor, Result

# 导入API路由
from .api.v1.api import api_router

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
    docs_url="/docs" if settings.debug else None,  # 生产环境禁用API文档
    redoc_url="/redoc" if settings.debug else None,
)

# 注册异常处理器
app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(BaseAPIException, base_api_exception_handler)
app.add_exception_handler(SQLAlchemyError, sqlalchemy_exception_handler)
app.add_exception_handler(Exception, general_exception_handler)

# 动态CORS配置
def get_cors_origins():
    origins = list(settings.backend_cors_origins)
    
    # 在生产环境中，使用严格的CORS配置
    if settings.environment == "production":
        # 生产环境：仅允许配置的域名
        origins.extend([])  # 移除通配符，仅使用backend_cors_origins中的域名
    else:
        # 开发环境：可以更宽松
        origins.extend([
            "http://localhost:3000",
            "http://127.0.0.1:3000"
        ])
    
    return origins

# 添加CORS中间件 - 生产环境严格配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=get_cors_origins(),
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],  # 限制允许的方法
    allow_headers=[
        "Accept",
        "Accept-Language",
        "Content-Language",
        "Content-Type",
        "Authorization",
        "X-Requested-With"
    ],  # 限制允许的头部
    expose_headers=["X-Total-Count"],  # 仅暴露必要的响应头
)

# 添加可信主机中间件
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["*"] if settings.debug else [
        "localhost",
        "127.0.0.1",
        "f1.251125.xyz",  # Caddy会转发这个Host头
        # 不需要添加VPS IP，因为请求通过Caddy代理
    ]
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


# 注册API路由
app.include_router(api_router, prefix=settings.api_v1_str)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.backend_host,
        port=settings.backend_port,
        reload=settings.debug,
        log_level=settings.log_level.lower()
    ) 