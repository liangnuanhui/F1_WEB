#!/usr/bin/env python3
"""
一键清空所有F1相关表数据（开发环境专用）
自动检测数据库中的表名，避免表名错误
"""
from app.core.database import get_db, engine
from sqlalchemy import inspect, text

def clear_all_tables():
    db = next(get_db())
    try:
        # 自动检测数据库中的所有表名
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        
        if not tables:
            print('❗ 数据库中没有表，无需清空。')
            return
        
        print(f"📋 检测到以下表: {tables}")
        
        # 拼接 TRUNCATE 语句
        truncate_sql = f"TRUNCATE TABLE {', '.join(tables)} RESTART IDENTITY CASCADE;"
        
        print(f"🔄 执行清空操作...")
        db.execute(text(truncate_sql))
        db.commit()
        
        print(f'✅ 已成功清空所有表: {len(tables)} 个表')
        print(f'📝 清空的表: {tables}')
        
    except Exception as e:
        db.rollback()
        print(f'❌ 清空失败: {e}')
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    clear_all_tables() 