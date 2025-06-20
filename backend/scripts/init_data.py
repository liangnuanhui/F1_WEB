        #!/usr/bin/env python3
"""
数据初始化脚本
从 FastF1 拉取真实的 F1 数据并填充数据库
"""

import asyncio
import logging
import sys
from pathlib import Path

# 添加项目根目录到 Python 路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from sqlalchemy.orm import Session

from app.core.database import get_db
from app.services.fastf1_service import FastF1Service

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


async def main():
    """主函数"""
    logger.info("开始初始化 F1 数据...")
    
    try:
        # 获取数据库会话
        db = next(get_db())
        
        # 创建 FastF1 服务
        fastf1_service = FastF1Service(db)
        
        # 初始化数据库（从 2020 年到 2024 年）
        await fastf1_service.initialize_database(start_year=2020, end_year=2024)
        
        logger.info("数据初始化完成！")
        
        # 显示统计信息
        await show_statistics(db)
        
    except Exception as e:
        logger.error(f"初始化数据时发生错误: {e}")
        sys.exit(1)
    finally:
        db.close()


async def show_statistics(db: Session):
    """显示数据库统计信息"""
    try:
        from app.models.season import Season
        from app.models.circuit import Circuit
        from app.models.race import Race
        from app.models.driver import Driver
        from app.models.constructor import Constructor
        from app.models.result import Result
        
        # 统计各表记录数
        seasons_count = db.query(Season).count()
        circuits_count = db.query(Circuit).count()
        races_count = db.query(Race).count()
        drivers_count = db.query(Driver).count()
        constructors_count = db.query(Constructor).count()
        results_count = db.query(Result).count()
        
        logger.info("=== 数据库统计信息 ===")
        logger.info(f"赛季数量: {seasons_count}")
        logger.info(f"赛道数量: {circuits_count}")
        logger.info(f"比赛数量: {races_count}")
        logger.info(f"车手数量: {drivers_count}")
        logger.info(f"车队数量: {constructors_count}")
        logger.info(f"比赛结果数量: {results_count}")
        
        # 显示赛季信息
        seasons = db.query(Season).order_by(Season.year).all()
        logger.info("\n=== 赛季信息 ===")
        for season in seasons:
            logger.info(f"{season.year}: {season.name}")
        
        # 显示最近的比赛
        recent_races = db.query(Race).order_by(Race.race_date.desc()).limit(5).all()
        logger.info("\n=== 最近的比赛 ===")
        for race in recent_races:
            logger.info(f"{race.race_date.strftime('%Y-%m-%d')}: {race.name}")
        
    except Exception as e:
        logger.error(f"显示统计信息时发生错误: {e}")


if __name__ == "__main__":
    asyncio.run(main()) 