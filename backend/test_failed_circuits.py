#!/usr/bin/env python3

import asyncio
import aiohttp
from bs4 import BeautifulSoup
import logging

# 设置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def test_circuit_urls():
    """测试两个失败赛道的URL访问"""
    
    # 测试URL
    test_urls = {
        "imola": "https://www.formula1.com/en/racing/2025/emiliaromagna",
        "yas_marina": "https://www.formula1.com/en/racing/2025/united-arab-emirates"
    }
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1'
    }
    
    connector = aiohttp.TCPConnector(limit=10, limit_per_host=3)
    timeout = aiohttp.ClientTimeout(total=60, connect=10, sock_read=30)
    
    async with aiohttp.ClientSession(connector=connector, timeout=timeout, headers=headers) as session:
        for circuit_id, url in test_urls.items():
            try:
                logger.info(f"🔍 测试 {circuit_id}: {url}")
                
                async with session.get(url) as response:
                    if response.status == 200:
                        html = await response.text()
                        soup = BeautifulSoup(html, 'html.parser')
                        
                        # 检查是否包含赛道信息
                        circuit_section = soup.find('section', {'class': 'circuit'}) or soup.find('div', text='Circuit')
                        if circuit_section:
                            logger.info(f"✅ {circuit_id} URL正确，找到赛道信息")
                        else:
                            logger.warning(f"⚠️ {circuit_id} URL可访问但未找到赛道信息")
                            
                        # 检查关键信息
                        text_content = soup.get_text()
                        
                        # 查找长度
                        if 'Circuit Length' in text_content:
                            logger.info(f"  ✓ 找到赛道长度信息")
                        else:
                            logger.warning(f"  ❌ 未找到赛道长度信息")
                            
                        # 查找首次GP
                        if 'First Grand Prix' in text_content:
                            logger.info(f"  ✓ 找到首次GP信息")
                        else:
                            logger.warning(f"  ❌ 未找到首次GP信息")
                            
                        # 查找圈数
                        if 'Number of Laps' in text_content:
                            logger.info(f"  ✓ 找到圈数信息")
                        else:
                            logger.warning(f"  ❌ 未找到圈数信息")
                            
                        # 查找最快圈速
                        if 'Fastest lap time' in text_content:
                            logger.info(f"  ✓ 找到最快圈速信息")
                        else:
                            logger.warning(f"  ❌ 未找到最快圈速信息")
                            
                        # 查找比赛距离
                        if 'Race Distance' in text_content:
                            logger.info(f"  ✓ 找到比赛距离信息")
                        else:
                            logger.warning(f"  ❌ 未找到比赛距离信息")
                            
                        logger.info(f"📄 {circuit_id} 页面内容长度: {len(html)} 字符")
                        
                    else:
                        logger.error(f"❌ {circuit_id} HTTP错误: {response.status}")
                        
            except Exception as e:
                logger.error(f"❌ {circuit_id} 访问失败: {e}")
                
            await asyncio.sleep(2)  # 延迟请求

if __name__ == "__main__":
    asyncio.run(test_circuit_urls()) 