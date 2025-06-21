#!/usr/bin/env python3
"""
FastF1 数据探索工具
用于分析 FastF1 的实际数据结构，为数据建模提供依据
结果保存为 Markdown 文件
"""

import sys
import os
import logging
import pandas as pd
from datetime import datetime
from io import StringIO

# 添加项目根目录到 Python 路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# 定义我们需要的赛季范围
TARGET_SEASONS = [2023, 2024, 2025]

# 用于捕获输出的 StringIO 对象
output_buffer = StringIO()

def log_and_capture(message, level="INFO"):
    """记录日志并捕获输出"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    formatted_message = f"[{timestamp}] {level}: {message}"
    
    # 输出到控制台
    print(formatted_message)
    
    # 同时写入到 Markdown 缓冲区
    output_buffer.write(formatted_message + "\n")
    
    # 记录到日志
    if level == "ERROR":
        logger.error(message)
    elif level == "WARNING":
        logger.warning(message)
    else:
        logger.info(message)

def explore_data_structure(data, name):
    """探索数据结构"""
    log_and_capture(f"\n{'='*60}")
    log_and_capture(f"📊 {name} 数据结构分析")
    log_and_capture(f"{'='*60}")
    
    try:
        # 检查是否是 FastF1 的 ErgastMultiResponse 类型
        if hasattr(data, '__class__') and 'ErgastMultiResponse' in str(data.__class__):
            log_and_capture(f"📋 数据类型: ErgastMultiResponse")
            
            # 显示描述信息
            if hasattr(data, 'description') and not data.description.empty:
                log_and_capture(f"📝 描述信息 (共{len(data.description)}个比赛):")
                log_and_capture(f"```")
                log_and_capture(data.description.to_string())
                log_and_capture(f"```")
            
            # 显示内容数据
            if hasattr(data, 'content') and data.content:
                log_and_capture(f"📏 内容数量: {len(data.content)} 个数据集")
                
                for idx, df in enumerate(data.content):
                    log_and_capture(f"\n📊 第 {idx + 1} 个数据集:")
                    log_and_capture(f"   数据类型: DataFrame")
                    log_and_capture(f"   数据形状: {df.shape}")
                    log_and_capture(f"   列名: {list(df.columns)}")
                    
                    # 显示对应的描述信息
                    if hasattr(data, 'description') and idx < len(data.description):
                        race_info = data.description.iloc[idx]
                        log_and_capture(f"   对应比赛: 第{race_info.get('round', 'N/A')}轮 - {race_info.get('raceName', 'N/A')}")
                    
                    print(f"\n   数据类型:")
                    for col, dtype in df.dtypes.items():
                        log_and_capture(f"     {col}: {dtype}")
                    
                    if not df.empty:
                        log_and_capture(f"\n   示例数据 (前3行):")
                        log_and_capture(f"```")
                        log_and_capture(df.head(3).to_string())
                        log_and_capture(f"```")
                        
                        log_and_capture(f"\n   数据统计:")
                        log_and_capture(f"   非空值统计:")
                        for col in df.columns:
                            try:
                                non_null_count = df[col].notna().sum()
                                null_count = df[col].isna().sum()
                                total_count = len(df)
                                if total_count > 0:
                                    percentage = (non_null_count / total_count) * 100
                                    log_and_capture(f"     {col}: {non_null_count}/{total_count} ({percentage:.1f}%) 非空, {null_count} 空值")
                                else:
                                    log_and_capture(f"     {col}: 0/0 (0.0%) 非空, 0 空值")
                            except Exception as e:
                                log_and_capture(f"     {col}: 统计失败 - {e}", "ERROR")
                        
                        # 检查唯一值
                        log_and_capture(f"\n   唯一值统计:")
                        for col in df.columns:
                            try:
                                unique_count = df[col].nunique()
                                log_and_capture(f"     {col}: {unique_count} 个唯一值")
                                if unique_count <= 10 and unique_count > 0:
                                    unique_values = df[col].dropna().unique()
                                    # 确保值是可哈希的
                                    safe_values = []
                                    for val in unique_values:
                                        try:
                                            hash(val)
                                            safe_values.append(str(val))
                                        except:
                                            safe_values.append(f"<不可哈希类型: {type(val).__name__}>")
                                    log_and_capture(f"       唯一值: {safe_values}")
                            except Exception as e:
                                log_and_capture(f"     {col}: 唯一值统计失败 - {e}", "ERROR")
                        
                        # 检查数值列的统计信息
                        try:
                            numeric_cols = df.select_dtypes(include=['number']).columns
                            if len(numeric_cols) > 0:
                                log_and_capture(f"\n   数值列统计:")
                                log_and_capture(f"```")
                                log_and_capture(df[numeric_cols].describe().to_string())
                                log_and_capture(f"```")
                        except Exception as e:
                            log_and_capture(f"   数值列统计失败: {e}", "ERROR")
                    else:
                        log_and_capture(f"   数据为空")
            else:
                log_and_capture("❌ 没有内容数据", "ERROR")
        
        elif isinstance(data, pd.DataFrame):
            log_and_capture(f"📋 数据类型: DataFrame")
            log_and_capture(f"📏 数据形状: {data.shape}")
            log_and_capture(f"📝 列名: {list(data.columns)}")
            
            log_and_capture(f"\n📊 数据类型:")
            for col, dtype in data.dtypes.items():
                log_and_capture(f"   {col}: {dtype}")
            
            if not data.empty:
                log_and_capture(f"\n📋 示例数据 (前3行):")
                log_and_capture(f"```")
                log_and_capture(data.head(3).to_string())
                log_and_capture(f"```")
                
                log_and_capture(f"\n🔍 数据统计:")
                log_and_capture(f"   非空值统计:")
                for col in data.columns:
                    try:
                        non_null_count = data[col].notna().sum()
                        null_count = data[col].isna().sum()
                        total_count = len(data)
                        if total_count > 0:
                            percentage = (non_null_count / total_count) * 100
                            log_and_capture(f"     {col}: {non_null_count}/{total_count} ({percentage:.1f}%) 非空, {null_count} 空值")
                        else:
                            log_and_capture(f"     {col}: 0/0 (0.0%) 非空, 0 空值")
                    except Exception as e:
                        log_and_capture(f"     {col}: 统计失败 - {e}", "ERROR")
                
                # 检查唯一值
                log_and_capture(f"\n🎯 唯一值统计:")
                for col in data.columns:
                    try:
                        unique_count = data[col].nunique()
                        log_and_capture(f"     {col}: {unique_count} 个唯一值")
                        if unique_count <= 10 and unique_count > 0:
                            unique_values = data[col].dropna().unique()
                            # 确保值是可哈希的
                            safe_values = []
                            for val in unique_values:
                                try:
                                    hash(val)
                                    safe_values.append(str(val))
                                except:
                                    safe_values.append(f"<不可哈希类型: {type(val).__name__}>")
                            log_and_capture(f"       唯一值: {safe_values}")
                    except Exception as e:
                        log_and_capture(f"     {col}: 唯一值统计失败 - {e}", "ERROR")
                
                # 检查数值列的统计信息
                try:
                    numeric_cols = data.select_dtypes(include=['number']).columns
                    if len(numeric_cols) > 0:
                        log_and_capture(f"\n📈 数值列统计:")
                        log_and_capture(f"```")
                        log_and_capture(data[numeric_cols].describe().to_string())
                        log_and_capture(f"```")
                except Exception as e:
                    log_and_capture(f"   数值列统计失败: {e}", "ERROR")
            else:
                log_and_capture(f"   数据为空")
        
        else:
            log_and_capture(f"📋 数据类型: {type(data)}")
            log_and_capture(f"📝 数据内容: {data}")
            
    except Exception as e:
        log_and_capture(f"❌ 数据结构分析失败: {e}", "ERROR")
        import traceback
        error_trace = traceback.format_exc()
        log_and_capture(f"错误详情:\n{error_trace}", "ERROR")

def explore_fastf1_data():
    """探索 FastF1 数据"""
    try:
        import fastf1
        from fastf1.ergast import Ergast
        
        log_and_capture("🔍 开始探索 FastF1 数据结构...")
        log_and_capture(f"🎯 目标赛季: {TARGET_SEASONS}")
        
        # 启用缓存
        fastf1.Cache.enable_cache('./cache')
        ergast = Ergast()
        
        # 1. 探索赛季数据 (只获取目标赛季)
        log_and_capture("📅 1. 探索赛季数据...")
        try:
            # 获取所有赛季，然后过滤出我们需要的
            all_seasons = ergast.get_seasons()
            target_seasons = all_seasons[all_seasons['season'].isin(TARGET_SEASONS)]
            
            log_and_capture(f"\n🎯 目标赛季数据:")
            log_and_capture(f"📏 数据形状: {target_seasons.shape}")
            log_and_capture(f"📝 列名: {list(target_seasons.columns)}")
            log_and_capture(f"📋 目标赛季: {list(target_seasons['season'].values)}")
            
            explore_data_structure(target_seasons, "目标赛季数据 (Target Seasons)")
        except Exception as e:
            log_and_capture(f"❌ 获取赛季数据失败: {e}", "ERROR")
        
        # 2. 探索赛道数据 (使用2025赛季作为示例)
        log_and_capture("🏁 2. 探索赛道数据...")
        try:
            circuits = ergast.get_circuits(season=2025)
            explore_data_structure(circuits, "赛道数据 (Circuits - 2025)")
        except Exception as e:
            log_and_capture(f"❌ 获取赛道数据失败: {e}", "ERROR")
        
        # 3. 探索车队数据 (使用2025赛季作为示例)
        log_and_capture("🏎️ 3. 探索车队数据...")
        try:
            constructors = ergast.get_constructor_info(season=2025)
            explore_data_structure(constructors, "车队数据 (Constructors - 2025)")
        except Exception as e:
            log_and_capture(f"❌ 获取车队数据失败: {e}", "ERROR")
        
        # 4. 探索车手数据 (使用2025赛季作为示例)
        log_and_capture("👤 4. 探索车手数据...")
        try:
            drivers = ergast.get_driver_info(season=2025)
            explore_data_structure(drivers, "车手数据 (Drivers - 2025)")
        except Exception as e:
            log_and_capture(f"❌ 获取车手数据失败: {e}", "ERROR")
        
        # 5. 探索比赛日程数据 (使用2025赛季作为示例)
        log_and_capture("🏁 5. 探索比赛日程数据...")
        try:
            # FastF1 方式
            races_fastf1 = fastf1.get_event_schedule(2025)
            explore_data_structure(races_fastf1, "比赛日程数据 (FastF1 - 2025)")
            
            # Ergast 方式
            races_ergast = ergast.get_race_schedule(season=2025)
            explore_data_structure(races_ergast, "比赛日程数据 (Ergast - 2025)")
        except Exception as e:
            log_and_capture(f"❌ 获取比赛日程数据失败: {e}", "ERROR")
        
        # 6. 探索积分榜数据 (使用2025赛季作为示例)
        log_and_capture("🏆 6. 探索积分榜数据...")
        try:
            driver_standings = ergast.get_driver_standings(season=2025)
            explore_data_structure(driver_standings, "车手积分榜数据 (Driver Standings - 2025)")
            
            constructor_standings = ergast.get_constructor_standings(season=2025)
            explore_data_structure(constructor_standings, "车队积分榜数据 (Constructor Standings - 2025)")
        except Exception as e:
            log_and_capture(f"❌ 获取积分榜数据失败: {e}", "ERROR")
        
        # 7. 探索比赛结果数据 (使用2025赛季作为示例)
        log_and_capture("🏁 7. 探索比赛结果数据...")
        try:
            results = ergast.get_race_results(season=2025)
            explore_data_structure(results, "比赛结果数据 (Race Results - 2025)")
        except Exception as e:
            log_and_capture(f"❌ 获取比赛结果数据失败: {e}", "ERROR")
        
        # 8. 探索排位赛结果数据 (使用2025赛季作为示例)
        log_and_capture("🏁 8. 探索排位赛结果数据...")
        try:
            qualifying_results = ergast.get_qualifying_results(season=2025)
            explore_data_structure(qualifying_results, "排位赛结果数据 (Qualifying Results - 2025)")
        except Exception as e:
            log_and_capture(f"❌ 获取排位赛结果数据失败: {e}", "ERROR")
        
        # 9. 探索冲刺赛结果数据 (使用2025赛季作为示例)
        log_and_capture("🏁 9. 探索冲刺赛结果数据...")
        try:
            sprint_results = ergast.get_sprint_results(season=2025)
            explore_data_structure(sprint_results, "冲刺赛结果数据 (Sprint Results - 2025)")
        except Exception as e:
            log_and_capture(f"❌ 获取冲刺赛结果数据失败: {e}", "ERROR")
        
        log_and_capture("✅ 数据探索完成")
        
    except Exception as e:
        log_and_capture(f"❌ 数据探索失败: {e}", "ERROR")
        import traceback
        traceback.print_exc()

def generate_model_suggestions():
    """生成模型建议"""
    log_and_capture(f"\n{'='*60}")
    log_and_capture(f"💡 数据建模建议")
    log_and_capture(f"{'='*60}")
    
    log_and_capture(f"""
