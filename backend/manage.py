#!/usr/bin/env python3
"""
F1 Web Backend Management CLI
统一管理后端脚本和任务的命令行工具
"""

import typer
from typing import List, Optional
from pathlib import Path
import sys
import os

# 添加app目录到Python路径
sys.path.insert(0, str(Path(__file__).parent / "app"))

app = typer.Typer(
    name="F1 Web Backend Manager",
    help="统一管理 F1 Web 后端脚本和任务的命令行工具",
    add_completion=False,
)

# 数据库相关命令
db_app = typer.Typer(help="数据库相关命令")
app.add_typer(db_app, name="db")

# 数据同步相关命令
sync_app = typer.Typer(help="数据同步相关命令")
app.add_typer(sync_app, name="sync")

# 调度器相关命令
scheduler_app = typer.Typer(help="调度器相关命令")
app.add_typer(scheduler_app, name="scheduler")

# 数据检查相关命令
check_app = typer.Typer(help="数据检查相关命令")
app.add_typer(check_app, name="check")


# ====== 数据库命令 ======
@db_app.command("clear")
def clear_database(
    confirm: bool = typer.Option(
        False, "--confirm", help="确认清空数据库"
    )
):
    """清空数据库中的所有数据"""
    if not confirm:
        typer.confirm(
            "这将清空数据库中的所有数据，确定要继续吗？", 
            abort=True
        )
    
    try:
        from scripts.clear_database import main as clear_main
        clear_main()
        typer.echo("✅ 数据库已清空")
    except Exception as e:
        typer.echo(f"❌ 清空数据库失败: {e}", err=True)
        raise typer.Exit(1)


@db_app.command("init")
def init_database():
    """初始化数据库数据"""
    try:
        from scripts.init_data import main as init_main
        init_main()
        typer.echo("✅ 数据库初始化完成")
    except Exception as e:
        typer.echo(f"❌ 初始化数据库失败: {e}", err=True)
        raise typer.Exit(1)


@db_app.command("drop-tables")
def drop_all_tables(
    confirm: bool = typer.Option(
        False, "--confirm", help="确认删除所有表"
    )
):
    """删除所有数据库表"""
    if not confirm:
        typer.confirm(
            "这将删除所有数据库表，确定要继续吗？", 
            abort=True
        )
    
    try:
        from scripts.drop_all_tables import main as drop_main
        drop_main()
        typer.echo("✅ 所有数据库表已删除")
    except Exception as e:
        typer.echo(f"❌ 删除表失败: {e}", err=True)
        raise typer.Exit(1)


@db_app.command("state")
def check_database_state():
    """检查数据库状态"""
    try:
        from scripts.check_database_state import main as check_main
        check_main()
    except Exception as e:
        typer.echo(f"❌ 检查数据库状态失败: {e}", err=True)
        raise typer.Exit(1)


# ====== 数据同步命令 ======
@sync_app.command("all")
def sync_all_data(
    cache_dir: Optional[str] = typer.Option(
        None, "--cache-dir", help="FastF1缓存目录"
    )
):
    """同步所有数据（连续三年）"""
    try:
        from scripts.sync_all_data import main as sync_main
        if cache_dir:
            os.environ["FASTF1_CACHE_DIR"] = cache_dir
        sync_main()
        typer.echo("✅ 所有数据同步完成")
    except Exception as e:
        typer.echo(f"❌ 同步数据失败: {e}", err=True)
        raise typer.Exit(1)


@sync_app.command("seasons")
def sync_custom_seasons(
    seasons: Optional[List[int]] = typer.Option(
        None, "--season", help="指定要同步的赛季年份"
    ),
    current_only: bool = typer.Option(
        False, "--current-only", help="只同步当前赛季"
    ),
    recent_only: bool = typer.Option(
        False, "--recent-only", help="只同步最近两个赛季"
    ),
    cache_dir: Optional[str] = typer.Option(
        None, "--cache-dir", help="FastF1缓存目录"
    )
):
    """同步自定义赛季数据"""
    try:
        from scripts.sync_custom_seasons import main as sync_main
        if cache_dir:
            os.environ["FASTF1_CACHE_DIR"] = cache_dir
        
        # 构建参数
        args = []
        if seasons:
            args.extend(["--seasons"] + [str(s) for s in seasons])
        if current_only:
            args.append("--current-only")
        if recent_only:
            args.append("--recent-only")
        
        sync_main(args)
        typer.echo("✅ 自定义赛季数据同步完成")
    except Exception as e:
        typer.echo(f"❌ 同步自定义赛季数据失败: {e}", err=True)
        raise typer.Exit(1)


