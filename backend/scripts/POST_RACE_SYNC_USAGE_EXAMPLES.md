# F1 比赛后数据同步系统使用示例

## 🚀 快速上手

### 1. 启动系统

```bash
cd backend

# 终端1: 启动API服务
poetry run uvicorn app.main:app --reload --port 8000

# 终端2: 启动Celery worker
poetry run celery -A app.tasks.celery_app worker --loglevel=info --pool=eventlet

# 终端3: 启动Celery Beat调度器
poetry run celery -A app.tasks.celery_app beat --loglevel=info
```

### 2. 使用管理脚本

```bash
# 使脚本可执行
chmod +x scripts/manage_post_race_sync.py

# 查看帮助
python scripts/manage_post_race_sync.py --help
```

## 📋 常用操作示例

### 为比赛安排同步计划

```bash
# 为2025赛季第10轮（奥地利大奖赛）安排同步计划
python scripts/manage_post_race_sync.py schedule 2025 10

# 自定义重试间隔（比赛后2、6、12小时执行）
python scripts/manage_post_race_sync.py schedule 2025 10 --intervals 2 6 12
```

### 查看同步计划状态

```bash
# 查看特定比赛的同步计划
python scripts/manage_post_race_sync.py get 2025 10

# 列出所有同步计划
python scripts/manage_post_race_sync.py list

# 列出2025赛季的计划
python scripts/manage_post_race_sync.py list --season 2025

# 列出未完成的计划
python scripts/manage_post_race_sync.py list --status pending
```

### 立即执行同步

```bash
# 立即执行第1次同步尝试
python scripts/manage_post_race_sync.py execute 2025 10 1

# 立即执行第2次同步尝试
python scripts/manage_post_race_sync.py execute 2025 10 2
```

### 取消同步计划

```bash
# 取消指定比赛的同步计划
python scripts/manage_post_race_sync.py cancel 2025 10
```

### 系统监控和维护

```bash
# 获取统计信息
python scripts/manage_post_race_sync.py stats

# 获取2025赛季的统计信息
python scripts/manage_post_race_sync.py stats --season 2025

# 手动触发系统监控
python scripts/manage_post_race_sync.py monitor

# 清理过期的同步计划
python scripts/manage_post_race_sync.py cleanup
```

## 🌐 使用 cURL 操作

### 基本 API 调用

```bash
# 为2025赛季第10轮安排同步计划
curl -X POST "http://localhost:8000/api/v1/post-race-sync/2025/10/schedule" \
  -H "Content-Type: application/json" \
  -d '{"retry_intervals": [6, 12, 24]}'

# 查看同步计划状态
curl "http://localhost:8000/api/v1/post-race-sync/2025/10/schedule" | jq

# 立即执行第1次同步尝试
curl -X POST "http://localhost:8000/api/v1/post-race-sync/2025/10/execute/1"

# 取消同步计划
curl -X DELETE "http://localhost:8000/api/v1/post-race-sync/2025/10/schedule"
```

### 批量操作

```bash
# 查看所有同步计划
curl "http://localhost:8000/api/v1/post-race-sync/schedules" | jq

# 查看2025赛季的同步计划
curl "http://localhost:8000/api/v1/post-race-sync/schedules?season_year=2025" | jq

# 查看待执行的同步任务
curl "http://localhost:8000/api/v1/post-race-sync/pending" | jq

# 获取统计信息
curl "http://localhost:8000/api/v1/post-race-sync/stats" | jq

# 获取2025赛季统计信息
curl "http://localhost:8000/api/v1/post-race-sync/stats?season_year=2025" | jq
```

### 维护操作

```bash
# 手动触发监控（检查遗漏的任务）
curl -X POST "http://localhost:8000/api/v1/post-race-sync/monitor"

# 清理过期的同步计划
curl -X POST "http://localhost:8000/api/v1/post-race-sync/cleanup"

# 批量安排未来7天的比赛
curl -X POST "http://localhost:8000/api/v1/post-race-sync/batch-schedule?season_year=2025&days_ahead=7"
```

