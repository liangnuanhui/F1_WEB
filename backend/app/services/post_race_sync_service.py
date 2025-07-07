"""
比赛后数据同步服务
在比赛结束后的指定时间点自动同步5个核心数据：
1. 比赛结果 (race results)
2. 排位赛结果 (qualifying results)  
3. 冲刺赛结果 (sprint results)
4. 车手积分榜 (driver standings)
5. 车队积分榜 (constructor standings)
"""

import logging
from typing import Dict, List, Optional, Tuple, Any
from datetime import datetime, timedelta, timezone
from dataclasses import dataclass
from enum import Enum
import json

from sqlalchemy.orm import Session
from ..core.redis import get_redis_client
from ..models import Race, Season
from .unified_sync_service import UnifiedSyncService

logger = logging.getLogger(__name__)


class SyncStatus(Enum):
    """同步状态枚举"""
    PENDING = "pending"          # 等待同步
    RUNNING = "running"          # 正在同步
    SUCCESS = "success"          # 同步成功
    PARTIAL_SUCCESS = "partial"  # 部分成功
    FAILED = "failed"            # 同步失败
    CANCELLED = "cancelled"      # 已取消


@dataclass
class SyncAttempt:
    """同步尝试记录"""
    attempt_number: int
    scheduled_time: datetime
    executed_time: Optional[datetime] = None
    status: SyncStatus = SyncStatus.PENDING
    results: Optional[Dict[str, bool]] = None
    error_message: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典格式用于存储"""
        return {
            "attempt_number": self.attempt_number,
            "scheduled_time": self.scheduled_time.isoformat(),
            "executed_time": self.executed_time.isoformat() if self.executed_time else None,
            "status": self.status.value,
            "results": self.results or {},
            "error_message": self.error_message
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'SyncAttempt':
        """从字典格式创建实例"""
        scheduled_time = datetime.fromisoformat(data["scheduled_time"])
        if scheduled_time.tzinfo is None:
            scheduled_time = scheduled_time.replace(tzinfo=timezone.utc)
        
        executed_time = None
        if data.get("executed_time"):
            executed_time = datetime.fromisoformat(data["executed_time"])
            if executed_time.tzinfo is None:
                executed_time = executed_time.replace(tzinfo=timezone.utc)
        
        return cls(
            attempt_number=data["attempt_number"],
            scheduled_time=scheduled_time,
            executed_time=executed_time,
            status=SyncStatus(data["status"]),
            results=data.get("results", {}),
            error_message=data.get("error_message")
        )


@dataclass
class PostRaceSchedule:
    """比赛后同步计划"""
    season_year: int
    race_round: int
    race_name: str
    race_end_time: datetime
    attempts: List[SyncAttempt]
    created_at: datetime
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典格式用于存储"""
        return {
            "season_year": self.season_year,
            "race_round": self.race_round,
            "race_name": self.race_name,
            "race_end_time": self.race_end_time.isoformat(),
            "attempts": [attempt.to_dict() for attempt in self.attempts],
            "created_at": self.created_at.isoformat()
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'PostRaceSchedule':
        """从字典格式创建实例"""
        race_end_time = datetime.fromisoformat(data["race_end_time"])
        if race_end_time.tzinfo is None:
            race_end_time = race_end_time.replace(tzinfo=timezone.utc)
        
        created_at = datetime.fromisoformat(data["created_at"])
        if created_at.tzinfo is None:
            created_at = created_at.replace(tzinfo=timezone.utc)
        
        return cls(
            season_year=data["season_year"],
            race_round=data["race_round"],
            race_name=data["race_name"],
            race_end_time=race_end_time,
            attempts=[SyncAttempt.from_dict(attempt_data) for attempt_data in data["attempts"]],
            created_at=created_at
        )
    
    @property
    def next_pending_attempt(self) -> Optional[SyncAttempt]:
        """获取下一个待执行的同步尝试"""
        for attempt in self.attempts:
            if attempt.status == SyncStatus.PENDING:
                return attempt
        return None
    
    @property
    def is_completed(self) -> bool:
        """检查是否已完成所有同步"""
        return any(attempt.status == SyncStatus.SUCCESS for attempt in self.attempts)
    
    @property
    def success_rate(self) -> float:
        """获取成功率"""
        completed_attempts = [a for a in self.attempts if a.status in [SyncStatus.SUCCESS, SyncStatus.PARTIAL_SUCCESS, SyncStatus.FAILED]]
        if not completed_attempts:
            return 0.0
        successful_attempts = [a for a in completed_attempts if a.status in [SyncStatus.SUCCESS, SyncStatus.PARTIAL_SUCCESS]]
        return len(successful_attempts) / len(completed_attempts)


class PostRaceSyncService:
    """比赛后数据同步服务"""
    
    # 同步的数据类型
    SYNC_DATA_TYPES = [
        "race_results",
        "qualifying_results", 
        "sprint_results",
        "driver_standings",
        "constructor_standings"
    ]
    
    # 默认重试时间点：比赛结束后6小时、12小时、24小时
    DEFAULT_RETRY_INTERVALS = [6, 12, 24]  # 小时
    
    def __init__(self, db: Session, cache_dir: Optional[str] = None):
        self.db = db
        self.redis_client = get_redis_client()
        self.sync_service = UnifiedSyncService(db, cache_dir)
        self.redis_key_prefix = "post_race_sync"
        
        logger.info("🏁 初始化比赛后数据同步服务")
    
    def _get_redis_key(self, season_year: int, race_round: int) -> str:
        """生成Redis存储键"""
        return f"{self.redis_key_prefix}:{season_year}:{race_round}"
    
    def schedule_post_race_sync(
        self, 
        race: Race, 
        retry_intervals: Optional[List[int]] = None
    ) -> PostRaceSchedule:
        """
        为比赛安排赛后数据同步
        
        Args:
            race: 比赛对象
            retry_intervals: 重试间隔时间（小时），默认[6, 12, 24]
        
        Returns:
            PostRaceSchedule: 同步计划
        """
        if retry_intervals is None:
            retry_intervals = self.DEFAULT_RETRY_INTERVALS
        
        # 计算比赛结束时间
        race_end_time = self._estimate_race_end_time(race)
        if not race_end_time:
            raise ValueError(f"无法确定比赛 {race.official_event_name} 的结束时间")
        
        # 创建同步尝试
        attempts = []
        for i, interval_hours in enumerate(retry_intervals, 1):
            scheduled_time = race_end_time + timedelta(hours=interval_hours)
            attempt = SyncAttempt(
                attempt_number=i,
                scheduled_time=scheduled_time
            )
            attempts.append(attempt)
        
        # 创建同步计划
        schedule = PostRaceSchedule(
            season_year=race.season.year,
            race_round=race.round_number,
            race_name=race.official_event_name,
            race_end_time=race_end_time,
            attempts=attempts,
            created_at=datetime.now(timezone.utc)
        )
        
        # 存储到Redis
        self._save_schedule(schedule)
        
        logger.info(
            f"✅ 已安排比赛 {race.official_event_name} 的数据同步计划\n"
            f"   比赛结束时间: {race_end_time}\n"
            f"   同步时间点: {[a.scheduled_time for a in attempts]}"
        )
        
        return schedule
    
    def _estimate_race_end_time(self, race: Race) -> Optional[datetime]:
        """
        估算比赛结束时间
        
        优先级：
        1. session5_date (通常是正赛时间) + 3小时
        2. session4_date (通常是排位赛时间) + 1天
        3. event_date + 3小时
        """
        if race.session5_date:
            # 正赛时间 + 3小时估算
            race_end = race.session5_date + timedelta(hours=3)
            # 确保有时区信息
            if race_end.tzinfo is None:
                race_end = race_end.replace(tzinfo=timezone.utc)
            return race_end
        elif race.session4_date:
            # 排位赛时间 + 1天（假设第二天是正赛）
            race_end = race.session4_date + timedelta(days=1, hours=3)
            if race_end.tzinfo is None:
                race_end = race_end.replace(tzinfo=timezone.utc)
            return race_end
        elif race.event_date:
            # 使用事件日期 + 3小时
            race_end = datetime.combine(race.event_date, datetime.min.time()) + timedelta(hours=15)  # 假设比赛在下午3点结束
            if race_end.tzinfo is None:
                race_end = race_end.replace(tzinfo=timezone.utc)
            return race_end
        else:
            logger.warning(f"比赛 {race.official_event_name} 没有有效的时间信息")
            return None
    
    def _save_schedule(self, schedule: PostRaceSchedule):
        """保存同步计划到Redis"""
        redis_key = self._get_redis_key(schedule.season_year, schedule.race_round)
        
        # 设置过期时间：最后一次尝试后1周
        last_attempt_time = max(attempt.scheduled_time for attempt in schedule.attempts)
        
        # 确保时间都有时区信息
        if last_attempt_time.tzinfo is None:
            last_attempt_time = last_attempt_time.replace(tzinfo=timezone.utc)
        
        now = datetime.now(timezone.utc)
        time_diff = (last_attempt_time - now).total_seconds()
        expire_seconds = int(time_diff) + 604800  # +1周
        
        self.redis_client.setex(
            redis_key,
            max(expire_seconds, 3600),  # 至少1小时
            json.dumps(schedule.to_dict())
        )
    
    def get_schedule(self, season_year: int, race_round: int) -> Optional[PostRaceSchedule]:
        """获取同步计划"""
        redis_key = self._get_redis_key(season_year, race_round)
        data = self.redis_client.get(redis_key)
        
        if data:
            try:
                # 处理Redis返回的数据类型差异
                if isinstance(data, bytes):
                    data_str = data.decode('utf-8')
                else:
                    data_str = data
                    
                schedule_dict = json.loads(data_str)
                return PostRaceSchedule.from_dict(schedule_dict)
            except Exception as e:
                logger.error(f"解析同步计划失败: {e}")
        
        return None
    
    def execute_sync_attempt(
        self, 
        season_year: int, 
        race_round: int, 
        attempt_number: int
    ) -> Tuple[SyncStatus, Dict[str, bool]]:
        """
        执行同步尝试
        
        Returns:
            Tuple[SyncStatus, Dict[str, bool]]: (整体状态, 各数据类型同步结果)
        """
        logger.info(f"🔄 开始执行 {season_year} 赛季第 {race_round} 轮的第 {attempt_number} 次同步...")
        
        # 获取同步计划
        schedule = self.get_schedule(season_year, race_round)
        if not schedule:
            logger.error(f"未找到 {season_year} 赛季第 {race_round} 轮的同步计划")
            return SyncStatus.FAILED, {}
        
        # 找到对应的尝试
        attempt = next(
            (a for a in schedule.attempts if a.attempt_number == attempt_number),
            None
        )
        if not attempt:
            logger.error(f"未找到第 {attempt_number} 次尝试")
            return SyncStatus.FAILED, {}
        
        # 更新尝试状态
        attempt.status = SyncStatus.RUNNING
        attempt.executed_time = datetime.now(timezone.utc)
        self._save_schedule(schedule)
        
        # 执行同步
        sync_results = {}
        try:
            # 1. 同步比赛结果
            sync_results["race_results"] = self.sync_service.sync_race_results(season_year)
            
            # 2. 同步排位赛结果
            sync_results["qualifying_results"] = self.sync_service.sync_qualifying_results(season_year)
            
            # 3. 同步冲刺赛结果（如果有的话）
            sync_results["sprint_results"] = self.sync_service.sync_sprint_results(season_year)
            
            # 4. 同步车手积分榜
            sync_results["driver_standings"] = self.sync_service.sync_driver_standings(season_year)
            
            # 5. 同步车队积分榜
            sync_results["constructor_standings"] = self.sync_service.sync_constructor_standings(season_year)
            
            # 判断整体状态
            successful_count = sum(1 for success in sync_results.values() if success)
            total_count = len(sync_results)
            
            if successful_count == total_count:
                overall_status = SyncStatus.SUCCESS
            elif successful_count > 0:
                overall_status = SyncStatus.PARTIAL_SUCCESS
            else:
                overall_status = SyncStatus.FAILED
            
            # 更新尝试结果
            attempt.status = overall_status
            attempt.results = sync_results
            
            logger.info(
                f"✅ 第 {attempt_number} 次同步完成\n"
                f"   成功: {successful_count}/{total_count}\n"
                f"   详细结果: {sync_results}"
            )
            
        except Exception as e:
            logger.error(f"❌ 第 {attempt_number} 次同步失败: {e}")
            attempt.status = SyncStatus.FAILED
            attempt.error_message = str(e)
            overall_status = SyncStatus.FAILED
            
        finally:
            # 保存更新后的计划
            self._save_schedule(schedule)
        
        return overall_status, sync_results
    
    def get_pending_syncs(self) -> List[Tuple[int, int, int, datetime]]:
        """
        获取所有待执行的同步任务
        
        Returns:
            List[Tuple[season_year, race_round, attempt_number, scheduled_time]]
        """
        pattern = f"{self.redis_key_prefix}:*"
        keys = self.redis_client.keys(pattern)
        
        pending_syncs = []
        now = datetime.now(timezone.utc)
        
        for key in keys:
            try:
                data = self.redis_client.get(key)
                if not data:
                    continue
                
                # 处理Redis返回的数据类型差异
                if isinstance(data, bytes):
                    data_str = data.decode('utf-8')
                else:
                    data_str = data
                    
                schedule_dict = json.loads(data_str)
                schedule = PostRaceSchedule.from_dict(schedule_dict)
                
                # 查找待执行的尝试
                for attempt in schedule.attempts:
                    if (attempt.status == SyncStatus.PENDING and 
                        attempt.scheduled_time <= now):
                        pending_syncs.append((
                            schedule.season_year,
                            schedule.race_round,
                            attempt.attempt_number,
                            attempt.scheduled_time
                        ))
                        
            except Exception as e:
                logger.warning(f"解析同步计划失败: {e}")
                continue
        
        # 按时间排序
        pending_syncs.sort(key=lambda x: x[3])
        return pending_syncs
    
    def cancel_schedule(self, season_year: int, race_round: int) -> bool:
        """取消同步计划"""
        redis_key = self._get_redis_key(season_year, race_round)
        
        schedule = self.get_schedule(season_year, race_round)
        if schedule:
            # 将所有待执行的尝试标记为已取消
            for attempt in schedule.attempts:
                if attempt.status == SyncStatus.PENDING:
                    attempt.status = SyncStatus.CANCELLED
            
            self._save_schedule(schedule)
            logger.info(f"✅ 已取消 {season_year} 赛季第 {race_round} 轮的同步计划")
            return True
        
        return False
    
    def get_all_schedules(self) -> List[PostRaceSchedule]:
        """获取所有同步计划"""
        pattern = f"{self.redis_key_prefix}:*"
        keys = self.redis_client.keys(pattern)
        
        schedules = []
        for key in keys:
            try:
                data = self.redis_client.get(key)
                if data:
                    # 处理Redis返回的数据类型差异
                    if isinstance(data, bytes):
                        data_str = data.decode('utf-8')
                    else:
                        data_str = data
                        
                    schedule_dict = json.loads(data_str)
                    schedule = PostRaceSchedule.from_dict(schedule_dict)
                    schedules.append(schedule)
            except Exception as e:
                logger.warning(f"解析同步计划失败: {e}")
                continue
        
        # 按赛季和轮次排序
        schedules.sort(key=lambda s: (s.season_year, s.race_round))
        return schedules
    
    def cleanup_expired_schedules(self) -> int:
        """清理过期的同步计划"""
        pattern = f"{self.redis_key_prefix}:*"
        keys = self.redis_client.keys(pattern)
        
        cleaned_count = 0
        now = datetime.now(timezone.utc)
        
        for key in keys:
            try:
                data = self.redis_client.get(key)
                if not data:
                    continue
                
                # 处理Redis返回的数据类型差异
                if isinstance(data, bytes):
                    data_str = data.decode('utf-8')
                else:
                    data_str = data
                    
                schedule_dict = json.loads(data_str)
                schedule = PostRaceSchedule.from_dict(schedule_dict)
                
                # 检查是否所有尝试都已完成且超过1周
                last_attempt_time = max(attempt.scheduled_time for attempt in schedule.attempts)
                if (now - last_attempt_time).days > 7:
                    self.redis_client.delete(key)
                    cleaned_count += 1
                    
            except Exception as e:
                logger.warning(f"清理过期计划失败: {e}")
                continue
        
        if cleaned_count > 0:
            logger.info(f"🧹 清理了 {cleaned_count} 个过期的同步计划")
        
        return cleaned_count 