@sync_app.command("circuits")
def sync_circuit_details():
    """同步赛道详细信息"""
    try:
        from scripts.sync_circuit_details_v2 import main as sync_main
        sync_main()
        typer.echo("✅ 赛道详细信息同步完成")
    except Exception as e:
        typer.echo(f"❌ 同步赛道详细信息失败: {e}", err=True)
        raise typer.Exit(1)


@sync_app.command("post-race")
def post_race_sync(
    race_id: Optional[int] = typer.Option(
        None, "--race-id", help="指定比赛ID"
    ),
    latest: bool = typer.Option(
        False, "--latest", help="同步最新比赛"
    )
):
    """同步比赛后结果数据"""
    try:
        from scripts.manage_post_race_sync import main as sync_main
        
        args = []
        if race_id:
            args.extend(["--race-id", str(race_id)])
        if latest:
            args.append("--latest")
        
        sync_main(args)
        typer.echo("✅ 比赛后结果数据同步完成")
    except Exception as e:
        typer.echo(f"❌ 同步比赛后结果数据失败: {e}", err=True)
        raise typer.Exit(1)


# ====== 调度器命令 ======
@scheduler_app.command("start")
def start_scheduler():
    """启动调度器"""
    try:
        from scripts.start_scheduler import main as scheduler_main
        scheduler_main()
    except Exception as e:
        typer.echo(f"❌ 启动调度器失败: {e}", err=True)
        raise typer.Exit(1)


@scheduler_app.command("demo")
def demo_scheduler():
    """演示调度器功能"""
    try:
        from scripts.demo_scheduler import main as demo_main
        demo_main()
    except Exception as e:
        typer.echo(f"❌ 演示调度器失败: {e}", err=True)
        raise typer.Exit(1)


# ====== 数据检查命令 ======
@check_app.command("circuits")
def check_circuits():
    """检查赛道数据"""
    try:
        from scripts.check_circuits import main as check_main
        check_main()
    except Exception as e:
        typer.echo(f"❌ 检查赛道数据失败: {e}", err=True)
        raise typer.Exit(1)


@check_app.command("races")
def check_races():
    """检查比赛数据"""
    try:
        from scripts.check_races import main as check_main
        check_main()
    except Exception as e:
        typer.echo(f"❌ 检查比赛数据失败: {e}", err=True)
        raise typer.Exit(1)


@check_app.command("drivers")
def check_drivers():
    """检查车手数据"""
    try:
        from scripts.check_db import main as check_main
        check_main()
    except Exception as e:
        typer.echo(f"❌ 检查车手数据失败: {e}", err=True)
        raise typer.Exit(1)


@check_app.command("standings")
def check_standings():
    """检查积分榜数据"""
    try:
        from scripts.diagnose_standings import main as check_main
        check_main()
    except Exception as e:
        typer.echo(f"❌ 检查积分榜数据失败: {e}", err=True)
        raise typer.Exit(1)


@check_app.command("fastf1-schedule")
def check_fastf1_schedule():
    """检查FastF1赛程数据"""
    try:
        from scripts.check_fastf1_schedule import main as check_main
        check_main()
    except Exception as e:
        typer.echo(f"❌ 检查FastF1赛程数据失败: {e}", err=True)
        raise typer.Exit(1)


@app.command("view-data")
def view_data():
    """查看数据库数据"""
    try:
        from scripts.view_data import main as view_main
        view_main()
    except Exception as e:
        typer.echo(f"❌ 查看数据失败: {e}", err=True)
        raise typer.Exit(1)


@app.command("validate-config")
def validate_config():
    """验证2025赛季配置"""
    try:
        from scripts.validate_2025_config import main as validate_main
        validate_main()
    except Exception as e:
        typer.echo(f"❌ 验证配置失败: {e}", err=True)
        raise typer.Exit(1)


if __name__ == "__main__":
    app() 