基于 FastF1 数据结构分析，建议采用以下建模策略：

## 1. 基础维度表 (独立实体)

### Season (赛季)
- 主键: year (INTEGER)
- 字段: name, description, start_date, end_date
- 特点: 独立存在，其他表的基础
- 范围: 2023-2025赛季

### Circuit (赛道)
- 主键: circuit_id (VARCHAR)
- 字段: name, location, country, length, corners
- 特点: 独立存在，可跨赛季使用

### Constructor (车队)
- 主键: constructor_id (VARCHAR)
- 字段: name, nationality, base, power_unit
- 特点: 独立存在，可跨赛季使用

## 2. 依赖维度表 (需要关联)

### Driver (车手)
- 主键: driver_id (VARCHAR)
- 外键: constructor_id, season_id
- 字段: first_name, last_name, nationality, number
- 特点: 依赖车队和赛季

### Race (比赛)
- 主键: race_id (VARCHAR)
- 外键: circuit_id, season_id
- 字段: name, round_number, race_date, status
- 特点: 依赖赛道和赛季

## 3. 事实表 (业务事件)

### Result (比赛结果)
- 主键: id (AUTO_INCREMENT)
- 外键: race_id, driver_id, constructor_id
- 字段: position, points, status, laps_completed
- 特点: 记录具体比赛结果

