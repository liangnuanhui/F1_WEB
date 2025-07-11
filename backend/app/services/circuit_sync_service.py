"""
F1赛道信息同步服务

整合F1官网抓取器和数据库更新功能
"""

import asyncio
import logging
from typing import List, Optional, Dict
from sqlalchemy.orm import Session

from ..core.database import get_db
from ..models.circuit import Circuit
from .f1_circuit_scraper import F1CircuitScraper, CircuitInfo

logger = logging.getLogger(__name__)


class CircuitSyncService:
    """赛道信息同步服务"""
    
    def __init__(self, db: Session):
        self.db = db
    
    async def sync_single_circuit(self, circuit: Circuit) -> bool:
        """同步单个赛道的详细信息"""
        try:
            logger.info(f"🔄 开始同步赛道: {circuit.circuit_name} ({circuit.country})")
            
            async with F1CircuitScraper() as scraper:
                circuit_info = await scraper.scrape_circuit_info(circuit.country)
                
                if not circuit_info:
                    logger.warning(f"⚠️ 未能获取赛道信息: {circuit.circuit_name}")
                    return False
                
                # 更新赛道信息
                self._update_circuit_from_info(circuit, circuit_info)
                
                # 提交数据库更改
                self.db.commit()
                self.db.refresh(circuit)
                
                logger.info(f"✅ 成功同步赛道: {circuit.circuit_name}")
                return True
                
        except Exception as e:
            logger.error(f"❌ 同步赛道失败 {circuit.circuit_name}: {e}")
            self.db.rollback()
            return False
    
    async def sync_all_circuits(self, force_update: bool = False) -> Dict[str, int]:
        """同步所有赛道的详细信息"""
        logger.info("🚀 开始批量同步所有赛道信息...")
        
        # 获取所有赛道
        if force_update:
            circuits = self.db.query(Circuit).all()
        else:
            # 只同步缺少详细信息的赛道
            circuits = self.db.query(Circuit).filter(
                Circuit.circuit_length.is_(None) |
                Circuit.first_grand_prix.is_(None) |
                Circuit.layout_image_url.is_(None)
            ).all()
        
        total = len(circuits)
        success = 0
        failed = 0
        
        logger.info(f"📊 找到 {total} 个赛道需要同步")
        
        for i, circuit in enumerate(circuits, 1):
            logger.info(f"📍 [{i}/{total}] 处理赛道: {circuit.circuit_name}")
            
            if await self.sync_single_circuit(circuit):
                success += 1
            else:
                failed += 1
            
            # 避免频繁请求
            if i < total:
                await asyncio.sleep(2)
        
        results = {
            "total": total,
            "success": success,
            "failed": failed
        }
        
        logger.info(f"🎯 同步完成! 总计: {total}, 成功: {success}, 失败: {failed}")
        return results
    
    def _update_circuit_from_info(self, circuit: Circuit, info: CircuitInfo):
        """从抓取信息更新赛道模型"""
        
        # 赛道长度 (km -> m)
        if info.circuit_length:
            circuit.length = info.circuit_length * 1000  # 转换为米
        
        # 首次大奖赛年份
        if info.first_grand_prix:
            circuit.first_grand_prix = info.first_grand_prix
        
        # 典型圈数
        if info.number_of_laps:
            circuit.typical_lap_count = info.number_of_laps
        
        # 最快圈速记录
        if info.fastest_lap_time:
            circuit.lap_record = info.fastest_lap_time
        if info.fastest_lap_driver:
            circuit.lap_record_driver = info.fastest_lap_driver
        if info.fastest_lap_year:
            circuit.lap_record_year = info.fastest_lap_year
        
        # 比赛距离
        if info.race_distance:
            circuit.race_distance = info.race_distance
        
        # 赛道布局图
        if info.layout_image_url:
            circuit.circuit_layout_image_url = info.layout_image_url
        if info.layout_image_path:
            circuit.circuit_layout_image_path = info.layout_image_path
        
        logger.debug(f"📝 更新赛道信息: {circuit.circuit_name}")
        logger.debug(f"   长度: {circuit.length} m")
        logger.debug(f"   首次GP: {circuit.first_grand_prix}")
        logger.debug(f"   圈数: {circuit.typical_lap_count}")
        logger.debug(f"   最快圈速: {circuit.lap_record} by {circuit.lap_record_driver} ({circuit.lap_record_year})")
        logger.debug(f"   比赛距离: {circuit.race_distance} km")
    
    async def sync_specific_circuits(self, circuit_ids: List[str]) -> Dict[str, int]:
        """同步指定的赛道"""
        logger.info(f"🎯 开始同步指定赛道: {circuit_ids}")
        
        circuits = self.db.query(Circuit).filter(
            Circuit.circuit_id.in_(circuit_ids)
        ).all()
        
        found_ids = [c.circuit_id for c in circuits]
        missing_ids = set(circuit_ids) - set(found_ids)
        
        if missing_ids:
            logger.warning(f"⚠️ 未找到以下赛道: {missing_ids}")
        
        total = len(circuits)
        success = 0
        failed = 0
        
        for i, circuit in enumerate(circuits, 1):
            logger.info(f"📍 [{i}/{total}] 处理赛道: {circuit.circuit_name}")
            
            if await self.sync_single_circuit(circuit):
                success += 1
            else:
                failed += 1
            
            # 避免频繁请求
            if i < total:
                await asyncio.sleep(2)
        
        results = {
            "total": total,
            "success": success,
            "failed": failed,
            "missing": list(missing_ids)
        }
        
        logger.info(f"🎯 指定赛道同步完成! 总计: {total}, 成功: {success}, 失败: {failed}")
        return results


async def sync_circuits_main(
    circuit_ids: Optional[List[str]] = None,
    force_update: bool = False,
    db: Optional[Session] = None
) -> Dict[str, int]:
    """主要的同步函数"""
    
    if db is None:
        db = next(get_db())
    
    try:
        sync_service = CircuitSyncService(db)
        
        if circuit_ids:
            # 同步指定赛道
            return await sync_service.sync_specific_circuits(circuit_ids)
        else:
            # 同步所有赛道
            return await sync_service.sync_all_circuits(force_update)
    
    finally:
        db.close()


if __name__ == "__main__":
    # 测试脚本
    
    # 同步所有缺少信息的赛道
    # results = asyncio.run(sync_circuits_main())
    
    # 同步指定赛道
    test_circuits = ["spa", "silverstone", "hungaroring"]
    results = asyncio.run(sync_circuits_main(circuit_ids=test_circuits))
    
    print("\n=== 同步结果 ===")
    for key, value in results.items():
        print(f"{key}: {value}") 