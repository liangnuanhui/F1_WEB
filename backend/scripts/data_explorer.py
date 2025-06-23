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
from pathlib import Path

# 添加项目根目录到 Python 路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

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
                log_and_capture("❌ 数据为空")
        
        else:
            log_and_capture(f"📋 数据类型: {type(data).__name__}")
            log_and_capture(f"📏 数据长度: {len(data) if hasattr(data, '__len__') else 'N/A'}")
            
            # 尝试转换为 DataFrame
            try:
                if hasattr(data, 'to_dataframe'):
                    df = data.to_dataframe()
                    log_and_capture(f"✅ 成功转换为 DataFrame")
                    explore_data_structure(df, f"{name} (转换后)")
                else:
                    log_and_capture(f"❌ 无法转换为 DataFrame")
            except Exception as e:
                log_and_capture(f"❌ 转换失败: {e}", "ERROR")
    
    except Exception as e:
        log_and_capture(f"❌ 探索数据结构失败: {e}", "ERROR")

def explore_fastf1_data():
    """探索 FastF1 数据"""
    log_and_capture("🚀 开始探索 FastF1 数据结构")
    log_and_capture("="*80)
    
    try:
        import fastf1
        
        for season in TARGET_SEASONS:
            log_and_capture(f"\n🏆 探索 {season} 赛季数据")
            log_and_capture("-"*40)
            
            try:
                # 1. 探索比赛日程
                log_and_capture(f"📅 获取 {season} 赛季比赛日程...")
                schedule = fastf1.get_event_schedule(season)
                explore_data_structure(schedule, f"{season}赛季比赛日程")
                
                # 2. 探索车手信息
                log_and_capture(f"👨‍🏁 获取 {season} 赛季车手信息...")
                drivers = fastf1.get_driver_info(season)
                explore_data_structure(drivers, f"{season}赛季车手信息")
                
                # 3. 探索车队信息
                log_and_capture(f"🏎️ 获取 {season} 赛季车队信息...")
                constructors = fastf1.get_constructor_info(season)
                explore_data_structure(constructors, f"{season}赛季车队信息")
                
                # 4. 探索积分榜
                log_and_capture(f"🏆 获取 {season} 赛季积分榜...")
                standings = fastf1.get_driver_standings(season)
                explore_data_structure(standings, f"{season}赛季积分榜")
                
                # 5. 探索比赛结果
                log_and_capture(f"🏁 获取 {season} 赛季比赛结果...")
                results = fastf1.get_race_results(season)
                explore_data_structure(results, f"{season}赛季比赛结果")
                
                # 6. 探索排位赛结果
                log_and_capture(f"⏱️ 获取 {season} 赛季排位赛结果...")
                qualifying = fastf1.get_qualifying_results(season)
                explore_data_structure(qualifying, f"{season}赛季排位赛结果")
                
                # 7. 探索冲刺赛结果
                log_and_capture(f"⚡ 获取 {season} 赛季冲刺赛结果...")
                sprint = fastf1.get_sprint_results(season)
                explore_data_structure(sprint, f"{season}赛季冲刺赛结果")
                
            except Exception as e:
                log_and_capture(f"❌ {season} 赛季数据探索失败: {e}", "ERROR")
                continue
    
    except ImportError:
        log_and_capture("❌ FastF1 库未安装", "ERROR")
    except Exception as e:
        log_and_capture(f"❌ 探索失败: {e}", "ERROR")

def generate_model_suggestions():
    """生成数据模型建议"""
    log_and_capture("\n" + "="*80)
    log_and_capture("🏗️ 数据模型建议")
    log_and_capture("="*80)
    
    log_and_capture("""
基于 FastF1 数据结构分析，建议的数据模型设计：

## 1. 核心实体

### Season (赛季)
- id: 主键
- year: 年份
- name: 赛季名称
- start_date: 开始日期
- end_date: 结束日期
- is_current: 是否当前赛季

### Circuit (赛道)
- id: 主键
- circuit_name: 赛道名称
- country: 国家
- locality: 城市
- latitude: 纬度
- longitude: 经度

### Constructor (车队)
- id: 主键
- constructor_name: 车队名称
- constructor_nationality: 国籍
- season_id: 关联赛季

### Driver (车手)
- id: 主键
- driver_number: 车手号码
- driver_code: 车手代码
- given_name: 名
- family_name: 姓
- driver_nationality: 国籍
- date_of_birth: 出生日期

### Race (比赛)
- id: 主键
- season_id: 关联赛季
- circuit_id: 关联赛道
- round_number: 轮次
- official_event_name: 官方比赛名称
- event_date: 比赛日期
- event_format: 比赛格式 (conventional, sprint_qualifying)
- is_sprint: 是否冲刺赛

## 2. 结果实体

### Result (比赛结果)
- id: 主键
- race_id: 关联比赛
- driver_id: 关联车手
- constructor_id: 关联车队
- position: 名次
- points: 积分
- grid_position: 发车位置
- status: 状态
- finish_time: 完赛时间

### QualifyingResult (排位赛结果)
- id: 主键
- race_id: 关联比赛
- driver_id: 关联车手
- constructor_id: 关联车队
- position: 名次
- q1_time: Q1时间
- q2_time: Q2时间
- q3_time: Q3时间

### SprintResult (冲刺赛结果)
- id: 主键
- race_id: 关联比赛
- driver_id: 关联车手
- constructor_id: 关联车队
- position: 名次
- points: 积分
- grid_position: 发车位置
- status: 状态
- finish_time: 完赛时间

## 3. 关系设计

### DriverSeason (车手赛季关系)
- id: 主键
- driver_id: 关联车手
- constructor_id: 关联车队
- season_id: 关联赛季
- driver_number: 车手号码

## 4. 建议

1. 使用外键约束确保数据完整性
2. 为常用查询字段添加索引
3. 考虑使用枚举类型定义比赛格式和状态
4. 实现软删除机制保留历史数据
5. 添加创建时间和更新时间字段用于审计
""")

def main():
    """主函数"""
    log_and_capture("🎯 FastF1 数据探索工具")
    log_and_capture("="*80)
    
    # 探索数据
    explore_fastf1_data()
    
    # 生成建议
    generate_model_suggestions()
    
    # 保存结果
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = f"fastf1_data_exploration_{timestamp}.md"
    
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("# FastF1 数据结构探索报告\n\n")
            f.write(f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write(output_buffer.getvalue())
        
        log_and_capture(f"✅ 探索报告已保存到: {output_file}")
        
    except Exception as e:
        log_and_capture(f"❌ 保存报告失败: {e}", "ERROR")

if __name__ == "__main__":
    main() 