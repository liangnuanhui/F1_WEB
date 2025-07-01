"""
数据同步 Celery 任务
处理比赛结束后的数据更新
"""

import logging
from typing import Optional, Dict, Any
from datetime import datetime, timedelta

from celery import Task
from sqlalchemy.orm import Session

from .celery_app import celery_app
from ..core.database import get_db
from ..services.unified_sync_service import UnifiedSyncService
from ..models import Race, Season

logger = logging.getLogger(__name__)


class CallbackTask(Task):
    """
    带回调的任务基类
    """
    def on_success(self, retval, task_id, args, kwargs):
        logger.info(f"任务 {task_id} 执行成功: {retval}")

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        logger.error(f"任务 {task_id} 执行失败: {exc}")
        logger.error(f"错误信息: {einfo}")


@celery_app.task(bind=True, base=CallbackTask, queue="data_sync")
def sync_race_results_task(self, season_year: int, race_round: int) -> Dict[str, Any]:
    """
    同步比赛结果任务
    """
    logger.info(f"开始同步 {season_year} 赛季第 {race_round} 轮比赛结果...")
    
    try:
        # 获取数据库会话
        db = next(get_db())
        
        # 创建同步服务
        sync_service = UnifiedSyncService(db, cache_dir="./cache")
        
        # 同步比赛结果
        success = sync_service.sync_race_results(season_year)
        
        result = {
            "task": "sync_race_results",
            "season_year": season_year,
            "race_round": race_round,
            "success": success,
            "timestamp": datetime.utcnow().isoformat(),
        }
        
        if success:
            logger.info(f"✅ {season_year} 赛季第 {race_round} 轮比赛结果同步完成")
        else:
            logger.warning(f"⚠️ {season_year} 赛季第 {race_round} 轮比赛结果同步部分失败")
            
        return result
        
    except Exception as e:
        logger.error(f"❌ 同步比赛结果时发生错误: {e}")
        raise self.retry(exc=e, countdown=300, max_retries=3)  # 5分钟后重试
    finally:
        db.close()


@celery_app.task(bind=True, base=CallbackTask, queue="data_sync")
def sync_qualifying_results_task(self, season_year: int, race_round: int) -> Dict[str, Any]:
    """
    同步排位赛结果任务
    """
    logger.info(f"开始同步 {season_year} 赛季第 {race_round} 轮排位赛结果...")
    
    try:
        db = next(get_db())
        sync_service = UnifiedSyncService(db, cache_dir="./cache")
        
        success = sync_service.sync_qualifying_results(season_year)
        
        result = {
            "task": "sync_qualifying_results",
            "season_year": season_year,
            "race_round": race_round,
            "success": success,
            "timestamp": datetime.utcnow().isoformat(),
        }
        
        if success:
            logger.info(f"✅ {season_year} 赛季第 {race_round} 轮排位赛结果同步完成")
        else:
            logger.warning(f"⚠️ {season_year} 赛季第 {race_round} 轮排位赛结果同步部分失败")
            
        return result
        
    except Exception as e:
        logger.error(f"❌ 同步排位赛结果时发生错误: {e}")
        raise self.retry(exc=e, countdown=300, max_retries=3)
    finally:
        db.close()


@celery_app.task(bind=True, base=CallbackTask, queue="data_sync")
def sync_sprint_results_task(self, season_year: int, race_round: int) -> Dict[str, Any]:
    """
    同步冲刺赛结果任务
    """
    logger.info(f"开始同步 {season_year} 赛季第 {race_round} 轮冲刺赛结果...")
    
    try:
        db = next(get_db())
        sync_service = UnifiedSyncService(db, cache_dir="./cache")
        
        success = sync_service.sync_sprint_results(season_year)
        
        result = {
            "task": "sync_sprint_results",
            "season_year": season_year,
            "race_round": race_round,
            "success": success,
            "timestamp": datetime.utcnow().isoformat(),
        }
        
        if success:
            logger.info(f"✅ {season_year} 赛季第 {race_round} 轮冲刺赛结果同步完成")
        else:
            logger.warning(f"⚠️ {season_year} 赛季第 {race_round} 轮冲刺赛结果同步部分失败")
            
        return result
        
    except Exception as e:
        logger.error(f"❌ 同步冲刺赛结果时发生错误: {e}")
        raise self.retry(exc=e, countdown=300, max_retries=3)
    finally:
        db.close()


