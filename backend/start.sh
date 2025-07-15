#!/bin/bash
# 启动脚本 - 用于Render平台

# 设置环境变量
export PYTHONPATH="/opt/render/project/src/backend:$PYTHONPATH"

# 根据服务类型启动不同组件
case "$1" in
  "web")
    echo "启动FastAPI web服务..."
    cd /opt/render/project/src/backend
    python -m uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}
    ;;
  "worker")
    echo "启动Celery worker..."
    cd /opt/render/project/src/backend
    celery -A app.tasks.celery_app worker \
      -Q post_race_sync,post_race_scheduler,post_race_monitor,post_race_cleanup,post_race_batch \
      --loglevel=info \
      --concurrency=2
    ;;
  "scheduler")
    echo "启动Celery beat调度器..."
    cd /opt/render/project/src/backend
    celery -A app.tasks.celery_app beat --loglevel=info
    ;;
  *)
    echo "用法: $0 {web|worker|scheduler}"
    exit 1
    ;;
esac