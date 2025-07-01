# FastF1 数据结构对比分析

## 概述

本文档对比 FastF1 Ergast API 返回的实际数据结构与当前数据模型定义之间的差异。

## 1. 赛道数据 (Circuit)

### FastF1 实际数据结构

```csv
circuitId,circuitUrl,circuitName,lat,long,locality,country
albert_park,https://en.wikipedia.org/wiki/Albert_Park_Circuit,Albert Park Grand Prix Circuit,-37.8497,144.968,Melbourne,Australia
```

### 当前模型定义

```python
class Circuit(Base):
    circuit_id = Column(String(50), primary_key=True)  # ✅ 匹配 circuitId
    circuit_url = Column(String(500), nullable=True)   # ✅ 匹配 circuitUrl
    circuit_name = Column(String(200), nullable=False) # ✅ 匹配 circuitName
    lat = Column(Float, nullable=True)                 # ✅ 匹配 lat
    long = Column(Float, nullable=True)                # ✅ 匹配 long
    locality = Column(String(100), nullable=True)     # ✅ 匹配 locality
    country = Column(String(100), nullable=True)      # ✅ 匹配 country

    # 额外字段（FastF1中不存在）
    length = Column(Float, nullable=True)
    corners = Column(Integer, nullable=True)
    # ... 其他额外字段
```

**结论**: ✅ 基本匹配，额外字段无影响

## 2. 车手数据 (Driver)

### FastF1 实际数据结构（从积分榜数据可见）

```csv
driverId,driverNumber,driverCode,driverUrl,givenName,familyName,dateOfBirth,driverNationality
piastri,81,PIA,http://en.wikipedia.org/wiki/Oscar_Piastri,Oscar,Piastri,2001-04-06,Australian
```

### 当前模型定义

```python
class Driver(Base):
    driver_id = Column(String(50), primary_key=True)           # ✅ 匹配 driverId
    number = Column("driver_number", Integer, nullable=True)   # ⚠️ 字段名不匹配
    code = Column("driver_code", String(10), nullable=True)    # ⚠️ 字段名不匹配
    driver_url = Column(String(500), nullable=True)           # ✅ 匹配 driverUrl
    forename = Column("given_name", String(100), nullable=False)  # ⚠️ 字段名不匹配
    surname = Column("family_name", String(100), nullable=False) # ⚠️ 字段名不匹配
    date_of_birth = Column(Date, nullable=True)               # ✅ 匹配 dateOfBirth
    nationality = Column("driver_nationality", String(100))   # ⚠️ 字段名不匹配
```

**问题**: 使用了 Column 别名，但实际列名与 FastF1 字段名不匹配

## 3. 车队数据 (Constructor)

### FastF1 实际数据结构

```csv
constructorId,constructorUrl,constructorName,constructorNationality
mclaren,http://en.wikipedia.org/wiki/McLaren,McLaren,British
```

### 当前模型定义

```python
class Constructor(Base):
    constructor_id = Column(String(50), primary_key=True)         # ✅ 匹配 constructorId
    constructor_url = Column(String(500), nullable=True)          # ✅ 匹配 constructorUrl
    name = Column("constructor_name", String(200), nullable=False) # ⚠️ 字段名不匹配
    nationality = Column("constructor_nationality", String(100))   # ⚠️ 字段名不匹配

    # ❌ 重大问题：不应该有 season_id 外键
    season_id = Column(Integer, ForeignKey("seasons.id"), nullable=False)

    # 额外字段（FastF1中不存在）
    base = Column(String(200), nullable=True)
    # ... 其他额外字段
```

**重大问题**:

1. 车队是跨赛季的实体，不应该绑定到特定赛季
2. 字段名使用别名但与 FastF1 不匹配

## 4. 排位赛结果 (QualifyingResult)

### FastF1 实际数据结构（根据文档）

```
ErgastMultiResponse.content:
number, position, Q1, Q2, Q3, driverId, driverNumber, driverCode,
driverUrl, givenName, familyName, dateOfBirth, driverNationality,
constructorId, constructorUrl, constructorName, constructorNationality
```

### 当前模型定义

```python
class QualifyingResult(Base):
    number = Column(Integer, nullable=True)           # ✅ 匹配 number
    position = Column(Integer, nullable=True)         # ✅ 匹配 position
    q1_time = Column(String(100), nullable=True)      # ❌ 应该是 Q1
    q2_time = Column(String(100), nullable=True)      # ❌ 应该是 Q2
    q3_time = Column(String(100), nullable=True)      # ❌ 应该是 Q3
```

