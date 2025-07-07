#!/bin/bash

# F1 比赛后数据同步系统停止脚本
# 停止API服务、Celery Worker和Beat调度器

set -e

echo "🛑 F1 比赛后数据同步系统停止脚本"
echo "=================================================="

# 函数：停止服务
stop_service() {
    local service_name="$1"
    local pid_file="logs/${service_name}.pid"
    
    if [ -f "$pid_file" ]; then
        local pid=$(cat "$pid_file")
        if ps -p $pid > /dev/null 2>&1; then
            echo "🛑 停止 ${service_name} (PID: $pid)..."
            kill $pid
            
            # 等待进程退出
            local count=0
            while ps -p $pid > /dev/null 2>&1 && [ $count -lt 10 ]; do
                sleep 1
                count=$((count + 1))
            done
            
            # 如果进程仍在运行，强制杀死
            if ps -p $pid > /dev/null 2>&1; then
                echo "⚠️  强制停止 ${service_name}..."
                kill -9 $pid
            fi
            
            echo "✅ ${service_name} 已停止"
        else
            echo "⚠️  ${service_name} 进程不存在 (PID: $pid)"
        fi
        rm -f "$pid_file"
    else
        echo "⚠️  ${service_name} PID文件不存在"
    fi
}

# 函数：按进程名停止服务
stop_by_name() {
    local process_pattern="$1"
    local service_name="$2"
    
    local pids=$(pgrep -f "$process_pattern" || true)
    if [ -n "$pids" ]; then
        echo "🛑 停止 ${service_name}..."
        echo "$pids" | xargs kill
        sleep 2
        
        # 检查是否还有残留进程
        local remaining_pids=$(pgrep -f "$process_pattern" || true)
        if [ -n "$remaining_pids" ]; then
            echo "⚠️  强制停止 ${service_name}..."
            echo "$remaining_pids" | xargs kill -9
        fi
        echo "✅ ${service_name} 已停止"
    else
        echo "⚠️  没有找到运行中的 ${service_name}"
    fi
}

# 停止Celery Beat调度器
stop_service "celery-beat"

# 停止Celery Worker
stop_service "celery-worker"

# 停止API服务
stop_service "fastapi"

# 额外检查：按进程名停止可能遗漏的进程
echo ""
echo "🔍 检查并清理可能遗漏的进程..."

stop_by_name "uvicorn.*app.main:app" "FastAPI服务"
stop_by_name "celery.*worker" "Celery Worker"
stop_by_name "celery.*beat" "Celery Beat"

echo ""
echo "🧹 清理临时文件..."

# 清理PID文件
rm -f logs/*.pid

# 清理Celery相关文件
rm -f celerybeat-schedule
rm -f celerybeat.pid

echo "✅ 临时文件清理完成"

echo ""
echo "🎉 F1 比赛后数据同步系统已完全停止！"
echo "=================================================="
echo "📊 验证系统状态:"
echo "   进程检查: ps aux | grep -E '(uvicorn|celery)'"
echo "   端口检查: lsof -i :8000"
echo ""
echo "🔄 重新启动系统:"
echo "   ./start_post_race_system.sh"
echo ""

# 最终验证
echo "🔍 最终验证..."
if pgrep -f "uvicorn\|celery" > /dev/null; then
    echo "⚠️  警告: 仍有相关进程在运行"
    echo "运行中的进程:"
    pgrep -fl "uvicorn\|celery"
else
    echo "✅ 确认所有相关进程已停止"
fi 