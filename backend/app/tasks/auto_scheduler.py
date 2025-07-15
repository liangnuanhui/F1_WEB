"""
增强的比赛数据自动同步调度器
实现完全自动化的多次重试同步机制
"""

import logging
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta, timezone
from sqlalchemy.orm import Session
from sqlalchemy import and_
import json

from .celery_app import celery_app
from .data_sync import sync_all_post_race_data_task
from ..core.database import get_db
from ..core.redis import get_redis_client
from ..models import Race, Season

logger = logging.getLogger(__name__)


class AutoRaceScheduler:
    """完全自动化的比赛数据同步调度器"""
    
    def __init__(self):
        self.redis_client = get_redis_client()
        self.schedule_key_prefix = "auto_race_schedule"
        # 比赛结束后的重试时间点（小时）
        self.retry_hours = [6, 12, 24, 30, 36, 42, 48]
    
    def _get_schedule_key(self, season_year: int, race_round: int) -> str:
        """生成 Redis 调度键"""
        return f"{self.schedule_key_prefix}:{season_year}:{race_round}"
    
    def _estimate_race_end_time(self, race: Race) -> Optional[datetime]:
        """
        智能估算比赛结束时间
        """
        # 1. 优先使用正赛时间 (session5)
        if race.session5_date:
            race_start = race.session5_date
            race_duration = timedelta(hours=2.5)  # 正赛约2.5小时
        # 2. 如果没有正赛，使用最后一个有效session
        elif race.session4_date:
            race_start = race.session4_date
            race_duration = timedelta(hours=1.5)  # 其他session约1.5小时
        elif race.session3_date:
            race_start = race.session3_date
            race_duration = timedelta(hours=1.5)
        else:
            logger.warning(f"比赛 {race.official_event_name} 没有找到有效的时间信息")
            return None
        
        # 确保时间是UTC
        if race_start.tzinfo is None:
            race_start = race_start.replace(tzinfo=timezone.utc)
        
        race_end_time = race_start + race_duration
        
        logger.info(f"比赛 {race.official_event_name} 预计结束时间: {race_end_time}")
        return race_end_time
    
    def schedule_race_auto_sync(self, race: Race) -> Dict[str, Any]:
        """
        为指定比赛安排自动同步计划
        在比赛结束后的多个时间点尝试同步
        """
        try:
            race_end_time = self._estimate_race_end_time(race)
            if not race_end_time:
                return {"success": False, "error": "无法确定比赛时间"}
            
            # 检查是否已经安排
            schedule_key = self._get_schedule_key(race.season.year, race.round_number)
            if self.redis_client.exists(schedule_key):
                logger.info(f"比赛 {race.official_event_name} 已有自动同步计划")
                return {"success": True, "status": "already_scheduled"}
            
            scheduled_tasks = []
            now_utc = datetime.now(timezone.utc)
            
            for i, hours_after in enumerate(self.retry_hours):
                sync_time = race_end_time + timedelta(hours=hours_after)
                
                # 跳过已经过期的时间点
                if sync_time <= now_utc:
                    logger.info(f"跳过过期的同步时间点: {sync_time} (比赛结束后{hours_after}小时)")
                    continue
                
                try:
                    # 创建唯一的任务ID
                    task_id = f"auto_sync_{race.season.year}_{race.round_number}_{hours_after}h"
                    
                    # 安排Celery任务
                    task = sync_all_post_race_data_task.apply_async(
                        args=[race.season.year, race.round_number, hours_after],
                        eta=sync_time,
                        task_id=task_id,
                        queue='post_race_sync'
                    )
                    
                    scheduled_tasks.append({
                        "attempt_number": i + 1,
                        "hours_after_race": hours_after,
                        "sync_time": sync_time.isoformat(),
                        "task_id": task_id,
                        "celery_task_id": task.id,
                        "status": "scheduled"
                    })
                    
                    logger.info(f"✅ 安排自动同步: {race.official_event_name} 比赛结束后{hours_after}小时 ({sync_time})")
                    
                except Exception as e:
                    logger.error(f"❌ 安排同步任务失败 (比赛结束后{hours_after}小时): {e}")
                    scheduled_tasks.append({
                        "attempt_number": i + 1,
                        "hours_after_race": hours_after,
                        "sync_time": sync_time.isoformat(),
                        "status": "failed",
                        "error": str(e)
                    })
            
            # 保存调度信息到Redis
            schedule_data = {
                "season_year": race.season.year,
                "race_round": race.round_number,
                "race_name": race.official_event_name,
                "race_end_time": race_end_time.isoformat(),
                "scheduled_tasks": scheduled_tasks,
                "created_at": now_utc.isoformat(),
                "total_attempts": len(scheduled_tasks),
                "successful_attempts": len([t for t in scheduled_tasks if t["status"] == "scheduled"])
            }
            
            # 设置过期时间：最后一个同步时间点后7天
            if scheduled_tasks:
                last_sync_time = max([
                    datetime.fromisoformat(t["sync_time"]) 
                    for t in scheduled_tasks 
                    if t["status"] == "scheduled"
                ], default=now_utc)
                expire_seconds = int((last_sync_time - now_utc).total_seconds()) + 604800  # 7天
            else:
                expire_seconds = 86400  # 1天
            
            self.redis_client.setex(
                schedule_key,
                expire_seconds,
                json.dumps(schedule_data, ensure_ascii=False)
            )
            
            success_count = schedule_data["successful_attempts"]
            logger.info(
                f"🎯 比赛 {race.official_event_name} 自动同步调度完成: "
                f"{success_count}/{len(self.retry_hours)} 个时间点成功安排"
            )
            
            return {
                "success": True,
                "race_name": race.official_event_name,
                "total_attempts": len(self.retry_hours),
                "scheduled_attempts": success_count,
                "schedule_data": schedule_data
            }
            
        except Exception as e:
            error_msg = f"安排比赛 {race.official_event_name} 自动同步失败: {e}"
            logger.error(f"❌ {error_msg}")
            return {"success": False, "error": error_msg}
    
    def get_auto_sync_status(self, season_year: int, race_round: int) -> Dict[str, Any]:
        """获取自动同步状态"""
        try:
            schedule_key = self._get_schedule_key(season_year, race_round)
            data = self.redis_client.get(schedule_key)
            
            if not data:
                return {"success": False, "error": "未找到自动同步计划"}
            
            schedule_data = json.loads(data)
            
            # 更新任务状态（检查是否已完成）
            now_utc = datetime.now(timezone.utc)
            for task in schedule_data["scheduled_tasks"]:
                if task["status"] == "scheduled":
                    sync_time = datetime.fromisoformat(task["sync_time"])
                    if sync_time <= now_utc:
                        # 检查任务是否已执行
                        task["status"] = "executed"  # 简化状态，实际可以查询Celery结果
            
            return {"success": True, "data": schedule_data}
            
        except Exception as e:
            logger.error(f"❌ 获取自动同步状态失败: {e}")
            return {"success": False, "error": str(e)}
    
    def cancel_auto_sync(self, season_year: int, race_round: int) -> Dict[str, Any]:
        """取消自动同步计划"""
        try:
            schedule_info = self.get_auto_sync_status(season_year, race_round)
            if not schedule_info["success"]:
                return schedule_info
            
            scheduled_tasks = schedule_info["data"]["scheduled_tasks"]
            cancelled_count = 0
            
            # 取消所有待执行的任务
            for task in scheduled_tasks:
                if task["status"] == "scheduled" and "celery_task_id" in task:
                    try:
                        celery_app.control.revoke(task["celery_task_id"], terminate=True)
                        cancelled_count += 1
                        logger.info(f"✅ 已取消任务: {task['task_id']}")
                    except Exception as e:
                        logger.error(f"❌ 取消任务失败 {task['task_id']}: {e}")
            
            # 删除Redis记录
            schedule_key = self._get_schedule_key(season_year, race_round)
            self.redis_client.delete(schedule_key)
            
            logger.info(f"🗑️ 已取消 {season_year} 赛季第 {race_round} 轮的自动同步计划")
            
            return {
                "success": True,
                "cancelled_tasks": cancelled_count,
                "message": f"已取消 {cancelled_count} 个待执行任务"
            }
            
        except Exception as e:
            error_msg = f"取消自动同步失败: {e}"
            logger.error(f"❌ {error_msg}")
            return {"success": False, "error": error_msg}