**问题**: Q1/Q2/Q3 字段名不匹配

## 5. 比赛结果 (Result)

### FastF1 实际数据结构（根据文档）

```
ErgastMultiResponse.content:
number, position, positionText, points, grid, laps, status,
totalRaceTimeMillis, totalRaceTime, fastestLapRank, fastestLapNumber,
fastestLapTime, fastestLapAvgSpeedUnits, fastestLapAvgSpeed
```

### 当前模型定义

```python
class Result(Base):
    number = Column(Integer, nullable=True)                      # ✅ 匹配
    position = Column(Integer, nullable=True)                    # ✅ 匹配
    position_text = Column(String(10), nullable=True)           # ✅ 匹配 positionText
    points = Column(Float, nullable=True)                       # ✅ 匹配
    grid = Column(Integer, nullable=True)                       # ✅ 匹配
    laps = Column(Integer, nullable=True)                       # ✅ 匹配
    status = Column(String(50), nullable=True)                  # ✅ 匹配
    total_race_time_millis = Column(BigInteger, nullable=True)   # ✅ 匹配 totalRaceTimeMillis
    total_race_time = Column(String(100), nullable=True)        # ✅ 匹配 totalRaceTime
    fastest_lap_rank = Column(Integer, nullable=True)           # ✅ 匹配 fastestLapRank
    fastest_lap_number = Column(Integer, nullable=True)         # ✅ 匹配 fastestLapNumber
    fastest_lap_time = Column(String(100), nullable=True)       # ✅ 匹配 fastestLapTime

    # ❌ 缺少字段
    # fastest_lap_avg_speed_units = Column(String(10), nullable=True)
    # fastest_lap_avg_speed = Column(Float, nullable=True)
```

**问题**: 缺少平均速度相关字段

## 6. 积分榜数据 (Standings)

### FastF1 实际数据结构

```csv
# 车手积分榜
position,positionText,points,wins,driverId,constructorIds,constructorNames
1,1,216.0,5,piastri,"['mclaren']","['McLaren']"

# 车队积分榜
position,positionText,points,wins,constructorId,constructorName
1,1,417.0,8,mclaren,McLaren
```

### 当前模型定义

```python
class DriverStanding(Base):
    position = Column(Integer, nullable=True)         # ✅ 匹配
    position_text = Column(String(10), nullable=True) # ✅ 匹配 positionText
    points = Column(Float, default=0, nullable=False) # ✅ 匹配
    wins = Column(Integer, default=0, nullable=False) # ✅ 匹配

    # ❌ 问题：车手可能在一个赛季为多个车队效力
    constructor_id = Column(String(50), ForeignKey(...), nullable=False)
```

**重大问题**:

1. 车手在一个赛季可能为多个车队效力（如 Lawson 数据显示）
2. 需要支持多对多关系

## 7. 比赛数据 (Race)

### FastF1 ErgastMultiResponse.description 结构

```
season, round, raceUrl, raceName, raceDate, raceTime,
circuitId, circuitUrl, circuitName, lat, long, locality, country
```

### 当前模型定义

```python
class Race(Base):
    round_number = Column(Integer, nullable=False)  # ✅ 对应 round
    # ❌ 缺少很多字段
    # race_url, race_name, race_date, race_time 等
```

**问题**: 字段名不匹配，缺少重要字段

## 主要问题总结

### 🔴 关键问题

1. **Constructor 模型设计错误**: 不应该有 `season_id` 外键
2. **车手积分榜关系错误**: 需要支持车手在一个赛季为多个车队效力
3. **字段名不匹配**: 使用了别名但与 FastF1 字段名不一致

### 🟡 次要问题

1. **QualifyingResult**: Q1/Q2/Q3 字段名需要调整
2. **Result**: 缺少平均速度字段
3. **Race**: 需要添加更多 Ergast 数据字段

### ✅ 正确设计

1. **Circuit 模型**: 基本正确，额外字段无影响
2. **Sprint 和 Result**: 大部分字段匹配良好

## 建议修复方案

1. **重新设计 Constructor 模型**: 移除 `season_id`，通过 `DriverSeason` 关联
2. **修正字段名**: 统一使用 FastF1 的字段名
3. **增强 DriverStanding**: 支持多车队关系
4. **完善 Race 模型**: 添加 Ergast 描述字段
5. **添加缺失字段**: 补充平均速度等字段
