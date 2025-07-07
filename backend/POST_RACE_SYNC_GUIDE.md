# F1 比赛后数据同步系统使用指南

## 🏁 系统概述

比赛后数据同步系统是一个智能的自动化解决方案，专门用于在 F1 比赛结束后及时同步和更新五个核心数据类型：

1. **比赛结果** (race_results)
2. **排位赛结果** (qualifying_results)
3. **冲刺赛结果** (sprint_results)
4. **车手积分榜** (driver_standings)
5. **车队积分榜** (constructor_standings)

## 🎯 核心特性

### 多时间点重试机制

- **默认重试时间点**：比赛结束后 6 小时、12 小时、24 小时
- **智能估算**：自动计算比赛结束时间
- **容错处理**：源数据维护延迟的补偿机制

### 实时监控和管理

- **计划管理**：创建、查看、取消同步计划
- **状态监控**：实时跟踪同步进度和结果
- **失败重试**：自动重试机制和手动触发
- **数据统计**：成功率统计和详细报告

## 🚀 快速开始

### 1. 为单场比赛安排同步计划

```bash
# 为2025赛季第10轮(英国大奖赛)安排同步计划
curl -X POST "http://localhost:8000/api/v1/post-race-sync/2025/10/schedule" \
  -H "Content-Type: application/json" \
  -d '{
    "retry_intervals": [6, 12, 24]
  }'
```

响应示例：

```json
{
  "message": "已开始安排 British Grand Prix 的赛后同步计划",
  "season_year": 2025,
  "race_round": 10,
  "race_name": "British Grand Prix",
  "retry_intervals": [6, 12, 24],
  "status": "scheduling"
}
```

### 2. 查看同步计划状态

```bash
# 查看特定比赛的同步计划
curl "http://localhost:8000/api/v1/post-race-sync/2025/10/schedule"
```

响应示例：

```json
{
  "schedule": {
    "season_year": 2025,
    "race_round": 10,
    "race_name": "British Grand Prix",
    "race_end_time": "2025-07-06T21:00:00+00:00",
    "created_at": "2025-07-06T15:00:00+00:00",
    "is_completed": false,
    "success_rate": 0.0,
    "next_pending_attempt": {
      "attempt_number": 1,
      "scheduled_time": "2025-07-07T03:00:00+00:00"
    },
    "attempts": [
      {
        "attempt_number": 1,
        "scheduled_time": "2025-07-07T03:00:00+00:00",
        "executed_time": null,
        "status": "pending",
        "results": null,
        "error_message": null
      },
      {
        "attempt_number": 2,
        "scheduled_time": "2025-07-07T09:00:00+00:00",
        "executed_time": null,
        "status": "pending",
        "results": null,
        "error_message": null
      },
      {
        "attempt_number": 3,
        "scheduled_time": "2025-07-07T21:00:00+00:00",
        "executed_time": null,
        "status": "pending",
        "results": null,
        "error_message": null
      }
    ]
  }
}
```

### 3. 手动触发立即同步

```bash
# 立即执行第1次同步尝试
curl -X POST "http://localhost:8000/api/v1/post-race-sync/2025/10/execute/1"
```

## 📋 API 端点详细说明

### 同步计划管理

#### 创建同步计划

```http
POST /api/v1/post-race-sync/{season_year}/{race_round}/schedule
Content-Type: application/json

{
  "retry_intervals": [6, 12, 24]  // 可选，默认[6, 12, 24]
}
```

#### 获取同步计划

```http
GET /api/v1/post-race-sync/{season_year}/{race_round}/schedule
```

#### 取消同步计划

```http
DELETE /api/v1/post-race-sync/{season_year}/{race_round}/schedule
```

#### 立即执行同步

```http
POST /api/v1/post-race-sync/{season_year}/{race_round}/execute/{attempt_number}
```

### 批量管理

#### 获取所有同步计划

```http
GET /api/v1/post-race-sync/schedules?season_year=2025&status_filter=pending
```

参数：

- `season_year` (可选): 按赛季过滤
- `status_filter` (可选): 状态过滤 (`pending`/`completed`/`failed`)

#### 批量安排即将到来的比赛

```http
POST /api/v1/post-race-sync/batch-schedule?season_year=2025&days_ahead=7
```

### 监控和维护

#### 获取待执行任务

```http
GET /api/v1/post-race-sync/pending
```

#### 手动触发监控

