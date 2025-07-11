# F1 赛道信息抓取系统使用指南

## 系统概览

我们为 F1 赛事数据网站开发了一个完整的赛道信息抓取系统，能够从 F1 官网自动获取并更新赛道的详细信息。

## 🎯 功能特性

### 从 F1 官网抓取的信息包括：

- **赛道布局图** - 高清 webp 格式的赛道布局图片
- **Circuit Length** - 赛道长度（公里）
- **First Grand Prix** - 首次举办大奖赛年份
- **Number of Laps** - 典型比赛圈数
- **Fastest lap time** - 最快圈速记录（时间、车手、年份）
- **Race Distance** - 比赛总距离（公里）

### 技术特点：

- 🚀 **异步抓取** - 使用 aiohttp 实现高效并发
- 🖼️ **智能图片处理** - 基于 URL 模式直接获取布局图
- 🎯 **精确数据解析** - 正则表达式提取结构化信息
- 💾 **自动存储** - 图片本地缓存，数据库自动更新
- 🔄 **增量同步** - 只更新缺少信息的赛道
- 📡 **API 集成** - 提供 RESTful API 接口

## 📁 文件结构

```
backend/
├── app/
│   ├── models/circuit.py              # 扩展的赛道数据模型
│   ├── schemas/circuit.py             # 更新的API响应模式
│   ├── services/
│   │   ├── f1_circuit_scraper.py      # 核心抓取器
│   │   └── circuit_sync_service.py    # 数据同步服务
│   └── api/v1/endpoints/circuits.py   # API端点
├── scripts/sync_circuit_details.py    # 命令行管理工具
├── test_circuit_scraper.py           # 测试脚本
└── static/circuit_images/             # 本地图片存储目录
```

## 🚀 安装和配置

### 1. 安装依赖

```bash
cd backend
poetry install
```

新增的依赖包：

- `aiohttp` - 异步 HTTP 客户端
- `beautifulsoup4` - HTML 解析器
- `lxml` - XML/HTML 解析引擎

### 2. 数据库迁移

```bash
# 创建迁移文件（如果还没有）
alembic revision --autogenerate -m "添加F1赛道详细信息字段"

# 应用迁移
alembic upgrade head
```

### 3. 创建图片存储目录

```bash
mkdir -p static/circuit_images
```

## 💻 使用方法

### 方法一：命令行工具

```bash
# 查看所有赛道及其信息状态
python scripts/sync_circuit_details.py --list

# 同步所有缺少信息的赛道
python scripts/sync_circuit_details.py

# 强制同步所有赛道
python scripts/sync_circuit_details.py --all

# 同步指定赛道
python scripts/sync_circuit_details.py --circuits spa silverstone hungaroring

# 预演模式（查看会做什么，但不实际执行）
python scripts/sync_circuit_details.py --dry-run
```

### 方法二：API 接口

```bash
# 启动API服务器
uvicorn app.main:app --reload

# 查看缺少信息的赛道
curl "http://localhost:8000/api/v1/circuits/missing-info"

# 启动同步所有缺少信息的赛道
curl -X POST "http://localhost:8000/api/v1/circuits/sync"

# 强制同步所有赛道
curl -X POST "http://localhost:8000/api/v1/circuits/sync?force_update=true"

# 同步指定赛道
curl -X POST "http://localhost:8000/api/v1/circuits/sync?circuit_ids=spa&circuit_ids=silverstone"
```

### 方法三：Python 代码

```python
import asyncio
from app.services.circuit_sync_service import sync_circuits_main

# 同步所有缺少信息的赛道
results = asyncio.run(sync_circuits_main())

# 同步指定赛道
results = asyncio.run(sync_circuits_main(
    circuit_ids=["spa", "silverstone", "hungaroring"]
))
```

## 🧪 测试

运行测试脚本验证功能：

```bash
python test_circuit_scraper.py
```

## 📊 数据库更改

新增的字段：