@celery_app.task(bind=True, queue="scheduler")
def auto_schedule_all_races(self, season_year: Optional[int] = None):
    """
    自动为整个赛季安排比赛数据同步
    系统启动时或手动触发时执行
    """
    if season_year is None:
        season_year = datetime.now().year
    
    logger.info(f"🚀 开始为 {season_year} 赛季自动安排所有比赛的数据同步...")
    
    try:
        db = next(get_db())
        scheduler = AutoRaceScheduler()
        
        # 获取指定赛季的所有比赛
        races = db.query(Race).join(Season).filter(
            Season.year == season_year
        ).order_by(Race.round_number).all()
        
        results = []
        scheduled_count = 0
        skipped_count = 0
        failed_count = 0
        
        for race in races:
            result = scheduler.schedule_race_auto_sync(race)
            results.append({
                "race_round": race.round_number,
                "race_name": race.official_event_name,
                "result": result
            })
            
            if result["success"]:
                if result.get("status") == "already_scheduled":
                    skipped_count += 1
                else:
                    scheduled_count += 1
            else:
                failed_count += 1
        
        summary = {
            "season_year": season_year,
            "total_races": len(races),
            "newly_scheduled": scheduled_count,
            "already_scheduled": skipped_count,
            "failed": failed_count,
            "completed_at": datetime.now(timezone.utc).isoformat()
        }
        
        logger.info(
            f"✅ {season_year} 赛季自动调度完成！"
            f"新安排: {scheduled_count} 场，已有: {skipped_count} 场，失败: {failed_count} 场"
        )
        
        return {
            "summary": summary,
            "details": results
        }
        
    except Exception as e:
        logger.error(f"❌ 自动安排 {season_year} 赛季比赛同步失败: {e}")
        raise
    finally:
        db.close()


