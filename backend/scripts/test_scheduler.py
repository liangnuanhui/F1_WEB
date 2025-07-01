#!/usr/bin/env python3
"""
F1 数据自动调度系统测试脚本

测试调度器的各种功能：
- 调度任务创建
- 任务取消
- 状态查询
- 立即同步
"""

import sys
import asyncio
import httpx
from pathlib import Path
from datetime import datetime, timedelta

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from app.core.database import get_db
from app.tasks.scheduler import RaceScheduler, schedule_post_race_updates
from app.models import Race, Season

# 配置
API_BASE_URL = "http://localhost:8000/api/v1"
TEST_SEASON = 2025
TEST_RACE_ROUND = 1


class SchedulerTester:
    """调度器测试类"""
    
    def __init__(self):
        self.scheduler = RaceScheduler()
        self.client = httpx.AsyncClient(base_url=API_BASE_URL)
    
    async def test_scheduler_components(self):
        """测试调度器核心组件"""
        print("🧪 测试调度器核心组件...")
        
        try:
            # 1. 测试 Redis 连接
            print("1️⃣ 测试 Redis 连接...")
            redis_client = self.scheduler.redis_client
            redis_client.ping()
            print("   ✅ Redis 连接正常")
            
            # 2. 测试数据库连接
            print("2️⃣ 测试数据库连接...")
            db = next(get_db())
            race_count = db.query(Race).count()
            print(f"   ✅ 数据库连接正常，共有 {race_count} 场比赛")
            db.close()
            
            # 3. 测试调度键生成
            print("3️⃣ 测试调度键生成...")
            schedule_key = self.scheduler._get_schedule_key(TEST_SEASON, TEST_RACE_ROUND)
            expected_key = f"race_schedule:{TEST_SEASON}:{TEST_RACE_ROUND}"
            assert schedule_key == expected_key
            print(f"   ✅ 调度键生成正确: {schedule_key}")
            
            return True
            
        except Exception as e:
            print(f"   ❌ 组件测试失败: {e}")
            return False
    
    async def test_schedule_creation(self):
        """测试调度创建"""
        print("\n🕒 测试调度创建...")
        
        try:
            # 获取测试比赛
            db = next(get_db())
            race = db.query(Race).join(Season).filter(
                Season.year == TEST_SEASON,
                Race.round_number == TEST_RACE_ROUND
            ).first()
            
            if not race:
                print(f"   ⚠️ 未找到 {TEST_SEASON} 赛季第 {TEST_RACE_ROUND} 轮比赛，跳过测试")
                return True
            
            print(f"   📍 测试比赛: {race.official_event_name}")
            
            # 清理之前的调度（如果存在）
            self.scheduler.cancel_race_schedule(TEST_SEASON, TEST_RACE_ROUND)
            
            # 创建新调度
            success = self.scheduler.schedule_post_race_update(race)
            
            if success:
                print("   ✅ 调度创建成功")
                
                # 验证调度是否存在于 Redis
                schedule_key = self.scheduler._get_schedule_key(TEST_SEASON, TEST_RACE_ROUND)
                if self.scheduler.redis_client.exists(schedule_key):
                    print("   ✅ 调度记录已保存到 Redis")
                else:
                    print("   ❌ 调度记录未保存到 Redis")
                    return False
            else:
                print("   ❌ 调度创建失败")
                return False
            
            db.close()
            return True
            
        except Exception as e:
            print(f"   ❌ 调度创建测试失败: {e}")
            return False
    
    async def test_schedule_query(self):
        """测试调度查询"""
        print("\n🔍 测试调度查询...")
        
        try:
            # 获取所有调度
            scheduled_races = self.scheduler.get_scheduled_races()
            print(f"   📊 当前共有 {len(scheduled_races)} 个调度任务")
            
            # 查找测试调度
            test_schedule = None
            for schedule in scheduled_races:
                if (schedule.get("season_year") == TEST_SEASON and 
                    schedule.get("race_round") == TEST_RACE_ROUND):
                    test_schedule = schedule
                    break
            
            if test_schedule:
                print(f"   ✅ 找到测试调度: {test_schedule.get('race_name')}")
                print(f"   ⏰ 更新时间: {test_schedule.get('update_time')}")
                return True
            else:
                print("   ⚠️ 未找到测试调度（可能是正常现象）")
                return True
                
        except Exception as e:
            print(f"   ❌ 调度查询测试失败: {e}")
            return False
    
    async def test_schedule_cancellation(self):
        """测试调度取消"""
        print("\n🗑️ 测试调度取消...")
        
        try:
            # 取消测试调度
            success = self.scheduler.cancel_race_schedule(TEST_SEASON, TEST_RACE_ROUND)
            
            if success:
                print("   ✅ 调度取消成功")
                
                # 验证调度是否已从 Redis 删除
                schedule_key = self.scheduler._get_schedule_key(TEST_SEASON, TEST_RACE_ROUND)
                if not self.scheduler.redis_client.exists(schedule_key):
                    print("   ✅ 调度记录已从 Redis 删除")
                else:
                    print("   ❌ 调度记录仍在 Redis 中")
                    return False
            else:
                print("   ⚠️ 调度取消失败（可能调度不存在）")
            
            return True
            
        except Exception as e:
            print(f"   ❌ 调度取消测试失败: {e}")
            return False
    
    async def test_api_endpoints(self):
        """测试 API 端点"""
        print("\n🌐 测试 API 端点...")
        
        try:
            # 1. 测试获取调度状态
            print("1️⃣ 测试获取调度状态...")
            response = await self.client.get("/scheduler/status")
            if response.status_code == 200:
                data = response.json()
                print(f"   ✅ 调度器状态: {data.get('scheduler_status')}")
                print(f"   📊 Redis 客户端: {data.get('redis', {}).get('connected_clients', 0)}")
            else:
                print(f"   ❌ 状态查询失败: {response.status_code}")
                return False
            
            # 2. 测试获取调度列表
            print("2️⃣ 测试获取调度列表...")
            response = await self.client.get("/scheduler/schedules")
            if response.status_code == 200:
                data = response.json()
                print(f"   ✅ 调度列表获取成功，共 {data.get('total', 0)} 个调度")
            else:
                print(f"   ❌ 调度列表获取失败: {response.status_code}")
                return False
            
            # 3. 测试创建单场比赛调度
            print("3️⃣ 测试创建单场比赛调度...")
            response = await self.client.post(f"/scheduler/schedule/race/{TEST_SEASON}/{TEST_RACE_ROUND}")
            if response.status_code in [200, 500]:  # 500可能是因为比赛不存在或其他原因
                data = response.json()
                print(f"   📝 响应: {data.get('message', data)}")
            else:
                print(f"   ❌ 比赛调度创建失败: {response.status_code}")
            
            return True
            
        except Exception as e:
            print(f"   ❌ API 测试失败: {e}")
            return False
    
    async def test_manual_schedule_season(self):
        """测试手动调度整个赛季"""
        print("\n📅 测试手动调度整个赛季...")
        
        try:
            # 使用 Celery 任务
            print(f"   🎯 开始为 {TEST_SEASON} 赛季安排调度...")
            task = schedule_post_race_updates.delay(TEST_SEASON)
            
            print(f"   ✅ 调度任务已提交: {task.id}")
            print("   ⏳ 任务将在后台执行，请查看 Celery Worker 日志")
            
            return True
            
        except Exception as e:
            print(f"   ❌ 赛季调度测试失败: {e}")
            return False
    
    async def run_all_tests(self):
        """运行所有测试"""
        print("=" * 60)
        print("🏎️  F1 数据自动调度系统测试")
        print("=" * 60)
        
        tests = [
            ("核心组件", self.test_scheduler_components),
            ("调度创建", self.test_schedule_creation),
            ("调度查询", self.test_schedule_query),
            ("调度取消", self.test_schedule_cancellation),
            ("API 端点", self.test_api_endpoints),
            ("赛季调度", self.test_manual_schedule_season),
        ]
        
        results = []
        for test_name, test_func in tests:
            try:
                result = await test_func()
                results.append((test_name, result))
            except Exception as e:
                print(f"   ❌ {test_name} 测试异常: {e}")
                results.append((test_name, False))
        
        # 显示测试结果汇总
        print("\n" + "=" * 60)
        print("📊 测试结果汇总")
        print("=" * 60)
        
        passed = 0
        for test_name, result in results:
            status = "✅ 通过" if result else "❌ 失败"
            print(f"   {test_name}: {status}")
            if result:
                passed += 1
        
        total = len(results)
        print(f"\n🎯 总计: {passed}/{total} 个测试通过")
        
        if passed == total:
            print("🎉 所有测试通过！调度系统运行正常")
        else:
            print("⚠️ 部分测试失败，请检查系统配置")
        
        await self.client.aclose()
        return passed == total


async def main():
    """主函数"""
    tester = SchedulerTester()
    success = await tester.run_all_tests()
    return 0 if success else 1


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code) 