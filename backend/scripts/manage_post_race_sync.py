#!/usr/bin/env python3
"""
F1 比赛后数据同步系统管理脚本
提供便捷的命令行接口来管理同步计划
"""

import asyncio
import sys
import argparse
from datetime import datetime, timezone
from typing import Optional
import httpx
import json

class PostRaceSyncManager:
    """比赛后同步系统管理器"""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url.rstrip('/')
        self.api_base = f"{self.base_url}/api/v1/post-race-sync"
    
    async def schedule_race(self, season_year: int, race_round: int, retry_intervals: Optional[list] = None):
        """为指定比赛安排同步计划"""
        url = f"{self.api_base}/{season_year}/{race_round}/schedule"
        
        data = {"retry_intervals": retry_intervals}
        
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(url, json=data)
                result = response.json()
                
                if response.status_code == 200:
                    print(f"✅ 成功安排 {season_year} 赛季第 {race_round} 轮的同步计划")
                    print(f"   比赛名称: {result.get('race_name', 'N/A')}")
                    print(f"   重试间隔: {result.get('retry_intervals', [6, 12, 24])} 小时")
                else:
                    print(f"❌ 安排失败: {result.get('detail', 'Unknown error')}")
                    
            except Exception as e:
                print(f"❌ 请求失败: {e}")
    
    async def get_schedule(self, season_year: int, race_round: int):
        """获取指定比赛的同步计划"""
        url = f"{self.api_base}/{season_year}/{race_round}/schedule"
        
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(url)
                
                if response.status_code == 200:
                    result = response.json()
                    schedule = result["schedule"]
                    
                    print(f"📋 {season_year} 赛季第 {race_round} 轮同步计划")
                    print(f"   比赛名称: {schedule['race_name']}")
                    print(f"   比赛结束时间: {schedule['race_end_time']}")
                    print(f"   计划创建时间: {schedule['created_at']}")
                    print(f"   是否完成: {schedule['is_completed']}")
                    print(f"   成功率: {schedule['success_rate']:.1%}")
                    
                    if schedule.get('next_pending_attempt'):
                        next_attempt = schedule['next_pending_attempt']
                        print(f"   下次尝试: 第 {next_attempt['attempt_number']} 次，时间: {next_attempt['scheduled_time']}")
                    
                    print("\n   尝试历史:")
                    for attempt in schedule['attempts']:
                        status_icon = {
                            'pending': '⏳',
                            'running': '🔄',
                            'success': '✅',
                            'partial_success': '⚠️',
                            'failed': '❌',
                            'cancelled': '🚫'
                        }.get(attempt['status'], '❓')
                        
                        print(f"     {status_icon} 第 {attempt['attempt_number']} 次尝试")
                        print(f"       计划时间: {attempt['scheduled_time']}")
                        if attempt['executed_time']:
                            print(f"       执行时间: {attempt['executed_time']}")
                        print(f"       状态: {attempt['status']}")
                        if attempt['results']:
                            # 处理两种结果格式
                            if isinstance(list(attempt['results'].values())[0], bool):
                                # 新格式：{'race_results': True, 'qualifying_results': True, ...}
                                successful_tasks = sum(1 for result in attempt['results'].values() if result)
                            else:
                                # 旧格式：{'race_results': {'success': True}, ...}
                                successful_tasks = sum(1 for result in attempt['results'].values() if result.get('success'))
                            total_tasks = len(attempt['results'])
                            print(f"       结果: {successful_tasks}/{total_tasks} 任务成功")
                
                elif response.status_code == 404:
                    print(f"⚠️ 未找到 {season_year} 赛季第 {race_round} 轮的同步计划")
                else:
                    result = response.json()
                    print(f"❌ 获取失败: {result.get('detail', 'Unknown error')}")
                    
            except Exception as e:
                print(f"❌ 请求失败: {e}")
    
    async def cancel_schedule(self, season_year: int, race_round: int):
        """取消指定比赛的同步计划"""
        url = f"{self.api_base}/{season_year}/{race_round}/schedule"
        
        async with httpx.AsyncClient() as client:
            try:
                response = await client.delete(url)
                result = response.json()
                
                if response.status_code == 200:
                    print(f"✅ 已取消 {season_year} 赛季第 {race_round} 轮的同步计划")
                else:
                    print(f"❌ 取消失败: {result.get('detail', 'Unknown error')}")
                    
            except Exception as e:
                print(f"❌ 请求失败: {e}")
    
    async def execute_immediately(self, season_year: int, race_round: int, attempt_number: int):
        """立即执行指定的同步尝试"""
        url = f"{self.api_base}/{season_year}/{race_round}/execute/{attempt_number}"
        
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(url)
                result = response.json()
                
                if response.status_code == 200:
                    print(f"✅ 已触发 {season_year} 赛季第 {race_round} 轮第 {attempt_number} 次同步")
                    print(f"   任务ID: {result.get('task_id', 'N/A')}")
                else:
                    print(f"❌ 执行失败: {result.get('detail', 'Unknown error')}")
                    
            except Exception as e:
                print(f"❌ 请求失败: {e}")
    
    async def list_all_schedules(self, season_year: Optional[int] = None, status_filter: Optional[str] = None):
        """列出所有同步计划"""
        url = f"{self.api_base}/schedules"
        
        params = {}
        if season_year:
            params["season_year"] = season_year
        if status_filter:
            params["status_filter"] = status_filter
        
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(url, params=params)
                
                if response.status_code == 200:
                    result = response.json()
                    schedules = result["schedules"]
                    
                    print(f"📊 同步计划列表（共 {len(schedules)} 个）")
                    
                    for schedule in schedules:
                        status_icon = "✅" if schedule["is_completed"] else "⏳"
                        print(f"\n{status_icon} {schedule['race_name']}")
                        print(f"   赛季: {schedule['season_year']}, 轮次: {schedule['race_round']}")
                        print(f"   成功率: {schedule['success_rate']:.1%}")
                        print(f"   尝试次数: {schedule['attempts_count']}")
                        
                        if schedule.get('next_attempt_time'):
                            print(f"   下次尝试: {schedule['next_attempt_time']}")
                
                else:
                    result = response.json()
                    print(f"❌ 获取失败: {result.get('detail', 'Unknown error')}")
                    
            except Exception as e:
                print(f"❌ 请求失败: {e}")
    
    async def get_stats(self, season_year: Optional[int] = None):
        """获取统计信息"""
        url = f"{self.api_base}/stats"
        
        params = {}
        if season_year:
            params["season_year"] = season_year
        
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(url, params=params)
                
                if response.status_code == 200:
                    result = response.json()
                    stats = result["stats"]
                    
                    print("📈 同步系统统计信息")
                    print(f"   总计划数: {stats['total_schedules']}")
                    print(f"   已完成: {stats['completed_schedules']}")
                    print(f"   进行中: {stats['pending_schedules']}")
                    print(f"   总体成功率: {stats['overall_success_rate']:.1%}")
                    print(f"   总尝试次数: {stats['total_attempts']}")
                    print(f"   成功尝试: {stats['successful_attempts']}")
                    
                    if season_year:
                        print(f"   （以上数据仅限 {season_year} 赛季）")
                
                else:
                    result = response.json()
                    print(f"❌ 获取失败: {result.get('detail', 'Unknown error')}")
                    
            except Exception as e:
                print(f"❌ 请求失败: {e}")
    
    async def monitor_system(self):
        """监控系统状态"""
        url = f"{self.api_base}/monitor"
        
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(url)
                result = response.json()
                
                if response.status_code == 200:
                    print("✅ 已触发系统监控")
                    print(f"   任务ID: {result.get('task_id', 'N/A')}")
                else:
                    print(f"❌ 监控触发失败: {result.get('detail', 'Unknown error')}")
                    
            except Exception as e:
                print(f"❌ 请求失败: {e}")
    
    async def cleanup_expired(self):
        """清理过期计划"""
        url = f"{self.api_base}/cleanup"
        
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(url)
                result = response.json()
                
                if response.status_code == 200:
                    print("✅ 已触发过期计划清理")
                    print(f"   任务ID: {result.get('task_id', 'N/A')}")
                else:
                    print(f"❌ 清理触发失败: {result.get('detail', 'Unknown error')}")
                    
            except Exception as e:
                print(f"❌ 请求失败: {e}")


