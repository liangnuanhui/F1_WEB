# F1 数据自动调度系统

## 📋 概述

这是一个基于 **Celery + Redis** 的自动化数据同步系统，能够在 F1 比赛结束后 6 小时自动更新以下数据：

- ✅ **比赛结果** (Race Results)
- ✅ **排位赛结果** (Qualifying Results)
- ✅ **冲刺赛结果** (Sprint Results)
- ✅ **车手积分榜** (Driver Standings)
- ✅ **车队积分榜** (Constructor Standings)

## 🏗️ 系统架构

```mermaid
graph TD
    A[比赛时间] --> B[Celery Beat 调度器]
    B --> C{比赛结束后6小时}
    C --> D[数据同步任务队列]
    D --> E[比赛结果同步]
    D --> F[排位赛结果同步]
    D --> G[冲刺赛结果同步]
    D --> H[车手积分榜同步]
    D --> I[车队积分榜同步]

    E --> J[FastF1/Ergast API]
    F --> J
    G --> J
    H --> J
    I --> J

    J --> K[PostgreSQL 数据库]

    L[Redis] --> B
    L --> D
```

## 🚀 快速开始

### 1. 安装依赖

```bash
cd backend
poetry install
```

### 2. 配置环境变量

```bash
# 复制环境变量模板
cp env.example .env

# 编辑配置文件
nano .env
```

关键配置项：

```env
# Redis 配置 (用于 Celery)
REDIS_URL=redis://localhost:6379/0
CELERY_BROKER_URL=redis://localhost:6379/1
CELERY_RESULT_BACKEND=redis://localhost:6379/1

# 数据库配置
DATABASE_URL=postgresql://username:password@localhost:5432/database_name

# 数据更新配置
DATA_UPDATE_INTERVAL=300  # 5分钟检查间隔
RACE_UPDATE_INTERVAL=60   # 比赛更新间隔
```

### 3. 启动服务

#### 方式一：使用启动脚本（推荐）

```bash
# 启动完整的调度系统
python scripts/start_scheduler.py

# 自定义参数
python scripts/start_scheduler.py --workers=8 --log-level=debug --flower-port=5555
```

#### 方式二：手动启动

```bash
# 启动 Celery Worker
celery -A app.tasks.celery_app:celery_app worker --loglevel=info --concurrency=4

# 启动 Celery Beat 调度器
celery -A app.tasks.celery_app:celery_app beat --loglevel=info

# 启动 Flower 监控 (可选)
celery -A app.tasks.celery_app:celery_app flower --port=5555
```

## 📅 调度机制

### 自动调度

系统会自动：

1. **每天检查** 即将到来的比赛（未来 7 天内，F1 比赛最频繁也就一周一次）
2. **自动安排** 比赛结束后 6 小时的数据更新任务
3. **每 6 小时清理** 过期的调度记录

### 调度时间计算

```python
# 比赛结束时间 = 比赛开始时间 + 3小时（预估时长）
race_end_time = race_start_time + timedelta(hours=3)

# 数据更新时间 = 比赛结束时间 + 6小时
update_time = race_end_time + timedelta(hours=6)
```

## 🎛️ API 管理

### 获取调度状态

```bash
# 获取所有已调度的比赛
GET /api/v1/scheduler/schedules

# 获取系统状态
GET /api/v1/scheduler/status
```

### 手动调度管理

```bash
# 为整个赛季安排调度
POST /api/v1/scheduler/schedule/season/2025

# 为单场比赛安排调度
POST /api/v1/scheduler/schedule/race/2025/1

# 取消比赛调度
DELETE /api/v1/scheduler/schedule/race/2025/1

# 立即同步比赛数据（不等待调度时间）
POST /api/v1/scheduler/sync/immediate/2025/1
```

### 示例 API 响应

```json
{
  "message": "已安排 2025 赛季第 1 轮比赛的数据更新任务",
  "season_year": 2025,
  "race_round": 1,
  "race_name": "FORMULA 1 LOUIS VUITTON AUSTRALIAN GRAND PRIX 2025",
  "status": "scheduled",
  "scheduled_at": "2025-01-01T12:00:00"
}
```

## 📊 监控面板

### Flower 监控

访问 **http://localhost:5555/flower** 查看：

- 🔄 **活跃任务** - 正在执行的同步任务
- ⏰ **调度任务** - 等待执行的任务
- 📈 **任务历史** - 执行结果和统计
- 🖥️ **Worker 状态** - 工作进程监控

### Redis 监控

```bash
# 连接 Redis CLI
redis-cli

# 查看调度键
KEYS race_schedule:*

# 查看具体调度信息
GET race_schedule:2025:1
```

## 🛠️ 故障排除

### 常见问题

**1. Redis 连接失败**

```bash
# 检查 Redis 服务状态
redis-cli ping

# 启动 Redis 服务
brew services start redis  # macOS
sudo systemctl start redis # Linux
```

**2. 数据库连接失败**

```bash
# 检查 PostgreSQL 服务
pg_isready -h localhost -p 5432

# 检查数据库连接
python scripts/check_database_state.py
```

**3. Celery Worker 无法启动**

```bash
# 检查依赖项
poetry install

# 检查配置文件
python -c "from app.core.config import get_settings; print(get_settings())"
```

**4. 任务执行失败**

```bash
# 查看 Celery Worker 日志
celery -A app.tasks.celery_app:celery_app events

# 查看具体任务状态
python scripts/check_celery_tasks.py
```

### 日志文件

- **Celery Worker**: `celery_worker.log`
- **Celery Beat**: `celery_beat.log`
- **数据同步**: `unified_sync.log`