@celery_app.task(bind=True, base=CallbackTask, queue="data_sync")
def sync_driver_standings_task(self, season_year: int, race_round: int) -> Dict[str, Any]:
    """
    同步车手积分榜任务
    """
    logger.info(f"开始同步 {season_year} 赛季第 {race_round} 轮后车手积分榜...")
    
    try:
        db = next(get_db())
        sync_service = UnifiedSyncService(db, cache_dir="./cache")
        
        success = sync_service.sync_driver_standings(season_year)
        
        result = {
            "task": "sync_driver_standings", 
            "season_year": season_year,
            "race_round": race_round,
            "success": success,
            "timestamp": datetime.utcnow().isoformat(),
        }
        
        if success:
            logger.info(f"✅ {season_year} 赛季第 {race_round} 轮后车手积分榜同步完成")
        else:
            logger.warning(f"⚠️ {season_year} 赛季第 {race_round} 轮后车手积分榜同步部分失败")
            
        return result
        
    except Exception as e:
        logger.error(f"❌ 同步车手积分榜时发生错误: {e}")
        raise self.retry(exc=e, countdown=300, max_retries=3)
    finally:
        db.close()


@celery_app.task(bind=True, base=CallbackTask, queue="data_sync")
def sync_constructor_standings_task(self, season_year: int, race_round: int) -> Dict[str, Any]:
    """
    同步车队积分榜任务
    """
    logger.info(f"开始同步 {season_year} 赛季第 {race_round} 轮后车队积分榜...")
    
    try:
        db = next(get_db())
        sync_service = UnifiedSyncService(db, cache_dir="./cache")
        
        success = sync_service.sync_constructor_standings(season_year)
        
        result = {
            "task": "sync_constructor_standings",
            "season_year": season_year,
            "race_round": race_round,
            "success": success,
            "timestamp": datetime.utcnow().isoformat(),
        }
        
        if success:
            logger.info(f"✅ {season_year} 赛季第 {race_round} 轮后车队积分榜同步完成")
        else:
            logger.warning(f"⚠️ {season_year} 赛季第 {race_round} 轮后车队积分榜同步部分失败")
            
        return result
        
    except Exception as e:
        logger.error(f"❌ 同步车队积分榜时发生错误: {e}")
        raise self.retry(exc=e, countdown=300, max_retries=3)
    finally:
        db.close()


@celery_app.task(bind=True, base=CallbackTask, queue="data_sync")
def sync_all_post_race_data_task(self, season_year: int, race_round: int) -> Dict[str, Any]:
    """
    同步比赛后所有相关数据的综合任务
    使用串行执行避免 .get() 调用
    """
    logger.info(f"🚀 开始全面同步 {season_year} 赛季第 {race_round} 轮比赛后所有数据...")
    
    start_time = datetime.utcnow()
    results = {
        "task": "sync_all_post_race_data",
        "season_year": season_year,
        "race_round": race_round,
        "start_time": start_time.isoformat(),
        "subtasks": {},
        "overall_success": True,
    }
    
    try:
        db = next(get_db())
        sync_service = UnifiedSyncService(db, cache_dir="./cache")
        
        # 1. 同步比赛结果
        logger.info("1️⃣ 同步比赛结果...")
        try:
            race_success = sync_service.sync_race_results(season_year)
            results["subtasks"]["race_results"] = {
                "success": race_success,
                "timestamp": datetime.utcnow().isoformat()
            }
            if not race_success:
                results["overall_success"] = False
        except Exception as e:
            logger.error(f"比赛结果同步失败: {e}")
            results["subtasks"]["race_results"] = {"success": False, "error": str(e)}
            results["overall_success"] = False
        
        # 2. 同步排位赛结果
        logger.info("2️⃣ 同步排位赛结果...")
        try:
            quali_success = sync_service.sync_qualifying_results(season_year)
            results["subtasks"]["qualifying_results"] = {
                "success": quali_success,
                "timestamp": datetime.utcnow().isoformat()
            }
            if not quali_success:
                results["overall_success"] = False
        except Exception as e:
            logger.error(f"排位赛结果同步失败: {e}")
            results["subtasks"]["qualifying_results"] = {"success": False, "error": str(e)}
            results["overall_success"] = False
        
        # 3. 检查是否有冲刺赛，如果有则同步
        try:
            race = db.query(Race).join(Season).filter(
                Season.year == season_year,
                Race.round_number == race_round
            ).first()
            
            if race and race.is_sprint:
                logger.info("3️⃣ 检测到冲刺赛，同步冲刺赛结果...")
                sprint_success = sync_service.sync_sprint_results(season_year)
                results["subtasks"]["sprint_results"] = {
                    "success": sprint_success,
                    "timestamp": datetime.utcnow().isoformat()
                }
                if not sprint_success:
                    results["overall_success"] = False
            else:
                logger.info("3️⃣ 本轮无冲刺赛，跳过冲刺赛结果同步")
                results["subtasks"]["sprint_results"] = {"skipped": True, "reason": "no_sprint"}
        except Exception as e:
            logger.error(f"冲刺赛结果同步失败: {e}")
            results["subtasks"]["sprint_results"] = {"success": False, "error": str(e)}
            results["overall_success"] = False
        
        # 4. 同步车手积分榜
        logger.info("4️⃣ 同步车手积分榜...")
        try:
            driver_standings_success = sync_service.sync_driver_standings(season_year)
            results["subtasks"]["driver_standings"] = {
                "success": driver_standings_success,
                "timestamp": datetime.utcnow().isoformat()
            }
            if not driver_standings_success:
                results["overall_success"] = False
        except Exception as e:
            logger.error(f"车手积分榜同步失败: {e}")
            results["subtasks"]["driver_standings"] = {"success": False, "error": str(e)}
            results["overall_success"] = False
        
        # 5. 同步车队积分榜
        logger.info("5️⃣ 同步车队积分榜...")
        try:
            constructor_standings_success = sync_service.sync_constructor_standings(season_year)
            results["subtasks"]["constructor_standings"] = {
                "success": constructor_standings_success,
                "timestamp": datetime.utcnow().isoformat()
            }
            if not constructor_standings_success:
                results["overall_success"] = False
        except Exception as e:
            logger.error(f"车队积分榜同步失败: {e}")
            results["subtasks"]["constructor_standings"] = {"success": False, "error": str(e)}
            results["overall_success"] = False
        
        # 完成时间
        end_time = datetime.utcnow()
        results["end_time"] = end_time.isoformat()
        results["duration_seconds"] = (end_time - start_time).total_seconds()
        
        if results["overall_success"]:
            logger.info(f"✅ {season_year} 赛季第 {race_round} 轮所有数据同步完成！耗时: {results['duration_seconds']:.1f}秒")
        else:
            logger.warning(f"⚠️ {season_year} 赛季第 {race_round} 轮数据同步完成，但部分任务失败")
        
        return results
        
    except Exception as e:
        logger.error(f"❌ 全面数据同步时发生错误: {e}")
        results["error"] = str(e)
        results["overall_success"] = False
        results["end_time"] = datetime.utcnow().isoformat()
        raise self.retry(exc=e, countdown=600, max_retries=2)  # 10分钟后重试
    finally:
        db.close()


