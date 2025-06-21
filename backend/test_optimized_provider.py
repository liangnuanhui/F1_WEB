#!/usr/bin/env python3
"""
测试优化后的数据提供者和同步服务
验证 FastF1 数据获取的完整性和正确性
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

def test_optimized_provider():
    """测试优化后的数据提供者"""
    try:
        from app.services.data_provider import DataProviderFactory
        
        logger.info("🔍 测试优化后的数据提供者...")
        
        # 创建数据提供者
        provider = DataProviderFactory.get_provider('fastf1', cache_dir='./cache')
        
        # 1. 测试获取2025赛季比赛数据
        logger.info("🏁 1. 测试获取2025赛季比赛数据...")
        races_2025 = provider.get_races(season=2025)
        
        if not races_2025.empty:
            logger.info(f"✅ 成功获取 {len(races_2025)} 条比赛数据")
            logger.info(f"📊 数据列: {list(races_2025.columns)}")
            
            # 显示比赛统计
            actual_races = races_2025[races_2025['RoundNumber'] > 0]
            logger.info(f"🏁 实际比赛: {len(actual_races)}场")
            logger.info(f"🧪 季前测试: {len(races_2025[races_2025['RoundNumber'] == 0])}场")
            
            # 显示比赛格式统计
            if 'EventFormat' in races_2025.columns:
                format_counts = races_2025['EventFormat'].value_counts()
                logger.info("📊 比赛格式统计:")
                for format_type, count in format_counts.items():
                    logger.info(f"   {format_type}: {count}场")
            
            # 显示前5场比赛
            logger.info("📋 前5场比赛:")
            for idx, race in actual_races.head().iterrows():
                logger.info(f"   第{race.get('RoundNumber', 'N/A')}轮: {race.get('EventName', 'N/A')} - {race.get('EventFormat', 'N/A')}")
        else:
            logger.error("❌ 获取2025赛季比赛数据失败")
            return False
        
        # 2. 测试获取特定轮次比赛
        logger.info("🏁 2. 测试获取特定轮次比赛...")
        race_1 = provider.get_races(season=2025, round_number=1)
        
        if not race_1.empty:
            logger.info(f"✅ 成功获取第1轮比赛数据: {race_1.iloc[0].get('EventName', 'N/A')}")
        else:
            logger.warning("⚠️ 获取第1轮比赛数据失败")
        
        # 3. 测试获取车手数据
        logger.info("👤 3. 测试获取车手数据...")
        drivers = provider.get_drivers(season=2025)
        
        if not drivers.empty:
            logger.info(f"✅ 成功获取车手数据: {len(drivers)}名车手")
        else:
            logger.warning("⚠️ 获取车手数据失败")
        
        # 4. 测试获取车队数据
        logger.info("🏎️ 4. 测试获取车队数据...")
        constructors = provider.get_constructors(season=2025)
        
        if not constructors.empty:
            logger.info(f"✅ 成功获取车队数据: {len(constructors)}支车队")
        else:
            logger.warning("⚠️ 获取车队数据失败")
        
        logger.info("✅ 数据提供者测试完成")
        return True
        
    except Exception as e:
        logger.error(f"❌ 数据提供者测试失败: {e}")
        return False

def test_data_sync_service():
    """测试数据同步服务"""
    try:
        from app.services.data_sync_service import DataSyncService
        from app.core.database import get_db
        
        logger.info("🔄 测试数据同步服务...")
        
        # 创建同步服务
        sync_service = DataSyncService(cache_dir='./cache')
        
        # 获取数据库会话
        db = next(get_db())
        
        try:
            # 1. 测试同步比赛数据
            logger.info("🏁 1. 测试同步比赛数据...")
            races_success = sync_service.sync_races(db, 2025)
            logger.info(f"比赛同步: {'✅ 成功' if races_success else '❌ 失败'}")
            
            # 2. 测试获取轮次列表
            logger.info("🔍 2. 测试获取轮次列表...")
            rounds = sync_service._get_rounds_to_sync(2025, None)
            logger.info(f"轮次列表: {rounds}")
            
            return races_success
            
        finally:
            db.close()
        
    except Exception as e:
        logger.error(f"❌ 数据同步服务测试失败: {e}")
        return False

def create_test_report():
    """创建测试报告"""
    try:
        report = []
        report.append("# 优化后数据提供者和同步服务测试报告")
        report.append(f"测试时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append("")
        
        # 测试数据提供者
        report.append("## 1. 数据提供者测试")
        provider_success = test_optimized_provider()
        report.append(f"- 数据提供者测试: {'✅ 通过' if provider_success else '❌ 失败'}")
        report.append("")
        
        # 测试数据同步服务
        report.append("## 2. 数据同步服务测试")
        sync_success = test_data_sync_service()
        report.append(f"- 数据同步服务测试: {'✅ 通过' if sync_success else '❌ 失败'}")
        report.append("")
        
        # 总结
        report.append("## 3. 测试总结")
        if provider_success and sync_success:
            report.append("✅ 所有测试通过，优化后的系统工作正常")
        else:
            report.append("⚠️ 部分测试失败，需要进一步检查")
        
        # 保存报告
        output_dir = './test_reports'
        os.makedirs(output_dir, exist_ok=True)
        
        report_file = os.path.join(output_dir, 'optimized_provider_test_report.md')
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(report))
        
        logger.info(f"📄 测试报告已保存: {report_file}")
        
    except Exception as e:
        logger.error(f"❌ 创建测试报告失败: {e}")

def main():
    """主函数"""
    logger.info("🚀 开始测试优化后的数据提供者和同步服务...")
    
    create_test_report()
    
    logger.info("✅ 测试完成！")

if __name__ == "__main__":
    main() 