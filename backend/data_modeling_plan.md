# F1 数据建模计划

## 目标

基于 FastF1 实际数据结构，重新设计数据模型并实现数据同步。

## 原则

1. **数据驱动** - 先获取数据，再设计模型
2. **渐进式** - 一次处理一个数据类型
3. **关联优先** - 先创建独立实体，再处理依赖关系
4. **范围控制** - 只同步 2023-2025 赛季数据，避免历史数据冗余

## 数据范围

### 目标赛季

- **2023 赛季** - 历史数据，用于对比分析
- **2024 赛季** - 当前赛季，完整数据
- **2025 赛季** - 最新赛季，进行中

### 数据量控制

- 避免获取 1950 年以来的所有历史数据
- 提高同步效率和性能
- 减少存储空间占用
- 专注于当前相关赛季

## 实施步骤

### Phase 1: 清理现有数据

- [ ] 清空数据库
- [ ] 删除现有模型文件
- [ ] 删除相关同步代码

### Phase 2: 基础维度表

#### 2.1 赛季数据 (Season)

1. **获取数据**

   ```python
   # 使用 fastf1.ergast 获取赛季信息，只获取目标赛季
   all_seasons = ergast.get_seasons()
   target_seasons = all_seasons[all_seasons['season'].isin([2023, 2024, 2025])]
   ```

2. **分析数据结构**

   - 字段类型和约束
   - 数据完整性
   - 业务规则

3. **设计模型**

   - 确定主键
   - 定义字段
   - 设置约束

4. **创建同步逻辑**
   - 数据获取
   - 数据转换
   - 数据库插入

#### 2.2 赛道数据 (Circuit)

1. **获取数据**

   ```python
   # 获取2025赛季的赛道数据作为示例
   circuits = ergast.get_circuits(season=2025)
   ```

2. **分析数据结构**
3. **设计模型**
4. **创建同步逻辑**

#### 2.3 车队数据 (Constructor)

1. **获取数据**

   ```python
   # 获取2025赛季的车队数据作为示例
   constructors = ergast.get_constructor_info(season=2025)
   ```

2. **分析数据结构**
3. **设计模型**
4. **创建同步逻辑**

### Phase 3: 依赖维度表

#### 3.1 车手数据 (Driver)

1. **获取数据**

   ```python
   # 获取2025赛季的车手数据作为示例
   drivers = ergast.get_driver_info(season=2025)
   ```

2. **分析数据结构**

   - 车队关联关系
   - 赛季关联关系

3. **设计模型**

   - 外键约束
   - 关联关系

4. **创建同步逻辑**
   - 车队查找/创建
   - 数据关联

#### 3.2 比赛数据 (Race)

1. **获取数据**

   ```python
   # 获取2025赛季的比赛日程
   races = fastf1.get_event_schedule(2025)
   # 或
   races = ergast.get_race_schedule(season=2025)
   ```

2. **分析数据结构**
3. **设计模型**
4. **创建同步逻辑**

### Phase 4: 事实表

#### 4.1 积分榜数据 (Standings)

1. **获取数据**

   ```python
   # 获取2025赛季的积分榜数据
   driver_standings = ergast.get_driver_standings(season=2025)
   constructor_standings = ergast.get_constructor_standings(season=2025)
   ```

2. **分析数据结构**
3. **设计模型**
4. **创建同步逻辑**

#### 4.2 比赛结果数据 (Results)

1. **获取数据**

   ```python
   # 获取2025赛季的比赛结果
   results = ergast.get_race_results(season=2025)
   ```

2. **分析数据结构**
3. **设计模型**
4. **创建同步逻辑**

## 关联关系处理策略

### 1. 外键约束设计

```sql
-- 车手表
CREATE TABLE drivers (
    id SERIAL PRIMARY KEY,
    driver_id VARCHAR(50) UNIQUE NOT NULL,
    constructor_id INTEGER REFERENCES constructors(id),
    season_id INTEGER REFERENCES seasons(id)
);

-- 比赛表
CREATE TABLE races (
    id SERIAL PRIMARY KEY,
    circuit_id INTEGER REFERENCES circuits(id),
    season_id INTEGER REFERENCES seasons(id)
);
```

### 2. 数据同步顺序

```
1. seasons (独立) - 2023, 2024, 2025
2. circuits (独立)
3. constructors (独立)
4. drivers (依赖 constructors, seasons)
5. races (依赖 circuits, seasons)
6. results (依赖 drivers, constructors, races)
7. standings (依赖 drivers, constructors)
```

### 3. 关联查找策略

```python
def get_or_create_constructor(db, constructor_id, season_id):
    """获取或创建车队"""
    constructor = db.query(Constructor).filter_by(
        constructor_id=constructor_id,
        season_id=season_id
    ).first()

    if not constructor:
        # 创建新车队
        constructor = Constructor(...)
        db.add(constructor)
        db.commit()

    return constructor
```

## 测试策略

### 1. 单元测试

- 数据获取测试
- 数据转换测试
- 模型验证测试

### 2. 集成测试

- 完整同步流程测试
- 关联关系测试
- 数据完整性测试

### 3. 数据验证

- 数据量验证
- 关联关系验证
- 业务规则验证

## 工具和脚本

### 1. 数据探索脚本

```python
def explore_data_structure(data, name):
    """探索数据结构"""
    print(f"=== {name} 数据结构 ===")
    print(f"数据类型: {type(data)}")
    print(f"数据形状: {data.shape}")
    print(f"列名: {list(data.columns)}")
    print(f"示例数据:")
    print(data.head())
    print(f"数据类型:")
    print(data.dtypes)
```

### 2. 模型生成脚本

```python
def generate_model_from_data(data, table_name):
    """根据数据生成模型"""
    # 分析数据类型
    # 生成 SQLAlchemy 模型
    # 生成 Pydantic 模式
```

### 3. 同步测试脚本

```python
def test_sync_workflow():
    """测试完整同步流程"""
    # 1. 获取数据
    # 2. 转换数据
    # 3. 同步到数据库
    # 4. 验证结果
```

## 预期成果

1. **清晰的数据模型** - 基于实际数据结构
2. **可靠的同步逻辑** - 处理所有边界情况
3. **完整的测试覆盖** - 确保数据质量
4. **可维护的代码** - 模块化和文档化
5. **高效的数据范围** - 只同步相关赛季数据

## 风险评估

1. **数据源变化** - FastF1 API 可能更新
2. **关联复杂性** - 多表关联可能复杂
3. **性能问题** - 大量数据同步可能慢

## 缓解措施

1. **版本控制** - 记录数据源版本
2. **渐进式开发** - 一次处理一个表
3. **性能优化** - 批量操作和索引
4. **数据范围控制** - 只同步目标赛季数据

## 数据范围控制策略

### 1. 赛季过滤

```python
# 定义目标赛季
TARGET_SEASONS = [2023, 2024, 2025]

# 过滤赛季数据
target_seasons = all_seasons[all_seasons['season'].isin(TARGET_SEASONS)]
```

### 2. 性能优化

- 避免获取不必要的历史数据
- 减少网络请求和数据处理时间
- 降低存储空间需求
- 提高同步效率

### 3. 业务价值

- 专注于当前相关赛季
- 提供更有价值的分析数据
- 减少数据噪音
- 提高用户体验
