#!/bin/bash

# F1 比赛后数据同步系统启动脚本
# 一键启动API服务、Celery Worker和Beat调度器

set -e

echo "🏎️  F1 比赛后数据同步系统启动脚本"
echo "=================================================="

# 检查是否在正确的目录
if [ ! -f "pyproject.toml" ]; then
    echo "❌ 错误: 请在 backend 目录下运行此脚本"
    exit 1
fi

# 检查 Poetry 是否安装
if ! command -v poetry &> /dev/null; then
    echo "❌ 错误: Poetry 未安装，请先安装 Poetry"
    echo "安装命令: curl -sSL https://install.python-poetry.org | python3 -"
    exit 1
fi

# 检查依赖是否已安装
echo "🔍 检查项目依赖..."
if [ ! -d ".venv" ] || [ ! -f "poetry.lock" ]; then
    echo "📦 正在安装项目依赖..."
    poetry install
else
    echo "✅ 依赖已安装"
fi

# 检查 Redis 是否运行
echo "🔍 检查 Redis 服务..."
if ! redis-cli ping &> /dev/null; then
    echo "❌ 错误: Redis 服务未运行"
    echo "请启动 Redis 服务:"
    echo "  - macOS: brew services start redis"
    echo "  - Ubuntu: sudo systemctl start redis-server"
    echo "  - Docker: docker run -d -p 6379:6379 redis:latest"
    exit 1
else
    echo "✅ Redis 服务运行中"
fi

# 检查数据库连接
echo "🔍 检查数据库连接..."
if ! poetry run python -c "
from app.core.database import engine
try:
    engine.connect()
    print('✅ 数据库连接正常')
except Exception as e:
    print(f'❌ 数据库连接失败: {e}')
    exit(1)
" 2>/dev/null; then
    echo "❌ 数据库连接失败，请检查数据库配置"
    exit 1
fi

# 创建日志目录
mkdir -p logs

# 函数：启动服务
start_service() {
    local service_name="$1"
    local command="$2"
    local log_file="logs/${service_name}.log"
    
    echo "🚀 启动 ${service_name}..."
    
    # 检查服务是否已经在运行
    if pgrep -f "$service_name" > /dev/null; then
        echo "⚠️  ${service_name} 已在运行中"
        return
    fi
    
    # 启动服务并记录日志
    nohup $command > "$log_file" 2>&1 &
    local pid=$!
    echo "$pid" > "logs/${service_name}.pid"
    
    sleep 2
    
    # 检查服务是否成功启动
    if ps -p $pid > /dev/null; then
        echo "✅ ${service_name} 启动成功 (PID: $pid)"
        echo "   日志文件: $log_file"
    else
        echo "❌ ${service_name} 启动失败"
        echo "   请查看日志: $log_file"
        return 1
    fi
}

# 启动API服务
start_service "fastapi" "poetry run uvicorn app.main:app --host 0.0.0.0 --port 8000"

# 等待API服务启动
echo "⏳ 等待API服务启动..."
sleep 5

# 检查API服务是否正常
if curl -s http://localhost:8000/docs > /dev/null; then
    echo "✅ API服务运行正常: http://localhost:8000"
else
    echo "❌ API服务启动失败"
    exit 1
fi

# 启动Celery Worker
start_service "celery-worker" "poetry run celery -A app.tasks.celery_app worker --loglevel=info --pool=solo"

# 启动Celery Beat调度器
start_service "celery-beat" "poetry run celery -A app.tasks.celery_app beat --loglevel=info"

echo ""
echo "🎉 F1 比赛后数据同步系统启动完成！"
echo "=================================================="
echo "📊 服务状态:"
echo "   API服务:     http://localhost:8000"
echo "   API文档:     http://localhost:8000/docs"
echo "   管理脚本:    python scripts/manage_post_race_sync.py --help"
echo ""
echo "📋 常用操作:"
echo "   查看服务状态: ps aux | grep -E '(uvicorn|celery)'"
echo "   查看日志:     tail -f logs/*.log"
echo "   停止系统:     ./stop_post_race_system.sh"
echo ""
echo "🔍 快速测试:"
echo "   # 安排同步计划"
echo "   python scripts/manage_post_race_sync.py schedule 2025 10"
echo ""
echo "   # 查看计划状态"
echo "   python scripts/manage_post_race_sync.py get 2025 10"
echo ""
echo "   # 查看统计信息"
echo "   python scripts/manage_post_race_sync.py stats"
echo ""

# 显示实时日志选项
read -p "是否查看实时日志? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "📝 显示实时日志 (Ctrl+C 退出)..."
    tail -f logs/*.log
fi 