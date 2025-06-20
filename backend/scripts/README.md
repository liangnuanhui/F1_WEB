# F1 数据同步脚本使用说明

## 数据提供者架构

项目采用统一的 FastF1 数据提供者设计，根据数据类型智能选择合适的方法：

### 数据来源策略

#### 基础信息数据（使用 `fastf1.ergast`）

- **赛道信息**: `ergast.get_circuits(season=2025)`
- **车手信息**: `ergast.get_driver_info(season=2025)`
- **车队信息**: `ergast.get_constructor_info(season=2025)`
- **车手排名**: `ergast.get_driver_standings(season=2025)`
- **车队排名**: `ergast.get_constructor_standings(season=2025)`

#### 比赛安排数据（使用 `fastf1` 核心功能）

- **比赛日程**: `fastf1.get_event_schedule(2025)`
- **特定比赛**: `fastf1.get_event(2025, 'Australian Grand Prix')`

#### 比赛结果数据（使用 `fastf1.get_session`）

- **比赛结果**: `fastf1.get_session(2025, 'Australian Grand Prix', 'R')`
- **排位赛结果**: `fastf1.get_session(2025, 'Australian Grand Prix', 'Q')`
- **历史比赛结果**: `fastf1.get_session(2019, 'Monza', 'R')`
- **历史排位赛结果**: `fastf1.get_session(2019, 'Monza', 'Q')`

### 数据管理策略

#### 主赛季数据（2025 年）

- **存储方式**: 本地数据库存储
- **数据源**: 统一的 FastF1 数据提供者
- **用途**: 当前赛季的详细分析、实时数据展示

#### 历史赛季数据

- **存储方式**: 实时拉取 + 缓存
- **数据源**: 统一的 FastF1 数据提供者
- **用途**: 历史数据查询、统计分析

## 脚本使用

### 1. 历史数据同步脚本

#### `history_data.py` - 历史数据实时拉取

```bash
# 同步指定年份范围的历史数据
python scripts/history_data.py all --start-year 2020 --end-year 2024

# 同步指定赛季的历史数据
python scripts/history_data.py season --season 2023

# 使用自定义缓存目录
python scripts/history_data.py season --season 2025 --cache-dir ./cache
```

### 2. 通用数据同步脚本

#### `sync_data.py` - 通用数据同步工具

```bash
# 初始化数据库表
python scripts/sync_data.py init

# 同步当前赛季数据
python scripts/sync_data.py current

# 同步特定类型数据
python scripts/sync_data.py drivers --season 2024
python scripts/sync_data.py race_results --season 2024 --round 1
python scripts/sync_data.py qualifying_results --season 2025

# 使用自定义缓存目录
python scripts/sync_data.py current --cache-dir ./cache
```

### 3. 数据提供者测试脚本

#### `test_data_providers.py` - 数据提供者功能测试

```bash
# 基础测试
python scripts/test_data_providers.py --season 2024

# 详细测试（显示详细信息）
python scripts/test_data_providers.py --season 2025 --verbose

# 测试数据一致性
python scripts/test_data_providers.py --season 2024 --consistency

# 使用自定义缓存目录
python scripts/test_data_providers.py --season 2025 --cache-dir ./cache --verbose
```

## 数据源选择建议

### 历史数据 (1950-2024)

```bash
# 同步历史基础数据
python scripts/history_data.py all --start-year 1950 --end-year 2024
```

### 当前赛季基础数据 (2025)

```bash
# 同步当前赛季基础数据
python scripts/sync_data.py current
```

### 当前赛季详细数据 (2025)

```bash
# 同步当前赛季详细数据
python scripts/history_data.py season --season 2025
```

## 推荐使用流程

### 1. 开发阶段

```bash
# 1. 初始化数据库
python scripts/sync_data.py init

# 2. 测试数据提供者功能
python scripts/test_data_providers.py --season 2024 --verbose

# 3. 同步历史基础数据
python scripts/history_data.py all --start-year 2020 --end-year 2024

# 4. 同步当前赛季基础数据
python scripts/sync_data.py current

# 5. 测试数据一致性
python scripts/test_data_providers.py --season 2024 --consistency
```

### 2. 生产环境

```bash
# 1. 定期同步历史数据
python scripts/history_data.py all --start-year 1950 --end-year 2024

# 2. 同步当前赛季详细数据
python scripts/history_data.py season --season 2025
```

## 数据提供者优势

| 特性         | 统一 FastF1 提供者          |
| ------------ | --------------------------- |
| 历史数据覆盖 | ✅ 1950-至今                |
| 数据一致性   | ✅ 统一接口                 |
| 详细程度     | ✅ 根据数据类型选择最佳方法 |
| 遥测数据     | ✅ 支持 (通过 get_session)  |
| 实时数据     | ✅ 支持                     |
| 积分榜       | ✅ 支持                     |
| 缓存支持     | ✅ 支持                     |
| 网络依赖     | 中等                        |
| 扩展性       | ✅ 易于添加新数据源         |

## 测试脚本说明

### `test_data_providers.py`

这是主要的测试脚本，提供以下功能：

#### 基础测试

- 测试所有数据获取方法
- 验证数据格式和内容
- 检查网络连接和数据可用性

#### 详细测试 (`--verbose`)

- 显示每个方法的详细结果
- 显示数据列名和示例数据
- 按类别统计成功率

#### 数据一致性测试 (`--consistency`)

- 验证比赛安排和比赛结果的一致性
- 检查数据完整性

#### 使用示例

```bash
# 快速测试
python scripts/test_data_providers.py --season 2024

# 详细测试
python scripts/test_data_providers.py --season 2025 --verbose

# 完整测试（包括一致性检查）
python scripts/test_data_providers.py --season 2024 --verbose --consistency
```

## 错误处理

### 常见问题

1. **网络连接问题**

   ```bash
   # 检查网络连接
   curl -I http://ergast.com/api/f1/2024.json
   ```

2. **缓存问题**

   ```bash
   # 清理 FastF1 缓存
   rm -rf cache/
   ```

3. **数据库连接问题**
   ```bash
   # 检查数据库服务
   docker-compose ps
   ```

### 日志查看

```bash
# 查看详细日志
tail -f logs/app.log
```

## 扩展性

### 添加新的数据提供者

1. 继承 `DataProvider` 抽象基类
2. 实现所有抽象方法
3. 在 `DataProviderFactory` 中注册
4. 更新脚本支持新的提供者

### 示例

```python
class NewProvider(DataProvider):
    def get_seasons(self, start_year=None, end_year=None):
        # 实现获取赛季数据
        pass

    # 实现其他方法...
```

这种架构设计确保了：

- **统一性**: 所有数据都通过统一的接口获取
- **智能选择**: 根据数据类型自动选择最佳方法
- **可扩展性**: 可以轻松添加新的数据源
- **可维护性**: 统一的接口和错误处理
- **性能优化**: 根据数据类型选择最合适的方法
