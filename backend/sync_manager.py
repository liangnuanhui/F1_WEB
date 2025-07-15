#!/usr/bin/env python3
"""
F1比赛数据同步管理工具
适用于生产环境的简化版本
"""

import requests
import json
import sys
from datetime import datetime
from typing import Optional, List

class F1SyncManager:
    def __init__(self, api_url: str):
        """
        初始化同步管理器
        
        Args:
            api_url: API服务器地址，如: https://your-app.onrender.com
        """
        self.api_url = api_url.rstrip('/')
        self.base_url = f"{self.api_url}/api/v1/post-race-sync"
    
    def schedule_race_sync(self, season_year: int, race_round: int, retry_hours: List[int] = None):
        """
        为指定比赛安排同步计划
        
        Args:
            season_year: 赛季年份 (如: 2025)
            race_round: 比赛轮次 (如: 1-24)
            retry_hours: 重试时间点(小时) (默认: [6, 12, 24])
        """
        url = f"{self.base_url}/{season_year}/{race_round}/schedule"
        
        data = {"retry_intervals": retry_hours or [6, 12, 24]}
        
        try:
            response = requests.post(url, json=data, timeout=30)
            response.raise_for_status()
            
            result = response.json()
            print(f"✅ 成功安排 {season_year} 赛季第 {race_round} 轮比赛的同步计划")
            print(f"   比赛名称: {result.get('race_name', 'Unknown')}")
            print(f"   重试间隔: {data['retry_intervals']} 小时")
            return True
            
        except requests.exceptions.RequestException as e:
            print(f"❌ 安排同步计划失败: {e}")
            return False
    
    def check_sync_status(self, season_year: int, race_round: int):
        """
        检查同步状态
        """
        url = f"{self.base_url}/{season_year}/{race_round}/schedule"
        
        try:
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            
            result = response.json()
            schedule = result.get('schedule', {})
            
            print(f"\n📊 {season_year} 赛季第 {race_round} 轮同步状态:")
            print(f"   比赛名称: {schedule.get('race_name', 'Unknown')}")
            print(f"   完成状态: {'✅ 已完成' if schedule.get('is_completed') else '⏳ 进行中'}")
            print(f"   成功率: {schedule.get('success_rate', 0):.1%}")
            
            # 显示尝试详情
            attempts = schedule.get('attempts', [])
            for attempt in attempts:
                status_icon = {
                    'pending': '⏳',
                    'running': '🏃',
                    'success': '✅',
                    'partial': '⚠️',
                    'failed': '❌'
                }.get(attempt.get('status'), '❓')
                
                print(f"   尝试 {attempt.get('attempt_number')}: {status_icon} {attempt.get('status')}")
            
            return True
            
        except requests.exceptions.RequestException as e:
            print(f"❌ 检查状态失败: {e}")
            return False
    
    def manual_sync_now(self, season_year: int, race_round: int, attempt_number: int = 1):
        """
        手动立即执行同步
        """
        url = f"{self.base_url}/{season_year}/{race_round}/execute/{attempt_number}"
        
        try:
            response = requests.post(url, timeout=60)
            response.raise_for_status()
            
            print(f"✅ 已触发 {season_year} 赛季第 {race_round} 轮的立即同步")
            print("   请稍等几分钟后检查同步状态")
            return True
            
        except requests.exceptions.RequestException as e:
            print(f"❌ 手动同步失败: {e}")
            return False
    
    def batch_schedule_upcoming(self, season_year: int, days_ahead: int = 7):
        """
        批量安排即将到来的比赛
        """
        url = f"{self.base_url}/batch-schedule"
        params = {"season_year": season_year, "days_ahead": days_ahead}
        
        try:
            response = requests.post(url, params=params, timeout=60)
            response.raise_for_status()
            
            result = response.json()
            scheduled_count = result.get('scheduled_count', 0)
            
            print(f"✅ 成功批量安排了 {scheduled_count} 场比赛的同步计划")
            print(f"   时间范围: 未来 {days_ahead} 天")
            return True
            
        except requests.exceptions.RequestException as e:
            print(f"❌ 批量安排失败: {e}")
            return False
    
    def get_overall_stats(self, season_year: int):
        """
        获取整体统计信息
        """
        url = f"{self.base_url}/stats"
        params = {"season_year": season_year}
        
        try:
            response = requests.get(url, params=params, timeout=30)
            response.raise_for_status()
            
            stats = response.json()
            
            print(f"\n📈 {season_year} 赛季同步统计:")
            print(f"   总计划数: {stats.get('total_schedules', 0)}")
            print(f"   已完成: {stats.get('completed_schedules', 0)}")
            print(f"   进行中: {stats.get('pending_schedules', 0)}")
            print(f"   失败: {stats.get('failed_schedules', 0)}")
            print(f"   整体成功率: {stats.get('overall_success_rate', 0):.1%}")
            
            return True
            
        except requests.exceptions.RequestException as e:
            print(f"❌ 获取统计失败: {e}")
            return False


def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("""
F1比赛数据同步管理工具

使用方法:
  python sync_manager.py <API_URL> <命令> [参数...]

命令:
  schedule <年份> <轮次>           - 安排单场比赛同步
  status <年份> <轮次>             - 检查同步状态  
  sync-now <年份> <轮次>           - 立即手动同步
  batch <年份> [天数]              - 批量安排(默认7天)
  stats <年份>                    - 查看统计信息

示例:
  # 安排2025赛季第1轮(巴林大奖赛)的同步
  python sync_manager.py https://your-app.onrender.com schedule 2025 1
  
  # 检查第5轮的同步状态
  python sync_manager.py https://your-app.onrender.com status 2025 5
  
  # 手动立即同步第10轮
  python sync_manager.py https://your-app.onrender.com sync-now 2025 10
  
  # 批量安排未来一周的比赛
  python sync_manager.py https://your-app.onrender.com batch 2025
""")
        sys.exit(1)
    
    api_url = sys.argv[1]
    command = sys.argv[2] if len(sys.argv) > 2 else ""
    
    manager = F1SyncManager(api_url)
    
    try:
        if command == "schedule" and len(sys.argv) >= 5:
            year = int(sys.argv[3])
            round_num = int(sys.argv[4])
            manager.schedule_race_sync(year, round_num)
            
        elif command == "status" and len(sys.argv) >= 5:
            year = int(sys.argv[3])
            round_num = int(sys.argv[4])
            manager.check_sync_status(year, round_num)
            
        elif command == "sync-now" and len(sys.argv) >= 5:
            year = int(sys.argv[3])
            round_num = int(sys.argv[4])
            manager.manual_sync_now(year, round_num)
            
        elif command == "batch" and len(sys.argv) >= 4:
            year = int(sys.argv[3])
            days = int(sys.argv[4]) if len(sys.argv) > 4 else 7
            manager.batch_schedule_upcoming(year, days)
            
        elif command == "stats" and len(sys.argv) >= 4:
            year = int(sys.argv[3])
            manager.get_overall_stats(year)
            
        else:
            print("❌ 无效的命令或参数不足")
            sys.exit(1)
            
    except ValueError:
        print("❌ 年份和轮次必须是数字")
        sys.exit(1)
    except Exception as e:
        print(f"❌ 执行失败: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()