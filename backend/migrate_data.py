#!/usr/bin/env python3
"""
数据迁移脚本 - 从本地Docker数据库迁移到Render
"""
import os
import sys
import subprocess
from pathlib import Path
import argparse

def check_docker_container():
    """检查Docker容器是否运行"""
    try:
        result = subprocess.run(
            ["docker", "ps", "--filter", "name=f1_postgres", "--format", "{{.Names}}"],
            capture_output=True,
            text=True,
            check=True
        )
        return "f1_postgres" in result.stdout
    except subprocess.CalledProcessError:
        return False

def export_local_data(output_file="f1_data_backup.sql"):
    """导出本地PostgreSQL数据"""
    print("🔄 正在导出本地数据...")
    
    if not check_docker_container():
        print("❌ 错误: f1_postgres容器未运行")
        print("请先运行: docker-compose up -d")
        return False
    
    # 导出数据
    cmd = [
        "docker", "exec", "f1_postgres",
        "pg_dump", "-U", "f1_user", "-d", "f1_web",
        "--clean", "--no-owner", "--no-privileges",
        "--exclude-table-data=alembic_version"
    ]
    
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            result = subprocess.run(cmd, stdout=f, stderr=subprocess.PIPE, text=True)
            if result.returncode != 0:
                print(f"❌ 导出失败: {result.stderr}")
                return False
        
        # 检查文件大小
        file_size = os.path.getsize(output_file)
        if file_size > 0:
            print(f"✅ 数据已导出到: {output_file} ({file_size:,} bytes)")
            return True
        else:
            print(f"❌ 导出文件为空: {output_file}")
            return False
    except Exception as e:
        print(f"❌ 导出失败: {e}")
        return False

def import_to_render(render_db_url, input_file="f1_data_backup.sql"):
    """导入数据到Render数据库"""
    print("🔄 正在导入数据到Render...")
    
    if not os.path.exists(input_file):
        print(f"❌ 错误: 找不到备份文件 {input_file}")
        print("请先运行: python migrate_data.py export")
        return False
    
    # 检查psql是否安装
    try:
        subprocess.run(["psql", "--version"], capture_output=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ 错误: 未找到psql命令")
        print("请安装PostgreSQL客户端: brew install postgresql")
        return False
    
    cmd = ["psql", render_db_url, "-f", input_file]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ 数据已成功导入到Render数据库")
            return True
        else:
            print(f"❌ 导入失败: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ 导入失败: {e}")
        return False

def test_render_connection(render_db_url):
    """测试Render数据库连接"""
    print("🔄 正在测试Render数据库连接...")
    
    cmd = ["psql", render_db_url, "-c", "SELECT version();"]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Render数据库连接成功")
            return True
        else:
            print(f"❌ 连接失败: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ 连接失败: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(description="F1数据库迁移工具")
    parser.add_argument("action", choices=["export", "import", "test", "full"], 
                       help="操作类型")
    parser.add_argument("--db-url", help="Render数据库URL")
    parser.add_argument("--file", default="f1_data_backup.sql", 
                       help="备份文件名")
    
    args = parser.parse_args()
    
    if args.action == "export":
        success = export_local_data(args.file)
        if success:
            print("\n📝 下一步:")
            print(f"python migrate_data.py import --db-url 'YOUR_RENDER_DB_URL' --file {args.file}")
    
    elif args.action == "import":
        if not args.db_url:
            print("❌ 错误: 请提供Render数据库URL")
            print("使用方法: python migrate_data.py import --db-url 'YOUR_RENDER_DB_URL'")
            return
        
        success = import_to_render(args.db_url, args.file)
        if success:
            print("\n🎉 数据迁移完成！")
    
    elif args.action == "test":
        if not args.db_url:
            print("❌ 错误: 请提供Render数据库URL")
            print("使用方法: python migrate_data.py test --db-url 'YOUR_RENDER_DB_URL'")
            return
        
        test_render_connection(args.db_url)
    
    elif args.action == "full":
        if not args.db_url:
            print("❌ 错误: 请提供Render数据库URL")
            print("使用方法: python migrate_data.py full --db-url 'YOUR_RENDER_DB_URL'")
            return
        
        print("🚀 开始完整数据迁移流程...")
        
        # 步骤1: 测试连接
        if not test_render_connection(args.db_url):
            return
        
        # 步骤2: 导出数据
        if not export_local_data(args.file):
            return
        
        # 步骤3: 导入数据
        if not import_to_render(args.db_url, args.file):
            return
        
        print("\n🎉 完整数据迁移完成！")
        print("📝 下一步: 可以在Render控制台检查部署状态")

if __name__ == "__main__":
    main()