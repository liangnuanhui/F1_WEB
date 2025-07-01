import fastf1
import pandas as pd
from datetime import datetime
import os
from fastf1.ergast import Ergast

def analyze_ergast_response(data, data_name):
    """分析 Ergast 响应对象的结构"""
    print(f"\n{'='*50}")
    print(f"分析 {data_name} 数据结构")
    print(f"{'='*50}")
    print(f"数据类型: {type(data)}")
    print(f"数据对象: {data}")
    
    # 检查是否有分页信息
    if hasattr(data, 'total_results'):
        print(f"总结果数: {data.total_results}")
        print(f"是否完整: {data.is_complete}")
    
    # 检查是否是 ErgastMultiResponse
    if hasattr(data, 'description') and hasattr(data, 'content'):
        print(f"这是 ErgastMultiResponse 对象")
        print(f"Description 类型: {type(data.description)}")
        print(f"Description 形状: {data.description.shape}")
        print(f"Description 列名: {list(data.description.columns)}")
        print(f"Content 元素数量: {len(data.content)}")
        
        print(f"\nDescription 数据预览:")
        print(data.description.head())
        
        for i, content_item in enumerate(data.content):
            print(f"\nContent[{i}] 类型: {type(content_item)}")
            print(f"Content[{i}] 形状: {content_item.shape}")
            print(f"Content[{i}] 列名: {list(content_item.columns)}")
            print(f"Content[{i}] 数据预览:")
            print(content_item.head())
            if i >= 2:  # 只显示前3个内容项
                print(f"... 还有 {len(data.content) - i - 1} 个内容项")
                break
                
        return data.description, data.content
        
    # 检查是否是 ErgastSimpleResponse 或直接的 DataFrame
    elif hasattr(data, 'shape') and hasattr(data, 'columns'):
        print(f"这是 ErgastSimpleResponse 或 DataFrame 对象")
        print(f"数据形状: {data.shape}")
        print(f"列名: {list(data.columns)}")
        print(f"数据预览:")
        print(data.head())
        
        return data, None
    else:
        print(f"未知的数据格式")
        print(f"可用属性: {dir(data)}")
        return data, None

def save_data_to_csv(data, filename, data_name):
    """保存数据到 CSV 文件"""
    try:
        data.to_csv(filename, index=False, encoding='utf-8')
        print(f"{data_name} 数据已保存到: {filename}")
    except Exception as e:
        print(f"保存 {data_name} 数据时出错: {e}")

# 创建 Ergast 对象
ergast = Ergast(result_type='pandas', auto_cast=True)

season_year = 2025

# 创建输出目录
output_dir = "fastF1_data"
os.makedirs(output_dir, exist_ok=True)

# 1 获取赛事安排数据 (使用fastf1.get_event_schedule)
print("正在获取赛事安排数据...")
schedule_data = fastf1.get_event_schedule(season_year)

# 分析数据结构
main_data, _ = analyze_ergast_response(schedule_data, "赛事安排")

# 保存数据
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
filename = f"{output_dir}/{season_year}_schedule_fastf1_{timestamp}.csv"
save_data_to_csv(main_data, filename, "赛事安排")

# 2 获取车手数据 (使用fastf1.ergast) ErgastSimpleResponse
print("\n正在获取车手数据...")
driver_data = ergast.get_driver_info(season=season_year)

# 分析数据结构
main_data, _ = analyze_ergast_response(driver_data, "车手")

# 保存数据
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
filename = f"{output_dir}/{season_year}_drivers_ergast_{timestamp}.csv"
save_data_to_csv(main_data, filename, "车手")

# 3 获取车队数据（使用fastf1.ergast）ErgastSimpleResponse
print("\n正在获取车队数据...")
constructor_data = ergast.get_constructor_info(season=season_year)

# 分析数据结构
main_data, _ = analyze_ergast_response(constructor_data, "车队")

# 保存数据
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
filename = f"{output_dir}/{season_year}_constructors_ergast_{timestamp}.csv"
save_data_to_csv(main_data, filename, "车队")

# 4 获取赛道数据（使用fastf1.ergast）ErgastSimpleResponse
print("\n正在获取赛道数据...")
circuit_data = ergast.get_circuits(season=season_year)

# 分析数据结构
main_data, _ = analyze_ergast_response(circuit_data, "赛道")