@celery_app.task(bind=True, queue="scheduler")
def check_and_schedule_upcoming_races(self):
    """
    检查并自动安排即将到来的比赛
    每天执行一次，确保不遗漏任何比赛
    """
    logger.info("🔍 检查并自动安排即将到来的比赛...")
    
    try:
        db = next(get_db())
        scheduler = AutoRaceScheduler()
        
        # 检查未来14天内的比赛（提前安排，避免遗漏）
        now_utc = datetime.now(timezone.utc)
        check_window = now_utc + timedelta(days=14)
        
        upcoming_races = db.query(Race).join(Season).filter(
            and_(
                Race.session5_date.isnot(None),  # 有正赛时间
                Race.session5_date >= now_utc,   # 未来的比赛
                Race.session5_date <= check_window  # 14天内
            )
        ).all()
        
        results = []
        newly_scheduled = 0
        
        for race in upcoming_races:
            # 检查是否已经有自动同步计划
            schedule_key = scheduler._get_schedule_key(race.season.year, race.round_number)
            if not scheduler.redis_client.exists(schedule_key):
                result = scheduler.schedule_race_auto_sync(race)
                results.append({
                    "race": f"{race.season.year} 第{race.round_number}轮 {race.official_event_name}",
                    "result": result
                })
                
                if result["success"]:
                    newly_scheduled += 1
            else:
                logger.info(f"⏭️ 跳过已安排的比赛: {race.official_event_name}")
        
        logger.info(f"✅ 检查完成，新安排了 {newly_scheduled} 场比赛的自动同步")
        
        return {
            "checked_at": now_utc.isoformat(),
            "upcoming_races_count": len(upcoming_races),
            "newly_scheduled": newly_scheduled,
            "results": results
        }
        
    except Exception as e:
        logger.error(f"❌ 检查即将到来的比赛失败: {e}")
        raise
    finally:
        db.close()


@celery_app.task(bind=True, queue="scheduler")
def cleanup_old_schedules(self):
    """
    清理过期的自动同步计划
    每天执行一次
    """
    logger.info("🧹 清理过期的自动同步计划...")
    
    try:
        scheduler = AutoRaceScheduler()
        pattern = f"{scheduler.schedule_key_prefix}:*"
        keys = scheduler.redis_client.keys(pattern)
        
        cleaned_count = 0
        now_utc = datetime.now(timezone.utc)
        
        for key in keys:
            try:
                data = scheduler.redis_client.get(key)
                if data:
                    schedule_data = json.loads(data)
                    
                    # 检查是否所有同步时间点都已过期
                    all_expired = True
                    for task in schedule_data["scheduled_tasks"]:
                        if task["status"] == "scheduled":
                            sync_time = datetime.fromisoformat(task["sync_time"])
                            if sync_time > now_utc:
                                all_expired = False
                                break
                    
                    # 如果所有时间点都已过期超过7天，删除计划
                    if all_expired:
                        race_end_time = datetime.fromisoformat(schedule_data["race_end_time"])
                        if race_end_time < now_utc - timedelta(days=7):
                            scheduler.redis_client.delete(key)
                            cleaned_count += 1
                            logger.info(f"🗑️ 删除过期计划: {schedule_data['race_name']}")
                            
            except Exception as e:
                logger.warning(f"处理计划 {key} 时发生错误: {e}")
                # 删除格式错误的记录
                scheduler.redis_client.delete(key)
                cleaned_count += 1
        
        logger.info(f"✅ 清理完成，删除了 {cleaned_count} 个过期计划")
        
        return {
            "cleaned_at": now_utc.isoformat(),
            "cleaned_count": cleaned_count
        }
        
    except Exception as e:
        logger.error(f"❌ 清理过期计划失败: {e}")
        raise