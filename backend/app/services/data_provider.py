"""
数据提供者抽象层
统一的 FastF1 数据提供者，根据数据类型智能选择合适的方法
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Any, Union
import pandas as pd
from datetime import datetime
import logging
import time

logger = logging.getLogger(__name__)


class RateLimitHandler:
    """API频率限制处理器"""
    
    def __init__(self, delay_seconds: float = 1.0, max_retries: int = 3):
        self.delay_seconds = delay_seconds
        self.max_retries = max_retries
        self.request_count = 0
        self.last_request_time = 0
        
    def execute_with_retry(self, func, *args, **kwargs):
        """执行函数并处理频率限制"""
        for attempt in range(self.max_retries):
            try:
                # 智能延迟：根据请求类型调整延迟
                if attempt > 0:
                    # 递增延迟策略
                    delay = self.delay_seconds * (2 ** attempt)
                    logger.info(f"等待 {delay} 秒后重试...")
                    time.sleep(delay)
                else:
                    # 基础延迟，避免过于频繁的请求
                    if self.request_count > 0:
                        time.sleep(self.delay_seconds * 0.5)
                
                result = func(*args, **kwargs)
                
                # 更新请求统计
                self.request_count += 1
                self.last_request_time = time.time()
                
                # 成功后添加基础延迟
                if self.delay_seconds > 0:
                    time.sleep(self.delay_seconds)
                
                return result
                
            except Exception as e:
                error_str = str(e).lower()
                if 'rate' in error_str or 'limit' in error_str or '500 calls' in error_str:
                    logger.warning(f"遇到API频率限制，尝试 {attempt + 1}/{self.max_retries}: {e}")
                    if attempt == self.max_retries - 1:
                        logger.error("达到最大重试次数，放弃")
                        raise
                else:
                    # 非频率限制错误，直接抛出
                    raise
        
        return None


class DataProvider(ABC):
    """数据提供者抽象基类"""
    
    @abstractmethod
    def get_circuits(self, season: int = None) -> pd.DataFrame:
        """获取赛道数据"""
        pass
    
    @abstractmethod
    def get_drivers(self, season: int = None) -> pd.DataFrame:
        """获取车手数据"""
        pass
    
    @abstractmethod
    def get_constructors(self, season: int = None) -> pd.DataFrame:
        """获取车队数据"""
        pass
    
    @abstractmethod
    def get_races(self, season: int, round_number: int = None) -> pd.DataFrame:
        """获取比赛数据"""
        pass
    
    @abstractmethod
    def get_race_results(self, season: int, round_number: int = None) -> pd.DataFrame:
        """获取比赛结果"""
        pass
    
    @abstractmethod
    def get_qualifying_results(self, season: int, round_number: int = None) -> pd.DataFrame:
        """获取排位赛结果"""
        pass
    
    @abstractmethod
    def get_driver_standings(self, season: int, round_number: int = None) -> pd.DataFrame:
        """获取车手积分榜"""
        pass
    
    @abstractmethod
    def get_constructor_standings(self, season: int, round_number: int = None) -> pd.DataFrame:
        """获取车队积分榜"""
        pass


class FastF1Provider(DataProvider):
    """统一的 FastF1 数据提供者"""
    
    def __init__(self, cache_dir: str = None):
        import fastf1
        from fastf1.ergast import Ergast
        
        if cache_dir:
            fastf1.Cache.enable_cache(cache_dir)
            logger.info(f"启用 FastF1 缓存目录: {cache_dir}")
        
        self.fastf1 = fastf1
        self.ergast = Ergast()
        
        # 为2025赛季优化频率限制配置
        self.rate_limiter = RateLimitHandler(delay_seconds=1.0, max_retries=3)
        
        # 设置FastF1配置
        fastf1.set_log_level('WARNING')  # 减少日志输出
        
        logger.info("初始化 FastF1 数据提供者，启用频率限制处理")
        logger.info("当前配置: 延迟1.0秒，最大重试3次")
    
    def get_circuits(self, season: int = None) -> pd.DataFrame:
        """获取赛道数据 - 使用 fastf1.ergast"""
        try:
            def _get_circuits():
                return self.ergast.get_circuits(season=season)
            
            return self.rate_limiter.execute_with_retry(_get_circuits)
        except Exception as e:
            logger.error(f"获取赛道数据失败: {e}")
            return pd.DataFrame()
    
    def get_drivers(self, season: int = None) -> pd.DataFrame:
        """获取车手数据 - 使用 fastf1.ergast"""
        try:
            def _get_drivers():
                return self.ergast.get_driver_info(season=season)
            
            return self.rate_limiter.execute_with_retry(_get_drivers)
        except Exception as e:
            logger.error(f"获取车手数据失败: {e}")
            return pd.DataFrame()
    
    def get_constructors(self, season: int = None) -> pd.DataFrame:
        """获取车队数据 - 使用 fastf1.ergast"""
        try:
            def _get_constructors():
                return self.ergast.get_constructor_info(season=season)
            
            return self.rate_limiter.execute_with_retry(_get_constructors)
        except Exception as e:
            logger.error(f"获取车队数据失败: {e}")
            return pd.DataFrame()
    
    def get_races(self, season: int, round_number: int = None) -> pd.DataFrame:
        """获取比赛数据 - 优先使用 FastF1，失败时降级到 Ergast"""
        try:
            def _get_races():
                # 优先使用 FastF1 获取详细日程
                try:
                    logger.info(f"尝试使用 FastF1 获取 {season} 赛季比赛日程...")
                    schedule = self.fastf1.get_event_schedule(season)
                    
                    if not schedule.empty:
                        logger.info(f"✅ FastF1 获取成功，共{len(schedule)}条记录")
                        
                        # 如果指定了轮次，过滤出指定轮次的比赛
                        if round_number is not None:
                            schedule = schedule[schedule.get('RoundNumber', 0) == round_number]
                            logger.info(f"过滤轮次 {round_number}，剩余{len(schedule)}条记录")
                        
                        return schedule
                    else:
                        logger.warning("FastF1 返回空数据，尝试 Ergast...")
                        raise Exception("FastF1 返回空数据")
                        
                except Exception as e:
                    logger.warning(f"FastF1 获取失败: {e}，降级到 Ergast...")
                    
                    # 降级到 Ergast
                    try:
                        schedule = self.ergast.get_race_schedule(season=season)
                        
                        if not schedule.empty:
                            logger.info(f"✅ Ergast 获取成功，共{len(schedule)}条记录")
                            
                            # 如果指定了轮次，过滤出指定轮次的比赛
                            if round_number is not None:
                                schedule = schedule[schedule.get('round', 0) == round_number]
                                logger.info(f"过滤轮次 {round_number}，剩余{len(schedule)}条记录")
                            
                            return schedule
                        else:
                            logger.error("Ergast 也返回空数据")
                            return pd.DataFrame()
                            
                    except Exception as ergast_error:
                        logger.error(f"Ergast 获取也失败: {ergast_error}")
                        return pd.DataFrame()
            
            return self.rate_limiter.execute_with_retry(_get_races)
        except Exception as e:
            logger.error(f"获取比赛数据失败: {e}")
            return pd.DataFrame()
    
    def get_race_results(self, season: int, round_number: int = None) -> pd.DataFrame:
        """获取比赛结果 - 使用 fastf1.ergast（避免session.load()）"""
        try:
            def _get_race_results():
                return self.ergast.get_race_results(season=season, round=round_number)
            
            results = self.rate_limiter.execute_with_retry(_get_race_results)
            
            # 处理Ergast返回的数据结构
            if hasattr(results, 'content') and results.content:
                all_results = []
                for idx, result_df in enumerate(results.content):
                    if idx < len(results.description):
                        race_info = results.description.iloc[idx]
                        result_df['season'] = season
                        result_df['round'] = race_info['round']
                        all_results.append(result_df)
                return pd.concat(all_results, ignore_index=True) if all_results else pd.DataFrame()
            
            return pd.DataFrame()
        except Exception as e:
            logger.error(f"获取比赛结果失败: {e}")
            return pd.DataFrame()
    
    def get_qualifying_results(self, season: int, round_number: int = None) -> pd.DataFrame:
        """获取排位赛结果 - 使用 fastf1.ergast（避免session.load()）"""
        try:
            def _get_qualifying_results():
                return self.ergast.get_qualifying_results(season=season, round=round_number)
            
            results = self.rate_limiter.execute_with_retry(_get_qualifying_results)
            
            # 处理Ergast返回的数据结构
            if hasattr(results, 'content') and results.content:
                all_results = []
                for idx, result_df in enumerate(results.content):
                    if idx < len(results.description):
                        race_info = results.description.iloc[idx]
                        result_df['season'] = season
                        result_df['round'] = race_info['round']
                        all_results.append(result_df)
                return pd.concat(all_results, ignore_index=True) if all_results else pd.DataFrame()
            
            return pd.DataFrame()
        except Exception as e:
            logger.error(f"获取排位赛结果失败: {e}")
            return pd.DataFrame()
    
    def get_driver_standings(self, season: int, round_number: int = None) -> pd.DataFrame:
        """获取车手积分榜 - 使用 fastf1.ergast"""
        try:
            def _get_driver_standings():
                return self.ergast.get_driver_standings(season=season, round=round_number)
            
            standings = self.rate_limiter.execute_with_retry(_get_driver_standings)
            
            if hasattr(standings, 'content') and standings.content:
                all_results = []
                for idx, result_df in enumerate(standings.content):
                    if idx < len(standings.description):
                        race_info = standings.description.iloc[idx]
                        result_df['season'] = season
                        result_df['round'] = race_info['round']
                        all_results.append(result_df)
                return pd.concat(all_results, ignore_index=True) if all_results else pd.DataFrame()
            return pd.DataFrame()
        except Exception as e:
            logger.error(f"获取车手积分榜失败: {e}")
            return pd.DataFrame()
    
    def get_constructor_standings(self, season: int, round_number: int = None) -> pd.DataFrame:
        """获取车队积分榜 - 使用 fastf1.ergast"""
        try:
            def _get_constructor_standings():
                return self.ergast.get_constructor_standings(season=season, round=round_number)
            
            standings = self.rate_limiter.execute_with_retry(_get_constructor_standings)
            
            if hasattr(standings, 'content') and standings.content:
                all_results = []
                for idx, result_df in enumerate(standings.content):
                    if idx < len(standings.description):
                        race_info = standings.description.iloc[idx]
                        result_df['season'] = season
                        result_df['round'] = race_info['round']
                        all_results.append(result_df)
                return pd.concat(all_results, ignore_index=True) if all_results else pd.DataFrame()
            return pd.DataFrame()
        except Exception as e:
            logger.error(f"获取车队积分榜失败: {e}")
            return pd.DataFrame()


class DataProviderFactory:
    """数据提供者工厂"""
    
    @staticmethod
    def get_provider(provider_type: str = 'fastf1', **kwargs) -> DataProvider:
        """
        获取数据提供者实例
        
        Args:
            provider_type: 提供者类型 (目前只支持 'fastf1')
            **kwargs: 额外参数
        """
        if provider_type.lower() == 'fastf1':
            cache_dir = kwargs.get('cache_dir')
            return FastF1Provider(cache_dir=cache_dir)
        else:
            # 为了向后兼容，默认返回 FastF1Provider
            logger.warning(f"不支持的数据提供者类型: {provider_type}，使用默认的 FastF1Provider")
            cache_dir = kwargs.get('cache_dir')
            return FastF1Provider(cache_dir=cache_dir)
    
    @staticmethod
    def get_multi_provider(providers: List[str], **kwargs) -> Dict[str, DataProvider]:
        """
        获取多个数据提供者实例
        
        Args:
            providers: 提供者类型列表
            **kwargs: 额外参数
        """
        result = {}
        for provider_type in providers:
            result[provider_type] = DataProviderFactory.get_provider(provider_type, **kwargs)
        return result 