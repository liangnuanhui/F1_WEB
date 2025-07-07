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
    def get_circuits(self, season: Optional[int] = None) -> pd.DataFrame:
        """获取赛道数据"""
        pass
    
    @abstractmethod
    def get_drivers(self, season: Optional[int] = None) -> pd.DataFrame:
        """获取车手数据"""
        pass
    
    @abstractmethod
    def get_constructors(self, season: Optional[int] = None) -> pd.DataFrame:
        """获取车队数据"""
        pass
    
    @abstractmethod
    def get_races(self, season: int, round_number: Optional[int] = None) -> pd.DataFrame:
        """获取比赛数据"""
        pass
    
    @abstractmethod
    def get_race_results(self, season: int, round_number: Optional[int] = None) -> pd.DataFrame:
        """获取比赛结果"""
        pass
    
    @abstractmethod
    def get_qualifying_results(self, season: int, round_number: Optional[int] = None) -> pd.DataFrame:
        """获取排位赛结果"""
        pass
    
    @abstractmethod
    def get_sprint_results(self, season: int, round_number: Optional[int] = None) -> pd.DataFrame:
        """获取冲刺赛结果"""
        pass
    
    @abstractmethod
    def get_driver_standings(self, season: int, round_number: Optional[int] = None) -> pd.DataFrame:
        """获取车手积分榜"""
        pass
    
    @abstractmethod
    def get_constructor_standings(self, season: int, round_number: Optional[int] = None) -> pd.DataFrame:
        """获取车队积分榜"""
        pass

    @abstractmethod
    def get_seasons(self, start_year: Optional[int] = None, end_year: Optional[int] = None) -> pd.DataFrame:
        """获取赛季数据"""
        pass


