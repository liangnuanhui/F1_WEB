#!/usr/bin/env python3
"""
数据迁移脚本 - 从本地Docker数据库迁移到Render
"""
import os
import sys
import subprocess
from pathlib import Path

def export_local_data():
    """导出本地PostgreSQL数据"""
    print("正在导出本地数据...")
    
    # 检查Docker容器是否运行
    result = subprocess.run(
        ["docker", "ps", "--filter", "name=f1_postgres", "--format", "{{.Names}}"],
        capture_output=True,
        text=True
    )
    
    if "f1_postgres" not in result.stdout:
        print("❌ 错误: f1_postgres容器未运行")
        print("请先运行: docker-compose up -d")
        return False
    
    # 导出数据
    dump_file = "f1_data_backup.sql"
    cmd = [
        "docker", "exec", "f1_postgres",
        "pg_dump", "-U", "f1_user", "-d", "f1_web",
        "--clean", "--no-owner", "--no-privileges"
    ]
    
    try:
        with open(dump_file, 'w') as f:
            subprocess.run(cmd, stdout=f, check=True)
        
        print(f"✅ 数据已导出到: {dump_file}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ 导出失败: {e}")
        return False

def import_to_render(render_db_url):
    """导入数据到Render数据库"""
    print("正在导入数据到Render...")
    
    dump_file = "f1_data_backup.sql"
    if not os.path.exists(dump_file):
        print(f"❌ 错误: 找不到备份文件 {dump_file}")
        return False
    
    cmd = ["psql", render_db_url, "-f", dump_file]
    
    try:
        subprocess.run(cmd, check=True)
        print("✅ 数据已成功导入到Render数据库")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ 导入失败: {e}")
        return False

def main():
    if len(sys.argv) < 2:
        print("用法:")
        print("  python migrate_data.py export                    # 导出本地数据")
        print("  python migrate_data.py import <RENDER_DB_URL>    # 导入到Render")
        return
    
    action = sys.argv[1]
    
    if action == "export":
        export_local_data()
    elif action == "import":
        if len(sys.argv) < 3:
            print("❌ 错误: 请提供Render数据库URL")
            print("使用方法: python migrate_data.py import <RENDER_DB_URL>")
            return
        
        render_db_url = sys.argv[2]
        import_to_render(render_db_url)
    else:
        print("❌ 错误: 无效的操作")
        print("支持的操作: export, import")

if __name__ == "__main__":
    main()