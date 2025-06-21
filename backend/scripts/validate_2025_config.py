#!/usr/bin/env python3
"""
2025赛季配置验证脚本
检查所有与2025赛季相关的配置是否正确
"""

import sys
import logging
from pathlib import Path

# 添加项目根目录到 Python 路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from sqlalchemy import text
from app.core.database import get_db
from app.services.data_sync_service import DataSyncService
from app.services.data_provider import DataProviderFactory

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def validate_database_config():
    """验证数据库配置"""
    logger.info("🔍 验证数据库配置...")
    
    try:
        db = next(get_db())
        
        # 检查Season表结构
        result = db.execute(text("""
            SELECT column_name, data_type, is_nullable, column_default
            FROM information_schema.columns 
            WHERE table_name = 'seasons' AND column_name = 'is_current'
        """))
        
        column_info = result.fetchone()
        if column_info:
            if column_info[1] == 'boolean':
                logger.info("✅ Season.is_current字段类型正确 (boolean)")
            else:
                logger.error(f"❌ Season.is_current字段类型错误: {column_info[1]} (应该是boolean)")
                return False
        else:
            logger.error("❌ 未找到Season.is_current字段")
            return False
        
        # 检查2025赛季是否存在
        season_2025 = db.execute(text("SELECT id, year, name, is_current FROM seasons WHERE year = 2025")).fetchone()
        if season_2025:
            logger.info(f"✅ 2025赛季存在: {season_2025[2]} (当前赛季: {season_2025[3]})")
        else:
            logger.warning("⚠️ 2025赛季不存在")
        
        # 检查当前赛季设置
        current_season = db.execute(text("SELECT year, name FROM seasons WHERE is_current = true")).fetchone()
        if current_season:
            logger.info(f"✅ 当前赛季: {current_season[0]} - {current_season[1]}")
        else:
            logger.warning("⚠️ 未设置当前赛季")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ 数据库配置验证失败: {e}")
        return False
    finally:
        db.close()


def validate_service_config():
    """验证服务配置"""
    logger.info("🔍 验证服务配置...")
    
    try:
        # 检查数据同步服务
        sync_service = DataSyncService()
        if sync_service.current_season == 2025:
            logger.info("✅ DataSyncService.current_season配置正确 (2025)")
        else:
            logger.error(f"❌ DataSyncService.current_season配置错误: {sync_service.current_season} (应该是2025)")
            return False
        
        # 检查频率限制配置
        expected_delays = {
            'basic': 0.5,
            'results': 1.0,
            'standings': 1.5,
            'session': 2.0
        }
        
        for delay_type, expected_delay in expected_delays.items():
            actual_delay = sync_service.rate_limit_delays.get(delay_type)
            if actual_delay == expected_delay:
                logger.info(f"✅ {delay_type}延迟配置正确: {actual_delay}s")
            else:
                logger.error(f"❌ {delay_type}延迟配置错误: {actual_delay}s (应该是{expected_delay}s)")
                return False
        
        # 检查数据提供者
        provider = DataProviderFactory.get_provider('fastf1')
        logger.info("✅ FastF1数据提供者创建成功")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ 服务配置验证失败: {e}")
        return False


def validate_script_config():
    """验证脚本配置"""
    logger.info("🔍 验证脚本配置...")
    
    try:
        # 检查脚本文件中的2025配置
        script_files = [
            'scripts/init_data.py',
            'scripts/sync_data_safe.py',
            'scripts/sync_data.py',
            'scripts/test_data_providers.py'
        ]
        
        for script_file in script_files:
            script_path = Path(project_root) / script_file
            if script_path.exists():
                content = script_path.read_text()
                if '2025' in content:
                    logger.info(f"✅ {script_file} 包含2025配置")
                else:
                    logger.warning(f"⚠️ {script_file} 可能缺少2025配置")
            else:
                logger.warning(f"⚠️ {script_file} 文件不存在")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ 脚本配置验证失败: {e}")
        return False


def validate_api_endpoints():
    """验证API端点配置"""
    logger.info("🔍 验证API端点配置...")
    
    try:
        from app.api.v1.endpoints.seasons import router
        
        # 检查路由是否包含当前赛季端点
        routes = [route.path for route in router.routes]
        if "/current" in routes:
            logger.info("✅ 当前赛季API端点存在")
        else:
            logger.warning("⚠️ 当前赛季API端点不存在")
        
        if "/year/{year}" in routes:
            logger.info("✅ 按年份查询API端点存在")
        else:
            logger.warning("⚠️ 按年份查询API端点不存在")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ API端点配置验证失败: {e}")
        return False


def test_data_provider():
    """测试数据提供者"""
    logger.info("🔍 测试数据提供者...")
    
    try:
        provider = DataProviderFactory.get_provider('fastf1')
        
        # 测试获取2025赛季数据
        seasons_data = provider.get_seasons(start_year=2025, end_year=2025)
        if not seasons_data.empty:
            logger.info(f"✅ 成功获取2025赛季数据: {len(seasons_data)} 条记录")
        else:
            logger.warning("⚠️ 2025赛季数据为空，可能尚未可用")
        
        # 测试获取最新赛季数据
        latest_seasons = provider.get_seasons()
        if not latest_seasons.empty:
            latest_year = latest_seasons['season'].max()
            logger.info(f"✅ 最新可用赛季: {latest_year}")
        else:
            logger.error("❌ 无法获取赛季数据")
            return False
        
        return True
        
    except Exception as e:
        logger.error(f"❌ 数据提供者测试失败: {e}")
        return False


def main():
    """主函数"""
    logger.info("🚀 开始2025赛季配置验证...")
    
    validation_results = []
    
    # 执行各项验证
    validation_results.append(("数据库配置", validate_database_config()))
    validation_results.append(("服务配置", validate_service_config()))
    validation_results.append(("脚本配置", validate_script_config()))
    validation_results.append(("API端点配置", validate_api_endpoints()))
    validation_results.append(("数据提供者", test_data_provider()))
    
    # 显示验证结果
    logger.info("\n📊 === 验证结果汇总 ===")
    all_passed = True
    
    for name, result in validation_results:
        status = "✅ 通过" if result else "❌ 失败"
        logger.info(f"{name}: {status}")
        if not result:
            all_passed = False
    
    if all_passed:
        logger.info("\n🎉 所有配置验证通过！2025赛季配置正确。")
    else:
        logger.error("\n❌ 部分配置验证失败，请检查上述问题。")
    
    return all_passed


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 