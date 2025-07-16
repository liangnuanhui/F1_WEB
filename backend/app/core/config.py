"""
应用配置管理
使用 Pydantic Settings 管理环境变量
"""
from typing import List
from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """应用配置类"""
    
    # 应用基础配置
    app_name: str = Field(default="F1赛事数据网站", description="应用名称")
    app_version: str = Field(default="1.0.0", description="应用版本")
    debug: bool = Field(default=True, description="调试模式")
    environment: str = Field(default="development", description="运行环境")
    
    # 后端配置
    backend_host: str = Field(default="0.0.0.0", description="后端主机")
    backend_port: int = Field(default=8000, description="后端端口")
    api_v1_str: str = Field(default="/api/v1", description="API版本路径")
    project_name: str = Field(default="F1 Web API", description="项目名称")
    
    # 数据库配置
    database_url: str = Field(
        default="postgresql://f1_user:f1_password@localhost:5432/f1_web",
        description="数据库连接URL"
    )
    database_host: str = Field(default="localhost", description="数据库主机")
    database_port: int = Field(default=5432, description="数据库端口")
    database_name: str = Field(default="f1_web", description="数据库名称")
    database_user: str = Field(default="f1_user", description="数据库用户")
    database_password: str = Field(default="f1_password", description="数据库密码")
    
    # Redis配置
    redis_url: str = Field(
        default="redis://localhost:6379/0",
        description="Redis连接URL"
    )
    redis_host: str = Field(default="localhost", description="Redis主机")
    redis_port: int = Field(default=6379, description="Redis端口")
    redis_db: int = Field(default=0, description="Redis数据库")
    redis_password: str = Field(default="", description="Redis密码")
    
    # FastF1配置
    fastf1_cache_dir: str = Field(default="./cache", description="FastF1缓存目录")
    fastf1_logging_level: str = Field(default="INFO", description="FastF1日志级别")
    
    # Celery配置
    celery_broker_url: str = Field(
        default="redis://localhost:6379/1",
        description="Celery消息代理URL"
    )
    celery_result_backend: str = Field(
        default="redis://localhost:6379/1",
        description="Celery结果后端URL"
    )
    
    # 安全配置
    secret_key: str = Field(
        default="dev-secret-key-change-in-production",
        description="密钥"
    )
    algorithm: str = Field(default="HS256", description="加密算法")
    access_token_expire_minutes: int = Field(default=30, description="访问令牌过期时间")
    
    # CORS配置
    backend_cors_origins: List[str] = Field(
        default=[
            "http://localhost:3000",
            "http://127.0.0.1:3000",
            "http://localhost:3001",
            "http://127.0.0.1:3001",
            "https://f1-web-woad.vercel.app",
            "https://*.vercel.app",
        ],
        description="CORS允许的源",
    )
    
    # 日志配置
    log_level: str = Field(default="INFO", description="日志级别")
    log_format: str = Field(default="json", description="日志格式")
    
    # 缓存配置
    cache_ttl: int = Field(default=3600, description="缓存TTL(秒)")
    cache_prefix: str = Field(default="f1_web", description="缓存前缀")
    
    # 数据更新配置
    data_update_interval: int = Field(default=300, description="数据更新间隔(秒)")
    race_update_interval: int = Field(default=60, description="比赛更新间隔(秒)")
    cache_update_interval: int = Field(default=600, description="缓存更新间隔(秒)")
    
    # 监控配置
    sentry_dsn: str = Field(default="", description="Sentry DSN")
    prometheus_enabled: bool = Field(default=False, description="Prometheus监控启用")
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


# 创建全局配置实例
settings = Settings() 