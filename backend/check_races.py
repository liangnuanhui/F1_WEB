#!/usr/bin/env python3
"""
查看2025赛季比赛数据
"""

from app.core.database import get_db
from app.models import Race, Season
from sqlalchemy.orm import Session

def main():
    db = next(get_db())
    
    try:
        season_2025 = db.query(Season).filter(Season.year == 2025).first()
        if not season_2025:
            print("❌ 2025赛季不存在")
            return
        
        races = db.query(Race).filter(Race.season_id == season_2025.id).order_by(Race.round_number).all()
        
        print(f'2025赛季比赛数据 (共{len(races)}场):')
        print('=' * 80)
        
        for race in races:
            print(f'第{race.round_number}轮: {race.official_event_name}')
            print(f'  地点: {race.location} ({race.country})')
            print(f'  日期: {race.event_date}')
            print(f'  格式: {race.event_format}')
            print('-' * 60)
            
    finally:
        db.close()

if __name__ == "__main__":
    main() 