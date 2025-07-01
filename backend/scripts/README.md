# F1 数据同步脚本

## 概述

本目录包含用于同步 F1 数据的各种脚本。我们使用统一的数据同步服务 (`UnifiedSyncService`) 来确保数据的一致性和完整性。

## 🎯 统一同步服务架构

### 服务层次结构

```
📁 数据提供者层 (data_provider.py)
├── DataProvider (抽象基类)
└── FastF1Provider (具体实现)
    ├── 频率限制处理
    ├── 错误重试机制
    └── 分页数据支持

📁 统一同步服务层 (unified_sync_service.py) ⭐
├── 整合 FastF1 和 Ergast API
├── 基于 FastF1 实际数据结构
├── 智能频率限制管理
└── 完整的数据同步功能

📁 脚本层
├── init_data.py (快速初始化)
├── sync_all_data.py (完整同步)
├── sync_custom_seasons.py (自定义同步)
└── test_sprint_sync.py (测试脚本)
```

### 主要特性

- ✅ 统一的 API 调用和错误处理
- ✅ 智能频率限制管理
- ✅ 完整的数据同步功能
- ✅ 基于 FastF1 实际数据结构
- ✅ 支持冲刺赛结果同步 🆕
- ✅ 动态年份支持 🆕

## 📁 脚本分类

### 🔄 数据同步脚本

#### 1. `sync_all_data.py` - 完整数据同步脚本 ⭐ **推荐使用**

**功能**: 使用统一同步服务同步连续三年的 F1 数据
**特点**:

- 同步基础数据：赛季、赛道、车队、车手、比赛
- 同步结果数据：比赛结果、排位赛结果、冲刺赛结果
- 同步排名数据：车手排名、车队排名
- 智能频率限制处理
- 完整的错误处理和重试机制
- **动态年份支持** 🆕 - 自动同步前一年、当前年、后一年

**使用方法**:

```bash
cd backend
python scripts/sync_all_data.py
```

**动态年份功能** 🆕:

- 自动获取连续三年的数据：**前一年、当前年、后一年**
- 无需手动指定年份，脚本会根据当前时间自动确定
- 提供更全面的数据覆盖范围

**示例**:

```bash
# 2025年运行时
python scripts/sync_all_data.py  # 同步2024-2025-2026赛季

# 2026年运行时
python scripts/sync_all_data.py  # 同步2025-2026-2027赛季
```

**同步的数据**:

- ✅ 赛季数据 (连续三年)
- ✅ 赛道数据
- ✅ 车队数据
- ✅ 车手数据
- ✅ 比赛数据
- ✅ 比赛结果
- ✅ 排位赛结果
- ✅ 冲刺赛结果 🆕
- ✅ 车手排名
- ✅ 车队排名

#### 2. `sync_custom_seasons.py` - 自定义赛季同步脚本 🆕

**功能**: 允许用户选择要同步的赛季，支持动态年份
**特点**:

- 支持命令行参数
- 灵活的赛季选择
- 多种预设模式
- **动态年份支持** 🆕

**使用方法**:

```bash
# 同步所有默认赛季 (当前年份和前一年)
python scripts/sync_custom_seasons.py

# 只同步当前赛季 (动态年份)
python scripts/sync_custom_seasons.py --current-only

# 只同步最近两个赛季 (当前年份和前一年)
python scripts/sync_custom_seasons.py --recent-only

# 自定义赛季
python scripts/sync_custom_seasons.py --seasons 2024 2025

# 指定缓存目录
python scripts/sync_custom_seasons.py --cache-dir ./my_cache
```

**动态年份功能** 🆕:

- `--current-only`: 自动同步**当前年份**的赛季
- `--recent-only`: 自动同步**当前年份和前一年**的赛季
- 无需手动更新年份，脚本会自动根据系统时间确定

**示例**:

```bash
# 2025年运行时
python scripts/sync_custom_seasons.py --current-only  # 同步2025赛季
python scripts/sync_custom_seasons.py --recent-only   # 同步2024-2025赛季

# 2026年运行时
python scripts/sync_custom_seasons.py --current-only  # 同步2026赛季
python scripts/sync_custom_seasons.py --recent-only   # 同步2025-2026赛季
```

#### 3. `init_data.py` - 初始化数据脚本

**功能**: 快速初始化基础数据和部分结果数据
**特点**:

- 同步基础数据：赛季、赛道、车队、车手、比赛
- 同步部分结果数据：前 3 轮比赛结果、排位赛结果、冲刺赛结果
- 适合快速测试和开发环境
- **动态年份支持** 🆕 - 只同步当前赛季

### 🔍 数据检查脚本

#### 4. `check_database_state.py` - 数据库状态检查

**功能**: 检查数据库的当前状态
**特点**:

- 显示赛季数据统计
- 检查 2025 赛季数据
- 显示比赛数据详情
- 显示赛道数据统计

#### 5. `check_circuits.py` - 赛道数据检查

**功能**: 检查数据库中的赛道数据
**特点**:

- 按赛道名称排序显示
- 显示赛道基本信息

#### 6. `check_fastf1_schedule.py` - FastF1 日程检查

**功能**: 检查 FastF1 返回的 2025 赛季日程数据
**特点**:

- 显示 FastF1 原始数据
- 按轮次排序显示

#### 7. `check_races.py` - 比赛数据检查

**功能**: 查看 2025 赛季比赛数据
**特点**:

- 显示比赛详细信息
- 包含地点、日期、格式等信息

#### 8. `check_db.py` - 数据库基础检查

**功能**: 检查数据库状态
**特点**:

- 显示赛季总数
- 显示赛季列表

#### 9. `view_data.py` - 数据可视化查看工具

**功能**: 数据库数据可视化查看工具
**特点**:

- 表格化显示所有数据
- 支持赛季、赛道、车队、车手、比赛数据查看
- 显示数据摘要统计

### 🧪 测试脚本

#### 10. `validate_2025_config.py` - 配置验证脚本

**功能**: 验证所有配置是否正确
**特点**: 检查数据库、服务、脚本配置

#### 11. `test_data_providers.py` - 数据提供者测试脚本

**功能**: 测试数据提供者是否正常工作
**特点**: 详细的数据源测试

#### 12. `test_sprint_sync.py` - 冲刺赛同步测试脚本 🆕

**功能**: 测试冲刺赛结果同步功能
**特点**:

- 专门测试冲刺赛数据同步
- 显示冲刺赛结果统计
- 验证冲刺赛数据完整性

**使用方法**:

```bash
python scripts/test_sprint_sync.py
```

#### 13. `test_qualifying_sync.py` - 排位赛同步测试

**功能**: 测试排位赛结果同步功能

#### 14. `test_full_qualifying_sync.py` - 完整排位赛同步测试

**功能**: 测试完整排位赛结果同步功能

#### 15. `test_full_race_results_sync.py` - 完整比赛结果同步测试

**功能**: 测试完整比赛结果同步功能

#### 16. `test_standings_sync.py` - 积分榜同步测试

**功能**: 测试积分榜同步功能

### 🛠️ 数据库管理脚本

#### 17. `clear_database.py` - 清空数据库

**功能**: 清空所有表数据
**特点**: 保留表结构，只删除数据

#### 18. `drop_all_tables.py` - 删除所有表

**功能**: 删除所有表
**特点**: 完全重置数据库结构

#### 19. `fix_database_field.py` - 修复数据库字段

**功能**: 修复数据库字段类型
**特点**: 修复 season 字段类型问题

### 📊 数据探索工具

#### 20. `data_explorer.py` - FastF1 数据探索工具

**功能**: 分析 FastF1 的实际数据结构
**特点**:

- 为数据建模提供依据
- 生成详细的 Markdown 报告
- 分析多个赛季的数据结构

## 🚀 推荐使用流程

### 首次设置（推荐）

