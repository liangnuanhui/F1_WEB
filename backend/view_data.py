#!/usr/bin/env python3
"""
数据库数据可视化查看工具
"""

from app.core.database import get_db
from app.models import Season, Circuit, Constructor, Driver, Race
from sqlalchemy.orm import Session
from tabulate import tabulate
import pandas as pd

def print_seasons(db: Session):
    """显示赛季数据"""
    print("\n" + "="*80)
    print("🏆 赛季数据")
    print("="*80)
    
    seasons = db.query(Season).order_by(Season.year).all()
    data = []
    for season in seasons:
        data.append([
            season.year,
            season.name,
            season.start_date,
            season.end_date,
            f"{len(season.races)} 场比赛"
        ])
    
    headers = ["年份", "名称", "开始日期", "结束日期", "比赛数量"]
    print(tabulate(data, headers=headers, tablefmt="grid"))

def print_circuits(db: Session):
    """显示赛道数据"""
    print("\n" + "="*80)
    print("🏁 赛道数据")
    print("="*80)
    
    circuits = db.query(Circuit).order_by(Circuit.circuit_name).all()
    data = []
    for circuit in circuits:
        data.append([
            circuit.circuit_name,
            circuit.country,
            circuit.locality,
            f"{len(circuit.races)} 场比赛"
        ])
    
    headers = ["赛道名称", "国家", "城市", "比赛数量"]
    print(tabulate(data, headers=headers, tablefmt="grid"))

def print_constructors(db: Session):
    """显示车队数据"""
    print("\n" + "="*80)
    print("🏎️ 车队数据")
    print("="*80)
    
    constructors = db.query(Constructor).order_by(Constructor.constructor_name).all()
    data = []
    for constructor in constructors:
        data.append([
            constructor.constructor_name,
            constructor.constructor_nationality,
            constructor.season.year,
            f"{len(constructor.driver_seasons)} 个车手"
        ])
    
    headers = ["车队名称", "国籍", "赛季", "车手数量"]
    print(tabulate(data, headers=headers, tablefmt="grid"))

def print_drivers(db: Session):
    """显示车手数据"""
    print("\n" + "="*80)
    print("👨‍🏁 车手数据")
    print("="*80)
    
    drivers = db.query(Driver).order_by(Driver.family_name).all()
    data = []
    for driver in drivers:
        data.append([
            f"{driver.given_name} {driver.family_name}",
            driver.driver_number,
            driver.driver_code,
            driver.driver_nationality,
            driver.date_of_birth
        ])
    
    headers = ["姓名", "号码", "代码", "国籍", "出生日期"]
    print(tabulate(data, headers=headers, tablefmt="grid"))

def print_races(db: Session, season_year: int = 2025):
    """显示比赛数据"""
    print(f"\n" + "="*80)
    print(f"🏁 {season_year}赛季比赛数据")
    print("="*80)
    
    season = db.query(Season).filter(Season.year == season_year).first()
    if not season:
        print(f"❌ {season_year}赛季不存在")
        return
    
    races = db.query(Race).filter(Race.season_id == season.id).order_by(Race.round_number).all()
    data = []
    for race in races:
        data.append([
            race.round_number,
            race.official_event_name,
            race.location,
            race.country,
            race.event_date,
            race.event_format
        ])
    
    headers = ["轮次", "比赛名称", "地点", "国家", "日期", "格式"]
    print(tabulate(data, headers=headers, tablefmt="grid"))

def print_summary(db: Session):
    """显示数据摘要"""
    print("\n" + "="*80)
    print("📊 数据摘要")
    print("="*80)
    
    summary_data = [
        ["赛季数量", db.query(Season).count()],
        ["赛道数量", db.query(Circuit).count()],
        ["车队数量", db.query(Constructor).count()],
        ["车手数量", db.query(Driver).count()],
        ["比赛数量", db.query(Race).count()],
    ]
    
    headers = ["数据类型", "数量"]
    print(tabulate(summary_data, headers=headers, tablefmt="grid"))

def main():
    """主函数"""
    db = next(get_db())
    
    try:
        print("🎯 F1数据库数据可视化")
        print("="*80)
        
        # 显示摘要
        print_summary(db)
        
        # 显示详细数据
        print_seasons(db)
        print_circuits(db)
        print_constructors(db)
        print_drivers(db)
        print_races(db, 2025)
        
    except Exception as e:
        print(f"❌ 错误: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    main() 