```sql
-- Circuit模型新增字段
ALTER TABLE circuits ADD COLUMN first_grand_prix INTEGER;
ALTER TABLE circuits ADD COLUMN typical_lap_count INTEGER;
ALTER TABLE circuits ADD COLUMN race_distance FLOAT;
ALTER TABLE circuits ADD COLUMN circuit_layout_image_url VARCHAR(500);
ALTER TABLE circuits ADD COLUMN circuit_layout_image_path VARCHAR(500);
```

## 🗺️ 支持的赛道

目前支持 2025 赛季所有 F1 赛道：

| 国家             | 赛道              | 支持状态 |
| ---------------- | ----------------- | -------- |
| 🇧🇭 Bahrain       | Sakhir            | ✅       |
| 🇸🇦 Saudi Arabia  | Jeddah            | ✅       |
| 🇦🇺 Australia     | Melbourne         | ✅       |
| 🇦🇿 Azerbaijan    | Baku              | ✅       |
| 🇺🇸 Miami         | Miami             | ✅       |
| 🇮🇹 Italy         | Imola             | ✅       |
| 🇲🇨 Monaco        | Monaco            | ✅       |
| 🇨🇦 Canada        | Montreal          | ✅       |
| 🇪🇸 Spain         | Barcelona         | ✅       |
| 🇦🇹 Austria       | Spielberg         | ✅       |
| 🇬🇧 Great Britain | Silverstone       | ✅       |
| 🇭🇺 Hungary       | Hungaroring       | ✅       |
| 🇧🇪 Belgium       | Spa-Francorchamps | ✅       |
| 🇳🇱 Netherlands   | Zandvoort         | ✅       |
| 🇸🇬 Singapore     | Marina Bay        | ✅       |
| 🇺🇸 United States | Austin            | ✅       |
| 🇲🇽 Mexico        | Mexico City       | ✅       |
| 🇧🇷 Brazil        | Interlagos        | ✅       |
| 🇺🇸 Las Vegas     | Las Vegas         | ✅       |
| 🇶🇦 Qatar         | Lusail            | ✅       |
| 🇦🇪 Abu Dhabi     | Yas Marina        | ✅       |
| 🇨🇳 China         | Shanghai          | ✅       |
| 🇯🇵 Japan         | Suzuka            | ✅       |

## 🛠️ 故障排除

### 常见问题

1. **网络连接问题**

   ```
   ❌ 访问失败: HTTP 403/503
   ```

   解决：添加延迟，避免频繁请求

2. **图片下载失败**

   ```
   ❌ 下载图片失败
   ```

   解决：检查存储目录权限，确保网络连接

3. **数据解析失败**
   ```
   ⚠️ 未能获取赛道信息
   ```
   解决：F1 官网页面结构可能有变化，需要更新解析逻辑

### 日志文件

查看详细日志：

```bash
tail -f circuit_sync.log
```

## 🔄 自动化建议

### 定时同步

可以设置 cron job 定期同步：

```bash
# 每周同步一次
0 2 * * 0 cd /path/to/backend && python scripts/sync_circuit_details.py

# 赛季开始前强制同步所有
0 1 1 3 * cd /path/to/backend && python scripts/sync_circuit_details.py --all
```

### Celery 集成

在生产环境中，建议集成到现有的 Celery 任务队列中：

```python
from celery import Celery
from app.services.circuit_sync_service import sync_circuits_main

@celery.task
async def sync_circuits_task():
    return await sync_circuits_main()
```

## 📝 注意事项

1. **请求频率限制** - 默认每个请求间隔 2 秒，避免被 F1 官网封禁
2. **数据准确性** - 抓取的数据基于 F1 官网，可能随时间变化
3. **存储空间** - 每个赛道布局图约 50-200KB
4. **网络依赖** - 需要稳定的互联网连接
5. **合规性** - 仅用于个人学习，请遵守 F1 官网的使用条款

## 🚀 未来计划

- [ ] 添加实时圈速记录更新
- [ ] 支持历史数据抓取
- [ ] 增加数据验证和清洗
- [ ] 集成图片压缩优化
- [ ] 添加更多赛道统计信息

---

**开发团队**: F1-web 项目组  
**最后更新**: 2025 年 1 月  
**版本**: v1.0.0
