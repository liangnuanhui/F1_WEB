#!/usr/bin/env python3
"""
测试 Session5 字段修复效果
只同步比赛数据并检查 session5_date 字段
"""

import sys
import logging
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.unified_sync_service import UnifiedSyncService
from app.models import Race, Season

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)


def test_session5_fix():
    """测试 session5_date 字段修复"""
    try:
        # 获取数据库会话
        db = next(get_db())
        
        logger.info("🔄 开始测试 session5_date 字段修复...")
        
        # 1. 查看修复前的状态
        logger.info("📊 修复前 session5_date 字段状态:")
        races_before = db.query(Race).join(Season).filter(Season.year == 2025).all()
        null_count_before = sum(1 for race in races_before if race.session5_date is None)
        total_races = len(races_before)
        logger.info(f"  - 总比赛数: {total_races}")
        logger.info(f"  - session5_date 为 NULL 的比赛数: {null_count_before}")
        
        # 2. 重新同步2025赛季的比赛数据
        logger.info("🔄 重新同步2025赛季比赛数据...")
        sync_service = UnifiedSyncService(db, cache_dir='./cache')
        
        # 只同步比赛数据
        races = sync_service.sync_races(2025)
        logger.info(f"✅ 同步完成，处理了 {len(races)} 场比赛")
        
        # 3. 查看修复后的状态
        logger.info("📊 修复后 session5_date 字段状态:")
        races_after = db.query(Race).join(Season).filter(Season.year == 2025).all()
        null_count_after = sum(1 for race in races_after if race.session5_date is None)
        
        logger.info(f"  - 总比赛数: {len(races_after)}")
        logger.info(f"  - session5_date 为 NULL 的比赛数: {null_count_after}")
        logger.info(f"  - 修复的比赛数: {null_count_before - null_count_after}")
        
        # 4. 详细显示每场比赛的 session5_date 状态
        logger.info("📋 各比赛的 session5_date 详情:")
        for race in races_after:
            status = "✅ 有数据" if race.session5_date else "❌ NULL"
            event_format = race.event_format or "unknown"
            logger.info(f"  第{race.round_number:2d}轮 - {race.official_event_name[:30]:<30} | 格式: {event_format:15} | {status}")
            if race.session5_date:
                logger.info(f"         Session5时间: {race.session5_date}")
        
        if null_count_after < null_count_before:
            logger.info(f"🎉 修复成功! 已填充 {null_count_before - null_count_after} 个 session5_date 字段")
        elif null_count_after == 0:
            logger.info("🎉 完美! 所有比赛的 session5_date 字段都已正确填充")
        else:
            logger.warning("⚠️ 修复效果不明显，可能还有其他问题")
            
    except Exception as e:
        logger.error(f"❌ 测试失败: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    test_session5_fix() 