class FastF1Provider(DataProvider):
    """统一的 FastF1 数据提供者"""
    
    def __init__(self, cache_dir: Optional[str] = None):
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
    
    def get_circuits(self, season: Optional[int] = None) -> pd.DataFrame:
        """获取赛道数据 - 使用 fastf1.ergast"""
        try:
            def _get_circuits():
                return self.ergast.get_circuits(season=season)
            
            result = self.rate_limiter.execute_with_retry(_get_circuits)
            return result if result is not None else pd.DataFrame()
        except Exception as e:
            logger.error(f"获取赛道数据失败: {e}")
            return pd.DataFrame()
    
    def get_drivers(self, season: Optional[int] = None) -> pd.DataFrame:
        """获取车手数据 - 使用 fastf1.ergast"""
        try:
            def _get_drivers():
                return self.ergast.get_driver_info(season=season)
            
            result = self.rate_limiter.execute_with_retry(_get_drivers)
            return result if result is not None else pd.DataFrame()
        except Exception as e:
            logger.error(f"获取车手数据失败: {e}")
            return pd.DataFrame()
    
    def get_constructors(self, season: Optional[int] = None) -> pd.DataFrame:
        """获取车队数据 - 使用 fastf1.ergast"""
        try:
            def _get_constructors():
                return self.ergast.get_constructor_info(season=season)
            
            result = self.rate_limiter.execute_with_retry(_get_constructors)
            return result if result is not None else pd.DataFrame()
        except Exception as e:
            logger.error(f"获取车队数据失败: {e}")
            return pd.DataFrame()
    
    def get_seasons(self, start_year: Optional[int] = None, end_year: Optional[int] = None) -> pd.DataFrame:
        """获取赛季数据 - 支持年份范围过滤，使用分页机制获取所有数据"""
        try:
            def _get_seasons():
                # 使用分页机制获取所有赛季数据
                all_seasons = []
                offset = 0
                limit = 30  # FastF1 默认限制
                
                while True:
                    # 获取当前页的赛季数据
                    seasons_page = self.ergast.get_seasons(limit=limit, offset=offset)
                    
                    if seasons_page.empty:
                        break
                    
                    all_seasons.append(seasons_page)
                    
                    # 检查是否还有更多数据
                    if seasons_page.is_complete:
                        break
                    
                    offset += limit
                
                # 合并所有页面的数据
                if all_seasons:
                    complete_seasons = pd.concat(all_seasons, ignore_index=True)
                    logger.info(f"获取到所有赛季数据，共{len(complete_seasons)}个赛季")
                else:
                    complete_seasons = pd.DataFrame()
                    logger.warning("没有获取到任何赛季数据")
                
                # 如果指定了年份范围，进行过滤
                if start_year is not None or end_year is not None:
                    # 设置默认值
                    filter_start_year = start_year if start_year is not None else (complete_seasons['season'].min() if not complete_seasons.empty else 1950)
                    filter_end_year = end_year if end_year is not None else (complete_seasons['season'].max() if not complete_seasons.empty else 2025)
                    
                    # 过滤指定年份范围的赛季
                    filtered_seasons = complete_seasons[
                        (complete_seasons['season'] >= filter_start_year) & 
                        (complete_seasons['season'] <= filter_end_year)
                    ]
                    logger.info(f"过滤赛季数据: {filter_start_year}-{filter_end_year}，共{len(filtered_seasons)}个赛季")
                    return filtered_seasons
                
                return complete_seasons
            
            result = self.rate_limiter.execute_with_retry(_get_seasons)
            return result if result is not None else pd.DataFrame()
        except Exception as e:
            logger.error(f"获取赛季数据失败: {e}")
            return pd.DataFrame()
    
    def get_races(self, season: int, round_number: Optional[int] = None) -> pd.DataFrame:
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
            
            result = self.rate_limiter.execute_with_retry(_get_races)
            return result if result is not None else pd.DataFrame()
        except Exception as e:
            logger.error(f"获取比赛数据失败: {e}")
            return pd.DataFrame()
    
    def get_race_results(self, season: int, round_number: Optional[int] = None) -> pd.DataFrame:
        """获取比赛结果 - 正确处理 ErgastMultiResponse 数据结构并支持分页"""
        try:
            def _get_race_results():
                return self.ergast.get_race_results(season=season, round=round_number)
            
            results = self.rate_limiter.execute_with_retry(_get_race_results)
            
            if results is None:
                return pd.DataFrame()
            
            # 正确处理 ErgastMultiResponse 数据结构并支持分页
            if hasattr(results, 'content') and results.content:
                all_results = []
                
                # 处理第一页数据
                for idx, result_df in enumerate(results.content):
                    if idx < len(results.description):
                        # 获取比赛描述信息
                        race_info = results.description.iloc[idx]
                        round_num = race_info['round']
                        
                        # 为结果数据添加比赛信息
                        result_df = result_df.copy()
                        result_df['season'] = season
                        result_df['round'] = round_num
                        result_df['raceName'] = race_info['raceName']
                        result_df['circuitName'] = race_info['circuitName']
                        result_df['country'] = race_info['country']
                        
                        all_results.append(result_df)
                        logger.info(f"📊 处理第 {round_num} 轮比赛: {race_info['raceName']} (第1页)")
                
                # 如果数据不完整，继续获取下一页
                current_results = results
                page_count = 1
                while hasattr(current_results, 'is_complete') and not current_results.is_complete:
                    try:
                        page_count += 1
                        logger.info(f"📄 获取第 {page_count} 页比赛结果数据...")
                        current_results = current_results.get_next_result_page()
                        
                        if hasattr(current_results, 'content') and current_results.content:
                            for idx, result_df in enumerate(current_results.content):
                                if idx < len(current_results.description):
                                    # 获取比赛描述信息
                                    race_info = current_results.description.iloc[idx]
                                    round_num = race_info['round']
                                    
                                    # 为结果数据添加比赛信息
                                    result_df = result_df.copy()
                                    result_df['season'] = season
                                    result_df['round'] = round_num
                                    result_df['raceName'] = race_info['raceName']
                                    result_df['circuitName'] = race_info['circuitName']
                                    result_df['country'] = race_info['country']
                                    
                                    all_results.append(result_df)
                                    logger.info(f"📊 处理第 {round_num} 轮比赛: {race_info['raceName']} (第{page_count}页)")
                    except ValueError:
                        # 没有更多页面了
                        break
                    except Exception as e:
                        logger.warning(f"⚠️ 获取下一页数据时出错: {e}")
                        break
                
                # 合并所有比赛的结果
                if all_results:
                    combined_results = pd.concat(all_results, ignore_index=True)
                    unique_rounds = sorted(combined_results['round'].unique())
                    logger.info(f"✅ 成功获取 {len(unique_rounds)} 场比赛的结果数据，共 {len(combined_results)} 条记录")
                    logger.info(f"🎯 包含轮次: {unique_rounds}")
                    return combined_results
                else:
                    logger.warning("⚠️ 没有比赛结果数据")
                    return pd.DataFrame()
            else:
                logger.warning("⚠️ ErgastMultiResponse 没有内容数据")
                return pd.DataFrame()
            
        except Exception as e:
            logger.error(f"获取比赛结果失败: {e}")
            return pd.DataFrame()
    
    def get_qualifying_results(self, season: int, round_number: Optional[int] = None) -> pd.DataFrame:
        """获取排位赛结果 - 正确处理 ErgastMultiResponse 数据结构并支持分页"""
        try:
            def _get_qualifying_results():
                return self.ergast.get_qualifying_results(season=season, round=round_number)
            
            results = self.rate_limiter.execute_with_retry(_get_qualifying_results)
            
            if results is None:
                return pd.DataFrame()
            
            # 正确处理 ErgastMultiResponse 数据结构并支持分页
            if hasattr(results, 'content') and results.content:
                all_results = []
                
                # 处理第一页数据
                for idx, result_df in enumerate(results.content):
                    if idx < len(results.description):
                        # 获取比赛描述信息
                        race_info = results.description.iloc[idx]
                        round_num = race_info['round']
                        
                        # 为结果数据添加比赛信息
                        result_df = result_df.copy()
                        result_df['season'] = season
                        result_df['round'] = round_num
                        result_df['raceName'] = race_info['raceName']
                        result_df['circuitName'] = race_info['circuitName']
                        result_df['country'] = race_info['country']
                        
                        all_results.append(result_df)
                        logger.info(f"📊 处理第 {round_num} 轮排位赛: {race_info['raceName']} (第1页)")
                
                # 如果数据不完整，继续获取下一页
                current_results = results
                page_count = 1
                while hasattr(current_results, 'is_complete') and not current_results.is_complete:
                    try:
                        page_count += 1
                        logger.info(f"📄 获取第 {page_count} 页排位赛结果数据...")
                        current_results = current_results.get_next_result_page()
                        
                        if hasattr(current_results, 'content') and current_results.content:
                            for idx, result_df in enumerate(current_results.content):
                                if idx < len(current_results.description):
                                    # 获取比赛描述信息
                                    race_info = current_results.description.iloc[idx]
                                    round_num = race_info['round']
                                    
                                    # 为结果数据添加比赛信息
                                    result_df = result_df.copy()
                                    result_df['season'] = season
                                    result_df['round'] = round_num
                                    result_df['raceName'] = race_info['raceName']
                                    result_df['circuitName'] = race_info['circuitName']
                                    result_df['country'] = race_info['country']
                                    
                                    all_results.append(result_df)
                                    logger.info(f"📊 处理第 {round_num} 轮排位赛: {race_info['raceName']} (第{page_count}页)")
                    except ValueError:
                        # 没有更多页面了
                        break
                    except Exception as e:
                        logger.warning(f"⚠️ 获取下一页数据时出错: {e}")
                        break
                
                # 合并所有比赛的结果
                if all_results:
                    combined_results = pd.concat(all_results, ignore_index=True)
                    unique_rounds = sorted(combined_results['round'].unique())
                    logger.info(f"✅ 成功获取 {len(unique_rounds)} 场比赛的排位赛数据，共 {len(combined_results)} 条记录")
                    logger.info(f"🎯 包含轮次: {unique_rounds}")
                    return combined_results
                else:
                    logger.warning("⚠️ 没有排位赛结果数据")
                    return pd.DataFrame()
            else:
                logger.warning("⚠️ ErgastMultiResponse 没有内容数据")
                return pd.DataFrame()
            
        except Exception as e:
            logger.error(f"获取排位赛结果失败: {e}")
            return pd.DataFrame()
    
    def get_sprint_results(self, season: int, round_number: Optional[int] = None) -> pd.DataFrame:
        """获取冲刺赛结果 - 正确处理 ErgastMultiResponse 数据结构并支持分页"""
        try:
            def _get_sprint_results():
                return self.ergast.get_sprint_results(season=season, round=round_number)
            
            results = self.rate_limiter.execute_with_retry(_get_sprint_results)
            
            if results is None:
                return pd.DataFrame()
            
            # 正确处理 ErgastMultiResponse 数据结构并支持分页
            if hasattr(results, 'content') and results.content:
                all_results = []
                
                # 处理第一页数据
                for idx, result_df in enumerate(results.content):
                    if idx < len(results.description):
                        # 获取比赛描述信息
                        race_info = results.description.iloc[idx]
                        round_num = race_info['round']
                        
                        # 为结果数据添加比赛信息
                        result_df = result_df.copy()
                        result_df['season'] = season
                        result_df['round'] = round_num
                        result_df['raceName'] = race_info['raceName']
                        result_df['circuitName'] = race_info['circuitName']
                        result_df['country'] = race_info['country']
                        
                        all_results.append(result_df)
                        logger.info(f"📊 处理第 {round_num} 轮冲刺赛: {race_info['raceName']} (第1页)")
                
                # 如果数据不完整，继续获取下一页
                current_results = results
                page_count = 1
                while hasattr(current_results, 'is_complete') and not current_results.is_complete:
                    try:
                        page_count += 1
                        logger.info(f"📄 获取第 {page_count} 页冲刺赛结果数据...")
                        current_results = current_results.get_next_result_page()
                        
                        if hasattr(current_results, 'content') and current_results.content:
                            for idx, result_df in enumerate(current_results.content):
                                if idx < len(current_results.description):
                                    # 获取比赛描述信息
                                    race_info = current_results.description.iloc[idx]
                                    round_num = race_info['round']
                                    
                                    # 为结果数据添加比赛信息
                                    result_df = result_df.copy()
                                    result_df['season'] = season
                                    result_df['round'] = round_num
                                    result_df['raceName'] = race_info['raceName']
                                    result_df['circuitName'] = race_info['circuitName']
                                    result_df['country'] = race_info['country']
                                    
                                    all_results.append(result_df)
                                    logger.info(f"📊 处理第 {round_num} 轮冲刺赛: {race_info['raceName']} (第{page_count}页)")
                    except ValueError:
                        # 没有更多页面了
                        break
                    except Exception as e:
                        logger.warning(f"⚠️ 获取下一页数据时出错: {e}")
                        break
                
                # 合并所有比赛的结果
                if all_results:
                    combined_results = pd.concat(all_results, ignore_index=True)
                    unique_rounds = sorted(combined_results['round'].unique())
                    logger.info(f"✅ 成功获取 {len(unique_rounds)} 场比赛的冲刺赛数据，共 {len(combined_results)} 条记录")
                    logger.info(f"🎯 包含轮次: {unique_rounds}")
                    return combined_results
                else:
                    logger.warning("⚠️ 没有冲刺赛结果数据")
                    return pd.DataFrame()
            else:
                logger.warning("⚠️ ErgastMultiResponse 没有内容数据")
                return pd.DataFrame()
            
        except Exception as e:
            logger.error(f"获取冲刺赛结果失败: {e}")
            return pd.DataFrame()
    
    def get_driver_standings(self, season: int, round_number: Optional[int] = None) -> pd.DataFrame:
        """获取车手积分榜 - 使用 fastf1.ergast"""
        try:
            def _get_driver_standings():
                return self.ergast.get_driver_standings(season=season, round=round_number)
            
            standings = self.rate_limiter.execute_with_retry(_get_driver_standings)
            
            if standings is None:
                return pd.DataFrame()
            
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
    
    def get_constructor_standings(self, season: int, round_number: Optional[int] = None) -> pd.DataFrame:
        """获取车队积分榜 - 使用 fastf1.ergast"""
        try:
            def _get_constructor_standings():
                return self.ergast.get_constructor_standings(season=season, round=round_number)
            
            standings = self.rate_limiter.execute_with_retry(_get_constructor_standings)
            
            if standings is None:
                return pd.DataFrame()
            
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
            cache_dir: Optional[str] = kwargs.get('cache_dir')
            return FastF1Provider(cache_dir=cache_dir)
        else:
            # 为了向后兼容，默认返回 FastF1Provider
            logger.warning(f"不支持的数据提供者类型: {provider_type}，使用默认的 FastF1Provider")
            cache_dir: Optional[str] = kwargs.get('cache_dir')
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