## ⚡ 性能优化

### Worker 配置

```bash
# 根据CPU核心数调整并发数
--concurrency=8  # 8核CPU推荐

# 设置内存限制
--max-memory-per-child=200000  # 200MB

# 优化任务预取
--prefetch-multiplier=1
```

### Redis 配置

```redis
# redis.conf 优化
maxmemory 2gb
maxmemory-policy allkeys-lru
save 900 1
```

### 队列配置

系统使用三个队列：

- `default` - 一般任务
- `data_sync` - 数据同步任务（高优先级）
- `scheduler` - 调度管理任务

## 🔐 安全配置

### 生产环境配置

```env
# 使用强密码
REDIS_PASSWORD=your_strong_redis_password
DATABASE_PASSWORD=your_strong_db_password

# 限制连接来源
REDIS_HOST=internal_redis_host
DATABASE_HOST=internal_db_host

# 启用SSL
DATABASE_URL=postgresql://user:pass@host:5432/db?sslmode=require
```

### 防火墙配置

```bash
# 只允许内部访问 Redis
iptables -A INPUT -p tcp --dport 6379 -s 192.168.1.0/24 -j ACCEPT
iptables -A INPUT -p tcp --dport 6379 -j DROP
```

## 📈 扩展部署

### 🚀 部署配置

### 📦 Docker 部署

```yaml
# docker-compose.yml
version: "3.8"
services:
  celery-worker:
    build: .
    environment:
      - CELERY_BROKER_URL=redis://redis:6379/0
      - CELERY_RESULT_BACKEND=redis://redis:6379/0
      - DATABASE_URL=postgresql://user:pass@db:5432/f1web
      # 重要：确保容器使用UTC时区
      - TZ=UTC
    command: celery -A app.tasks.celery_app worker --loglevel=info --queues=data_sync,scheduler
    depends_on:
      - redis
      - db

  celery-beat:
    build: .
    environment:
      - CELERY_BROKER_URL=redis://redis:6379/0
      - TZ=UTC # 确保Beat调度器使用UTC时区
    command: celery -A app.tasks.celery_app beat --loglevel=info
    depends_on:
      - redis

  flower:
    build: .
    environment:
      - CELERY_BROKER_URL=redis://redis:6379/0
      - TZ=UTC
    command: celery -A app.tasks.celery_app flower --port=5555
    ports:
      - "5555:5555"
    depends_on:
      - redis
```

### ⏰ 时区配置说明

**系统时间处理机制：**

- ✅ 系统内部统一使用 **UTC 时间**
- ✅ Celery 配置为 `timezone="UTC"`，`enable_utc=True`
- ✅ 所有调度和计算都基于 UTC 时间
- ✅ 数据库存储的时间字段都是 UTC 时间

**部署到不同时区的优势：**

```bash
# 部署到任何时区的服务器都无需额外配置
# 系统自动处理所有时区转换

# 美国东部时间服务器 (EST/EDT)
export TZ=UTC  # 仍然使用UTC

# 欧洲中部时间服务器 (CET/CEST)
export TZ=UTC  # 仍然使用UTC

# 亚洲东部时间服务器 (JST/CST)
export TZ=UTC  # 仍然使用UTC
```

**FastF1 数据时区处理：**

```python
# 数据同步时，系统会正确处理时区转换
# FastF1 数据包含：
# - Session1Date: "2025-03-14 12:30:00+11:00" (本地时间)
# - Session1DateUtc: "2025-03-14 01:30:00" (UTC时间)
# 系统使用 UTC 字段进行调度计算
```

### 🌐 Serverless 部署

```yaml
# serverless.yml (AWS Lambda示例)
service: f1-web-scheduler

provider:
  name: aws
  runtime: python3.9
  region: us-east-1 # 任何地区都可以
  environment:
    TZ: UTC # 确保Lambda使用UTC时区
    CELERY_BROKER_URL: ${env:REDIS_URL}
    DATABASE_URL: ${env:DATABASE_URL}

functions:
  scheduler:
    handler: app.tasks.scheduler.lambda_handler
    timeout: 900
    events:
      - schedule: rate(1 hour) # 每小时检查
    environment:
      TZ: UTC
```

### 🔍 时区验证脚本

创建验证脚本确保时区配置正确：

```python
# scripts/verify_timezone.py
import os
from datetime import datetime
from app.tasks.celery_app import celery_app

def verify_timezone():
    print(f"系统时区: {os.environ.get('TZ', '未设置')}")
    print(f"当前UTC时间: {datetime.utcnow()}")
    print(f"Celery时区配置: {celery_app.conf.timezone}")
    print(f"Celery UTC启用: {celery_app.conf.enable_utc}")

    # 验证调度时间计算
    from app.tasks.scheduler import RaceScheduler
    scheduler = RaceScheduler()
    print(f"调度器初始化成功，使用UTC时间")

if __name__ == "__main__":
    verify_timezone()
```

## 🧪 测试

### 单元测试

```bash
# 运行调度器测试
python -m pytest tests/test_scheduler.py

# 运行数据同步测试
python -m pytest tests/test_data_sync.py
```

### 集成测试

```bash
# 测试完整的同步流程
python scripts/test_scheduler_integration.py

# 测试API端点
python scripts/test_scheduler_api.py
```

## 📞 支持

如有问题或建议，请：

1. 查看 [故障排除](#故障排除) 部分
2. 检查系统日志文件
3. 使用 Flower 监控面板分析任务状态
4. 提交 Issue 到项目仓库

---

**最后更新**: 2025 年 1 月  
**版本**: v1.0.0
