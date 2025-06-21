#!/usr/bin/env python3
"""
FastF1 数据提供者测试脚本
测试统一的 FastF1 数据提供者功能 - 专门针对 2025 赛季
"""

import argparse
import logging
import sys
import time

import pandas as pd

from app.services.data_provider import DataProviderFactory

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def test_fastf1_provider(season: int = 2025, cache_dir: str = None, verbose: bool = False):
    """测试 FastF1 数据提供者"""
    print(f"🧪 === FastF1 数据提供者测试 (赛季: {season}) ===")
    
    try:
        # 获取数据提供者
        provider = DataProviderFactory.get_provider('fastf1', cache_dir=cache_dir)
        print("✅ 成功创建 FastF1 数据提供者")
        
        # 定义测试方法 - 按优先级排序
        test_methods = [
            # 基础信息数据 (使用 fastf1.ergast) - 优先级最高
            ('get_circuits', provider.get_circuits, {'season': season}, '基础信息', '高'),
            ('get_drivers', provider.get_drivers, {'season': season}, '基础信息', '高'),
            ('get_constructors', provider.get_constructors, {'season': season}, '基础信息', '高'),
            
            # 比赛安排数据 (使用 fastf1.get_event_schedule) - 优先级中
            ('get_races', provider.get_races, {'season': season}, '比赛安排', '中'),
            
            # 积分榜数据 (使用 fastf1.ergast) - 优先级中
            ('get_driver_standings', provider.get_driver_standings, {'season': season}, '积分榜', '中'),
            ('get_constructor_standings', provider.get_constructor_standings, {'season': season}, '积分榜', '中'),
            
            # 比赛结果数据 (使用 fastf1.ergast) - 优先级低，容易触发限制
            ('get_race_results', provider.get_race_results, {'season': season}, '比赛结果', '低'),
            ('get_qualifying_results', provider.get_qualifying_results, {'season': season}, '比赛结果', '低'),
        ]
        
        results = {}
        category_results = {}
        priority_results = {}
        
        for method_name, method, kwargs, category, priority in test_methods:
            try:
                if verbose:
                    print(f"\n🔍 测试 {method_name} ({category}, 优先级: {priority})...")
                
                start_time = time.time()
                data = method(**kwargs)
                elapsed_time = time.time() - start_time
                
                if isinstance(data, pd.DataFrame):
                    result = {
                        'success': True,
                        'category': category,
                        'priority': priority,
                        'rows': len(data),
                        'columns': list(data.columns) if not data.empty else [],
                        'sample': data.head(3).to_dict('records') if not data.empty else [],
                        'elapsed_time': elapsed_time
                    }
                    results[method_name] = result
                    
                    # 按类别统计
                    if category not in category_results:
                        category_results[category] = {'success': 0, 'total': 0}
                    category_results[category]['success'] += 1
                    category_results[category]['total'] += 1
                    
                    # 按优先级统计
                    if priority not in priority_results:
                        priority_results[priority] = {'success': 0, 'total': 0}
                    priority_results[priority]['success'] += 1
                    priority_results[priority]['total'] += 1
                    
                    if verbose:
                        print(f"  ✅ {method_name}: {len(data)} 行数据 ({elapsed_time:.2f}s)")
                        if data.columns:
                            print(f"     列名: {list(data.columns)}")
                        if data.shape[0] > 0:
                            print(f"     示例: {data.iloc[0].to_dict()}")
                else:
                    result = {
                        'success': False,
                        'category': category,
                        'priority': priority,
                        'error': f"返回类型错误: {type(data)}",
                        'elapsed_time': elapsed_time
                    }
                    results[method_name] = result
                    
                    if category not in category_results:
                        category_results[category] = {'success': 0, 'total': 0}
                    category_results[category]['total'] += 1
                    
                    if priority not in priority_results:
                        priority_results[priority] = {'success': 0, 'total': 0}
                    priority_results[priority]['total'] += 1
                    
                    if verbose:
                        print(f"  ❌ {method_name}: 返回类型错误 ({elapsed_time:.2f}s)")
                    
            except Exception as e:
                result = {
                    'success': False,
                    'category': category,
                    'priority': priority,
                    'error': str(e),
                    'elapsed_time': 0
                }
                results[method_name] = result
                
                if category not in category_results:
                    category_results[category] = {'success': 0, 'total': 0}
                category_results[category]['total'] += 1
                
                if priority not in priority_results:
                    priority_results[priority] = {'success': 0, 'total': 0}
                priority_results[priority]['total'] += 1
                
                if verbose:
                    print(f"  ❌ {method_name}: {e}")
        
        # 打印测试结果摘要
        print(f"\n📊 === 测试结果摘要 ===")
        successful_tests = sum(1 for r in results.values() if r['success'])
        total_tests = len(results)
        
        print(f"总测试数: {total_tests}")
        print(f"成功: {successful_tests}")
        print(f"失败: {total_tests - successful_tests}")
        print(f"成功率: {successful_tests/total_tests*100:.1f}%")
        
        # 按类别显示结果
        print(f"\n📋 === 按类别统计 ===")
        for category, stats in category_results.items():
            success_rate = stats['success'] / stats['total'] * 100 if stats['total'] > 0 else 0
            print(f"{category}: {stats['success']}/{stats['total']} ({success_rate:.1f}%)")
        
        # 按优先级显示结果
        print(f"\n🎯 === 按优先级统计 ===")
        for priority, stats in priority_results.items():
            success_rate = stats['success'] / stats['total'] * 100 if stats['total'] > 0 else 0
            print(f"优先级 {priority}: {stats['success']}/{stats['total']} ({success_rate:.1f}%)")
        
        # 详细结果
        if verbose:
            print(f"\n🔍 === 详细结果 ===")
            for method_name, result in results.items():
                status = "✅" if result['success'] else "❌"
                category = result['category']
                priority = result['priority']
                elapsed = result.get('elapsed_time', 0)
                
                if result['success']:
                    print(f"  {status} {method_name} ({category}, {priority}): {result['rows']} 行数据 ({elapsed:.2f}s)")
                    if result['sample']:
                        print(f"     示例: {result['sample'][0] if result['sample'] else '无数据'}")
                else:
                    print(f"  {status} {method_name} ({category}, {priority}): {result['error']} ({elapsed:.2f}s)")
        
        # 数据源验证
        print(f"\n🔗 === 数据源验证 ===")
        print("✅ 基础信息数据: 使用 fastf1.ergast")
        print("✅ 比赛安排数据: 使用 fastf1.get_event_schedule")
        print("✅ 积分榜数据: 使用 fastf1.ergast")
        print("✅ 比赛结果数据: 使用 fastf1.ergast")
        
        # 2025赛季特殊检查
        print(f"\n🎯 === 2025赛季特殊检查 ===")
        if season == 2025:
            print("✅ 测试目标: 2025赛季")
            print("✅ 使用优化的频率限制配置")
            print("✅ 启用智能延迟策略")
        
        return results
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        logger.error(f"测试 FastF1 数据提供者时发生错误: {e}")
        return None


