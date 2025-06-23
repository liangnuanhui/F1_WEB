#!/usr/bin/env python3
"""
检查数据库状态
"""

import sys
from pathlib import Path

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from app.core.database import get_db
from app.models.season import Season

def check_seasons():
    db = next(get_db())
    try:
        count = db.query(Season).count()
        print(f"数据库中的赛季总数: {count}")
        
        if count > 0:
            seasons = db.query(Season).all()
            print("赛季列表:")
            for season in seasons:
                print(f"  ID: {season.id}, 年份: {season.year} - {season.name} (当前: {season.is_current})")
        else:
            print("数据库中没有赛季数据")
            
    finally:
        db.close()

if __name__ == "__main__":
    check_seasons() 