### QualifyingResult (排位赛结果)
- 主键: id (AUTO_INCREMENT)
- 外键: race_id, driver_id, constructor_id
- 字段: position, q1_time, q2_time, q3_time
- 特点: 记录排位赛结果

### SprintResult (冲刺赛结果)
- 主键: id (AUTO_INCREMENT)
- 外键: race_id, driver_id, constructor_id
- 字段: position, points, status, laps_completed
- 特点: 记录冲刺赛结果

### DriverStanding (车手积分榜)
- 主键: id (AUTO_INCREMENT)
- 外键: driver_id, constructor_id
- 字段: season, position, points, wins
- 特点: 记录积分榜状态

### ConstructorStanding (车队积分榜)
- 主键: id (AUTO_INCREMENT)
- 外键: constructor_id
- 字段: season, position, points, wins
- 特点: 记录车队积分榜状态

## 4. 同步顺序建议

1. Season (独立) - 2023, 2024, 2025
2. Circuit (独立)
3. Constructor (独立)
4. Driver (依赖 Constructor, Season)
5. Race (依赖 Circuit, Season)
6. Result (依赖 Driver, Constructor, Race)
7. QualifyingResult (依赖 Driver, Constructor, Race)
8. SprintResult (依赖 Driver, Constructor, Race)
9. Standings (依赖 Driver, Constructor)

