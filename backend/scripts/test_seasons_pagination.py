#!/usr/bin/env python3
"""
测试赛季数据分页机制
验证新的 get_seasons 方法是否正确处理分页
"""

import sys
import os
import logging
import pandas as pd

# 添加项目根目录到 Python 路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.services.data_provider import DataProviderFactory

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def test_seasons_pagination():
    """测试赛季数据分页机制"""
    logger.info("🧪 开始测试赛季数据分页机制...")
    
    try:
        # 创建数据提供者
        provider = DataProviderFactory.get_provider('fastf1')
        
        # 测试1: 获取所有赛季数据
        logger.info("📊 测试1: 获取所有赛季数据...")
        all_seasons = provider.get_seasons()
        
        if not all_seasons.empty:
            logger.info(f"✅ 成功获取所有赛季数据，共{len(all_seasons)}个赛季")
            logger.info(f"📅 赛季范围: {all_seasons['season'].min()} - {all_seasons['season'].max()}")
            
            # 显示最近的几个赛季
            recent_seasons = all_seasons.tail(10)
            logger.info(f"📋 最近10个赛季: {list(recent_seasons['season'].values)}")
        else:
            logger.error("❌ 获取所有赛季数据失败")
            return False
        
        # 测试2: 获取2023-2025赛季数据
        logger.info("📊 测试2: 获取2023-2025赛季数据...")
        target_seasons = provider.get_seasons(start_year=2023, end_year=2025)
        
        if not target_seasons.empty:
            logger.info(f"✅ 成功获取目标赛季数据，共{len(target_seasons)}个赛季")
            logger.info(f"📋 目标赛季: {list(target_seasons['season'].values)}")
        else:
            logger.error("❌ 获取目标赛季数据失败")
            return False
        
        # 测试3: 获取单个赛季数据
        logger.info("📊 测试3: 获取2025赛季数据...")
        season_2025 = provider.get_seasons(start_year=2025, end_year=2025)
        
        if not season_2025.empty:
            logger.info(f"✅ 成功获取2025赛季数据，共{len(season_2025)}个赛季")
            logger.info(f"📋 2025赛季信息: {season_2025.to_dict('records')}")
        else:
            logger.error("❌ 获取2025赛季数据失败")
            return False
        
        # 测试4: 验证数据完整性
        logger.info("📊 测试4: 验证数据完整性...")
        
        # 检查是否包含2023-2025赛季
        seasons_2023_2025 = all_seasons[all_seasons['season'].isin([2023, 2024, 2025])]
        if len(seasons_2023_2025) == 3:
            logger.info("✅ 验证通过：所有目标赛季都存在")
        else:
            logger.warning(f"⚠️ 验证警告：只找到{len(seasons_2023_2025)}个目标赛季")
        
        # 检查数据格式
        expected_columns = ['season', 'seasonUrl']
        if all(col in all_seasons.columns for col in expected_columns):
            logger.info("✅ 验证通过：数据格式正确")
        else:
            logger.error("❌ 验证失败：数据格式不正确")
            return False
        
        logger.info("🎉 所有测试通过！")
        return True
        
    except Exception as e:
        logger.error(f"❌ 测试过程中发生错误: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_direct_ergast_pagination():
    """直接测试 Ergast 分页机制"""
    logger.info("🧪 直接测试 Ergast 分页机制...")
    
    try:
        import fastf1
        from fastf1.ergast import Ergast
        
        # 启用缓存
        fastf1.Cache.enable_cache('./cache')
        ergast = Ergast()
        
        # 测试默认获取
        logger.info("📊 测试默认获取（应该只返回前30项）...")
        default_seasons = ergast.get_seasons()
        logger.info(f"📏 默认获取的赛季数量: {len(default_seasons)}")
        logger.info(f"📋 是否完整: {getattr(default_seasons, 'is_complete', 'Unknown')}")
        logger.info(f"📊 总结果数: {getattr(default_seasons, 'total_results', 'Unknown')}")
        
        # 测试分页获取
        if hasattr(default_seasons, 'is_complete') and not default_seasons.is_complete:
            logger.info("📊 测试分页获取...")
            
            all_seasons = []
            offset = 0
            limit = 30
            
            while True:
                seasons_page = ergast.get_seasons(limit=limit, offset=offset)
                logger.info(f"📄 获取第{offset//limit + 1}页，包含{len(seasons_page)}个赛季")
                
                if seasons_page.empty:
                    break
                
                all_seasons.append(seasons_page)
                
                if getattr(seasons_page, 'is_complete', True):
                    break
                
                offset += limit
            
            # 合并所有页面
            if all_seasons:
                complete_seasons = pd.concat(all_seasons, ignore_index=True)
                logger.info(f"✅ 分页获取完成，总共{len(complete_seasons)}个赛季")
                logger.info(f"📅 赛季范围: {complete_seasons['season'].min()} - {complete_seasons['season'].max()}")
                
                # 检查是否包含2023-2025
                target_seasons = complete_seasons[complete_seasons['season'].isin([2023, 2024, 2025])]
                logger.info(f"🎯 目标赛季(2023-2025): {list(target_seasons['season'].values)}")
            else:
                logger.error("❌ 分页获取失败")
                return False
        else:
            logger.info("📊 默认获取已包含所有数据，无需分页")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ 直接测试过程中发生错误: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """主函数"""
    logger.info("🚀 开始测试赛季数据分页机制...")
    
    # 测试1: 直接测试 Ergast 分页
    if test_direct_ergast_pagination():
        logger.info("✅ 直接 Ergast 分页测试通过")
    else:
        logger.error("❌ 直接 Ergast 分页测试失败")
        return False
    
    # 测试2: 测试数据提供者的分页
    if test_seasons_pagination():
        logger.info("✅ 数据提供者分页测试通过")
    else:
        logger.error("❌ 数据提供者分页测试失败")
        return False
    
    logger.info("🎉 所有测试完成！")
    return True


if __name__ == "__main__":
    success = main()
    if not success:
        sys.exit(1) 