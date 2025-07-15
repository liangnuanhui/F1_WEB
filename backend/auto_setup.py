"""
一键设置脚本 - 完全自动化比赛数据同步
运行一次即可为整个赛季设置自动同步
"""

import asyncio
import sys
import argparse
from datetime import datetime
import httpx
import json

class AutoSyncSetup:
    """自动同步设置管理器"""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url.rstrip('/')
        self.api_base = f"{self.base_url}/api/v1"
    
    async def setup_full_auto_sync(self, season_year: int):
        """
        一键设置整个赛季的完全自动同步
        这是你唯一需要运行的命令！
        """
        print(f"🚀 开始为 {season_year} 赛季设置完全自动化同步...")
        
        async with httpx.AsyncClient(timeout=60.0) as client:
            try:
                # 调用后端API安排整个赛季的自动同步
                url = f"{self.api_base}/auto-sync/setup-season/{season_year}"
                response = await client.post(url)
                response.raise_for_status()
                
                result = response.json()
                
                print("✅ 完全自动化同步设置成功！")
                print(f"   赛季: {season_year}")
                print(f"   新安排的比赛: {result.get('newly_scheduled', 0)} 场")
                print(f"   已有安排的比赛: {result.get('already_scheduled', 0)} 场")
                print(f"   失败的比赛: {result.get('failed', 0)} 场")
                
                print("\n🎯 系统现在会自动：")
                print("   • 在每场比赛结束后的 6, 12, 24, 30, 36, 42, 48 小时自动尝试同步")
                print("   • 一旦成功获取到新数据就停止重试")
                print("   • 每天检查是否有新比赛需要安排")
                print("   • 你不需要再做任何手动操作！")
                
                return True
                
            except httpx.HTTPStatusError as e:
                print(f"❌ API请求失败: HTTP {e.response.status_code}")
                print(f"   错误信息: {e.response.text}")
                return False
            except Exception as e:
                print(f"❌ 设置失败: {e}")
                return False
    
    async def check_auto_sync_status(self, season_year: int):
        """检查自动同步状态"""
        async with httpx.AsyncClient(timeout=30.0) as client:
            try:
                url = f"{self.api_base}/auto-sync/status/{season_year}"
                response = await client.get(url)
                response.raise_for_status()
                
                result = response.json()
                
                print(f"📊 {season_year} 赛季自动同步状态:")
                print(f"   总比赛数: {result.get('total_races', 0)}")
                print(f"   已安排自动同步: {result.get('scheduled_races', 0)}")
                print(f"   待执行任务: {result.get('pending_tasks', 0)}")
                print(f"   已完成任务: {result.get('completed_tasks', 0)}")
                
                return True
                
            except Exception as e:
                print(f"❌ 检查状态失败: {e}")
                return False
    
    async def test_connection(self):
        """测试API连接"""
        async with httpx.AsyncClient(timeout=10.0) as client:
            try:
                url = f"{self.base_url}/health"
                response = await client.get(url)
                response.raise_for_status()
                
                print("✅ API连接正常")
                return True
                
            except Exception as e:
                print(f"❌ API连接失败: {e}")
                print("   请确保后端服务正在运行")
                return False


async def main():
    """主函数"""
    parser = argparse.ArgumentParser(description="F1比赛数据完全自动化同步设置")
    parser.add_argument("api_url", help="API服务器地址 (如: https://your-app.onrender.com)")
    parser.add_argument("--season", type=int, default=datetime.now().year, 
                       help="赛季年份 (默认: 当前年份)")
    parser.add_argument("--action", choices=["setup", "status", "test"], 
                       default="setup", help="操作类型")
    
    args = parser.parse_args()
    
    setup = AutoSyncSetup(args.api_url)
    
    if args.action == "test":
        print("🔍 测试API连接...")
        success = await setup.test_connection()
        sys.exit(0 if success else 1)
        
    elif args.action == "status":
        print("📊 检查自动同步状态...")
        success = await setup.check_auto_sync_status(args.season)
        sys.exit(0 if success else 1)
        
    elif args.action == "setup":
        print("🚀 设置完全自动化同步...")
        
        # 先测试连接
        if not await setup.test_connection():
            sys.exit(1)
        
        # 执行设置
        success = await setup.setup_full_auto_sync(args.season)
        
        if success:
            print(f"\n🎉 {args.season} 赛季完全自动化同步设置完成！")
            print("   从现在开始，系统会自动处理所有比赛数据更新")
            print("   你可以完全不用管了！")
            
            # 显示状态
            await setup.check_auto_sync_status(args.season)
        
        sys.exit(0 if success else 1)


if __name__ == "__main__":
    if len(sys.argv) == 1:
        print("""
🏎️  F1比赛数据完全自动化同步设置工具

这个工具让你一次设置后就完全不用管了！

使用方法:
  python auto_setup.py <API_URL> [选项]

示例:
  # 一键设置2025赛季完全自动同步 (推荐)
  python auto_setup.py https://your-app.onrender.com --season 2025
  
  # 检查自动同步状态
  python auto_setup.py https://your-app.onrender.com --action status --season 2025
  
  # 测试API连接
  python auto_setup.py https://your-app.onrender.com --action test

设置完成后，系统会自动：
✓ 在每场比赛结束后的 6, 12, 24, 30, 36, 42, 48 小时尝试同步数据
✓ 一旦成功获取数据就停止重试  
✓ 每天检查新比赛并自动安排
✓ 完全不需要你再手动操作！
""")
        sys.exit(1)
    
    asyncio.run(main())