"""
Redis连接和缓存管理
"""
import redis
from .config import settings

# 创建Redis连接池
redis_pool = redis.ConnectionPool.from_url(
    settings.redis_url,
    decode_responses=True,
    max_connections=20,
)

# 创建Redis客户端
redis_client = redis.Redis(connection_pool=redis_pool)


def get_redis():
    """
    获取Redis客户端
    使用依赖注入模式
    """
    return redis_client


def init_redis():
    """
    初始化Redis连接
    测试连接是否正常
    """
    try:
        redis_client.ping()
        print("✅ Redis连接成功")
        return True
    except redis.ConnectionError as e:
        print(f"❌ Redis连接失败: {e}")
        return False 