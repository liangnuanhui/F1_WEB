# F1 赛事数据网站后端

## 项目简介

F1 赛事数据网站的后端 API 服务，使用 FastAPI 框架构建。

## 技术栈

- **框架**: FastAPI
- **数据库**: PostgreSQL + SQLAlchemy
- **缓存**: Redis
- **数据源**: FastF1
- **包管理**: Poetry

## 快速开始

### 安装依赖

```bash
poetry install
```

### 运行开发服务器

```bash
poetry run dev
```

### 运行测试

```bash
poetry run test
```

## 数据同步

### 测试数据提供者

```bash
# 基础测试
poetry run test-providers --season 2024

# 详细测试
poetry run test-providers-verbose --season 2024
```

### 同步数据

```bash
# 同步当前赛季数据
poetry run sync-data current

# 同步历史数据
poetry run history-data season --season 2024
```

## 项目结构

```
backend/
├── app/
│   ├── api/           # API 路由
│   ├── core/          # 核心配置
│   ├── models/        # 数据库模型
│   ├── schemas/       # Pydantic 模式
│   └── services/      # 业务逻辑
├── scripts/           # 脚本文件
└── tests/             # 测试文件
```
