#!/usr/bin/env python3
"""
数据库字段修复脚本
修复seasons表的is_current字段类型
"""

import sys
import logging
from pathlib import Path

# 添加项目根目录到 Python 路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from sqlalchemy import text
from app.core.database import get_db

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def fix_season_field_type():
    """修复seasons表的is_current字段类型"""
    logger.info("🔧 开始修复seasons表的is_current字段类型...")
    
    try:
        db = next(get_db())
        
        # 检查当前字段类型
        logger.info("📋 检查当前字段类型...")
        result = db.execute(text("""
            SELECT column_name, data_type, is_nullable, column_default
            FROM information_schema.columns 
            WHERE table_name = 'seasons' AND column_name = 'is_current'
        """))
        
        column_info = result.fetchone()
        if column_info:
            logger.info(f"当前is_current字段: {column_info}")
            
            if column_info[1] == 'boolean':
                logger.info("✅ is_current字段已经是boolean类型，无需修复")
                return True
            elif column_info[1] == 'integer':
                logger.info("🔄 开始修复字段类型从integer到boolean...")
                
                # 备份当前数据
                seasons_data = db.execute(text("SELECT id, year, is_current FROM seasons")).fetchall()
                logger.info(f"备份了 {len(seasons_data)} 条赛季数据")
                
                # 修改字段类型
                db.execute(text("""
                    ALTER TABLE seasons 
                    ALTER COLUMN is_current TYPE boolean 
                    USING CASE WHEN is_current = 1 THEN true ELSE false END
                """))
                
                # 设置2025赛季为当前赛季
                logger.info("🎯 设置2025赛季为当前赛季...")
                db.execute(text("UPDATE seasons SET is_current = false"))
                db.execute(text("UPDATE seasons SET is_current = true WHERE year = 2025"))
                
                # 如果没有2025赛季，创建它
                season_2025 = db.execute(text("SELECT id FROM seasons WHERE year = 2025")).fetchone()
                if not season_2025:
                    logger.info("📝 创建2025赛季...")
                    db.execute(text("""
                        INSERT INTO seasons (year, name, is_current, is_active, created_at, updated_at)
                        VALUES (2025, '2025 Formula 1 World Championship', true, true, NOW(), NOW())
                    """))
                
                db.commit()
                logger.info("✅ 字段类型修复完成")
                
                # 验证修复结果
                result = db.execute(text("""
                    SELECT column_name, data_type, is_nullable, column_default
                    FROM information_schema.columns 
                    WHERE table_name = 'seasons' AND column_name = 'is_current'
                """))
                
                new_column_info = result.fetchone()
                if new_column_info and new_column_info[1] == 'boolean':
                    logger.info("✅ 字段类型修复验证成功")
                    
                    # 显示当前赛季状态
                    seasons = db.execute(text("SELECT year, name, is_current FROM seasons ORDER BY year DESC")).fetchall()
                    logger.info("📊 当前赛季状态:")
                    for year, name, is_current in seasons:
                        status = "✅ 当前赛季" if is_current else ""
                        logger.info(f"  {year}: {name} {status}")
                    
                    return True
                else:
                    logger.error("❌ 字段类型修复验证失败")
                    return False
            else:
                logger.error(f"❌ 未知的字段类型: {column_info[1]}")
                return False
        else:
            logger.error("❌ 未找到is_current字段")
            return False
        
    except Exception as e:
        logger.error(f"❌ 修复字段类型时发生错误: {e}")
        db.rollback()
        return False
    finally:
        db.close()


def main():
    """主函数"""
    logger.info("🚀 开始数据库字段修复流程...")
    
    success = fix_season_field_type()
    
    if success:
        logger.info("🎉 数据库字段修复成功！")
        return True
    else:
        logger.error("❌ 数据库字段修复失败！")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 