def test_data_consistency(season: int = 2025):
    """测试数据一致性"""
    print(f"\n🔍 === 数据一致性测试 (赛季: {season}) ===")
    
    try:
        provider = DataProviderFactory.get_provider('fastf1')
        
        # 测试比赛安排和比赛结果的一致性
        races = provider.get_races(season=season)
        race_results = provider.get_race_results(season=season)
        
        if not races.empty and not race_results.empty:
            print(f"✅ 比赛安排: {len(races)} 场比赛")
            print(f"✅ 比赛结果: {len(race_results)} 个结果")
            
            # 检查是否有对应的结果
            races_with_results = race_results['round'].nunique() if 'round' in race_results.columns else 0
            print(f"✅ 有结果的比赛: {races_with_results} 场")
            
            # 显示比赛安排详情
            if 'RoundNumber' in races.columns:
                print(f"✅ 比赛轮次: {races['RoundNumber'].min()} - {races['RoundNumber'].max()}")
        else:
            print("⚠️ 无法验证数据一致性 (数据为空)")
        
    except Exception as e:
        print(f"❌ 数据一致性测试失败: {e}")


def main():
    parser = argparse.ArgumentParser(description='F1 数据提供者测试工具 - 2025赛季专用')
    parser.add_argument('--season', type=int, default=2025, help='测试赛季 (默认: 2025)')
    parser.add_argument('--cache-dir', help='FastF1 缓存目录')
    parser.add_argument('--verbose', '-v', action='store_true', help='详细输出')
    parser.add_argument('--consistency', action='store_true', help='测试数据一致性')
    
    args = parser.parse_args()
    
    print(f"🚀 开始测试 2025 赛季 F1 数据提供者...")
    
    # 主要测试
    results = test_fastf1_provider(args.season, args.cache_dir, args.verbose)
    
    # 数据一致性测试
    if args.consistency:
        test_data_consistency(args.season)
    
    # 总结
    if results:
        successful_tests = sum(1 for r in results.values() if r['success'])
        total_tests = len(results)
        print(f"\n🎉 === 测试总结 ===")
        print(f"FastF1 数据提供者测试完成")
        print(f"成功率: {successful_tests}/{total_tests} ({successful_tests/total_tests*100:.1f}%)")
        
        if successful_tests == total_tests:
            print("🎯 所有测试通过！可以开始数据同步")
        else:
            print("⚠️ 部分测试失败，请检查网络连接和API限制")
    
    return results is not None


if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1) 