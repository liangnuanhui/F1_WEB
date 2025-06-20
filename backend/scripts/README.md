# F1 数据同步脚本

本目录包含用于同步 F1 数据的各种脚本。

## 🚨 API 频率限制解决方案

由于 FastF1/Ergast API 有 **500 calls/h** 的限制，我们重新设计了数据同步策略：

### 数据分类

#### 🟢 **基础数据**（安全，API 调用少）

- ✅ 赛季信息 (seasons)
- ✅ 赛道信息 (circuits)
- ✅ 车手信息 (drivers)
- ✅ 车队信息 (constructors)
- ✅ **车手积分榜** (driver standings) - 通过 Ergast API 获取
- ✅ **车队积分榜** (constructor standings) - 通过 Ergast API 获取

#### 🟡 **会话数据**（谨慎，可能触发限制）

- ⚠️ 比赛结果 (race results) - 现已改用 Ergast API
- ⚠️ 排位赛结果 (qualifying results) - 现已改用 Ergast API

## 🛠️ 推荐使用方法

### 1. 安全同步脚本（推荐）

```bash
# 只同步基础数据（包括积分榜）- 最安全
cd backend
poetry run python scripts/sync_data_safe.py --basic-only --season 2024

# 同步基础数据 + 限量会话数据（3轮比赛）
poetry run python scripts/sync_data_safe.py --season 2024 --max-rounds 3

# 同步更多轮次（需要更长时间）
poetry run python scripts/sync_data_safe.py --season 2024 --max-rounds 10
```

### 2. 完整同步脚本（谨慎使用）

```bash
# 传统脚本 - 可能遇到API限制
poetry run python scripts/sync_data.py --season 2024
```

## 📋 脚本说明

### `sync_data_safe.py` ⭐ 推荐

- **安全的数据同步脚本**
- 内置频率限制处理和重试机制
- 分阶段同步，降低 API 调用压力
- 支持仅同步基础数据模式

**参数说明：**

- `--season 2024`: 指定赛季
- `--basic-only`: 只同步基础数据（含积分榜）
- `--max-rounds 3`: 限制会话数据同步轮次
- `--cache-dir`: 指定 FastF1 缓存目录

### `sync_data.py`

- 原始的完整同步脚本
- 可能遇到 API 频率限制错误

### `init_data.py`

- 数据库初始化脚本

### `test_data_providers.py`

- 数据提供者测试脚本
- 用于验证数据获取功能

## 🔧 频率限制解决方案

我们实施了以下措施来避免 API 限制：

1. **使用 Ergast API 替代 session.load()**

   - 避免加载完整会话数据（圈速、遥测等）
   - 只获取必要的结果数据

2. **智能重试机制**

   - 检测 "500 calls/h" 错误
   - 指数退避策略 (1s, 2s, 4s...)
   - 最大重试 3 次

3. **请求间延迟**

   - 每次 API 调用后延迟 0.8 秒
   - 轮次间更长延迟 (2-3 秒)

4. **分批处理**
   - 基础数据优先
   - 会话数据限量同步
   - 支持中断和恢复

## 💡 使用建议

1. **首次使用**：先运行 `--basic-only` 模式
2. **测试环境**：使用 `--max-rounds 3` 限制数据量
3. **生产环境**：分多次运行，每次间隔几小时
4. **遇到错误**：查看日志文件 `data_sync.log`

## 📊 数据完整性

使用安全同步脚本后，你将获得：

- ✅ 完整的基础数据（赛道、车手、车队）
- ✅ 完整的积分榜数据
- ✅ 有限的比赛结果数据（根据 `--max-rounds` 设置）

这足以支持大部分 F1 网站功能，详细的圈速数据可以后续按需获取。
