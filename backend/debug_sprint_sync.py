#!/usr/bin/env python3
"""
调试冲刺赛同步问题
"""

import sys
from pathlib import Path
import logging
import pandas as pd

project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.unified_sync_service import UnifiedSyncService
from app.models.race import Race
from app.models.sprint_result import SprintResult

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def debug_sprint_sync():
    """调试冲刺赛同步问题"""
    logger.info("🔍 开始调试冲刺赛同步问题...")
    
    try:
        db = next(get_db())
        sync_service = UnifiedSyncService(db, cache_dir="./cache")
        
        # 1. 检查数据库中的冲刺赛
        sprint_races = db.query(Race).filter(
            Race.season_id == 2025,
            Race.is_sprint == True
        ).order_by(Race.round_number).all()
        
        logger.info(f"📊 数据库中找到 {len(sprint_races)} 场冲刺赛:")
        for race in sprint_races:
            logger.info(f"  - 第{race.round_number}轮: {race.official_event_name} (ID: {race.id})")
        
        # 2. 获取API数据
        logger.info("🔄 获取API冲刺赛数据...")
        sprint_response = sync_service._handle_api_call(
            sync_service.ergast.get_sprint_results, 
            season=2025
        )
        
        if sprint_response is None:
            logger.error("❌ API没有返回数据")
            return False
        
        # 3. 分析API响应结构
        logger.info(f"📊 API响应类型: {type(sprint_response)}")
        
        if hasattr(sprint_response, 'content'):
            sprint_dfs = sprint_response.content
            logger.info(f"📊 获取到 {len(sprint_dfs)} 个冲刺赛结果DataFrame")
            
            for idx, df in enumerate(sprint_dfs):
                if df is not None and not df.empty:
                    logger.info(f"📋 DataFrame {idx}: {len(df)} 条记录")
                    logger.info(f"📋 列名: {list(df.columns)}")
                    if len(df) > 0:
                        logger.info(f"📋 第一条记录: {df.iloc[0].to_dict()}")
                else:
                    logger.warning(f"⚠️ DataFrame {idx} 为空")
        else:
            logger.info("📊 单个DataFrame响应")
            if sprint_response is not None and not sprint_response.empty:
                logger.info(f"📋 DataFrame: {len(sprint_response)} 条记录")
                logger.info(f"📋 列名: {list(sprint_response.columns)}")
                if len(sprint_response) > 0:
                    logger.info(f"📋 第一条记录: {sprint_response.iloc[0].to_dict()}")
        
        # 4. 检查匹配逻辑
        logger.info("🔍 检查匹配逻辑...")
        
        if hasattr(sprint_response, 'content'):
            sprint_dfs = sprint_response.content
        else:
            sprint_dfs = [sprint_response]
        
        for df_idx, sprint_df in enumerate(sprint_dfs):
            if sprint_df is None or sprint_df.empty:
                logger.warning(f"DataFrame {df_idx} 为空，跳过")
                continue
            
            logger.info(f"📊 处理DataFrame {df_idx}: {len(sprint_df)} 条记录")
            
            # 根据DataFrame索引匹配冲刺赛
            if df_idx < len(sprint_races):
                race = sprint_races[df_idx]
                logger.info(f"✅ 匹配到第 {race.round_number} 轮冲刺赛: {race.official_event_name}")
                
                # 尝试处理前几条记录
                for i, (_, row) in enumerate(sprint_df.head(3).iterrows()):
                    logger.info(f"📋 处理记录 {i}:")
                    logger.info(f"   车手ID: {row.get('driverId', 'N/A')}")
                    logger.info(f"   车队ID: {row.get('constructorId', 'N/A')}")
                    logger.info(f"   位置: {row.get('position', 'N/A')}")
                    logger.info(f"   积分: {row.get('points', 'N/A')}")
                    
                    # 尝试获取车手和车队
                    driver = sync_service._get_or_create_driver_from_result(row)
                    constructor = sync_service._get_or_create_constructor_from_result(row)
                    
                    if driver:
                        logger.info(f"   ✅ 找到车手: {driver.driver_id}")
                    else:
                        logger.warning(f"   ❌ 未找到车手")
                    
                    if constructor:
                        logger.info(f"   ✅ 找到车队: {constructor.constructor_id}")
                    else:
                        logger.warning(f"   ❌ 未找到车队")
            else:
                logger.warning(f"❌ DataFrame {df_idx} 无法匹配到冲刺赛，跳过")
        
        # 5. 检查现有冲刺赛结果
        existing_results = db.query(SprintResult).count()
        logger.info(f"📊 现有冲刺赛结果数量: {existing_results}")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ 调试失败: {e}", exc_info=True)
        return False
    finally:
        db.close()

if __name__ == "__main__":
    debug_sprint_sync() 