@celery_app.task(bind=True, name="sync_post_race_data")
def sync_post_race_data(self, season_year: int, race_round: int = None):
    """
    比赛后数据同步任务
    专注于5个核心数据：排位赛结果、比赛结果、冲刺赛结果、车手积分榜、车队积分榜
    """
    try:
        logger.info(f"🏎️ 开始比赛后数据同步 - 赛季: {season_year}, 轮次: {race_round or '全部'}")
        
        db = next(get_db())
        service = UnifiedSyncService(db)
        
        results = {}
        
        # 1. 排位赛结果
        logger.info("🚥 同步排位赛结果...")
        try:
            results['qualifying'] = service.sync_qualifying_results(season_year)
            logger.info(f"   排位赛结果: {'✅ 成功' if results['qualifying'] else '⏳ 暂无数据'}")
        except Exception as e:
            results['qualifying'] = False
            logger.error(f"   排位赛结果: ❌ 失败 - {e}")

        # 2. 比赛结果
        logger.info("🏁 同步比赛结果...")
        try:
            results['race'] = service.sync_race_results(season_year)
            logger.info(f"   比赛结果: {'✅ 成功' if results['race'] else '⏳ 暂无数据'}")
        except Exception as e:
            results['race'] = False
            logger.error(f"   比赛结果: ❌ 失败 - {e}")

        # 3. 冲刺赛结果
        logger.info("🏃 同步冲刺赛结果...")
        try:
            results['sprint'] = service.sync_sprint_results(season_year)
            logger.info(f"   冲刺赛结果: {'✅ 成功' if results['sprint'] else '⏳ 暂无数据'}")
        except Exception as e:
            results['sprint'] = False
            logger.error(f"   冲刺赛结果: ❌ 失败 - {e}")

        # 4. 车手积分榜
        logger.info("🏆 同步车手积分榜...")
        try:
            results['driver_standings'] = service.sync_driver_standings(season_year)
            logger.info(f"   车手积分榜: {'✅ 成功' if results['driver_standings'] else '⏳ 暂无数据'}")
        except Exception as e:
            results['driver_standings'] = False
            logger.error(f"   车手积分榜: ❌ 失败 - {e}")

        # 5. 车队积分榜
        logger.info("🏁 同步车队积分榜...")
        try:
            results['constructor_standings'] = service.sync_constructor_standings(season_year)
            logger.info(f"   车队积分榜: {'✅ 成功' if results['constructor_standings'] else '⏳ 暂无数据'}")
        except Exception as e:
            results['constructor_standings'] = False
            logger.error(f"   车队积分榜: ❌ 失败 - {e}")
        
        # 统计结果
        success_count = sum(1 for success in results.values() if success)
        total_count = len(results)
        
        logger.info(f"🎯 比赛后数据同步完成: {success_count}/{total_count} 项成功")
        
        db.close()
        return {
            "success": True,
            "season_year": season_year,
            "race_round": race_round,
            "results": results,
            "summary": f"{success_count}/{total_count} 项成功"
        }
        
    except Exception as e:
        logger.error(f"❌ 比赛后数据同步失败: {e}", exc_info=True)
        return {
            "success": False,
            "error": str(e),
            "season_year": season_year,
            "race_round": race_round
        } 