## 5. 关键设计原则

- 使用自然键作为业务标识 (driver_id, constructor_id)
- 使用自增ID作为物理主键
- 建立适当的外键约束
- 考虑数据的历史性和时效性
- 优化查询性能的索引设计
- 处理 ErgastMultiResponse 的复杂数据结构
- 只同步目标赛季数据 (2023-2025)，避免历史数据冗余

## 6. 数据范围控制

- 赛季范围: 2023-2025
- 避免获取过多历史数据
- 提高同步效率和性能
- 减少存储空间占用
""")

def main():
    """主函数"""
    log_and_capture("🚀 开始 FastF1 数据探索...")
    log_and_capture(f"🎯 目标赛季: {TARGET_SEASONS}")
    
    # 探索数据结构
    explore_fastf1_data()
    
    # 生成建模建议
    generate_model_suggestions()
    
    log_and_capture("✅ 数据探索和建议生成完成")
    
    # 保存结果到 Markdown 文件
    try:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"fastf1_data_exploration_{timestamp}.md"
        
        # 创建 Markdown 文件头部
        markdown_content = f"""# FastF1 数据结构探索报告

生成时间: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
目标赛季: {TARGET_SEASONS}

## 探索结果

"""
        
        # 添加捕获的输出内容
        markdown_content += output_buffer.getvalue()
        
        # 写入文件
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(markdown_content)
        
        log_and_capture(f"📄 结果已保存到: {filename}")
        
    except Exception as e:
        log_and_capture(f"❌ 保存 Markdown 文件失败: {e}", "ERROR")

if __name__ == "__main__":
    main() 