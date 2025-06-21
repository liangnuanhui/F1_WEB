#!/usr/bin/env python3
"""
完全删除所有F1相关表（开发环境专用）
删除表、索引、约束等所有数据库对象
"""
from app.core.database import get_db, engine
from sqlalchemy import inspect, text

def drop_all_tables():
    db = next(get_db())
    try:
        # 自动检测数据库中的所有表名
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        
        if not tables:
            print('❗ 数据库中没有表，无需删除。')
            return
        
        print(f"📋 检测到以下表: {tables}")
        
        # 禁用外键约束检查
        db.execute(text("SET session_replication_role = replica;"))
        
        # 删除所有表
        for table in tables:
            print(f"🗑️  删除表: {table}")
            db.execute(text(f"DROP TABLE IF EXISTS {table} CASCADE;"))
        
        # 重新启用外键约束检查
        db.execute(text("SET session_replication_role = DEFAULT;"))
        
        db.commit()
        
        print(f'✅ 已成功删除所有表: {len(tables)} 个表')
        print(f'📝 删除的表: {tables}')
        
    except Exception as e:
        db.rollback()
        print(f'❌ 删除失败: {e}')
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    drop_all_tables() 