# 保存数据
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
filename = f"{output_dir}/{season_year}_circuits_ergast_{timestamp}.csv"
save_data_to_csv(main_data, filename, "赛道")

# 5 获取正赛比赛结果（使用fastf1.ergast） ErgastMultiResponse
print("\n正在获取正赛比赛结果...")
race_results = ergast.get_race_results(season=season_year)

# 分析数据结构
description_data, content_data = analyze_ergast_response(race_results, "正赛结果")

# 保存描述数据
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
filename = f"{output_dir}/{season_year}_race_results_description_{timestamp}.csv"
save_data_to_csv(description_data, filename, "正赛结果描述")

# 保存内容数据（如果有的话）
if content_data:
    for i, content_item in enumerate(content_data):
        filename = f"{output_dir}/{season_year}_race_results_content_{i}_{timestamp}.csv"
        save_data_to_csv(content_item, filename, f"正赛结果内容_{i}")

# 6 获取排位赛比赛结果（使用fastf1.ergast） ErgastMultiResponse
print("\n正在获取排位赛比赛结果...")
qualifying_results = ergast.get_qualifying_results(season=season_year)

# 分析数据结构
description_data, content_data = analyze_ergast_response(qualifying_results, "排位赛结果")

# 保存描述数据
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
filename = f"{output_dir}/{season_year}_qualifying_results_description_{timestamp}.csv"
save_data_to_csv(description_data, filename, "排位赛结果描述")

# 保存内容数据（如果有的话）
if content_data:
    for i, content_item in enumerate(content_data):
        filename = f"{output_dir}/{season_year}_qualifying_results_content_{i}_{timestamp}.csv"
        save_data_to_csv(content_item, filename, f"排位赛结果内容_{i}")

# 7 获取冲刺赛比赛结果（使用fastf1.ergast） ErgastMultiResponse
print("\n正在获取冲刺赛比赛结果...")
sprint_results = ergast.get_sprint_results(season=season_year)

# 分析数据结构
description_data, content_data = analyze_ergast_response(sprint_results, "冲刺赛结果")

# 保存描述数据
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
filename = f"{output_dir}/{season_year}_sprint_results_description_{timestamp}.csv"
save_data_to_csv(description_data, filename, "冲刺赛结果描述")

# 保存内容数据（如果有的话）
if content_data:
    for i, content_item in enumerate(content_data):
        filename = f"{output_dir}/{season_year}_sprint_results_content_{i}_{timestamp}.csv"
        save_data_to_csv(content_item, filename, f"冲刺赛结果内容_{i}")

# 8 获取车手积分榜（使用fastf1.ergast） ErgastMultiResponse
print("\n正在获取车手积分榜...")
driver_standings = ergast.get_driver_standings(season=season_year)

# 分析数据结构
description_data, content_data = analyze_ergast_response(driver_standings, "车手积分榜")

# 保存描述数据
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
filename = f"{output_dir}/{season_year}_driver_standings_description_{timestamp}.csv"
save_data_to_csv(description_data, filename, "车手积分榜描述")

# 保存内容数据（如果有的话）
if content_data:
    for i, content_item in enumerate(content_data):
        filename = f"{output_dir}/{season_year}_driver_standings_content_{i}_{timestamp}.csv"
        save_data_to_csv(content_item, filename, f"车手积分榜内容_{i}")

# 9 获取车队积分榜（使用fastf1.ergast） ErgastMultiResponse
print("\n正在获取车队积分榜...")
constructor_standings = ergast.get_constructor_standings(season=season_year)

# 分析数据结构
description_data, content_data = analyze_ergast_response(constructor_standings, "车队积分榜")

# 保存描述数据
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
filename = f"{output_dir}/{season_year}_constructor_standings_description_{timestamp}.csv"
save_data_to_csv(description_data, filename, "车队积分榜描述")

# 保存内容数据（如果有的话）
if content_data:
    for i, content_item in enumerate(content_data):
        filename = f"{output_dir}/{season_year}_constructor_standings_content_{i}_{timestamp}.csv"
        save_data_to_csv(content_item, filename, f"车队积分榜内容_{i}")

print(f"\n{'='*60}")
print("所有数据获取和分析完成！")
print(f"数据已保存到 {output_dir} 目录")
print("请查看生成的 CSV 文件来了解每个接口的数据结构")
print(f"{'='*60}")

            