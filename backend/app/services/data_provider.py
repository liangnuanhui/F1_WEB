"""
数据提供者抽象层
统一的 FastF1 数据提供者，根据数据类型智能选择合适的方法
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Any, Union
import pandas as pd
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class DataProvider(ABC):
    """数据提供者抽象基类"""
    
    @abstractmethod
    def get_seasons(self, start_year: int = None, end_year: int = None) -> pd.DataFrame:
        """获取赛季数据"""
        pass
    
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
        
        self.fastf1 = fastf1
        self.ergast = Ergast()
        logger.info("初始化 FastF1 数据提供者")
    
    def get_seasons(self, start_year: int = None, end_year: int = None) -> pd.DataFrame:
        """获取赛季数据"""
        try:
            seasons = self.ergast.get_seasons()
            if start_year and end_year:
                seasons = seasons[(seasons['season'] >= start_year) & (seasons['season'] <= end_year)]
            return seasons
        except Exception as e:
            logger.error(f"获取赛季数据失败: {e}")
            return pd.DataFrame()
    
    def get_circuits(self, season: int = None) -> pd.DataFrame:
        """获取赛道数据 - 使用 fastf1.ergast"""
        try:
            return self.ergast.get_circuits(season=season)
        except Exception as e:
            logger.error(f"获取赛道数据失败: {e}")
            return pd.DataFrame()
    
    def get_drivers(self, season: int = None) -> pd.DataFrame:
        """获取车手数据 - 使用 fastf1.ergast"""
        try:
            return self.ergast.get_driver_info(season=season)
        except Exception as e:
            logger.error(f"获取车手数据失败: {e}")
            return pd.DataFrame()
    
    def get_constructors(self, season: int = None) -> pd.DataFrame:
        """获取车队数据 - 使用 fastf1.ergast"""
        try:
            return self.ergast.get_constructor_info(season=season)
        except Exception as e:
            logger.error(f"获取车队数据失败: {e}")
            return pd.DataFrame()
    
    def get_races(self, season: int, round_number: int = None) -> pd.DataFrame:
        """获取比赛数据 - 使用 fastf1.get_event_schedule"""
        try:
            schedule = self.fastf1.get_event_schedule(season)
            if round_number:
                schedule = schedule[schedule.get('RoundNumber', 0) == round_number]
            return schedule
        except Exception as e:
            logger.error(f"获取比赛数据失败: {e}")
            return pd.DataFrame()
    
    def get_race_results(self, season: int, round_number: int = None) -> pd.DataFrame:
        """获取比赛结果 - 使用 fastf1.get_session"""
        try:
            schedule = self.fastf1.get_event_schedule(season)
            if round_number:
                schedule = schedule[schedule.get('RoundNumber', 0) == round_number]
            
            all_results = []
            for _, race in schedule.iterrows():
                event_name = race.get('EventName') or race.get('Event')
                try:
                    session = self.fastf1.get_session(season, event_name, 'R')
                    session.load()
                    if hasattr(session, 'results') and session.results is not None:
                        results = session.results.copy()
                        results['season'] = season
                        results['round'] = race.get('RoundNumber', 0)
                        all_results.append(results)
                except Exception as e:
                    logger.warning(f"获取 {event_name} 比赛结果时出错: {e}")
            
            return pd.concat(all_results, ignore_index=True) if all_results else pd.DataFrame()
        except Exception as e:
            logger.error(f"获取比赛结果失败: {e}")
            return pd.DataFrame()
    
    def get_qualifying_results(self, season: int, round_number: int = None) -> pd.DataFrame:
        """获取排位赛结果 - 使用 fastf1.get_session"""
        try:
            schedule = self.fastf1.get_event_schedule(season)
            if round_number:
                schedule = schedule[schedule.get('RoundNumber', 0) == round_number]
            
            all_results = []
            for _, race in schedule.iterrows():
                event_name = race.get('EventName') or race.get('Event')
                try:
                    session = self.fastf1.get_session(season, event_name, 'Q')
                    session.load()
                    if hasattr(session, 'results') and session.results is not None:
                        results = session.results.copy()
                        results['season'] = season
                        results['round'] = race.get('RoundNumber', 0)
                        all_results.append(results)
                except Exception as e:
                    logger.warning(f"获取 {event_name} 排位赛结果时出错: {e}")
            
            return pd.concat(all_results, ignore_index=True) if all_results else pd.DataFrame()
        except Exception as e:
            logger.error(f"获取排位赛结果失败: {e}")
            return pd.DataFrame()
    
    def get_driver_standings(self, season: int, round_number: int = None) -> pd.DataFrame:
        """获取车手积分榜 - 使用 fastf1.ergast"""
        try:
            standings = self.ergast.get_driver_standings(season=season, round=round_number)
            if hasattr(standings, 'content') and standings.content:
                all_results = []
                for idx, result_df in enumerate(standings.content):
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
            standings = self.ergast.get_constructor_standings(season=season, round=round_number)
            if hasattr(standings, 'content') and standings.content:
                all_results = []
                for idx, result_df in enumerate(standings.content):
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