```bash
# 1. 验证所有配置
python scripts/validate_2025_config.py

# 2. 测试数据提供者
python scripts/test_data_providers.py --verbose

# 3. 同步连续三年数据（推荐）
python scripts/sync_all_data.py

# 4. 或者只同步当前赛季
python scripts/sync_custom_seasons.py --current-only

# 5. 检查数据状态
python scripts/check_database_state.py
```

### 日常同步（推荐）

```bash
# 同步连续三年数据
python scripts/sync_all_data.py

# 或者只同步当前赛季
python scripts/sync_custom_seasons.py --current-only

# 检查数据状态
python scripts/view_data.py
```

### 数据检查（推荐）

```bash
# 查看完整数据状态
python scripts/view_data.py

# 检查数据库状态
python scripts/check_database_state.py

# 检查特定数据
python scripts/check_races.py
python scripts/check_circuits.py
```

## 赛季选择说明

### 动态年份功能 🆕

脚本现在支持动态年份，无需手动更新：

1. **连续三年数据** (`sync_all_data.py`) - 前一年、当前年、后一年

   - 2025 年运行时：同步 2024-2025-2026 赛季
   - 2026 年运行时：同步 2025-2026-2027 赛季

2. **当前赛季** - 根据系统时间自动确定

   - 2025 年运行时：同步 2025 赛季
   - 2026 年运行时：同步 2026 赛季

3. **最近两个赛季** - 当前年份和前一年
   - 2025 年运行时：同步 2024-2025 赛季
   - 2026 年运行时：同步 2025-2026 赛季

### 为什么选择动态年份？

1. **自动化** - 无需手动更新年份
2. **准确性** - 始终同步正确的赛季
3. **便利性** - 跨年时自动适应
4. **维护性** - 减少手动配置错误
5. **全面性** - 连续三年数据提供更好的历史对比

### 数据范围控制策略

**性能考虑**:

- 避免获取不必要的历史数据
- 减少网络请求和数据处理时间
- 降低存储空间需求
- 提高同步效率

## 📝 文件整理说明

### 已删除的临时文件

以下文件已被删除，因为它们的功能已经整合到其他脚本中：

- `debug_race_query.py` - 功能已整合到 `check_races.py`
- `check_sprint_races.py` - 功能已整合到 `check_database_state.py`
- `debug_sprint_sync.py` - 功能已整合到 `test_sprint_sync.py`
- `verify_2025_season.py` - 功能已整合到 `check_database_state.py`
- `fix_sprint_races_correct.py` - 功能已整合到 `sync_all_data.py`
- `sync_2025_season_complete.py` - 功能已整合到 `sync_all_data.py`
- `test_sprint_sync_complete.py` - 功能已整合到 `test_sprint_sync.py`
- `test_sprint_sync_final.py` - 功能已整合到 `test_sprint_sync.py`
- `test_sprint_results.py` - 功能已整合到 `test_sprint_sync.py`
- `test_driver_standings_only.py` - 功能已整合到 `test_standings_sync.py`
- `test_driver_standings.py` - 功能已整合到 `test_standings_sync.py`

### 已删除的日志文件

以下日志文件已被删除，因为它们占用空间且不再需要：

- `custom_sync.log` - 同步日志
- `fastf1_sync.log` - FastF1 同步日志
- `data_init_2025.log` - 数据初始化日志
- `fastf1_data_exploration_20250621_153234.md` - 数据探索报告

### 保留的重要文件

- `schedule_data/` - 2025 赛季日程数据文件
- `data_modeling_plan.md` - 数据建模计划文档
- `scripts/` - 所有整理后的脚本文件

## 🚀 新增功能 - 自动调度系统

### 调度器脚本

#### `start_scheduler.py` - 启动调度系统

启动完整的 F1 数据自动调度系统，包括 Celery Worker、Beat 调度器和 Flower 监控。

```bash
# 启动调度系统
python scripts/start_scheduler.py

# 自定义配置
python scripts/start_scheduler.py --workers=8 --log-level=debug --no-flower
```

