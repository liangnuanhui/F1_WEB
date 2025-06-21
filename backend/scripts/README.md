# F1 数据同步脚本

本目录包含用于从 FastF1 拉取和同步 F1 数据到本地数据库的脚本。

## 🎯 2025 赛季优化

所有脚本已针对 2025 赛季进行了优化：

- ✅ 统一默认年份为 2025
- ✅ 智能频率限制处理
- ✅ 避免重复数据同步
- ✅ 详细的日志记录
- ✅ 错误恢复机制
- ✅ 数据模型自动修复

## 📁 脚本说明

### 1. `validate_2025_config.py` - 配置验证脚本 ⭐ 推荐先运行

**用途**: 验证所有 2025 赛季相关配置是否正确

```bash
# 验证所有配置
poetry run python scripts/validate_2025_config.py

# 功能:
# - 验证数据库配置
# - 验证服务配置
# - 验证脚本配置
# - 验证API端点配置
# - 测试数据提供者
```

### 2. `fix_season_model.py` - 数据模型修复脚本

**用途**: 修复 Season 模型中的字段类型问题

```bash
# 修复数据模型
poetry run python scripts/fix_season_model.py

# 功能:
# - 修复is_current字段类型
# - 设置2025赛季为当前赛季
# - 验证修复结果
```

### 3. `init_data.py` - 数据初始化脚本

**用途**: 初始化 2025 赛季的主数据

```bash
# 基本使用
poetry run python scripts/init_data.py

# 功能:
# - 自动修复数据模型
# - 同步赛季数据 (2025)
# - 同步赛道数据
# - 同步车手数据
# - 同步车队数据
# - 同步积分榜数据
# - 同步前3轮比赛结果
```

### 4. `test_data_providers.py` - 数据提供者测试脚本

**用途**: 测试 FastF1 数据提供者是否正常工作

```bash
# 基本测试
poetry run python scripts/test_data_providers.py

# 详细测试
poetry run python scripts/test_data_providers.py --verbose

# 测试数据一致性
poetry run python scripts/test_data_providers.py --consistency

# 指定缓存目录
poetry run python scripts/test_data_providers.py --cache-dir ./cache
```

### 5. `sync_data_safe.py` - 安全数据同步脚本

**用途**: 安全地同步数据，包含频率限制处理

```bash
# 同步基础数据（推荐）
poetry run python scripts/sync_data_safe.py --basic-only

# 同步所有数据（包括比赛结果）
poetry run python scripts/sync_data_safe.py

# 限制同步轮次
poetry run python scripts/sync_data_safe.py --max-rounds 2

# 指定缓存目录
poetry run python scripts/sync_data_safe.py --cache-dir ./cache
```

### 6. `sync_data.py` - 标准数据同步脚本

**用途**: 标准的数据同步，支持多种数据类型

```bash
# 初始化数据库表
poetry run python scripts/sync_data.py init

# 同步当前赛季数据
poetry run python scripts/sync_data.py current

# 同步特定数据类型
poetry run python scripts/sync_data.py drivers --season 2025
poetry run python scripts/sync_data.py constructors --season 2025
poetry run python scripts/sync_data.py circuits --season 2025
poetry run python scripts/sync_data.py race_results --season 2025 --round 1
```

### 7. `history_data.py` - 历史数据同步脚本

**用途**: 同步历史赛季数据

```bash
# 同步指定赛季
poetry run python scripts/history_data.py season --season 2024

# 同步年份范围
poetry run python scripts/history_data.py all --start-year 2020 --end-year 2024
```

## 🚀 推荐使用流程

### 首次设置（推荐）

```bash
# 1. 验证所有配置
poetry run python scripts/validate_2025_config.py

# 2. 如果验证失败，修复数据模型
poetry run python scripts/fix_season_model.py

# 3. 测试数据提供者
poetry run python scripts/test_data_providers.py --verbose

# 4. 初始化 2025 赛季数据
poetry run python scripts/init_data.py

# 5. 再次验证配置
poetry run python scripts/validate_2025_config.py
```

### 日常同步（推荐）

```bash
# 同步基础数据（安全，不会触发API限制）
poetry run python scripts/sync_data_safe.py --basic-only

# 如果需要比赛结果数据
poetry run python scripts/sync_data_safe.py --max-rounds 3
```

## ⚙️ 配置说明

### 频率限制配置

- **基础数据**: 0.5 秒延迟
- **比赛结果**: 1.0 秒延迟
- **积分榜**: 1.5 秒延迟
- **会话数据**: 2.0 秒延迟

### 缓存配置

```bash
# 启用缓存（推荐）
poetry run python scripts/init_data.py --cache-dir ./cache
```

### 日志配置

- 控制台输出 + 文件日志
- 详细的时间戳和状态信息
- 错误追踪和恢复建议

## 🔧 故障排除

### 常见问题

1. **Season 模型字段类型错误**

   ```
   解决方案: 运行 fix_season_model.py 脚本
   ```

2. **API 频率限制**

   ```
   解决方案: 使用 --basic-only 模式，或增加延迟时间
   ```

3. **网络连接问题**

   ```
   解决方案: 检查网络连接，使用缓存目录
   ```

4. **数据库连接问题**

   ```
   解决方案: 确保 PostgreSQL 服务运行，检查连接配置
   ```

5. **数据不完整**
   ```
   解决方案: 运行一致性测试，重新同步缺失的数据
   ```

### 调试模式

```bash
# 验证配置
poetry run python scripts/validate_2025_config.py

# 启用详细日志
poetry run python scripts/test_data_providers.py --verbose

# 查看日志文件
tail -f data_init_2025.log
```

## 📊 数据统计

运行初始化脚本后，会显示详细的统计信息：

- 赛季数量
- 赛道数量
- 比赛数量
- 车手数量
- 车队数量
- 比赛结果数量
- 排位赛结果数量
- 积分榜数量

## 🎯 2025 赛季特殊说明

- 所有脚本默认配置为 2025 赛季
- 使用优化的频率限制策略
- 支持智能延迟和错误恢复
- 避免重复数据同步
- 详细的进度和状态反馈
- 自动数据模型修复
- 2025 赛季数据不可用时的降级处理

## 📝 注意事项

1. **首次运行**: 建议先运行验证脚本检查环境
2. **网络环境**: 确保稳定的网络连接
3. **API 限制**: 注意 FastF1 API 的频率限制
4. **数据完整性**: 定期运行一致性测试
5. **备份**: 重要数据建议定期备份
6. **模型修复**: 如果遇到字段类型错误，运行修复脚本

## 🔄 更新日志

- **v2.1**: 添加配置验证和模型修复脚本
- **v2.0**: 针对 2025 赛季优化
- **v1.5**: 增加智能延迟和错误恢复
- **v1.0**: 基础数据同步功能
