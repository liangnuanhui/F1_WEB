#!/usr/bin/env python3

import asyncio
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.services.f1_circuit_scraper_v2 import F1CircuitScraperV2
import logging

# 设置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

async def test_fixed_failed_circuits():
    """测试修复后的两个失败赛道"""
    
    # 需要测试的赛道ID
    test_circuits = ["imola", "yas_marina"]
    
    logger.info("🔧 开始测试修复后的赛道数据抓取")
    
    # 使用修复后的爬虫
    async with F1CircuitScraperV2(images_dir="static/test_images") as scraper:
        results = await scraper.scrape_circuits_batch(test_circuits, delay_between_requests=3.0)
        
        logger.info("=" * 60)
        logger.info("📊 测试结果汇总")
        logger.info("=" * 60)
        
        for circuit_id, circuit_info in results.items():
            if circuit_info:
                logger.info(f"✅ {circuit_id.upper()} - 数据抓取成功")
                logger.info(f"  赛道长度: {circuit_info.circuit_length}km")
                logger.info(f"  首次GP: {circuit_info.first_grand_prix}")
                logger.info(f"  圈数: {circuit_info.number_of_laps}")
                logger.info(f"  比赛距离: {circuit_info.race_distance}km")
                
                if circuit_info.fastest_lap_time:
                    logger.info(f"  最快圈速: {circuit_info.fastest_lap_time} by {circuit_info.fastest_lap_driver} ({circuit_info.fastest_lap_year})")
                else:
                    logger.warning(f"  ⚠️ 未获取到最快圈速")
                
                if circuit_info.layout_image_path:
                    logger.info(f"  布局图: {circuit_info.layout_image_path}")
                else:
                    logger.warning(f"  ⚠️ 未下载布局图")
                
                # 检查数据完整性
                if circuit_info.is_complete():
                    logger.info(f"  ✅ 数据完整")
                else:
                    missing = circuit_info.missing_fields()
                    logger.warning(f"  ⚠️ 缺失字段: {', '.join(missing)}")
                    
            else:
                logger.error(f"❌ {circuit_id.upper()} - 数据抓取失败")
                
            logger.info("-" * 40)
        
        # 统计结果
        successful = sum(1 for info in results.values() if info is not None)
        total = len(results)
        success_rate = (successful / total) * 100
        
        logger.info(f"📈 总体成功率: {successful}/{total} ({success_rate:.1f}%)")
        
        if success_rate == 100:
            logger.info("🎉 所有赛道数据抓取成功！修复验证通过！")
        else:
            logger.warning("⚠️ 部分赛道仍有问题，需要进一步调查")

if __name__ == "__main__":
    asyncio.run(test_fixed_failed_circuits()) 