async def main():
    parser = argparse.ArgumentParser(description="F1 比赛后数据同步系统管理工具")
    parser.add_argument("--base-url", default="http://localhost:8000", help="API基础URL")
    
    subparsers = parser.add_subparsers(dest="command", help="可用命令")
    
    # 安排同步计划
    schedule_parser = subparsers.add_parser("schedule", help="安排比赛后同步计划")
    schedule_parser.add_argument("season_year", type=int, help="赛季年份")
    schedule_parser.add_argument("race_round", type=int, help="比赛轮次")
    schedule_parser.add_argument("--intervals", nargs="+", type=int, help="重试间隔（小时）")
    
    # 查看同步计划
    get_parser = subparsers.add_parser("get", help="查看同步计划")
    get_parser.add_argument("season_year", type=int, help="赛季年份")
    get_parser.add_argument("race_round", type=int, help="比赛轮次")
    
    # 取消同步计划
    cancel_parser = subparsers.add_parser("cancel", help="取消同步计划")
    cancel_parser.add_argument("season_year", type=int, help="赛季年份")
    cancel_parser.add_argument("race_round", type=int, help="比赛轮次")
    
    # 立即执行
    execute_parser = subparsers.add_parser("execute", help="立即执行同步")
    execute_parser.add_argument("season_year", type=int, help="赛季年份")
    execute_parser.add_argument("race_round", type=int, help="比赛轮次")
    execute_parser.add_argument("attempt_number", type=int, help="尝试次数")
    
    # 列出所有计划
    list_parser = subparsers.add_parser("list", help="列出所有同步计划")
    list_parser.add_argument("--season", type=int, help="筛选赛季")
    list_parser.add_argument("--status", help="筛选状态")
    
    # 获取统计信息
    stats_parser = subparsers.add_parser("stats", help="获取统计信息")
    stats_parser.add_argument("--season", type=int, help="筛选赛季")
    
    # 监控系统
    subparsers.add_parser("monitor", help="监控系统状态")
    
    # 清理过期计划
    subparsers.add_parser("cleanup", help="清理过期计划")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    manager = PostRaceSyncManager(args.base_url)
    
    try:
        if args.command == "schedule":
            await manager.schedule_race(args.season_year, args.race_round, args.intervals)
        elif args.command == "get":
            await manager.get_schedule(args.season_year, args.race_round)
        elif args.command == "cancel":
            await manager.cancel_schedule(args.season_year, args.race_round)
        elif args.command == "execute":
            await manager.execute_immediately(args.season_year, args.race_round, args.attempt_number)
        elif args.command == "list":
            await manager.list_all_schedules(args.season, args.status)
        elif args.command == "stats":
            await manager.get_stats(args.season)
        elif args.command == "monitor":
            await manager.monitor_system()
        elif args.command == "cleanup":
            await manager.cleanup_expired()
    except KeyboardInterrupt:
        print("\n操作已取消")
    except Exception as e:
        print(f"❌ 操作失败: {e}")


if __name__ == "__main__":
    asyncio.run(main()) 