"""
F1官网赛道信息抓取服务 v2.0 - 改进版

改进内容：
1. 修复国家名称映射问题，支持多赛道对应一个国家
2. 增强错误处理和重试机制
3. 添加详细的日志记录和数据验证
4. 改进批量处理的稳定性
5. 添加超时和频率限制保护
"""

import asyncio
import aiohttp
import logging
from typing import Dict, Optional, List, Tuple
from pathlib import Path
import re
from bs4 import BeautifulSoup
from dataclasses import dataclass
import time
from urllib.parse import urljoin

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
    
    def is_complete(self) -> bool:
        """检查是否获取到完整信息"""
        required_fields = [
            self.circuit_length,
            self.first_grand_prix,
            self.number_of_laps,
            self.race_distance
        ]
        return all(field is not None for field in required_fields)
    
    def missing_fields(self) -> List[str]:
        """返回缺失的字段列表"""
        missing = []
        if self.circuit_length is None:
            missing.append("赛道长度")
        if self.first_grand_prix is None:
            missing.append("首次GP")
        if self.number_of_laps is None:
            missing.append("圈数")
        if self.race_distance is None:
            missing.append("比赛距离")
        if self.fastest_lap_time is None:
            missing.append("最快圈速")
        return missing


class F1CircuitScraperV2:
    """F1官网赛道信息抓取器 v2.0"""
    
    def __init__(self, images_dir: str = "static/circuit_images"):
        self.base_url = "https://www.formula1.com"
        self.circuit_image_base_url = "https://media.formula1.com/image/upload/c_fit,h_704/q_auto/v1740000000/content/dam/fom-website/2018-redesign-assets/Circuit%20maps%2016x9/"
        self.session: Optional[aiohttp.ClientSession] = None
        self.images_dir = Path(images_dir)
        self.images_dir.mkdir(parents=True, exist_ok=True)
        
        # 改进的映射关系 - 支持赛道ID到国家和URL的直接映射
        self.circuit_mapping = {
            # 巴林
            "bahrain": {
                "country_match": ["bahrain"],
                "url_name": "bahrain",
                "image_name": "Bahrain_Circuit.webp"
            },
            # 沙特阿拉伯
            "jeddah": {
                "country_match": ["saudi arabia"],
                "url_name": "saudi-arabia", 
                "image_name": "Saudi_Arabia_Circuit.webp"
            },
            # 澳大利亚
            "albert_park": {
                "country_match": ["australia"],
                "url_name": "australia",
                "image_name": "Australia_Circuit.webp"
            },
            # 阿塞拜疆
            "baku": {
                "country_match": ["azerbaijan"],
                "url_name": "azerbaijan",
                "image_name": "Baku_Circuit.webp"
            },
            # 美国 - 迈阿密
            "miami": {
                "country_match": ["usa"],
                "url_name": "miami",
                "image_name": "Miami_Circuit.webp"
            },
            # 意大利 - 伊莫拉
            "imola": {
                "country_match": ["italy"],
                "url_name": "emiliaromagna",  # F1官网使用的URL名称 (无连字符)
                "image_name": "Emilia_Romagna_Circuit.webp"
            },
            # 摩纳哥
            "monaco": {
                "country_match": ["monaco"],
                "url_name": "monaco",
                "image_name": "Monaco_Circuit.webp"
            },
            # 加拿大
            "villeneuve": {
                "country_match": ["canada"],
                "url_name": "canada",
                "image_name": "Canada_Circuit.webp"
            },
            # 西班牙
            "catalunya": {
                "country_match": ["spain"],
                "url_name": "spain",
                "image_name": "Spain_Circuit.webp"
            },
            # 奥地利
            "red_bull_ring": {
                "country_match": ["austria"],
                "url_name": "austria",
                "image_name": "Austria_Circuit.webp"
            },
            # 英国
            "silverstone": {
                "country_match": ["uk", "great britain"],
                "url_name": "great-britain",
                "image_name": "Great_Britain_Circuit.webp"
            },
            # 匈牙利
            "hungaroring": {
                "country_match": ["hungary"],
                "url_name": "hungary",
                "image_name": "Hungary_Circuit.webp"
            },
            # 比利时
            "spa": {
                "country_match": ["belgium"],
                "url_name": "belgium",
                "image_name": "Belgium_Circuit.webp"
            },
            # 荷兰
            "zandvoort": {
                "country_match": ["netherlands"], 
                "url_name": "netherlands",
                "image_name": "Netherlands_Circuit.webp"
            },
            # 意大利 - 蒙扎
            "monza": {
                "country_match": ["italy"],
                "url_name": "italy",
                "image_name": "Italy_Circuit.webp"
            },
            # 新加坡
            "marina_bay": {
                "country_match": ["singapore"],
                "url_name": "singapore",
                "image_name": "Singapore_Circuit.webp"
            },
            # 美国 - 奥斯汀
            "americas": {
                "country_match": ["usa"],
                "url_name": "united-states",
                "image_name": "USA_Circuit.webp"
            },
            # 墨西哥
            "rodriguez": {
                "country_match": ["mexico"],
                "url_name": "mexico",
                "image_name": "Mexico_Circuit.webp"
            },
            # 巴西
            "interlagos": {
                "country_match": ["brazil"],
                "url_name": "brazil",
                "image_name": "Brazil_Circuit.webp"
            },
            # 美国 - 拉斯维加斯
            "vegas": {
                "country_match": ["usa"],
                "url_name": "las-vegas",
                "image_name": "Las_Vegas_Circuit.webp"
            },
            # 卡塔尔
            "losail": {
                "country_match": ["qatar"],
                "url_name": "qatar",
                "image_name": "Qatar_Circuit.webp"
            },
            # 阿联酋
            "yas_marina": {
                "country_match": ["uae", "abu dhabi"],
                "url_name": "united-arab-emirates",
                "image_name": "Abu_Dhabi_Circuit.webp"
            },
            # 中国
            "shanghai": {
                "country_match": ["china"],
                "url_name": "china",
                "image_name": "China_Circuit.webp"
            },
            # 日本
            "suzuka": {
                "country_match": ["japan"],
                "url_name": "japan",
                "image_name": "Japan_Circuit.webp"
            }
        }
    
    async def __aenter__(self):
        """异步上下文管理器入口"""
        connector = aiohttp.TCPConnector(limit=10, limit_per_host=3)
        timeout = aiohttp.ClientTimeout(total=60, connect=10, sock_read=30)
        
        self.session = aiohttp.ClientSession(
            connector=connector,
            timeout=timeout,
            headers={
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.9',
                'Accept-Encoding': 'gzip, deflate, br',
                'DNT': '1',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1'
            }
        )
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """异步上下文管理器退出"""
        if self.session:
            await self.session.close()
    
    def find_circuit_mapping_by_country(self, country: str) -> Optional[Tuple[str, Dict]]:
        """根据国家名称查找赛道映射"""
        country_lower = country.lower()
        
        for circuit_id, mapping in self.circuit_mapping.items():
            if country_lower in [c.lower() for c in mapping["country_match"]]:
                return circuit_id, mapping
        
        return None
    
    def find_circuit_mapping_by_id(self, circuit_id: str) -> Optional[Dict]:
        """根据赛道ID查找映射"""
        return self.circuit_mapping.get(circuit_id)
    
    def get_circuit_page_url(self, circuit_id: str) -> Optional[str]:
        """根据赛道ID获取F1官网页面URL"""
        mapping = self.find_circuit_mapping_by_id(circuit_id)
        if mapping:
            return f"{self.base_url}/en/racing/2025/{mapping['url_name']}"
        return None
    
    def get_circuit_image_url(self, circuit_id: str) -> Optional[str]:
        """根据赛道ID获取布局图URL"""
        mapping = self.find_circuit_mapping_by_id(circuit_id)
        if mapping:
            return self.circuit_image_base_url + mapping["image_name"]
        return None
    
    async def download_image_with_retry(self, image_url: str, filename: str, max_retries: int = 3) -> Optional[str]:
        """带重试机制的图片下载"""
        for attempt in range(max_retries):
            try:
                if not self.session:
                    return None
                
                logger.info(f"📥 下载图片 (尝试 {attempt + 1}/{max_retries}): {filename}")
                
                async with self.session.get(image_url) as response:
                    if response.status == 200:
                        file_path = self.images_dir / filename
                        content = await response.read()
                        
                        with open(file_path, 'wb') as f:
                            f.write(content)
                        
                        file_size = len(content) / 1024  # KB
                        logger.info(f"✅ 下载成功: {filename} ({file_size:.1f}KB)")
                        return str(file_path)
                    else:
                        logger.warning(f"❌ HTTP错误 {response.status}: {image_url}")
                        
            except asyncio.TimeoutError:
                logger.warning(f"⏰ 下载超时 (尝试 {attempt + 1}/{max_retries}): {filename}")
            except Exception as e:
                logger.warning(f"❌ 下载失败 (尝试 {attempt + 1}/{max_retries}): {e}")
            
            if attempt < max_retries - 1:
                await asyncio.sleep(2 ** attempt)  # 指数退避
        
        logger.error(f"💥 下载失败，已达最大重试次数: {filename}")
        return None
    
    def extract_circuit_data(self, text_content: str) -> CircuitInfo:
        """从网页文本中提取赛道数据"""
        circuit_info = CircuitInfo()
        
        try:
            # 提取赛道长度 (Circuit Length)
            length_match = re.search(r'Circuit Length\s*([0-9.]+)\s*km', text_content, re.I)
            if length_match:
                circuit_info.circuit_length = float(length_match.group(1))
                logger.debug(f"  ✓ 赛道长度: {circuit_info.circuit_length}km")
            
            # 提取首次大奖赛年份 (First Grand Prix)
            first_gp_match = re.search(r'First Grand Prix\s*(\d{4})', text_content, re.I)
            if first_gp_match:
                circuit_info.first_grand_prix = int(first_gp_match.group(1))
                logger.debug(f"  ✓ 首次GP: {circuit_info.first_grand_prix}")
            
            # 提取圈数 (Number of Laps)
            laps_match = re.search(r'Number of Laps\s*(\d+)', text_content, re.I)
            if laps_match:
                circuit_info.number_of_laps = int(laps_match.group(1))
                logger.debug(f"  ✓ 圈数: {circuit_info.number_of_laps}")
            
            # 提取最快圈速 (Fastest lap time) - 使用改进的正则表达式
            fastest_lap_patterns = [
                r'Fastest lap time\s*\n?\s*(\d+:\d+\.\d+)\s*\n?\s*([^(]+?)\s*\((\d+)\)',
                r'Fastest.*?(\d+:\d+\.\d+).*?([A-Za-z ]+)\s*\((\d+)\)',
                r'(\d+:\d+\.\d+)\s+([A-Za-z ]+(?:[A-Za-z ]+)?)\s*\((\d{4})\)'
            ]
            
            for pattern in fastest_lap_patterns:
                fastest_lap_match = re.search(pattern, text_content, re.I)
                if fastest_lap_match:
                    circuit_info.fastest_lap_time = fastest_lap_match.group(1)
                    circuit_info.fastest_lap_driver = fastest_lap_match.group(2).strip()
                    circuit_info.fastest_lap_year = int(fastest_lap_match.group(3))
                    logger.debug(f"  ✓ 最快圈速: {circuit_info.fastest_lap_time} by {circuit_info.fastest_lap_driver} ({circuit_info.fastest_lap_year})")
                    break
            
            # 提取比赛距离 (Race Distance)
            distance_match = re.search(r'Race Distance\s*([0-9.]+)\s*km', text_content, re.I)
            if distance_match:
                circuit_info.race_distance = float(distance_match.group(1))
                logger.debug(f"  ✓ 比赛距离: {circuit_info.race_distance}km")
                
        except Exception as e:
            logger.error(f"❌ 数据提取失败: {e}")
        
        return circuit_info
    
    async def scrape_circuit_info_with_retry(self, circuit_id: str, max_retries: int = 3) -> Optional[CircuitInfo]:
        """带重试机制的赛道信息抓取"""
        
        for attempt in range(max_retries):
            try:
                logger.info(f"🔍 抓取赛道信息 {circuit_id} (尝试 {attempt + 1}/{max_retries})")
                
                # 获取页面URL
                page_url = self.get_circuit_page_url(circuit_id)
                if not page_url:
                    logger.error(f"❌ 未找到赛道 {circuit_id} 的URL映射")
                    return None
                
                if not self.session:
                    logger.error("❌ HTTP会话未初始化")
                    return None
                
                logger.info(f"📄 访问页面: {page_url}")
                
                # 获取页面内容
                async with self.session.get(page_url) as response:
                    if response.status != 200:
                        logger.warning(f"❌ HTTP错误 {response.status}: {page_url}")
                        if attempt < max_retries - 1:
                            await asyncio.sleep(2 ** attempt)
                            continue
                        return None
                    
                    html = await response.text()
                    logger.info(f"✅ 页面获取成功，内容长度: {len(html)}")
                
                # 解析页面内容
                soup = BeautifulSoup(html, 'html.parser')
                text_content = soup.get_text()
                
                # 提取数据
                circuit_info = self.extract_circuit_data(text_content)
                
                # 设置布局图URL
                circuit_info.layout_image_url = self.get_circuit_image_url(circuit_id)
                
                # 下载布局图
                if circuit_info.layout_image_url:
                    img_filename = f"{circuit_id}_circuit.webp"
                    downloaded_path = await self.download_image_with_retry(
                        circuit_info.layout_image_url, img_filename
                    )
                    if downloaded_path:
                        circuit_info.layout_image_path = downloaded_path
                
                # 验证数据完整性
                missing_fields = circuit_info.missing_fields()
                if missing_fields:
                    logger.warning(f"⚠️ 缺失字段 {circuit_id}: {', '.join(missing_fields)}")
                else:
                    logger.info(f"✅ 数据完整 {circuit_id}")
                
                # 输出摘要
                logger.info(f"📊 {circuit_id} 抓取摘要:")
                logger.info(f"   📏 赛道长度: {circuit_info.circuit_length or 'N/A'} km")
                logger.info(f"   🏁 首次GP: {circuit_info.first_grand_prix or 'N/A'}")
                logger.info(f"   🔄 圈数: {circuit_info.number_of_laps or 'N/A'}")
                logger.info(f"   ⏱️ 最快圈速: {circuit_info.fastest_lap_time or 'N/A'}")
                logger.info(f"   📐 比赛距离: {circuit_info.race_distance or 'N/A'} km")
                
                return circuit_info
                
            except asyncio.TimeoutError:
                logger.warning(f"⏰ 请求超时 {circuit_id} (尝试 {attempt + 1}/{max_retries})")
            except Exception as e:
                logger.warning(f"❌ 抓取失败 {circuit_id} (尝试 {attempt + 1}/{max_retries}): {e}")
            
            if attempt < max_retries - 1:
                delay = 2 ** attempt
                logger.info(f"⏳ 等待 {delay} 秒后重试...")
                await asyncio.sleep(delay)
        
        logger.error(f"💥 抓取失败，已达最大重试次数: {circuit_id}")
        return None
    
    async def scrape_circuits_batch(self, circuit_ids: List[str], delay_between_requests: float = 3.0) -> Dict[str, Optional[CircuitInfo]]:
        """批量抓取多个赛道信息"""
        results = {}
        total = len(circuit_ids)
        
        logger.info(f"🚀 开始批量抓取 {total} 个赛道")
        
        for i, circuit_id in enumerate(circuit_ids, 1):
            logger.info(f"🎯 进度 [{i}/{total}] 处理赛道: {circuit_id}")
            
            try:
                circuit_info = await self.scrape_circuit_info_with_retry(circuit_id)
                results[circuit_id] = circuit_info
                
                if circuit_info:
                    status = "✅ 成功"
                    if not circuit_info.is_complete():
                        status += f" (缺失: {', '.join(circuit_info.missing_fields())})"
                else:
                    status = "❌ 失败"
                
                logger.info(f"   结果: {status}")
                
            except Exception as e:
                logger.error(f"💥 处理赛道 {circuit_id} 时发生异常: {e}")
                results[circuit_id] = None
            
            # 请求间延迟
            if i < total:
                logger.info(f"⏳ 等待 {delay_between_requests} 秒后继续...")
                await asyncio.sleep(delay_between_requests)
        
        # 输出批量处理摘要
        successful = sum(1 for info in results.values() if info is not None)
        complete = sum(1 for info in results.values() if info and info.is_complete())
        
        logger.info(f"📊 批量处理完成:")
        logger.info(f"   总计: {total}")
        logger.info(f"   成功: {successful}")
        logger.info(f"   完整: {complete}")
        logger.info(f"   失败: {total - successful}")
        
        return results
    
    def validate_circuit_mapping_coverage(self, db_circuit_ids: List[str]) -> Dict[str, List[str]]:
        """验证映射覆盖情况"""
        mapped = []
        unmapped = []
        
        for circuit_id in db_circuit_ids:
            if circuit_id in self.circuit_mapping:
                mapped.append(circuit_id)
            else:
                unmapped.append(circuit_id)
        
        logger.info(f"📋 映射覆盖情况:")
        logger.info(f"   已映射: {len(mapped)}/{len(db_circuit_ids)}")
        logger.info(f"   未映射: {unmapped if unmapped else '无'}")
        
        return {
            "mapped": mapped,
            "unmapped": unmapped
        }


# 测试函数
async def test_scraper_v2():
    """测试改进版爬虫"""
    test_circuits = ["spa", "silverstone", "monaco"]
    
    async with F1CircuitScraperV2() as scraper:
        # 测试映射验证
        coverage = scraper.validate_circuit_mapping_coverage(test_circuits)
        
        # 批量测试
        results = await scraper.scrape_circuits_batch(test_circuits, delay_between_requests=2.0)
        
        for circuit_id, info in results.items():
            print(f"\n=== {circuit_id.upper()} ===")
            if info:
                print(f"赛道长度: {info.circuit_length} km")
                print(f"首次GP: {info.first_grand_prix}")
                print(f"圈数: {info.number_of_laps}")
                print(f"最快圈速: {info.fastest_lap_time}")
                print(f"比赛距离: {info.race_distance} km")
                print(f"数据完整: {'✅' if info.is_complete() else '❌'}")
            else:
                print("❌ 获取失败")


if __name__ == "__main__":
    asyncio.run(test_scraper_v2()) 