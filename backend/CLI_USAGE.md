# F1 Web Backend CLI 使用指南

本项目现在提供了统一的 CLI 工具来管理所有后端脚本和任务。

## 安装依赖

首先确保安装了 typer 依赖：

```bash
cd backend
poetry install
```

## 基本用法

使用以下命令来运行 CLI 工具：

```bash
# 查看帮助
python manage.py --help

# 查看特定命令分组的帮助
python manage.py db --help
python manage.py sync --help
python manage.py check --help
python manage.py scheduler --help
```

## 命令分组

### 数据库命令 (db)

```bash
# 清空数据库 (需要确认)
python manage.py db clear --confirm

# 初始化数据库
python manage.py db init

# 删除所有表 (需要确认)
python manage.py db drop-tables --confirm

# 检查数据库状态
python manage.py db state
```

### 数据同步命令 (sync)

```bash
# 同步所有数据 (连续三年)
python manage.py sync all

# 同步所有数据并指定缓存目录
python manage.py sync all --cache-dir ./custom_cache

# 同步自定义赛季
python manage.py sync seasons --season 2024 --season 2025

# 只同步当前赛季
python manage.py sync seasons --current-only

# 只同步最近两个赛季
python manage.py sync seasons --recent-only

# 同步赛道详细信息
python manage.py sync circuits

# 同步比赛后结果数据
python manage.py sync post-race --latest
python manage.py sync post-race --race-id 123
```

### 数据检查命令 (check)

```bash
# 检查赛道数据
python manage.py check circuits

# 检查比赛数据
python manage.py check races

# 检查车手数据
python manage.py check drivers

# 检查积分榜数据
python manage.py check standings

# 检查FastF1赛程数据
python manage.py check fastf1-schedule
```

### 调度器命令 (scheduler)

```bash
# 启动调度器
python manage.py scheduler start

# 演示调度器功能
python manage.py scheduler demo
```

### 其他命令

```bash
# 查看数据库数据
python manage.py view-data

# 验证2025赛季配置
python manage.py validate-config
```

## 常用工作流

### 1. 初始化项目

```bash
# 清空并初始化数据库
python manage.py db clear --confirm
python manage.py db init

# 同步所有数据
python manage.py sync all
```

### 2. 日常开发

```bash
# 检查数据库状态
python manage.py db state

# 检查特定数据
python manage.py check circuits
python manage.py check races

# 查看数据
python manage.py view-data
```

### 3. 数据更新

```bash
# 同步最新比赛结果
python manage.py sync post-race --latest

# 同步特定赛季
python manage.py sync seasons --season 2025
```

## 优势

使用统一 CLI 工具的优势：

1. **统一入口**: 所有脚本通过一个命令管理
2. **自文档化**: 使用 `--help` 查看所有可用命令
3. **类型安全**: 参数验证和类型检查
4. **错误处理**: 统一的错误处理和用户友好的错误信息
5. **易于扩展**: 添加新命令非常简单

## 从旧脚本迁移

| 旧脚本                              | 新命令                                |
| ----------------------------------- | ------------------------------------- |
| `python scripts/sync_all_data.py`   | `python manage.py sync all`           |
| `python scripts/clear_database.py`  | `python manage.py db clear --confirm` |
| `python scripts/init_data.py`       | `python manage.py db init`            |
| `python scripts/check_circuits.py`  | `python manage.py check circuits`     |
| `python scripts/check_races.py`     | `python manage.py check races`        |
| `python scripts/start_scheduler.py` | `python manage.py scheduler start`    |

## 环境变量

CLI 工具支持以下环境变量：

- `FASTF1_CACHE_DIR`: FastF1 缓存目录（也可通过 `--cache-dir` 参数指定）
- 其他应用配置环境变量（参考 `.env.example`）

## 故障排除

如果遇到问题：

1. 确保已安装所有依赖：`poetry install`
2. 检查数据库连接配置
3. 检查环境变量设置
4. 查看详细错误信息

使用 `--help` 查看具体命令的使用方法。
