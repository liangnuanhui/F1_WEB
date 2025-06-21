#!/usr/bin/env python3
"""
FastF1 诊断脚本
用于诊断 FastF1 连接和数据获取问题
"""

import sys
import os
import logging
import pandas as pd
from datetime import datetime

# 添加项目根目录到 Python 路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def test_fastf1_import():
    """测试 FastF1 导入"""
    try:
        import fastf1
        logger.info(f"✅ FastF1 版本: {fastf1.__version__}")
        return True
    except ImportError as e:
        logger.error(f"❌ FastF1 导入失败: {e}")
        return False

def test_ergast_connection():
    """测试 Ergast API 连接"""
    try:
        import fastf1
        from fastf1.ergast import Ergast
        
        logger.info("🔗 测试 Ergast API 连接...")
        ergast = Ergast()
        
        # 测试获取所有赛季
        logger.info("📊 获取所有赛季数据...")
        seasons = ergast.get_seasons()
        logger.info(f"✅ 成功获取 {len(seasons)} 个赛季")
        logger.info(f"📅 赛季范围: {seasons['season'].min()} - {seasons['season'].max()}")
        
        # 显示最近的几个赛季
        recent_seasons = seasons.tail(10)
        logger.info("📋 最近10个赛季:")
        for _, row in recent_seasons.iterrows():
            logger.info(f"   {row['season']}: {row['url']}")
        
        return seasons
        
    except Exception as e:
        logger.error(f"❌ Ergast API 连接失败: {e}")
        return None

def test_2025_season():
    """测试 2025 赛季数据"""
    try:
        import fastf1
        from fastf1.ergast import Ergast
        
        logger.info("🔍 测试 2025 赛季数据...")
        ergast = Ergast()
        
        # 尝试获取 2025 赛季
        seasons_2025 = ergast.get_seasons()
        seasons_2025 = seasons_2025[seasons_2025['season'] == 2025]
        
        if not seasons_2025.empty:
            logger.info("✅ 2025 赛季数据可用")
            logger.info(f"📄 2025 赛季信息: {seasons_2025.iloc[0].to_dict()}")
        else:
            logger.warning("⚠️ 2025 赛季数据不可用")
            
            # 检查最新可用赛季
            all_seasons = ergast.get_seasons()
            latest_year = all_seasons['season'].max()
            logger.info(f"📅 最新可用赛季: {latest_year}")
            
            # 尝试获取 2024 赛季
            seasons_2024 = all_seasons[all_seasons['season'] == 2024]
            if not seasons_2024.empty:
                logger.info("✅ 2024 赛季数据可用，可以作为备选")
            else:
                logger.warning("⚠️ 2024 赛季数据也不可用")
        
        return seasons_2025
        
    except Exception as e:
        logger.error(f"❌ 2025 赛季测试失败: {e}")
        return None

def test_cache_configuration():
    """测试缓存配置"""
    try:
        import fastf1
        
        logger.info("🗂️ 测试缓存配置...")
        
        # 检查当前缓存状态
        cache_dir = "./cache"
        if os.path.exists(cache_dir):
            logger.info(f"✅ 缓存目录存在: {cache_dir}")
            
            # 统计缓存文件
            cache_files = []
            for root, dirs, files in os.walk(cache_dir):
                for file in files:
                    if file.endswith('.ff1pkl'):
                        cache_files.append(os.path.join(root, file))
            
            logger.info(f"📁 缓存文件数量: {len(cache_files)}")
            
            # 显示最近的缓存文件
            if cache_files:
                recent_files = sorted(cache_files, key=os.path.getmtime, reverse=True)[:5]
                logger.info("📋 最近的缓存文件:")
                for file in recent_files:
                    mtime = datetime.fromtimestamp(os.path.getmtime(file))
                    logger.info(f"   {file} (修改时间: {mtime})")
        else:
            logger.warning(f"⚠️ 缓存目录不存在: {cache_dir}")
        
        # 测试启用缓存
        try:
            fastf1.Cache.enable_cache(cache_dir)
            logger.info("✅ 缓存启用成功")
        except Exception as e:
            logger.error(f"❌ 缓存启用失败: {e}")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ 缓存配置测试失败: {e}")
        return False

def test_network_connectivity():
    """测试网络连接"""
    try:
        import httpx
        
        logger.info("🌐 测试网络连接...")
        
        # 测试 Ergast API
        ergast_url = "http://ergast.com/api/f1/seasons.json"
        
        with httpx.Client(timeout=10.0) as client:
            response = client.get(ergast_url)
            
            if response.status_code == 200:
                logger.info("✅ Ergast API 连接正常")
                data = response.json()
                seasons = data.get('MRData', {}).get('SeasonTable', {}).get('Seasons', [])
                logger.info(f"📊 API 返回 {len(seasons)} 个赛季")
                
                # 检查最新赛季
                if seasons:
                    latest_season = max(int(s['season']) for s in seasons)
                    logger.info(f"📅 API 最新赛季: {latest_season}")
                    
                    # 检查 2025 赛季
                    season_2025 = any(s['season'] == '2025' for s in seasons)
                    if season_2025:
                        logger.info("✅ API 中 2025 赛季可用")
                    else:
                        logger.warning("⚠️ API 中 2025 赛季不可用")
                
                return True
            else:
                logger.error(f"❌ Ergast API 连接失败: {response.status_code}")
                return False
                
    except Exception as e:
        logger.error(f"❌ 网络连接测试失败: {e}")
        return False

def main():
    """主诊断函数"""
    logger.info("🔍 开始 FastF1 诊断...")
    
    # 1. 测试 FastF1 导入
    if not test_fastf1_import():
        logger.error("❌ FastF1 导入失败，请检查安装")
        return
    
    # 2. 测试网络连接
    if not test_network_connectivity():
        logger.error("❌ 网络连接失败，请检查网络")
        return
    
    # 3. 测试 Ergast 连接
    seasons = test_ergast_connection()
    if seasons is None:
        logger.error("❌ Ergast 连接失败")
        return
    
    # 4. 测试 2025 赛季
    test_2025_season()
    
    # 5. 测试缓存配置
    test_cache_configuration()
    
    logger.info("✅ 诊断完成")

if __name__ == "__main__":
    main() 