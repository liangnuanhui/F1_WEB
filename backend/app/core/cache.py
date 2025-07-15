"""
缓存工具模块
提供Redis缓存装饰器和工具函数
"""
import json
import functools
from typing import Any, Optional, Callable
import structlog
from .redis import get_redis_client
from .config import settings

logger = structlog.get_logger()


def cache_key_builder(prefix: str, *args, **kwargs) -> str:
    """
    构建缓存键
    """
    key_parts = [settings.cache_prefix, prefix]
    
    # 添加位置参数
    if args:
        key_parts.extend([str(arg) for arg in args])
    
    # 添加关键字参数（排序后确保一致性）
    if kwargs:
        sorted_kwargs = sorted(kwargs.items())
        for k, v in sorted_kwargs:
            if v is not None:
                key_parts.append(f"{k}:{v}")
    
    return ":".join(key_parts)


def redis_cache(prefix: str, ttl: int = None):
    """
    Redis缓存装饰器
    
    Args:
        prefix: 缓存键前缀
        ttl: 过期时间（秒），默认使用配置中的cache_ttl
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            redis_client = get_redis_client()
            cache_ttl = ttl or settings.cache_ttl
            
            # 构建缓存键
            cache_key = cache_key_builder(prefix, *args, **kwargs)
            
            try:
                # 尝试从缓存获取
                cached_data = redis_client.get(cache_key)
                if cached_data:
                    logger.info("缓存命中", cache_key=cache_key)
                    return json.loads(cached_data)
                
                # 缓存未命中，执行原函数
                logger.info("缓存未命中，执行查询", cache_key=cache_key)
                result = await func(*args, **kwargs)
                
                # 存储到缓存
                redis_client.setex(
                    cache_key,
                    cache_ttl,
                    json.dumps(result, default=str, ensure_ascii=False)
                )
                logger.info("结果已缓存", cache_key=cache_key, ttl=cache_ttl)
                
                return result
                
            except Exception as e:
                logger.error("缓存操作失败", error=str(e), cache_key=cache_key)
                # 缓存失败时直接执行原函数
                return await func(*args, **kwargs)
        
        return wrapper
    return decorator


def invalidate_cache_pattern(pattern: str):
    """
    根据模式删除缓存
    """
    try:
        redis_client = get_redis_client()
        keys = redis_client.keys(f"{settings.cache_prefix}:{pattern}")
        if keys:
            redis_client.delete(*keys)
            logger.info("缓存已失效", pattern=pattern, count=len(keys))
    except Exception as e:
        logger.error("缓存失效操作失败", error=str(e), pattern=pattern)