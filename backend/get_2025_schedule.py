#!/usr/bin/env python3
"""
获取2025赛季完整比赛安排数据并保存为文件
"""

import sys
import os
import logging
import pandas as pd
import json
from datetime import datetime

# 添加项目根目录到 Python 路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def get_2025_schedule():
    """获取2025赛季完整比赛安排"""
    try:
        import fastf1
        from fastf1.ergast import Ergast
        
        logger.info("🔍 获取2025赛季完整比赛安排...")
        
        # 启用缓存
        fastf1.Cache.enable_cache('./cache')
        
        # 创建输出目录
        output_dir = './schedule_data'
        os.makedirs(output_dir, exist_ok=True)
        
        # 1. 使用 FastF1 获取详细日程
        logger.info("📊 1. 使用 FastF1 获取详细日程...")
        try:
            fastf1_schedule = fastf1.get_event_schedule(2025)
            
            if not fastf1_schedule.empty:
                logger.info(f"✅ FastF1 获取成功，共{len(fastf1_schedule)}条记录")
                
                # 保存为 CSV 文件
                csv_file = os.path.join(output_dir, '2025_schedule_fastf1.csv')
                fastf1_schedule.to_csv(csv_file, index=False, encoding='utf-8')
                logger.info(f"💾 保存为 CSV: {csv_file}")
                
                # 保存为 JSON 文件（更易读）
                json_file = os.path.join(output_dir, '2025_schedule_fastf1.json')
                fastf1_schedule.to_json(json_file, orient='records', indent=2, force_ascii=False)
                logger.info(f"💾 保存为 JSON: {json_file}")
                
                # 显示详细信息
                logger.info("📋 FastF1 日程详情:")
                logger.info(f"📊 总记录数: {len(fastf1_schedule)}")
                logger.info(f"📋 列名: {list(fastf1_schedule.columns)}")
                
                # 显示每场比赛的详细信息
                logger.info("🏁 比赛详情:")
                for idx, event in fastf1_schedule.iterrows():
                    logger.info(f"   {idx+1}. {event.get('EventName', 'N/A')}")
                    logger.info(f"      轮次: {event.get('RoundNumber', 'N/A')}")
                    logger.info(f"      国家: {event.get('Country', 'N/A')}")
                    logger.info(f"      地点: {event.get('Location', 'N/A')}")
                    logger.info(f"      日期: {event.get('EventDate', 'N/A')}")
                    logger.info(f"      格式: {event.get('EventFormat', 'N/A')}")
                    
                    # 显示所有session信息
                    sessions = []
                    for i in range(1, 6):
                        session_name = event.get(f'Session{i}', '')
                        session_date = event.get(f'Session{i}Date', '')
                        if session_name and session_date:
                            sessions.append(f"{session_name}: {session_date}")
                    
                    if sessions:
                        logger.info(f"      Sessions: {', '.join(sessions)}")
                    logger.info("")
                
                return fastf1_schedule
            else:
                logger.warning("⚠️ FastF1 返回空数据")
                return pd.DataFrame()
                
        except Exception as e:
            logger.error(f"❌ FastF1 获取失败: {e}")
            return pd.DataFrame()
        
    except Exception as e:
        logger.error(f"❌ 获取失败: {e}")
        return pd.DataFrame()