```http
POST /api/v1/post-race-sync/monitor
```

#### 清理过期计划

```http
POST /api/v1/post-race-sync/cleanup
```

#### 获取统计信息

```http
GET /api/v1/post-race-sync/stats?season_year=2025
```

## 🔄 工作流程

### 自动工作流程

1. **比赛前准备**

   - 系统自动或手动为即将到来的比赛创建同步计划
   - 计算比赛结束时间和同步时间点

2. **比赛进行中**

   - 系统等待比赛结束
   - 自动监控同步时间点

3. **比赛结束后**

   - **第 1 次尝试**（6 小时后）：执行数据同步
   - **第 2 次尝试**（12 小时后）：如果第 1 次失败或部分成功
   - **第 3 次尝试**（24 小时后）：最后一次尝试
   - **监控检查**：每小时检查遗漏的任务

4. **同步完成**
   - 记录同步结果和统计信息
   - 清理过期的同步计划

### 手动干预场景

1. **紧急同步**：比赛结束后立即手动触发同步
2. **失败重试**：当自动同步失败时，手动重新执行
3. **计划调整**：取消或重新安排同步计划
4. **批量操作**：为多场比赛批量创建同步计划

## ⚙️ 配置参数

### 默认配置

```python
# 默认重试时间点（小时）
DEFAULT_RETRY_INTERVALS = [6, 12, 24]

# 同步的数据类型
SYNC_DATA_TYPES = [
    "race_results",
    "qualifying_results",
    "sprint_results",
    "driver_standings",
    "constructor_standings"
]

# Redis键前缀
REDIS_KEY_PREFIX = "post_race_sync"
```

### 自定义配置示例

```python
# 更频繁的重试（适用于重要比赛）
custom_intervals = [3, 6, 12, 24, 48]

# 为摩纳哥大奖赛设置特殊同步计划
curl -X POST "http://localhost:8000/api/v1/post-race-sync/2025/6/schedule" \
  -H "Content-Type: application/json" \
  -d '{
    "retry_intervals": [3, 6, 12, 24, 48]
  }'
```

## 📊 监控和统计

### 状态说明

- **pending**: 等待执行
- **running**: 正在执行
- **success**: 全部成功
- **partial**: 部分成功
- **failed**: 执行失败
- **cancelled**: 已取消

### 成功率计算

```python
# 整体成功率
overall_success = (完全成功 + 部分成功) / 总尝试次数

# 数据类型成功率
data_type_success = 特定数据类型成功次数 / 特定数据类型总尝试次数
```

### 统计信息示例

```json
{
  "total_schedules": 24,
  "completed_schedules": 20,
  "pending_schedules": 3,
  "failed_schedules": 1,
  "overall_success_rate": 0.85,
  "data_type_stats": {
    "race_results": {
      "success_rate": 0.95,
      "total_attempts": 60,
      "successes": 57
    },
    "qualifying_results": {
      "success_rate": 0.92,
      "total_attempts": 60,
      "successes": 55
    },
    "sprint_results": {
      "success_rate": 0.88,
      "total_attempts": 25,
      "successes": 22
    },
    "driver_standings": {
      "success_rate": 0.9,
      "total_attempts": 60,
      "successes": 54
    },
    "constructor_standings": {
      "success_rate": 0.88,
      "total_attempts": 60,
      "successes": 53
    }
  }
}
```

## 🛠️ 运维管理

### Celery 任务队列

系统使用以下 Celery 队列：

- `post_race_sync`: 执行同步任务
- `post_race_scheduler`: 调度计划任务
- `post_race_monitor`: 监控任务
- `post_race_cleanup`: 清理任务
- `post_race_batch`: 批量操作任务

### 定期任务

```python
# 每小时监控待执行任务
@celery_app.task(name="hourly_monitor_post_race_syncs")
def hourly_monitor_post_race_syncs():
    return monitor_pending_syncs.delay()

# 每天清理过期计划
@celery_app.task(name="daily_cleanup_expired_schedules")
def daily_cleanup_expired_schedules():
    return cleanup_expired_schedules.delay()

# 每周批量安排即将到来的比赛
@celery_app.task(name="weekly_batch_schedule_races")
def weekly_batch_schedule_races():
    return batch_schedule_upcoming_races.delay()
```

### 启动监控

