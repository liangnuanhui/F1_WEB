# FastF1 数据模型实际修复方案

## 🎯 **核心问题优先级**

根据实际 FastF1 数据分析，按重要性排序：

### 🔴 **严重问题（必须修复）**

1. **Constructor.season_id 问题**

   - 车队不应该绑定到特定赛季
   - 这是最严重的架构问题

2. **Lawson 转会数据处理**
   - FastF1 数据：`"['red_bull', 'rb']"`
   - 当前模型无法处理

### 🟡 **重要问题（建议修复）**

3. **字段名不匹配**

   - Driver 模型字段使用别名但不匹配 FastF1
   - QualifyingResult 的 Q1/Q2/Q3 字段名

4. **缺少重要字段**
   - Race 模型缺少 event_name, event_format 等
   - 积分榜缺少详细信息字段

## 🔧 **安全修复策略**

### 方案 1: 渐进式修复（推荐）

**阶段 1: 只修复最关键问题**

```python
# 1. 修复 Constructor 模型
class Constructor(Base):
    constructor_id = Column(String(50), primary_key=True)
    constructor_name = Column(String(200), nullable=False)  # 去掉别名
    constructor_nationality = Column(String(100), nullable=True)  # 去掉别名
    # 移除 season_id = Column(Integer, ForeignKey("seasons.id"))
```

**阶段 2: 处理车手转会**

```python
# 2. 增强 DriverStanding 支持转会
class DriverStanding(Base):
    # 基础字段保持不变
    # 添加当前车队字段（保存最新车队）
    current_constructor_id = Column(String(50), nullable=False)
    # 可选：添加转会历史 JSON 字段
    constructor_history = Column(JSON, nullable=True)  # {"red_bull": [1,5], "rb": [6,11]}
```

**阶段 3: 修复字段名**

```python
# 3. 修复关键字段名
class QualifyingResult(Base):
    Q1 = Column(String(100), nullable=True)  # 改名
    Q2 = Column(String(100), nullable=True)  # 改名
    Q3 = Column(String(100), nullable=True)  # 改名
```

### 方案 2: 数据映射层（最安全）

保持现有模型不变，创建数据转换层：

```python
# 创建 FastF1 数据转换器
class FastF1DataMapper:
    @staticmethod
    def map_driver_data(fastf1_driver):
        return {
            'driver_id': fastf1_driver['driverId'],
            'given_name': fastf1_driver['givenName'],  # 映射到 forename
            'family_name': fastf1_driver['familyName'], # 映射到 surname
            'driver_number': fastf1_driver['driverNumber'], # 映射到 number
            # ...
        }

    @staticmethod
    def handle_driver_transfer(driver_standing_data):
        """处理 Lawson 类型的转会数据"""
        constructor_ids = driver_standing_data['constructorIds']
        if isinstance(constructor_ids, list):
            # 只保留最新车队
            return constructor_ids[-1]  # 'rb'
        return constructor_ids
```

## 📋 **立即行动建议**

### 选择 1: 最小修复（推荐）

只修复最关键的 Constructor.season_id 问题：

```sql
-- 1. 备份数据
CREATE TABLE constructors_backup AS SELECT * FROM constructors;

-- 2. 移除 season_id 约束
ALTER TABLE constructors DROP CONSTRAINT IF EXISTS constructors_season_id_fkey;
ALTER TABLE constructors DROP COLUMN IF EXISTS season_id;

-- 3. 通过 DriverSeason 表关联赛季
```

### 选择 2: 保持现状，优化数据处理

不修改模型，在数据同步时处理：

```python
def sync_driver_standings_with_transfer_handling():
    """同步车手积分榜，处理转会情况"""
    for standing in fastf1_standings:
        constructor_ids = standing['constructorIds']
        if isinstance(constructor_ids, list):
            # Lawson 情况：['red_bull', 'rb'] -> 只保存 'rb'
            current_constructor = constructor_ids[-1]
        else:
            current_constructor = constructor_ids

        # 保存到数据库
        driver_standing = DriverStanding(
            constructor_id=current_constructor,  # 只保存当前车队
            # ... 其他字段
        )
```

## 🤔 **您的选择**

请告诉我您希望采用哪种方案：

1. **方案 1**: 渐进式修复模型（需要数据库迁移）
2. **方案 2**: 保持模型不变，优化数据处理层（更安全）
3. **方案 3**: 只修复最关键的 Constructor.season_id 问题

## 🚧 **风险评估**

- **方案 1**: 中等风险，需要处理数据库迁移
- **方案 2**: 低风险，不影响现有数据库
- **方案 3**: 最低风险，只修复明确的架构错误

您倾向于哪种方案？我可以立即开始实施。
