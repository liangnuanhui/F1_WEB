#!/usr/bin/env python3
"""
FastF1 测试脚本
用于了解 FastF1 的实际用法和数据结构
"""

import fastf1
import pandas as pd
from datetime import datetime
from fastf1.ergast import Ergast


# 设置缓存
fastf1.Cache.enable_cache('cache')
ergast = Ergast()

def print_ergast_multi_response(multi_resp, name="数据"):
    """辅助函数：打印 ErgastMultiResponse 内容"""
    if hasattr(multi_resp, 'content') and hasattr(multi_resp, 'description'):
        desc = multi_resp.description
        content = multi_resp.content
        for idx, df in enumerate(content):
            print(f"{name} - 回合/分站: {desc.iloc[idx].to_dict() if not desc.empty else idx}")
            print(df.head())
    elif hasattr(multi_resp, 'content'):
        for idx, df in enumerate(multi_resp.content):
            print(f"{name} - 回合/分站: {idx}")
            print(df.head())
    else:
        print(f"{name} 不包含 content 属性")

def test_fastf1_basic():
    """测试 FastF1 基本功能"""
    print("=== FastF1 基本功能测试 ===")
    
    try:
        # 测试获取比赛日程 使用fastf1.get_event_schedule
        print("\n1. 获取 2025 赛季赛季日程 (fastf1.get_event_schedule):")
        try:
            schedule_2025 = fastf1.get_event_schedule(2025)
           
            print(f"比赛日程数据类型: {type(schedule_2025)}")
            print(f"比赛日程数据形状: {schedule_2025.shape}")
            print(f"比赛日程列名: {list(schedule_2025.columns)}")
            print("\n比赛日程信息:")
            print(schedule_2025.head())
        except Exception as e:
            print(f"获取比赛日程失败: {e}")

        # 测试获取比赛日程 - 使用 Ergast API-get_race_schedule
        print("\n2. 获取比赛2025赛季日程 (Ergast API):")
        try:
            schedule_data = ergast.get_race_schedule(season=2025)
            print(f"比赛日程数据类型: {type(schedule_data)}")
            print(f"比赛日程数据形状: {schedule_data.shape}")
            print(f"比赛日程列名: {list(schedule_data.columns)}")   
            print("\n比赛日程信息:")
            print(schedule_data.head())
        except Exception as e:
            print(f"获取比赛日程失败: {e}")
        
        # 测试获取特定比赛 - 使用fastf1.get_event
        print("\n3. 获取 2025 澳大利亚大奖赛 (fastf1.get_event):")
        try:
            aus_gp = fastf1.get_event(2025, 'Australian Grand Prix')
            print(f"比赛对象: {type(aus_gp)}")
            print(f"比赛名称: {getattr(aus_gp, 'EventName', getattr(aus_gp, 'Event', '未知'))}")
            print(f"赛道: {getattr(aus_gp, 'CircuitShortName', getattr(aus_gp, 'Circuit', '未知'))}")
            print(f"日期: {getattr(aus_gp, 'EventDate', '未知')}")
            print("\nAustralian Grand Prix比赛信息:")
            print(aus_gp)
        except Exception as e:
            print(f"获取澳大利亚大奖赛失败: {e}")

        # 测试获取比赛结果 - 使用fastf1.get_session  
        print("\n4. 获取 2025 澳大利亚大奖赛结果:(fastf1.get_session)")
        try:
            session = fastf1.get_session(2025, 'Australian Grand Prix', 'R')
            print(f"比赛对象: {type(session)}")
            print(f"Session object: {session}")
            
            session.load()
            
            if hasattr(session, 'results') and session.results is not None and not session.results.empty:
                print(f"结果数据类型: {type(session.results)}")
                print(f"结果数据形状: {session.results.shape}")
                print(f"结果列名: {list(session.results.columns)}")
                print("\n前5名结果:")
                print(session.results.head())
            else:
                print("没有找到比赛结果")   
        except Exception as e:
            print(f"获取比赛结果失败: {e}")
        
        # 测试获取比赛结果 - 使用Ergast API-get_race_results
        print("\n5. 获取比赛结果 Australian Grand Prix (Ergast API):")
        try:
            results_data = ergast.get_race_results(season=2025, round=1)
            print(f"比赛结果数据类型: {type(results_data)}")
            print("\n比赛结果信息:")
            print_ergast_multi_response(results_data, "比赛结果")
        except Exception as e:
            print(f"获取比赛结果失败: {e}")

        # 测试获取赛道信息 - 使用 Ergast API-get_circuits
        print("\n6. 获取赛道信息 (Ergast API):")
        try:
            # 使用 fetch_season 获取赛道信息
            season_data = ergast.get_circuits(season=2025)
            print(f"赛道数据类型: {type(season_data)}")
            print(f"赛道数据形状: {season_data.shape}")
            print(f"赛道列名: {list(season_data.columns)}")
            print("\n赛道信息:")
            print(season_data.head())
        except Exception as e:
            print(f"获取赛道信息失败: {e}")
        

        # 测试获取排位赛成绩 - 使用 Ergast API-get_qualifying_results
        print("\n9. 获取排位赛成绩 Australian Grand Prix (Ergast API):")
        try:
            qualifying_data = ergast.get_qualifying_results(season=2025, round=1)
            print(f"排位赛成绩数据类型: {type(qualifying_data)}")
            print("\n排位赛成绩信息:")
            print_ergast_multi_response(qualifying_data, "排位赛成绩")
        except Exception as e:
            print(f"获取排位赛成绩失败: {e}")

        # 测试获取冲刺赛成绩 - 使用 Ergast API-get_sprint_results
        print("\n7. 获取冲刺赛成绩 (Ergast API):")
        try:
            sprint_data = ergast.get_sprint_results(season=2025,round=2)
            print(f"冲刺赛成绩数据类型: {type(sprint_data)}")
            print("\n冲刺赛成绩信息:")
            print_ergast_multi_response(sprint_data, "冲刺赛成绩")  
        except Exception as e:
            print(f"获取冲刺赛成绩失败: {e}")

         # 测试获取车手信息 - 使用 Ergast API-get_driver_info
        print("\n7. 获取车手信息 (Ergast API):")
        try:
            drivers_data = ergast.get_driver_info(season=2025)
            print(f"车手数据类型: {type(drivers_data)}")
            print(f"车手数据形状: {drivers_data.shape}")
            print(f"车手列名: {list(drivers_data.columns)}")
            print("\n车手信息:")
            print(drivers_data.head())
        except Exception as e:
            print(f"获取车手信息失败: {e}")
        
        # 测试获取车队信息 - 使用 Ergast API-get_constructor_info
        print("\n8. 获取车队信息 (Ergast API):")
        try:
            # 使用 fetch_season 获取车队信息
            constructors_data = ergast.get_constructor_info(season=2025)
            print(f"车队数据类型: {type(constructors_data)}")
            print(f"车队数据形状: {constructors_data.shape}")
            print(f"车队列名: {list(constructors_data.columns)}")
            print("\n车队信息:")
            print(constructors_data.head())
        except Exception as e:
            print(f"获取车队信息失败: {e}")

        #测试获取车手排名 - 使用 Ergast API-get_driver_standings
        print("\n10. 获取车手排名 (Ergast API):")
        try:
            driver_standings_data = ergast.get_driver_standings(season=2025)
            print(f"车手排名数据类型: {type(driver_standings_data)}")
            print("\n车手排名信息:")
            print_ergast_multi_response(driver_standings_data, "车手排名")
        except Exception as e:
            print(f"获取车手排名失败: {e}")

        #测试获取车队排名 - 使用 Ergast API-get_constructor_standings
        print("\n11. 获取车队排名 (Ergast API):")
        try:
            constructor_standings_data = ergast.get_constructor_standings(season=2025)
            print(f"车队排名数据类型: {type(constructor_standings_data)}")
            print("\n车队排名信息:")    
            print_ergast_multi_response(constructor_standings_data, "车队排名")
        except Exception as e:
            print(f"获取车队排名失败: {e}")
            
        # # 测试获取比赛状态 - 使用 Ergast API
        # print("\n8. 获取比赛状态 (Ergast API):")
        # try:
        #     status_data = ergast.get_finishing_status(season=2025)  
        #     print(f"比赛状态数据类型: {type(status_data)}")
        #     print(f"比赛状态数据形状: {status_data.shape}")
        #     print(f"比赛状态列名: {list(status_data.columns)}")
        #     print("\n比赛状态信息:")
        #     print(status_data)
        # except Exception as e:
        #     print(f"获取比赛状态失败: {e}")
        

        
    except Exception as e:
        print(f"测试过程中发生错误: {e}")

if __name__ == "__main__":
    print("开始 FastF1 测试...")
    test_fastf1_basic()
    print("\n测试完成！")