```bash
# 启动Celery worker处理比赛后同步任务
celery -A app.tasks.celery_app worker -Q post_race_sync,post_race_scheduler,post_race_monitor,post_race_cleanup,post_race_batch --loglevel=info

# 启动Celery beat调度器
celery -A app.tasks.celery_app beat --loglevel=info
```

## 🚨 故障处理

### 常见问题和解决方案

#### 1. 同步失败

**症状**: 同步状态显示为`failed`
**解决方案**:

```bash
# 1. 检查错误信息
curl "http://localhost:8000/api/v1/post-race-sync/2025/10/schedule"

# 2. 手动重试
curl -X POST "http://localhost:8000/api/v1/post-race-sync/2025/10/execute/1"

# 3. 检查API连接和频率限制
```

#### 2. 计划遗漏

**症状**: 比赛结束后没有自动执行同步
**解决方案**:

```bash
# 1. 触发监控检查
curl -X POST "http://localhost:8000/api/v1/post-race-sync/monitor"

# 2. 手动创建同步计划
curl -X POST "http://localhost:8000/api/v1/post-race-sync/2025/10/schedule"
```

#### 3. 数据部分成功

**症状**: 某些数据类型同步成功，其他失败
**解决方案**:

```bash
# 1. 检查详细结果
curl "http://localhost:8000/api/v1/post-race-sync/2025/10/schedule"

# 2. 等待下一次自动重试，或手动重试
curl -X POST "http://localhost:8000/api/v1/post-race-sync/2025/10/execute/2"
```

### 紧急处理流程

1. **立即响应** (0-30 分钟)

   - 检查系统状态
   - 确认比赛数据的重要性
   - 如果是重要比赛，立即手动触发同步

2. **问题诊断** (30 分钟-2 小时)

   - 查看详细日志
   - 检查 API 连接状态
   - 分析失败原因

3. **修复和恢复** (2-24 小时)
   - 修复技术问题
   - 重新执行失败的同步
   - 验证数据完整性

## 📈 最佳实践

### 1. 比赛前准备

- 提前 1 周批量安排即将到来的比赛的同步计划
- 为重要比赛（如摩纳哥、银石、蒙扎）设置更频繁的重试间隔
- 确认 Celery worker 和 beat 调度器正常运行

### 2. 比赛期间监控

- 比赛结束后立即检查同步计划状态
- 必要时手动触发紧急同步
- 监控系统资源使用情况

### 3. 比赛后管理

- 检查同步结果的完整性
- 分析成功率统计，优化重试策略
- 清理过期的同步计划，释放存储空间

### 4. 维护建议

- 定期检查 Redis 存储状态
- 监控 API 频率限制使用情况
- 保持 FastF1 缓存目录的磁盘空间

### 5. 性能优化

- 根据历史数据调整重试间隔
- 优化 API 请求频率限制
- 使用 Redis 集群提高可用性

## 🔧 开发和扩展

### 添加新的数据类型

```python
# 在PostRaceSyncService中添加新的同步方法
def sync_new_data_type(self, season_year: int) -> bool:
    """同步新的数据类型"""
    # 实现同步逻辑
    pass

# 在execute_sync_attempt中添加新的同步调用
sync_results["new_data_type"] = self.sync_service.sync_new_data_type(season_year)
```

### 自定义重试策略

```python
# 为特定赛道或赛季定制重试策略
TRACK_SPECIFIC_INTERVALS = {
    "monaco": [2, 6, 12, 24, 48],  # 摩纳哥更频繁
    "silverstone": [3, 8, 16, 32], # 银石不同策略
}

# 赛季特殊配置
SEASON_SPECIFIC_CONFIG = {
    2025: {
        "default_intervals": [6, 12, 24],
        "important_races": [1, 6, 10, 16, 22],  # 重要比赛轮次
        "important_intervals": [3, 6, 12, 24, 48]
    }
}
```

### 添加通知机制

```python
# 添加邮件/Slack通知
def send_sync_notification(self, schedule: PostRaceSchedule, status: SyncStatus):
    """发送同步状态通知"""
    if status == SyncStatus.FAILED:
        # 发送失败通知
        pass
    elif status == SyncStatus.SUCCESS:
        # 发送成功通知
        pass
```

## 📞 支持和联系

如有任何问题或建议，请联系：

- **技术支持**: tech-support@f1-web.com
- **GitHub Issues**: https://github.com/your-org/f1-web/issues
- **文档更新**: docs@f1-web.com

---

_本文档最后更新时间：2025 年 1 月_
