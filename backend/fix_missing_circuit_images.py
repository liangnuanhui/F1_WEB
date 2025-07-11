#!/usr/bin/env python3
"""
修复缺失的赛道图片下载

问题：americas和baku赛道的图片映射配置错误，导致图片未能正确下载
解决：使用正确的图片URL重新下载并更新数据库记录
"""

import asyncio
import aiohttp
import sys
import os
from pathlib import Path
from sqlalchemy.orm import Session

# 添加app目录到路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.core.database import get_db
from app.models.circuit import Circuit
from app.services.f1_circuit_scraper_v2 import F1CircuitScraperV2
import logging

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# 需要修复的赛道配置
CIRCUIT_FIXES = {
    "americas": {
        "name": "Circuit of the Americas",
        "correct_image_url": "https://media.formula1.com/image/upload/c_fit,h_704/q_auto/v1740000000/content/dam/fom-website/2018-redesign-assets/Circuit%20maps%2016x9/USA_Circuit.webp",
        "filename": "USA_Circuit.webp"
    },
    "baku": {
        "name": "Baku City Circuit",
        "correct_image_url": "https://media.formula1.com/image/upload/c_fit,h_704/q_auto/v1740000000/content/dam/fom-website/2018-redesign-assets/Circuit%20maps%2016x9/Baku_Circuit.webp",
        "filename": "Baku_Circuit.webp"
    }
}

async def download_image_direct(url: str, file_path: Path) -> bool:
    """直接下载图片"""
    try:
        connector = aiohttp.TCPConnector(limit=10, limit_per_host=3)
        timeout = aiohttp.ClientTimeout(total=60, connect=10, sock_read=30)
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'image/webp,image/apng,image/*,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        }
        
        async with aiohttp.ClientSession(connector=connector, timeout=timeout, headers=headers) as session:
            logger.info(f"📥 下载图片: {url}")
            
            async with session.get(url) as response:
                if response.status == 200:
                    content = await response.read()
                    
                    # 确保目录存在
                    file_path.parent.mkdir(parents=True, exist_ok=True)
                    
                    # 写入文件
                    with open(file_path, 'wb') as f:
                        f.write(content)
                    
                    file_size = len(content) / 1024  # KB
                    logger.info(f"✅ 下载成功: {file_path.name} ({file_size:.1f}KB)")
                    return True
                else:
                    logger.error(f"❌ HTTP错误 {response.status}: {url}")
                    return False
                    
    except Exception as e:
        logger.error(f"❌ 下载失败: {e}")
        return False

async def fix_circuit_images():
    """修复赛道图片"""
    
    logger.info("🔧 开始修复赛道图片")
    
    # 获取数据库会话
    db = next(get_db())
    images_dir = Path("static/circuit_images")
    
    try:
        success_count = 0
        
        for circuit_id, config in CIRCUIT_FIXES.items():
            logger.info(f"🎯 处理赛道: {circuit_id} ({config['name']})")
            
            # 查找数据库中的赛道记录
            circuit = db.query(Circuit).filter(Circuit.circuit_id == circuit_id).first()
            if not circuit:
                logger.warning(f"⚠️ 数据库中未找到赛道: {circuit_id}")
                continue
            
            # 准备文件路径
            file_path = images_dir / config["filename"]
            
            # 下载图片
            if await download_image_direct(config["correct_image_url"], file_path):
                # 更新数据库记录
                circuit.circuit_layout_image_url = config["correct_image_url"]
                circuit.circuit_layout_image_path = str(file_path)
                
                db.commit()
                db.refresh(circuit)
                
                logger.info(f"✅ 成功修复 {circuit_id}")
                success_count += 1
            else:
                logger.error(f"❌ 修复失败 {circuit_id}")
        
        logger.info("=" * 60)
        logger.info(f"📊 修复完成: {success_count}/{len(CIRCUIT_FIXES)} 个赛道")
        logger.info("=" * 60)
        
        if success_count == len(CIRCUIT_FIXES):
            logger.info("🎉 所有赛道图片修复成功!")
        else:
            logger.warning("⚠️ 部分赛道修复失败")
            
    except Exception as e:
        logger.error(f"💥 修复过程中发生异常: {e}")
        db.rollback()
    finally:
        db.close()

async def verify_fixes():
    """验证修复结果"""
    
    logger.info("🔍 验证修复结果")
    
    db = next(get_db())
    images_dir = Path("static/circuit_images")
    
    try:
        for circuit_id, config in CIRCUIT_FIXES.items():
            circuit = db.query(Circuit).filter(Circuit.circuit_id == circuit_id).first()
            
            if circuit:
                # 检查数据库记录
                has_url = circuit.circuit_layout_image_url is not None
                has_path = circuit.circuit_layout_image_path is not None
                
                # 检查文件是否存在
                file_path = images_dir / config["filename"]
                file_exists = file_path.exists()
                
                logger.info(f"🔍 {circuit_id}:")
                logger.info(f"  数据库URL: {'✅' if has_url else '❌'}")
                logger.info(f"  数据库路径: {'✅' if has_path else '❌'}")
                logger.info(f"  文件存在: {'✅' if file_exists else '❌'}")
                
                if has_url:
                    logger.info(f"  图片URL: {circuit.circuit_layout_image_url}")
                if file_exists:
                    file_size = file_path.stat().st_size / 1024  # KB
                    logger.info(f"  文件大小: {file_size:.1f}KB")
                
                print("-" * 40)
                
    except Exception as e:
        logger.error(f"❌ 验证失败: {e}")
    finally:
        db.close()

async def main():
    """主函数"""
    
    logger.info("🚀 开始修复缺失的赛道图片")
    
    # 修复图片
    await fix_circuit_images()
    
    # 验证结果
    await verify_fixes()
    
    logger.info("✅ 修复完成!")

if __name__ == "__main__":
    asyncio.run(main()) 