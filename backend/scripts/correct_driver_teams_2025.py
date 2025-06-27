"""
一个一次性脚本，用于修正2025赛季特定车手的车队归属。
"""
import os
import sys
from sqlalchemy import select

# 确保脚本可以找到app模块
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.database import SessionLocal
from app.models import Driver, Constructor, Season, DriverSeason

def correct_driver_teams_for_2025():
    """
    为2025赛季的车手Liam Lawson和Yuki Tsunoda设置正确的车队。
    - Liam Lawson -> RB F1 Team (rb)
    - Yuki Tsunoda -> Red Bull Racing (red_bull)
    """
    db = SessionLocal()
    try:
        print("开始修正2025赛季车队数据...")

        # 1. 定义需要修正的数据
        # driver_id -> constructor_id
        corrections = {
            "lawson": "rb",
            "tsunoda": "red_bull"
        }
        
        # 2. 获取2025赛季的ID
        season_result = db.execute(select(Season).where(Season.year == 2025))
        season = season_result.scalar_one_or_none()
        
        if not season:
            print("错误: 未找到2025赛季。请先运行数据初始化脚本。")
            return
            
        print(f"找到2025赛季 (ID: {season.id})")

        for driver_id, constructor_id in corrections.items():
            # 3. 验证车手和车队是否存在
            driver_res = db.execute(select(Driver).where(Driver.driver_id == driver_id))
            driver = driver_res.scalar_one_or_none()
            
            constructor_res = db.execute(select(Constructor).where(Constructor.constructor_id == constructor_id))
            constructor = constructor_res.scalar_one_or_none()

            if not driver:
                print(f"警告: 未找到车手ID为 '{driver_id}' 的车手，跳过此条修正。")
                continue
            if not constructor:
                print(f"警告: 未找到车队ID为 '{constructor_id}' 的车队，跳过此条修正。")
                continue

            print(f"处理车手: {driver.forename} {driver.surname} -> 车队: {constructor.name}")

            # 4. 查找是否已存在记录
            existing_entry_res = db.execute(
                select(DriverSeason).where(
                    DriverSeason.driver_id == driver.driver_id,
                    DriverSeason.season_id == season.id
                )
            )
            existing_entry = existing_entry_res.scalar_one_or_none()

            if existing_entry:
                # 如果记录存在且车队不正确，则更新
                if existing_entry.constructor_id != constructor.constructor_id:
                    print(f"  > 发现已存在记录，车队信息不匹配。正在更新...")
                    print(f"    旧车队: {existing_entry.constructor_id} -> 新车队: {constructor.constructor_id}")
                    existing_entry.constructor_id = constructor.constructor_id
                    db.add(existing_entry)
                else:
                    print(f"  > 车队信息已正确，无需修改。")
            else:
                # 如果记录不存在，则创建新记录
                print(f"  > 未发现记录，正在创建新条目...")
                new_entry = DriverSeason(
                    driver_id=driver.driver_id,
                    constructor_id=constructor.constructor_id,
                    season_id=season.id
                )
                db.add(new_entry)
        
        # 5. 提交更改到数据库
        db.commit()
        print("\n数据修正完成！")
    finally:
        db.close()

def main():
    correct_driver_teams_for_2025()

if __name__ == "__main__":
    main() 