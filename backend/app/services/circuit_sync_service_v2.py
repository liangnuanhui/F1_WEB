"""
F1赛道信息同步服务 v2.0 - 改进版

改进内容：
1. 使用v2爬虫，支持100%赛道覆盖
2. 增强错误处理和重试机制
3. 支持批量处理和进度追踪
4. 添加数据验证和完整性检查
5. 改进的事务管理和回滚机制
"""

import asyncio
import logging
from typing import List, Optional, Dict, Tuple
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from ..core.database import get_db
from ..models.circuit import Circuit
from .f1_circuit_scraper_v2 import F1CircuitScraperV2, CircuitInfo

logger = logging.getLogger(__name__)


class CircuitSyncResult:
    """同步结果类"""
    def __init__(self):
        self.total = 0
        self.successful = 0
        self.failed = 0
        self.skipped = 0
        self.errors: List[Tuple[str, str]] = []  # (circuit_id, error_message)
        self.successful_circuits: List[str] = []
        self.failed_circuits: List[str] = []
        self.skipped_circuits: List[str] = []
    
    def add_success(self, circuit_id: str):
        """添加成功记录"""
        self.successful += 1
        self.successful_circuits.append(circuit_id)
    
    def add_failure(self, circuit_id: str, error_message: str):
        """添加失败记录"""
        self.failed += 1
        self.failed_circuits.append(circuit_id)
        self.errors.append((circuit_id, error_message))
    
    def add_skip(self, circuit_id: str):
        """添加跳过记录"""
        self.skipped += 1
        self.skipped_circuits.append(circuit_id)
    
    def print_summary(self):
        """打印同步摘要"""
        logger.info("=" * 60)
        logger.info("📊 同步结果汇总")
        logger.info("=" * 60)
        logger.info(f"📈 总计: {self.total}")
        logger.info(f"✅ 成功: {self.successful}")
        logger.info(f"❌ 失败: {self.failed}")
        logger.info(f"⏭️ 跳过: {self.skipped}")
        
        if self.successful_circuits:
            logger.info(f"✅ 成功的赛道: {', '.join(self.successful_circuits)}")
        
        if self.failed_circuits:
            logger.info(f"❌ 失败的赛道: {', '.join(self.failed_circuits)}")
            for circuit_id, error in self.errors:
                logger.info(f"   {circuit_id}: {error}")
        
        if self.skipped_circuits:
            logger.info(f"⏭️ 跳过的赛道: {', '.join(self.skipped_circuits)}")
        
        logger.info("=" * 60)


