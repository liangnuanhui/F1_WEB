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

## 📁 脚本说明

### 1. `sync_all_data.py` - 完整数据同步脚本 ⭐ **推荐使用**

**功能**: 使用统一同步服务同步所有 F1 数据
**特点**:

- 同步基础数据：赛季、赛道、车队、车手、比赛
- 同步结果数据：比赛结果、排位赛结果、冲刺赛结果
- 同步排名数据：车手排名、车队排名
- 智能频率限制处理
- 完整的错误处理和重试机制

**使用方法**:

```bash
cd backend
python scripts/sync_all_data.py
```

**同步的数据**:

- ✅ 赛季数据 (2023-2025)
- ✅ 赛道数据
- ✅ 车队数据
- ✅ 车手数据
- ✅ 比赛数据
- ✅ 比赛结果
- ✅ 排位赛结果
- ✅ 冲刺赛结果 🆕
- ✅ 车手排名
- ✅ 车队排名

### 2. `sync_custom_seasons.py` - 自定义赛季同步脚本 🆕

**功能**: 允许用户选择要同步的赛季
**特点**:

- 支持命令行参数
- 灵活的赛季选择
- 多种预设模式

**使用方法**:

```bash
# 同步所有默认赛季 (2023-2025)
python scripts/sync_custom_seasons.py

# 只同步当前赛季 (2025)
python scripts/sync_custom_seasons.py --current-only

# 只同步最近两个赛季 (2024-2025)
python scripts/sync_custom_seasons.py --recent-only

# 自定义赛季
python scripts/sync_custom_seasons.py --seasons 2024 2025

# 指定缓存目录
python scripts/sync_custom_seasons.py --cache-dir ./my_cache
```

### 3. `init_data.py` - 初始化数据脚本

**功能**: 快速初始化基础数据和部分结果数据
**特点**:

- 同步基础数据：赛季、赛道、车队、车手、比赛
- 同步部分结果数据：前 3 轮比赛结果、排位赛结果、冲刺赛结果
- 适合快速测试和开发环境

### 4. `validate_2025_config.py` - 配置验证脚本

**功能**: 验证所有配置是否正确
**特点**: 检查数据库、服务、脚本配置

### 5. `test_data_providers.py` - 数据提供者测试脚本

**功能**: 测试数据提供者是否正常工作
**特点**: 详细的数据源测试

### 6. `test_sprint_sync.py` - 冲刺赛同步测试脚本 🆕

**功能**: 测试冲刺赛结果同步功能
**特点**:

- 专门测试冲刺赛数据同步
- 显示冲刺赛结果统计
- 验证冲刺赛数据完整性

**使用方法**:

```bash
python scripts/test_sprint_sync.py
```

### 7. 数据库管理脚本

- **`clear_database.py`**: 清空所有表数据
- **`drop_all_tables.py`**: 删除所有表
- **`fix_database_field.py`**: 修复数据库字段

## 🚀 推荐使用流程

### 首次设置（推荐）

```bash
# 1. 验证所有配置
python scripts/validate_2025_config.py

# 2. 测试数据提供者
python scripts/test_data_providers.py --verbose

# 3. 同步所有数据
python scripts/sync_all_data.py

# 4. 或者只同步当前赛季
python scripts/sync_custom_seasons.py --current-only
```

### 日常同步（推荐）

```bash
# 同步所有数据
python scripts/sync_all_data.py

# 或者只同步当前赛季
python scripts/sync_custom_seasons.py --current-only
```

## 赛季选择说明

### 为什么选择 2023-2025 赛季？

1. **2025 赛季** - 当前赛季 ⭐

   - 正在进行中的赛季
   - 数据最完整和最新
   - 用户最关心的数据
   - 支持实时更新

2. **2024 赛季** - 刚结束的赛季 ⭐

   - 完整的赛季数据
   - 有历史对比价值
   - 数据质量高
   - 支持趋势分析

3. **2023 赛季** - 历史赛季
   - 提供更多历史数据
   - 支持长期趋势分析
   - 但数据可能不如新赛季完整

### 数据范围控制策略

**性能考虑**:

- 避免获取不必要的历史数据
- 减少网络请求和数据处理时间
- 降低存储空间需求
- 提高同步效率

**业务价值**:

- 专注于当前相关赛季
- 提供更有价值的分析数据
- 减少数据噪音
- 提高用户体验

**API 限制**:

- FastF1 API 有频率限制
- 减少请求数量避免被限制
- 优化数据获取策略

## 统一同步服务

我们使用 `UnifiedSyncService` 来统一管理所有数据同步操作：

### 主要特性

1. **智能频率限制**: 根据 API 类型自动调整请求频率
2. **错误重试**: 自动处理 API 频率限制和网络错误
3. **数据完整性**: 确保所有相关数据都被正确同步
4. **缓存支持**: 支持 FastF1 缓存以提高性能

### 同步流程

1. **基础数据同步**

   - 赛季数据
   - 赛道数据
   - 车队数据
   - 车手数据

2. **比赛数据同步**

   - 比赛日程
   - 比赛结果
   - 排位赛结果
   - 冲刺赛结果 🆕

3. **排名数据同步**
   - 车手积分榜
   - 车队积分榜

## 数据源

- **FastF1**: 主要数据源，提供详细的比赛和结果数据
- **Ergast API**: 通过 FastF1 访问，提供标准化的 F1 数据

## 注意事项

1. **频率限制**: API 有频率限制，脚本会自动处理
2. **数据范围**: 默认同步 2023-2025 赛季数据
3. **缓存**: 建议启用 FastF1 缓存以提高性能
4. **错误处理**: 脚本包含完整的错误处理和日志记录

## 故障排除

### 常见问题

1. **API 频率限制**

   - 脚本会自动重试
   - 增加延迟时间

2. **数据不完整**

   - 检查网络连接
   - 查看日志文件

3. **数据库错误**
   - 检查数据库连接
   - 验证模型定义

### 日志文件

- `unified_sync.log`: 统一同步服务的详细日志
- `custom_sync.log`: 自定义同步的详细日志
- 控制台输出: 实时同步状态

## 开发说明

### 添加新的同步功能

1. 在 `UnifiedSyncService` 中添加新方法
2. 在 `sync_all_data()` 中调用新方法
3. 更新文档和测试

### 自定义同步

```python
from app.services.unified_sync_service import UnifiedSyncService

# 创建同步服务
sync_service = UnifiedSyncService(db, cache_dir="./cache")

# 同步特定赛季
sync_service.sync_all_data(target_seasons=[2025])

# 同步特定数据类型
sync_service.sync_race_results(2025)
sync_service.sync_driver_standings(2025)
```

## 🔄 更新日志

- **v3.0**: 统一同步服务，删除冗余脚本
- **v2.1**: 添加配置验证和模型修复脚本
- **v2.0**: 针对 2025 赛季优化
- **v1.5**: 增加智能延迟和错误恢复
- **v1.0**: 基础数据同步功能
