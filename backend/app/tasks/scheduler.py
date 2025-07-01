"""
比赛数据自动调度器
基于比赛时间自动安排数据更新任务
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


class RaceScheduler:
    """比赛数据更新调度器"""
    
    def __init__(self):
        self.redis_client = get_redis_client()
        self.schedule_key_prefix = "race_schedule"
        self.post_race_delay_hours = 6  # 比赛结束后6小时更新
    
    def _get_schedule_key(self, season_year: int, race_round: int) -> str:
        """生成 Redis 调度键"""
        return f"{self.schedule_key_prefix}:{season_year}:{race_round}"
    
    def _get_race_end_time(self, race: Race) -> Optional[datetime]:
        """
        计算比赛结束时间
        基于比赛开始时间 + 预估时长(3小时)
        """
        # 优先使用 session5_date (通常是正赛时间)
        if race.session5_date:
            race_start = race.session5_date
        elif race.session4_date:  # 如果没有session5，使用session4
            race_start = race.session4_date
        else:
            logger.warning(f"比赛 {race.official_event_name} 没有找到有效的比赛时间")
            return None
        
        # 估算比赛时长：正赛约2小时，加上1小时缓冲
        estimated_duration = timedelta(hours=3)
        race_end_time = race_start + estimated_duration
        
        logger.info(f"比赛 {race.official_event_name} 预计结束时间: {race_end_time}")
        return race_end_time
    
    def schedule_post_race_update(self, race: Race) -> bool:
        """
        为指定比赛安排赛后数据更新
        """
        try:
            race_end_time = self._get_race_end_time(race)
            if not race_end_time:
                return False
            
            # 计算更新时间：比赛结束后6小时
            update_time = race_end_time + timedelta(hours=self.post_race_delay_hours)
            
            # 检查是否已经过期
            if update_time <= datetime.utcnow():
                logger.warning(f"比赛 {race.official_event_name} 的更新时间已过期，立即执行更新")
                # 立即执行更新
                sync_all_post_race_data_task.delay(race.season.year, race.round_number)
                return True
            
            # 安排延迟任务
            eta = update_time
            task = sync_all_post_race_data_task.apply_async(
                args=[race.season.year, race.round_number],
                eta=eta
            )
            
            # 在 Redis 中记录调度信息
            schedule_key = self._get_schedule_key(race.season.year, race.round_number)
            schedule_data = {
                "task_id": task.id,
                "season_year": race.season.year,
                "race_round": race.round_number,
                "race_name": race.official_event_name,
                "race_end_time": race_end_time.isoformat(),
                "update_time": update_time.isoformat(),
                "scheduled_at": datetime.utcnow().isoformat(),
            }
            
            # 存储到 Redis，设置过期时间（比赛结束后1周）
            expire_time = int((update_time - datetime.utcnow()).total_seconds()) + 604800  # 1周
            self.redis_client.setex(
                schedule_key,
                expire_time,
                str(schedule_data)
            )
            
            logger.info(
                f"✅ 已安排比赛 {race.official_event_name} "
                f"的数据更新任务，将在 {update_time} 执行"
            )
            return True
            
        except Exception as e:
            logger.error(f"安排比赛 {race.official_event_name} 数据更新时发生错误: {e}")
            return False
    
    def get_scheduled_races(self) -> List[Dict[str, Any]]:
        """获取所有已调度的比赛"""
        try:
            pattern = f"{self.schedule_key_prefix}:*"
            keys = self.redis_client.keys(pattern)
            
            scheduled_races = []
            for key in keys:
                data = self.redis_client.get(key)
                if data:
                    try:
                        import ast
                        schedule_data = ast.literal_eval(data.decode('utf-8'))
                        scheduled_races.append(schedule_data)
                    except Exception as e:
                        logger.warning(f"解析调度数据失败: {e}")
                        continue
            
            return scheduled_races
            
        except Exception as e:
            logger.error(f"获取已调度比赛时发生错误: {e}")
            return []
    
    def cancel_race_schedule(self, season_year: int, race_round: int) -> bool:
        """取消指定比赛的调度"""
        try:
            schedule_key = self._get_schedule_key(season_year, race_round)
            
            # 获取任务ID
            data = self.redis_client.get(schedule_key)
            if data:
                import ast
                schedule_data = ast.literal_eval(data.decode('utf-8'))
                task_id = schedule_data.get("task_id")
                
                # 撤销 Celery 任务
                if task_id:
                    celery_app.control.revoke(task_id, terminate=True)
                
                # 删除 Redis 记录
                self.redis_client.delete(schedule_key)
                
                logger.info(f"✅ 已取消 {season_year} 赛季第 {race_round} 轮的调度")
                return True
            else:
                logger.warning(f"未找到 {season_year} 赛季第 {race_round} 轮的调度记录")
                return False
                
        except Exception as e:
            logger.error(f"取消调度时发生错误: {e}")
            return False

    def schedule_post_race_updates(self, race_id: str, race_end_time: datetime, season_year: int = 2025) -> Dict[str, Any]:
        """
        为比赛结束后安排数据更新
        
        Args:
            race_id: 比赛ID
            race_end_time: 比赛结束时间 (UTC)
            season_year: 赛季年份，默认2025
        
        Returns:
            调度结果信息
        """
        try:
            # 计算更新时间点：比赛结束后3小时、6小时、12小时
            update_times = [
                race_end_time + timedelta(hours=3),   # 3小时后
                race_end_time + timedelta(hours=6),   # 6小时后  
                race_end_time + timedelta(hours=12),  # 12小时后
            ]
            
            scheduled_tasks = []
            
            for i, update_time in enumerate(update_times, 1):
                # 创建任务ID
                task_id = f"post_race_update_{race_id}_{i}"
                
                # 检查是否已过期
                if update_time <= datetime.now(timezone.utc):
                    logger.warning(f"⚠️ 更新时间已过期，跳过: {update_time}")
                    continue
                
                # 安排比赛后数据更新任务
                try:
                    result = celery_app.send_task(
                        'sync_post_race_data',
                        args=[season_year],
                        kwargs={},
                        eta=update_time,
                        task_id=task_id,
                        queue='data_sync'
                    )
                    
                    scheduled_tasks.append({
                        'task_id': task_id,
                        'update_time': update_time.isoformat(),
                        'hours_after_race': i * 3 if i <= 2 else 12,
                        'celery_task_id': result.id,
                        'status': 'scheduled'
                    })
                    
                    logger.info(f"✅ 安排比赛后数据更新: {task_id} 于 {update_time}")
                    
                except Exception as e:
                    logger.error(f"❌ 安排任务失败 {task_id}: {e}")
                    scheduled_tasks.append({
                        'task_id': task_id,
                        'update_time': update_time.isoformat(),
                        'hours_after_race': i * 3 if i <= 2 else 12,
                        'status': 'failed',
                        'error': str(e)
                    })
            
            # 保存到Redis
            redis_key = f"post_race_schedule:{race_id}"
            schedule_data = {
                'race_id': race_id,
                'race_end_time': race_end_time.isoformat(),
                'season_year': season_year,
                'scheduled_tasks': scheduled_tasks,
                'created_at': datetime.now(timezone.utc).isoformat()
            }
            
            redis_client = get_redis_client()
            redis_client.setex(
                redis_key,
                timedelta(days=7),  # 7天后过期
                json.dumps(schedule_data, ensure_ascii=False)
            )
            
            success_count = len([t for t in scheduled_tasks if t['status'] == 'scheduled'])
            
            logger.info(f"🎯 比赛后更新调度完成: {success_count}/{len(update_times)} 个任务成功安排")
            
            return {
                "success": True,
                "race_id": race_id,
                "race_end_time": race_end_time.isoformat(),
                "season_year": season_year,
                "scheduled_tasks": scheduled_tasks,
                "summary": f"{success_count}/{len(update_times)} 个任务成功安排"
            }
            
        except Exception as e:
            error_msg = f"比赛后更新调度失败: {e}"
            logger.error(f"❌ {error_msg}", exc_info=True)
            return {
                "success": False,
                "error": error_msg,
                "race_id": race_id
            }

    def get_post_race_schedule(self, race_id: str) -> Dict[str, Any]:
        """获取比赛后更新调度信息"""
        try:
            redis_client = get_redis_client()
            redis_key = f"post_race_schedule:{race_id}"
            
            data = redis_client.get(redis_key)
            if not data:
                return {"success": False, "error": "未找到调度信息"}
            
            schedule_data = json.loads(data)
            return {"success": True, "data": schedule_data}
            
        except Exception as e:
            logger.error(f"❌ 获取调度信息失败: {e}")
            return {"success": False, "error": str(e)}

    def cancel_post_race_schedule(self, race_id: str) -> Dict[str, Any]:
        """取消比赛后更新调度"""
        try:
            # 获取调度信息
            schedule_info = self.get_post_race_schedule(race_id)
            if not schedule_info["success"]:
                return schedule_info
            
            scheduled_tasks = schedule_info["data"]["scheduled_tasks"]
            cancelled_count = 0
            
            # 取消所有任务
            for task in scheduled_tasks:
                if task['status'] == 'scheduled':
                    try:
                        celery_app.control.revoke(task['celery_task_id'], terminate=True)
                        cancelled_count += 1
                        logger.info(f"✅ 已取消任务: {task['task_id']}")
                    except Exception as e:
                        logger.error(f"❌ 取消任务失败 {task['task_id']}: {e}")
            
            # 删除Redis记录
            redis_client = get_redis_client()
            redis_client.delete(f"post_race_schedule:{race_id}")
            
            logger.info(f"🗑️ 比赛后更新调度已取消: {race_id} ({cancelled_count} 个任务)")
            
            return {
                "success": True,
                "race_id": race_id,
                "cancelled_tasks": cancelled_count,
                "message": f"已取消 {cancelled_count} 个任务"
            }
            
        except Exception as e:
            error_msg = f"取消调度失败: {e}"
            logger.error(f"❌ {error_msg}")
            return {"success": False, "error": error_msg}


@celery_app.task(bind=True, queue="scheduler")
def check_race_schedules(self):
    """
    检查并安排即将到来的比赛的数据更新任务
    每天执行一次（因为F1比赛最频繁也就一周一次）
    """
    logger.info("🔍 开始检查需要安排的比赛调度...")
    
    try:
        db = next(get_db())
        scheduler = RaceScheduler()
        
        # 获取未来7天内的比赛（扩大检查窗口，避免遗漏）
        now = datetime.utcnow()
        next_week = now + timedelta(days=7)
        
        upcoming_races = db.query(Race).join(Season).filter(
            and_(
                Race.session5_date.isnot(None),  # 有比赛时间
                Race.session5_date >= now,       # 未来的比赛
                Race.session5_date <= next_week  # 7天内
            )
        ).all()
        
        scheduled_count = 0
        for race in upcoming_races:
            # 检查是否已经调度
            schedule_key = scheduler._get_schedule_key(race.season.year, race.round_number)
            if not scheduler.redis_client.exists(schedule_key):
                if scheduler.schedule_post_race_update(race):
                    scheduled_count += 1
        
        logger.info(f"✅ 检查完成，新安排了 {scheduled_count} 场比赛的数据更新")
        
        return {
            "checked_at": now.isoformat(),
            "upcoming_races": len(upcoming_races),
            "newly_scheduled": scheduled_count,
        }
        
    except Exception as e:
        logger.error(f"检查比赛调度时发生错误: {e}")
        raise
    finally:
        db.close()


@celery_app.task(bind=True, queue="scheduler")
def cleanup_expired_schedules(self):
    """
    清理过期的调度记录
    每6小时执行一次
    """
    logger.info("🧹 开始清理过期的调度记录...")
    
    try:
        scheduler = RaceScheduler()
        pattern = f"{scheduler.schedule_key_prefix}:*"
        keys = scheduler.redis_client.keys(pattern)
        
        cleaned_count = 0
        for key in keys:
            try:
                data = scheduler.redis_client.get(key)
                if data:
                    import ast
                    schedule_data = ast.literal_eval(data.decode('utf-8'))
                    update_time = datetime.fromisoformat(schedule_data["update_time"])
                    
                    # 如果更新时间已过期超过7天，清理记录
                    if update_time < datetime.utcnow() - timedelta(days=7):
                        scheduler.redis_client.delete(key)
                        cleaned_count += 1
            except Exception as e:
                logger.warning(f"处理调度记录 {key} 时发生错误: {e}")
                # 删除格式错误的记录
                scheduler.redis_client.delete(key)
                cleaned_count += 1
        
        logger.info(f"✅ 清理完成，删除了 {cleaned_count} 个过期调度记录")
        
        return {
            "cleaned_at": datetime.utcnow().isoformat(),
            "cleaned_count": cleaned_count,
        }
        
    except Exception as e:
        logger.error(f"清理过期调度时发生错误: {e}")
        raise


@celery_app.task(bind=True, queue="scheduler")
def schedule_post_race_updates(self, season_year: Optional[int] = None):
    """
    手动安排指定赛季的所有比赛数据更新
    如果不指定赛季，则安排当前赛季
    """
    if season_year is None:
        season_year = datetime.now().year
    
    logger.info(f"📅 开始为 {season_year} 赛季安排所有比赛的数据更新...")
    
    try:
        db = next(get_db())
        scheduler = RaceScheduler()
        
        # 获取指定赛季的所有比赛
        races = db.query(Race).join(Season).filter(
            Season.year == season_year
        ).order_by(Race.round_number).all()
        
        scheduled_count = 0
        skipped_count = 0
        
        for race in races:
            # 检查是否已经调度
            schedule_key = scheduler._get_schedule_key(race.season.year, race.round_number)
            if scheduler.redis_client.exists(schedule_key):
                logger.info(f"⏭️ 跳过已调度的比赛: {race.official_event_name}")
                skipped_count += 1
                continue
            
            if scheduler.schedule_post_race_update(race):
                scheduled_count += 1
        
        logger.info(
            f"✅ {season_year} 赛季调度完成！"
            f"新安排: {scheduled_count} 场，跳过: {skipped_count} 场"
        )
        
        return {
            "season_year": season_year,
            "total_races": len(races),
            "newly_scheduled": scheduled_count,
            "skipped": skipped_count,
            "scheduled_at": datetime.utcnow().isoformat(),
        }
        
    except Exception as e:
        logger.error(f"安排 {season_year} 赛季比赛调度时发生错误: {e}")
        raise
    finally:
        db.close() 