class CircuitSyncServiceV2:
    """赛道信息同步服务 v2.0"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def _update_circuit_from_info(self, circuit: Circuit, circuit_info: CircuitInfo) -> bool:
        """从爬取信息更新赛道数据"""
        try:
            updated_fields = []
            
            # 更新赛道长度 (转换为米)
            if circuit_info.circuit_length is not None:
                new_length = circuit_info.circuit_length * 1000  # km -> m
                if circuit.length != new_length:
                    circuit.length = new_length
                    updated_fields.append("length")
            
            # 更新首次GP年份
            if circuit_info.first_grand_prix is not None:
                if circuit.first_grand_prix != circuit_info.first_grand_prix:
                    circuit.first_grand_prix = circuit_info.first_grand_prix
                    updated_fields.append("first_grand_prix")
            
            # 更新典型圈数
            if circuit_info.number_of_laps is not None:
                if circuit.typical_lap_count != circuit_info.number_of_laps:
                    circuit.typical_lap_count = circuit_info.number_of_laps
                    updated_fields.append("typical_lap_count")
            
            # 更新比赛距离 (保持km单位)
            if circuit_info.race_distance is not None:
                if circuit.race_distance != circuit_info.race_distance:
                    circuit.race_distance = circuit_info.race_distance
                    updated_fields.append("race_distance")
            
            # 更新最快圈速记录
            if circuit_info.fastest_lap_time is not None:
                if circuit.lap_record != circuit_info.fastest_lap_time:
                    circuit.lap_record = circuit_info.fastest_lap_time
                    updated_fields.append("lap_record")
            
            # 更新最快圈速车手
            if circuit_info.fastest_lap_driver is not None:
                if circuit.lap_record_driver != circuit_info.fastest_lap_driver:
                    circuit.lap_record_driver = circuit_info.fastest_lap_driver
                    updated_fields.append("lap_record_driver")
            
            # 更新最快圈速年份
            if circuit_info.fastest_lap_year is not None:
                if circuit.lap_record_year != circuit_info.fastest_lap_year:
                    circuit.lap_record_year = circuit_info.fastest_lap_year
                    updated_fields.append("lap_record_year")
            
            # 更新布局图URL
            if circuit_info.layout_image_url is not None:
                if circuit.circuit_layout_image_url != circuit_info.layout_image_url:
                    circuit.circuit_layout_image_url = circuit_info.layout_image_url
                    updated_fields.append("circuit_layout_image_url")
            
            # 更新本地图片路径
            if circuit_info.layout_image_path is not None:
                if circuit.circuit_layout_image_path != circuit_info.layout_image_path:
                    circuit.circuit_layout_image_path = circuit_info.layout_image_path
                    updated_fields.append("circuit_layout_image_path")
            
            if updated_fields:
                logger.info(f"   🔄 更新字段: {', '.join(updated_fields)}")
                return True
            else:
                logger.info(f"   ℹ️ 数据无变化，跳过更新")
                return False
                
        except Exception as e:
            logger.error(f"❌ 更新赛道数据失败: {e}")
            return False
    
    async def sync_single_circuit(self, circuit: Circuit, force_update: bool = False) -> Tuple[bool, str]:
        """同步单个赛道的详细信息"""
        try:
            logger.info(f"🎯 处理赛道: {circuit.circuit_name} ({circuit.circuit_id})")
            
            # 检查是否需要同步
            if not force_update and self._circuit_has_complete_info(circuit):
                logger.info(f"   ℹ️ 赛道信息已完整，跳过同步")
                return True, "数据已完整"
            
            logger.info(f"🔄 开始同步赛道: {circuit.circuit_name}")
            
            async with F1CircuitScraperV2() as scraper:
                circuit_info = await scraper.scrape_circuit_info_with_retry(circuit.circuit_id)
                
                if not circuit_info:
                    error_msg = f"未能获取赛道信息"
                    logger.warning(f"⚠️ {error_msg}: {circuit.circuit_name}")
                    return False, error_msg
                
                # 数据验证
                if not circuit_info.is_complete():
                    missing_fields = circuit_info.missing_fields()
                    warning_msg = f"数据不完整，缺失: {', '.join(missing_fields)}"
                    logger.warning(f"⚠️ {warning_msg}")
                    # 即使不完整也继续更新已有的数据
                
                # 更新赛道信息
                updated = self._update_circuit_from_info(circuit, circuit_info)
                
                if updated:
                    # 提交数据库更改
                    self.db.commit()
                    self.db.refresh(circuit)
                    logger.info(f"✅ 成功同步赛道: {circuit.circuit_name}")
                    return True, "同步成功"
                else:
                    logger.info(f"ℹ️ 赛道无需更新: {circuit.circuit_name}")
                    return True, "无需更新"
                
        except SQLAlchemyError as e:
            logger.error(f"❌ 数据库错误 {circuit.circuit_name}: {e}")
            self.db.rollback()
            return False, f"数据库错误: {str(e)}"
        except Exception as e:
            logger.error(f"❌ 同步赛道失败 {circuit.circuit_name}: {e}")
            self.db.rollback()
            return False, f"同步失败: {str(e)}"
    
    def _circuit_has_complete_info(self, circuit: Circuit) -> bool:
        """检查赛道是否已有完整信息"""
        required_fields = [
            circuit.length,
            circuit.first_grand_prix,
            circuit.typical_lap_count,
            circuit.race_distance,
            circuit.circuit_layout_image_url
        ]
        return all(field is not None for field in required_fields)
    
    async def sync_circuits_batch(
        self, 
        circuit_ids: Optional[List[str]] = None, 
        force_update: bool = False,
        delay_between_requests: float = 3.0
    ) -> CircuitSyncResult:
        """批量同步赛道信息"""
        
        result = CircuitSyncResult()
        
        try:
            # 获取要同步的赛道
            if circuit_ids:
                circuits = self.db.query(Circuit).filter(Circuit.circuit_id.in_(circuit_ids)).all()
                missing_ids = set(circuit_ids) - {c.circuit_id for c in circuits}
                if missing_ids:
                    logger.warning(f"⚠️ 未找到的赛道ID: {', '.join(missing_ids)}")
            else:
                circuits = self.db.query(Circuit).all()
            
            result.total = len(circuits)
            logger.info(f"🚀 开始批量同步 {result.total} 个赛道")
            
            # 逐个同步
            for i, circuit in enumerate(circuits, 1):
                try:
                    logger.info(f"🎯 进度 [{i}/{result.total}] 处理: {circuit.circuit_id}")
                    
                    success, message = await self.sync_single_circuit(circuit, force_update)
                    
                    if success:
                        if "跳过" in message or "无需更新" in message:
                            result.add_skip(circuit.circuit_id)
                        else:
                            result.add_success(circuit.circuit_id)
                    else:
                        result.add_failure(circuit.circuit_id, message)
                    
                    # 请求间延迟（最后一个赛道不需要延迟）
                    if i < result.total:
                        logger.info(f"⏳ 等待 {delay_between_requests} 秒后继续...")
                        await asyncio.sleep(delay_between_requests)
                
                except Exception as e:
                    error_msg = f"处理异常: {str(e)}"
                    logger.error(f"💥 {circuit.circuit_id}: {error_msg}")
                    result.add_failure(circuit.circuit_id, error_msg)
            
        except Exception as e:
            logger.error(f"💥 批量同步过程中发生异常: {e}")
        
        # 输出结果摘要
        result.print_summary()
        
        return result
    
    async def sync_missing_circuits(self, delay_between_requests: float = 3.0) -> CircuitSyncResult:
        """只同步缺失信息的赛道"""
        
        # 查找缺失信息的赛道
        circuits = self.db.query(Circuit).all()
        missing_circuits = [
            circuit for circuit in circuits
            if not self._circuit_has_complete_info(circuit)
        ]
        
        missing_ids = [c.circuit_id for c in missing_circuits]
        
        logger.info(f"🔍 发现 {len(missing_circuits)} 个赛道缺失信息")
        if missing_ids:
            logger.info(f"缺失信息的赛道: {', '.join(missing_ids)}")
        
        return await self.sync_circuits_batch(missing_ids, force_update=False, delay_between_requests=delay_between_requests)


async def sync_circuits_main(
    circuit_ids: Optional[List[str]] = None,
    force_update: bool = False,
    missing_only: bool = False,
    delay_between_requests: float = 3.0
) -> CircuitSyncResult:
    """主同步函数 - 供脚本调用"""
    
    db = next(get_db())
    service = CircuitSyncServiceV2(db)
    
    try:
        if missing_only:
            logger.info("🎯 只同步缺失信息的赛道")
            return await service.sync_missing_circuits(delay_between_requests)
        else:
            if circuit_ids:
                logger.info(f"🎯 同步指定赛道: {circuit_ids}")
            else:
                logger.info("🎯 同步所有赛道")
            
            return await service.sync_circuits_batch(
                circuit_ids=circuit_ids,
                force_update=force_update,
                delay_between_requests=delay_between_requests
            )
    
    finally:
        db.close()


# 测试函数
async def test_sync_service():
    """测试同步服务"""
    
    # 测试少量赛道
    test_circuits = ["spa", "silverstone", "monaco"]
    
    result = await sync_circuits_main(
        circuit_ids=test_circuits,
        force_update=True,  # 强制更新用于测试
        delay_between_requests=2.0
    )
    
    print(f"\n测试完成:")
    print(f"成功: {result.successful}")
    print(f"失败: {result.failed}")
    print(f"跳过: {result.skipped}")


if __name__ == "__main__":
    asyncio.run(test_sync_service()) 