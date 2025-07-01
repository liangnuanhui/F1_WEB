#!/usr/bin/env python3
"""
启动 F1 数据自动调度系统

使用方法:
python scripts/start_scheduler.py [--workers=4] [--log-level=info]
"""

import os
import sys
import subprocess
import argparse
import signal
import time
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from app.core.config import settings


def start_celery_worker(workers=4, log_level="info"):
    """启动 Celery Worker (macOS 兼容模式)"""
    print(f"🚀 启动 Celery Worker (进程数: {workers}, 日志级别: {log_level})...")
    
    # macOS 兼容：使用 solo 执行池避免 fork() 问题
    import platform
    if platform.system() == 'Darwin':  # macOS
        cmd = [
            "celery", "-A", "app.tasks.celery_app:celery_app", "worker",
            "--loglevel", log_level,
            "--pool", "solo",  # 使用 solo 执行池
            "--queues", "default,data_sync,scheduler",
            "--prefetch-multiplier", "1",
        ]
        print("💡 检测到 macOS，使用 solo 执行池模式")
    else:
        cmd = [
            "celery", "-A", "app.tasks.celery_app:celery_app", "worker",
            "--loglevel", log_level,
            "--concurrency", str(workers),
            "--queues", "default,data_sync,scheduler",
            "--prefetch-multiplier", "1",
            "--max-tasks-per-child", "1000",
        ]
    
    return subprocess.Popen(cmd, cwd=project_root)


def start_celery_beat(log_level="info"):
    """启动 Celery Beat 调度器"""
    print(f"⏰ 启动 Celery Beat 调度器 (日志级别: {log_level})...")
    
    cmd = [
        "celery", "-A", "app.tasks.celery_app:celery_app", "beat",
        "--loglevel", log_level,
        "--schedule", "./celerybeat-schedule",
    ]
    
    return subprocess.Popen(cmd, cwd=project_root)


def start_flower(port=5555):
    """启动 Flower 监控面板"""
    print(f"🌸 启动 Flower 监控面板 (端口: {port})...")
    
    cmd = [
        "celery", "-A", "app.tasks.celery_app:celery_app", "flower",
        f"--port={port}",  # 修复端口参数格式
    ]
    
    return subprocess.Popen(cmd, cwd=project_root)


def signal_handler(sig, frame):
    """处理终止信号"""
    print("\n🛑 收到终止信号，正在停止所有进程...")
    
    # 终止所有子进程
    for proc in processes:
        if proc.poll() is None:  # 进程仍在运行
            proc.terminate()
    
    # 等待进程退出
    for proc in processes:
        proc.wait()
    
    print("✅ 所有进程已停止")
    sys.exit(0)


def check_dependencies():
    """检查依赖项"""
    print("🔍 检查依赖项...")
    
    # 检查 Redis 连接
    try:
        from app.core.redis import init_redis
        if not init_redis():
            print("❌ Redis 连接失败，请确保 Redis 服务正在运行")
            return False
    except Exception as e:
        print(f"❌ Redis 检查失败: {e}")
        return False
    
    # 检查数据库连接
    try:
        from app.core.database import get_db
        db = next(get_db())
        db.close()
        print("✅ 数据库连接正常")
    except Exception as e:
        print(f"❌ 数据库连接失败: {e}")
        return False
    
    print("✅ 依赖项检查通过")
    return True


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description="F1 数据自动调度系统")
    parser.add_argument("--workers", type=int, default=4, help="Worker 进程数 (默认: 4)")
    parser.add_argument("--log-level", default="info", choices=["debug", "info", "warning", "error"], help="日志级别")
    parser.add_argument("--no-flower", action="store_true", help="不启动 Flower 监控")
    parser.add_argument("--flower-port", type=int, default=5555, help="Flower 端口 (默认: 5555)")
    
    args = parser.parse_args()
    
    print("=" * 60)
    print("🏎️  F1 数据自动调度系统启动器")
    print("=" * 60)
    
    # 检查依赖项
    if not check_dependencies():
        print("❌ 依赖项检查失败，请解决问题后重试")
        sys.exit(1)
    
    # 注册信号处理器
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    global processes
    processes = []
    
    try:
        # 启动 Celery Worker
        worker_proc = start_celery_worker(args.workers, args.log_level)
        processes.append(worker_proc)
        
        # 启动 Celery Beat
        beat_proc = start_celery_beat(args.log_level)
        processes.append(beat_proc)
        
        # 启动 Flower (可选)
        if not args.no_flower:
            flower_proc = start_flower(args.flower_port)
            processes.append(flower_proc)
            print(f"📊 Flower 监控面板: http://localhost:{args.flower_port}/flower")
        
        print("\n" + "=" * 60)
        print("✅ F1 数据自动调度系统启动完成！")
        print("=" * 60)
        print(f"🔧 配置信息:")
        print(f"   - Worker 进程数: {args.workers}")
        print(f"   - 日志级别: {args.log_level}")
        print(f"   - Redis URL: {settings.redis_url}")
        print(f"   - 数据库: {settings.database_url}")
        print("\n🎯 系统功能:")
        print("   - ⏰ 每天自动检查即将到来的比赛（F1比赛最频繁也就一周一次）")
        print("   - 📊 比赛结束后6小时自动更新数据")
        print("   - 🧹 每6小时清理过期调度记录")
        print("\n💡 使用 Ctrl+C 停止系统")
        print("=" * 60)
        
        # 等待进程运行
        while True:
            time.sleep(1)
            
            # 检查进程状态
            for i, proc in enumerate(processes):
                if proc.poll() is not None:
                    print(f"⚠️ 进程 {i} 意外退出 (退出码: {proc.returncode})")
    
    except KeyboardInterrupt:
        signal_handler(signal.SIGINT, None)
    except Exception as e:
        print(f"❌ 启动时发生错误: {e}")
        signal_handler(signal.SIGTERM, None)


if __name__ == "__main__":
    main() 