def get_ergast_schedule():
    """获取 Ergast 的2025赛季日程作为对比"""
    try:
        from fastf1.ergast import Ergast
        
        logger.info("📊 2. 使用 Ergast 获取日程（对比）...")
        
        ergast = Ergast()
        ergast_schedule = ergast.get_race_schedule(season=2025)
        
        if not ergast_schedule.empty:
            logger.info(f"✅ Ergast 获取成功，共{len(ergast_schedule)}条记录")
            
            # 保存为文件
            output_dir = './schedule_data'
            csv_file = os.path.join(output_dir, '2025_schedule_ergast.csv')
            ergast_schedule.to_csv(csv_file, index=False, encoding='utf-8')
            logger.info(f"💾 保存为 CSV: {csv_file}")
            
            json_file = os.path.join(output_dir, '2025_schedule_ergast.json')
            ergast_schedule.to_json(json_file, orient='records', indent=2, force_ascii=False)
            logger.info(f"💾 保存为 JSON: {json_file}")
            
            return ergast_schedule
        else:
            logger.warning("⚠️ Ergast 返回空数据")
            return pd.DataFrame()
            
    except Exception as e:
        logger.error(f"❌ Ergast 获取失败: {e}")
        return pd.DataFrame()

def create_summary_report():
    """创建汇总报告"""
    try:
        output_dir = './schedule_data'
        
        # 读取数据
        fastf1_file = os.path.join(output_dir, '2025_schedule_fastf1.csv')
        ergast_file = os.path.join(output_dir, '2025_schedule_ergast.csv')
        
        report = []
        report.append("# 2025赛季F1比赛安排数据报告")
        report.append(f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append("")
        
        if os.path.exists(fastf1_file):
            fastf1_data = pd.read_csv(fastf1_file)
            report.append("## FastF1 数据")
            report.append(f"- 总记录数: {len(fastf1_data)}")
            report.append(f"- 列数: {len(fastf1_data.columns)}")
            report.append(f"- 列名: {', '.join(fastf1_data.columns)}")
            report.append("")
            
            # 统计比赛类型
            if 'EventFormat' in fastf1_data.columns:
                format_counts = fastf1_data['EventFormat'].value_counts()
                report.append("### 比赛格式统计:")
                for format_type, count in format_counts.items():
                    report.append(f"- {format_type}: {count}场")
                report.append("")
            
            # 显示前10场比赛
            report.append("### 前10场比赛:")
            for idx, event in fastf1_data.head(10).iterrows():
                report.append(f"{idx+1}. {event.get('EventName', 'N/A')} - {event.get('EventDate', 'N/A')}")
            report.append("")
        
        if os.path.exists(ergast_file):
            ergast_data = pd.read_csv(ergast_file)
            report.append("## Ergast 数据")
            report.append(f"- 总记录数: {len(ergast_data)}")
            report.append(f"- 列数: {len(ergast_data.columns)}")
            report.append(f"- 列名: {', '.join(ergast_data.columns)}")
            report.append("")
            
            # 显示前10场比赛
            report.append("### 前10场比赛:")
            for idx, race in ergast_data.head(10).iterrows():
                report.append(f"{idx+1}. {race.get('raceName', 'N/A')} - {race.get('date', 'N/A')}")
            report.append("")
        
        # 保存报告
        report_file = os.path.join(output_dir, '2025_schedule_report.md')
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(report))
        
        logger.info(f"📄 汇总报告已保存: {report_file}")
        
    except Exception as e:
        logger.error(f"❌ 创建报告失败: {e}")

def main():
    """主函数"""
    logger.info("🚀 开始获取2025赛季比赛安排...")
    
    # 获取 FastF1 数据
    fastf1_data = get_2025_schedule()
    
    # 获取 Ergast 数据作为对比
    ergast_data = get_ergast_schedule()
    
    # 创建汇总报告
    create_summary_report()
    
    logger.info("✅ 数据获取完成！")
    logger.info("📁 所有文件已保存到 ./schedule_data/ 目录")
    logger.info("📄 查看以下文件:")
    logger.info("   - 2025_schedule_fastf1.csv (FastF1数据)")
    logger.info("   - 2025_schedule_fastf1.json (FastF1数据，JSON格式)")
    logger.info("   - 2025_schedule_ergast.csv (Ergast数据)")
    logger.info("   - 2025_schedule_ergast.json (Ergast数据，JSON格式)")
    logger.info("   - 2025_schedule_report.md (汇总报告)")

if __name__ == "__main__":
    main() 