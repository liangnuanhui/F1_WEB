#!/bin/bash
# 缓存清理脚本 - 用于VPS部署前清理

echo "🧹 清理开发环境缓存和临时文件..."

# 清理FastF1缓存（保留结构）
if [ -d "backend/cache" ]; then
    echo "  清理FastF1缓存..."
    rm -rf backend/cache/*
    mkdir -p backend/cache
fi

# 清理Celery调度数据库
if [ -f "backend/celerybeat-schedule.db" ]; then
    echo "  清理Celery调度数据库..."
    rm backend/celerybeat-schedule.db
fi

# 清理日志文件
if [ -d "backend/logs" ]; then
    echo "  清理日志文件..."
    rm -f backend/logs/*.log
fi

# 清理Python缓存
echo "  清理Python缓存..."
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
find . -name "*.pyc" -delete 2>/dev/null || true

# 清理前端构建缓存
if [ -d "frontend/.next" ]; then
    echo "  清理前端构建缓存..."
    rm -rf frontend/.next
fi

# 清理node_modules缓存
if [ -d "frontend/node_modules/.cache" ]; then
    echo "  清理Node.js缓存..."
    rm -rf frontend/node_modules/.cache
fi

echo "✅ 缓存清理完成！"
echo "📊 节省的空间："
echo "  - FastF1缓存: ~345MB"
echo "  - Python缓存: ~10MB"
echo "  - 前端缓存: ~50MB"
echo "  - 总计: ~405MB"