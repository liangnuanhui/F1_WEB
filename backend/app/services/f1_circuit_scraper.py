"""
F1官网赛道信息抓取服务

从F1官网获取赛道详细信息：
- 赛道布局图（基于URL模式直接构建）
- Circuit Length（赛道长度）
- First Grand Prix（首次举办大奖赛年份）
- Number of Laps（圈数）
- Fastest lap time（最快圈速）
- Race Distance（比赛距离）
"""

import asyncio
import aiohttp
import logging
from typing import Dict, Optional, List
from pathlib import Path
import re
from bs4 import BeautifulSoup
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class CircuitInfo:
    """赛道信息数据类"""
    circuit_length: Optional[float] = None  # km
    first_grand_prix: Optional[int] = None
    number_of_laps: Optional[int] = None
    fastest_lap_time: Optional[str] = None
    fastest_lap_driver: Optional[str] = None
    fastest_lap_year: Optional[int] = None
    race_distance: Optional[float] = None  # km
    layout_image_url: Optional[str] = None
    layout_image_path: Optional[str] = None


class F1CircuitScraper:
    """F1官网赛道信息抓取器"""
    
    def __init__(self, images_dir: str = "static/circuit_images"):
        self.base_url = "https://www.formula1.com"
        self.circuit_image_base_url = "https://media.formula1.com/image/upload/c_fit,h_704/q_auto/v1740000000/content/dam/fom-website/2018-redesign-assets/Circuit%20maps%2016x9/"
        self.session: Optional[aiohttp.ClientSession] = None
        self.images_dir = Path(images_dir)
        self.images_dir.mkdir(parents=True, exist_ok=True)
        
        # 国家名称到F1官网URL和图片文件名的映射
        self.circuit_mapping = {
            "bahrain": {
                "url_name": "bahrain",
                "image_name": "Bahrain_Circuit.webp"
            },
            "saudi arabia": {
                "url_name": "saudi-arabia", 
                "image_name": "Saudi_Arabia_Circuit.webp"
            },
            "australia": {
                "url_name": "australia",
                "image_name": "Australia_Circuit.webp"
            },
            "azerbaijan": {
                "url_name": "azerbaijan",
                "image_name": "Azerbaijan_Circuit.webp"
            },
            "miami": {
                "url_name": "miami",
                "image_name": "Miami_Circuit.webp"
            },
            "italy": {
                "url_name": "italy",
                "image_name": "Italy_Circuit.webp"
            },
            "monaco": {
                "url_name": "monaco",
                "image_name": "Monaco_Circuit.webp"
            },
            "canada": {
                "url_name": "canada",
                "image_name": "Canada_Circuit.webp"
            },
            "spain": {
                "url_name": "spain",
                "image_name": "Spain_Circuit.webp"
            },
            "austria": {
                "url_name": "austria",
                "image_name": "Austria_Circuit.webp"
            },
            "great britain": {
                "url_name": "great-britain",
                "image_name": "Great_Britain_Circuit.webp"
            },
            "hungary": {
                "url_name": "hungary",
                "image_name": "Hungary_Circuit.webp"
            },
            "belgium": {
                "url_name": "belgium",
                "image_name": "Belgium_Circuit.webp"
            },
            "netherlands": {
                "url_name": "netherlands", 
                "image_name": "Netherlands_Circuit.webp"
            },
            "singapore": {
                "url_name": "singapore",
                "image_name": "Singapore_Circuit.webp"
            },
            "united states": {
                "url_name": "united-states",
                "image_name": "United_States_Circuit.webp"
            },
            "mexico": {
                "url_name": "mexico",
                "image_name": "Mexico_Circuit.webp"
            },
            "brazil": {
                "url_name": "brazil",
                "image_name": "Brazil_Circuit.webp"
            },
            "las vegas": {
                "url_name": "las-vegas",
                "image_name": "Las_Vegas_Circuit.webp"
            },
            "qatar": {
                "url_name": "qatar",
                "image_name": "Qatar_Circuit.webp"
            },
            "abu dhabi": {
                "url_name": "abu-dhabi",
                "image_name": "Abu_Dhabi_Circuit.webp"
            },
            "china": {
                "url_name": "china",
                "image_name": "China_Circuit.webp"
            },
            "japan": {
                "url_name": "japan",
                "image_name": "Japan_Circuit.webp"
            }
        }
    
    async def __aenter__(self):
        """异步上下文管理器入口"""
        self.session = aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(total=30),
            headers={
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
            }
        )
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """异步上下文管理器退出"""
        if self.session:
            await self.session.close()
    
    def _get_circuit_info(self, country: str) -> Optional[Dict[str, str]]:
        """根据国家获取赛道信息"""
        country_lower = country.lower()
        return self.circuit_mapping.get(country_lower)
    
    def _get_circuit_image_url(self, country: str) -> Optional[str]:
        """根据国家获取赛道布局图URL"""
        circuit_info = self._get_circuit_info(country)
        if circuit_info:
            return self.circuit_image_base_url + circuit_info["image_name"]
        return None
    
    def _get_circuit_page_url(self, country: str) -> Optional[str]:
        """根据国家获取F1官网赛道页面URL"""
        circuit_info = self._get_circuit_info(country)
        if circuit_info:
            return f"{self.base_url}/en/racing/2025/{circuit_info['url_name']}"
        return None
    
    async def _download_image(self, image_url: str, filename: str) -> Optional[str]:
        """下载赛道布局图"""
        try:
            if not self.session:
                return None
                
            async with self.session.get(image_url) as response:
                if response.status == 200:
                    file_path = self.images_dir / filename
                    with open(file_path, 'wb') as f:
                        f.write(await response.read())
                    
                    logger.info(f"✅ 下载赛道布局图: {filename}")
                    return str(file_path)
                else:
                    logger.warning(f"❌ 下载失败 {image_url}: HTTP {response.status}")
                    return None
        except Exception as e:
            logger.error(f"❌ 下载图片失败 {image_url}: {e}")
            return None
    
    def _parse_lap_time(self, lap_time_text: str) -> tuple[Optional[str], Optional[str], Optional[int]]:
        """解析最快圈速信息"""
        # 示例: "1:44.701 Sergio Perez (2024)"
        pattern = r'(\d+:\d+\.\d+)\s+([^(]+)\s*\((\d+)\)'
        match = re.search(pattern, lap_time_text)
        
        if match:
            time = match.group(1).strip()
            driver = match.group(2).strip()
            year = int(match.group(3))
            return time, driver, year
        
        return None, None, None
    
    def _extract_number(self, text: str) -> Optional[float]:
        """从文本中提取数字"""
        # 匹配数字（包括小数点）
        pattern = r'(\d+\.?\d*)'
        match = re.search(pattern, text.replace(',', ''))
        
        if match:
            return float(match.group(1))
        return None
    
    async def scrape_circuit_info(self, country: str, locality: str = "") -> Optional[CircuitInfo]:
        """抓取指定赛道的详细信息"""
        circuit_page_url = self._get_circuit_page_url(country)
        if not circuit_page_url:
            logger.warning(f"未找到 {country} 对应的F1官网URL")
            return None
        
        try:
            if not self.session:
                return None
                
            logger.info(f"🏁 开始抓取赛道信息: {circuit_page_url}")
            
            async with self.session.get(circuit_page_url) as response:
                if response.status != 200:
                    logger.error(f"❌ 访问失败 {circuit_page_url}: HTTP {response.status}")
                    return None
                
                html = await response.text()
                soup = BeautifulSoup(html, 'html.parser')
                
                circuit_info = CircuitInfo()
                
                # 设置赛道布局图URL（使用我们发现的模式）
                circuit_info.layout_image_url = self._get_circuit_image_url(country)
                
                # 查找赛道信息区域 - 使用更通用的选择器
                # F1官网通常将这些信息放在包含"circuit"关键词的区域
                text_content = soup.get_text()
                
                # 提取赛道长度 (Circuit Length)
                length_match = re.search(r'Circuit Length\s*([0-9.]+)\s*km', text_content, re.I)
                if length_match:
                    circuit_info.circuit_length = float(length_match.group(1))
                
                # 提取首次大奖赛年份 (First Grand Prix)
                first_gp_match = re.search(r'First Grand Prix\s*(\d{4})', text_content, re.I)
                if first_gp_match:
                    circuit_info.first_grand_prix = int(first_gp_match.group(1))
                
                # 提取圈数 (Number of Laps)
                laps_match = re.search(r'Number of Laps\s*(\d+)', text_content, re.I)
                if laps_match:
                    circuit_info.number_of_laps = int(laps_match.group(1))
                
                # 提取最快圈速 (Fastest lap time) - 使用更宽松的模式处理换行和空格
                fastest_lap_match = re.search(r'Fastest lap time\s*\n?\s*(\d+:\d+\.\d+)\s*\n?\s*([^(]+?)\s*\((\d+)\)', text_content, re.I)
                if fastest_lap_match:
                    circuit_info.fastest_lap_time = fastest_lap_match.group(1)
                    circuit_info.fastest_lap_driver = fastest_lap_match.group(2).strip()
                    circuit_info.fastest_lap_year = int(fastest_lap_match.group(3))
                
                # 提取比赛距离 (Race Distance)
                distance_match = re.search(r'Race Distance\s*([0-9.]+)\s*km', text_content, re.I)
                if distance_match:
                    circuit_info.race_distance = float(distance_match.group(1))
                
                # 下载赛道布局图
                if circuit_info.layout_image_url:
                    country_clean = re.sub(r'[^a-zA-Z0-9]', '_', country.lower())
                    img_filename = f"{country_clean}_circuit.webp"
                    
                    downloaded_path = await self._download_image(circuit_info.layout_image_url, img_filename)
                    if downloaded_path:
                        circuit_info.layout_image_path = downloaded_path
                
                logger.info(f"✅ 抓取完成: {country}")
                logger.info(f"   赛道长度: {circuit_info.circuit_length} km")
                logger.info(f"   首次GP: {circuit_info.first_grand_prix}")
                logger.info(f"   圈数: {circuit_info.number_of_laps}")
                logger.info(f"   最快圈速: {circuit_info.fastest_lap_time} by {circuit_info.fastest_lap_driver} ({circuit_info.fastest_lap_year})")
                logger.info(f"   比赛距离: {circuit_info.race_distance} km")
                
                return circuit_info
                
        except Exception as e:
            logger.error(f"❌ 抓取失败 {country}: {e}")
            return None
    
    async def scrape_all_circuits(self, circuits: List[Dict[str, str]]) -> Dict[str, CircuitInfo]:
        """批量抓取多个赛道信息"""
        results = {}
        
        for circuit in circuits:
            country = circuit.get('country', '')
            locality = circuit.get('locality', '')
            circuit_id = circuit.get('circuit_id', f"{country}_{locality}")
            
            info = await self.scrape_circuit_info(country, locality)
            if info:
                results[circuit_id] = info
            
            # 添加延迟避免被封
            await asyncio.sleep(2)
        
        return results


async def test_scraper():
    """测试抓取器"""
    test_circuits = [
        {"country": "Belgium", "locality": "Spa-Francorchamps", "circuit_id": "spa"},
        {"country": "Great Britain", "locality": "Silverstone", "circuit_id": "silverstone"},
        {"country": "Hungary", "locality": "Hungaroring", "circuit_id": "hungaroring"}
    ]
    
    async with F1CircuitScraper() as scraper:
        results = await scraper.scrape_all_circuits(test_circuits)
        
        for circuit_id, info in results.items():
            print(f"\n=== {circuit_id.upper()} ===")
            print(f"Circuit Length: {info.circuit_length} km")
            print(f"First Grand Prix: {info.first_grand_prix}")
            print(f"Number of Laps: {info.number_of_laps}")
            print(f"Fastest Lap: {info.fastest_lap_time} by {info.fastest_lap_driver} ({info.fastest_lap_year})")
            print(f"Race Distance: {info.race_distance} km")
            print(f"Layout Image URL: {info.layout_image_url}")
            print(f"Local Image Path: {info.layout_image_path}")


if __name__ == "__main__":
    asyncio.run(test_scraper()) 