## 🏎️ 实际使用场景

### 场景 1: 周末比赛后的常规流程

假设奥地利大奖赛于 2025 年 6 月 29 日 15:00 UTC 结束：

```bash
# 1. 比赛开始前，为比赛安排同步计划
python scripts/manage_post_race_sync.py schedule 2025 10

# 2. 比赛后，查看同步计划状态
python scripts/manage_post_race_sync.py get 2025 10

# 3. 如果第一次尝试失败，可以立即重试
python scripts/manage_post_race_sync.py execute 2025 10 2

# 4. 查看整体统计
python scripts/manage_post_race_sync.py stats --season 2025
```

### 场景 2: 大量比赛的批量管理

```bash
# 1. 批量安排即将到来的比赛
curl -X POST "http://localhost:8000/api/v1/post-race-sync/batch-schedule?season_year=2025&days_ahead=14"

# 2. 查看所有计划状态
python scripts/manage_post_race_sync.py list --season 2025

# 3. 定期清理过期计划
python scripts/manage_post_race_sync.py cleanup
```

### 场景 3: 故障排除

```bash
# 1. 检查是否有遗漏的同步任务
curl "http://localhost:8000/api/v1/post-race-sync/pending" | jq

# 2. 手动触发监控
python scripts/manage_post_race_sync.py monitor

# 3. 查看失败的同步计划
python scripts/manage_post_race_sync.py list --status failed

# 4. 重新执行失败的同步
python scripts/manage_post_race_sync.py execute 2025 10 1
```

## 🔍 监控和日志

### Celery 监控

```bash
# 查看Celery worker状态
poetry run celery -A app.tasks.celery_app inspect active

# 查看已注册的任务
poetry run celery -A app.tasks.celery_app inspect registered

# 查看队列状态
poetry run celery -A app.tasks.celery_app inspect active_queues
```

### Redis 监控

```bash
# 连接Redis查看存储的同步计划
redis-cli

# 查看所有同步计划的键
127.0.0.1:6379> KEYS "post_race_sync:*"

# 查看特定计划的内容
127.0.0.1:6379> GET "post_race_sync:2025:10"
```

### 应用日志

Celery 任务执行时会输出详细的日志，包括：

```
🏎️ 开始执行比赛后数据同步 - 2025 赛季第 10 轮 (第 1 次尝试)
🚥 同步排位赛结果...
   排位赛结果: ✅ 成功，更新了 20 条记录
🏁 同步比赛结果...
   比赛结果: ✅ 成功，更新了 20 条记录
🎯 同步冲刺赛结果...
   冲刺赛结果: ⏳ 暂无数据（比赛尚未进行）
📊 同步车手积分榜...
   车手积分榜: ✅ 成功，更新了 20 条记录
🏆 同步车队积分榜...
   车队积分榜: ✅ 成功，更新了 10 条记录
✅ 比赛后数据同步完成: 4/5 项成功
```

## ⚠️ 注意事项

1. **时区处理**: 系统统一使用 UTC 时间，确保服务器时区设置正确
2. **网络延迟**: FastF1 数据源可能有延迟，系统会自动重试
3. **资源使用**: 避免同时执行过多同步任务，建议使用默认队列配置
4. **错误处理**: 单个数据类型失败不会影响其他数据的同步

## 🎯 最佳实践

1. **提前安排**: 在比赛开始前就安排好同步计划
2. **监控统计**: 定期查看统计信息，了解系统运行状况
3. **及时清理**: 定期清理过期的同步计划，避免 Redis 存储过多数据
4. **故障恢复**: 利用监控功能自动发现和处理遗漏的同步任务
5. **批量操作**: 对于多场比赛，使用批量操作提高效率

---

这个系统提供了完整的 F1 比赛后数据同步解决方案，具备企业级的可靠性和可监控性。通过合理使用这些工具，可以确保网站始终展示最新的 F1 比赛数据。