**参数说明:**

- `--workers`: Worker 进程数 (默认: 4)
- `--log-level`: 日志级别 (debug/info/warning/error)
- `--no-flower`: 不启动 Flower 监控面板
- `--flower-port`: Flower 端口 (默认: 5555)

#### `test_scheduler.py` - 测试调度系统

全面测试调度系统的各个组件和功能。

```bash
# 运行完整测试
python scripts/test_scheduler.py
```

**测试内容:**

- Redis 连接测试
- 数据库连接测试
- 调度创建/查询/取消
- API 端点测试
- 赛季调度测试

#### `schedule_current_season.py` - 调度赛季

为指定赛季的所有比赛安排自动数据更新任务。

```bash
# 为当前年份安排调度
python scripts/schedule_current_season.py

# 为指定年份安排调度
python scripts/schedule_current_season.py --year=2025

# 强制覆盖已存在的调度
python scripts/schedule_current_season.py --year=2025 --force

# 试运行模式（只查看不创建）
python scripts/schedule_current_season.py --year=2025 --dry-run
```

**参数说明:**

- `--year`: 指定赛季年份 (默认: 当前年份)
- `--force`: 强制覆盖已存在的调度
- `--dry-run`: 仅显示将要安排的调度，不实际创建

### 🔄 数据自动更新工作流

1. **系统启动**: 使用 `start_scheduler.py` 启动调度系统
2. **自动检查**: 系统每小时检查即将到来的比赛（未来 24 小时内）
3. **安排调度**: 自动为比赛安排结束后 6 小时的数据更新任务
4. **执行更新**: 按时执行以下数据同步：
   - 比赛结果 (Race Results)
   - 排位赛结果 (Qualifying Results)
   - 冲刺赛结果 (Sprint Results，如适用)
   - 车手积分榜 (Driver Standings)
   - 车队积分榜 (Constructor Standings)
5. **清理维护**: 每 6 小时清理过期的调度记录

### 📊 监控和管理

#### Flower 监控面板

访问 **http://localhost:5555/flower** 查看：

- 活跃任务和调度任务
- 任务执行历史和统计
- Worker 状态监控
- 任务失败分析

#### API 管理端点

```bash
# 获取系统状态
curl http://localhost:8000/api/v1/scheduler/status

# 获取所有调度
curl http://localhost:8000/api/v1/scheduler/schedules

# 为单场比赛安排调度
curl -X POST http://localhost:8000/api/v1/scheduler/schedule/race/2025/1

# 取消比赛调度
curl -X DELETE http://localhost:8000/api/v1/scheduler/schedule/race/2025/1

# 立即同步比赛数据
curl -X POST http://localhost:8000/api/v1/scheduler/sync/immediate/2025/1
```

### 🛠️ 故障排除

#### 常见问题

**调度系统无法启动**

```bash
# 检查 Redis 服务
redis-cli ping

# 检查数据库连接
python scripts/check_database_state.py

# 检查依赖项
poetry install
```

**任务执行失败**

```bash
# 查看 Celery 日志
tail -f celery_worker.log

# 测试调度系统
python scripts/test_scheduler.py

# 检查具体任务状态
# 在 Flower 面板中查看失败任务详情
```

**数据同步不及时**

```bash
# 检查调度是否正确创建
python scripts/schedule_current_season.py --dry-run

# 手动触发数据同步
curl -X POST http://localhost:8000/api/v1/scheduler/sync/immediate/2025/1
```

### 📝 最佳实践

1. **部署前测试**: 使用 `test_scheduler.py` 确保系统正常
2. **监控日志**: 定期检查 Celery Worker 和 Beat 日志
3. **备份调度**: 在重要比赛前确认调度已正确设置
4. **性能优化**: 根据系统负载调整 Worker 进程数
5. **故障恢复**: 定期备份 Redis 数据和任务状态

---

详细使用说明请参考：[AUTO_SCHEDULER_README.md](../AUTO_SCHEDULER_README.md)
