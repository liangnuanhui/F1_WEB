# F1 赛事数据网站

一个全面展示 F1 比赛日程、赛道详情、车手与车队排行及比赛结果的现代化网站。

## 🏎️ 功能特性

- 📅 **赛季赛程**: 完整的 F1 赛季日程安排，支持多时区显示
- 🏁 **实时比赛数据**: WebSocket 实时推送比赛进程和结果
- 🏆 **积分榜**: 车手和车队实时积分排名
- 🛣️ **赛道详情**: 赛道布局图、历史数据和特点介绍
- 📊 **数据可视化**: 丰富的图表展示比赛数据和分析
- 📱 **响应式设计**: 完美适配桌面端和移动端
- ⚡ **高性能**: 缓存优化，快速加载体验

## 🛠️ 技术栈

### 后端

- **框架**: FastAPI
- **数据库**: PostgreSQL + SQLAlchemy
- **缓存**: Redis
- **数据源**: FastF1
- **任务队列**: Celery
- **WebSocket**: FastAPI 内置

### 前端

- **框架**: Next.js 14 + TypeScript
- **样式**: Tailwind CSS
- **状态管理**: React Query + Zustand
- **图表**: Recharts
- **部署**: Vercel

## 🚀 快速开始

### 环境要求

- Node.js 18+
- Python 3.11+
- Docker & Docker Compose
- pnpm
- Poetry

### 开发环境设置

1. **克隆项目**

```bash
git clone <repository-url>
cd F1-web
```

2. **启动基础设施**

```bash
docker-compose up -d postgres redis
```

3. **后端设置**

```bash
cd backend
poetry install
poetry run alembic upgrade head
poetry run uvicorn main:app --reload
```

4. **前端设置**

```bash
cd frontend
pnpm install
pnpm dev
```

5. **访问应用**

- 前端: http://localhost:3000
- 后端 API: http://localhost:8000
- API 文档: http://localhost:8000/docs

## 📁 项目结构

```
F1-web/
├── backend/                 # FastAPI后端
│   ├── app/
│   │   ├── api/            # API路由
│   │   ├── core/           # 核心配置
│   │   ├── models/         # 数据模型
│   │   ├── services/       # 业务逻辑
│   │   └── utils/          # 工具函数
│   ├── alembic/            # 数据库迁移
│   └── tests/              # 测试
├── frontend/               # Next.js前端
│   ├── src/
│   │   ├── app/           # App Router页面
│   │   ├── components/    # React组件
│   │   ├── hooks/         # 自定义Hooks
│   │   ├── lib/           # 工具库
│   │   └── types/         # TypeScript类型
│   └── public/            # 静态资源
├── docker-compose.yml      # 开发环境
└── README.md
```

## 🔧 开发规范

### 代码风格

- **后端**: Black + isort + flake8
- **前端**: ESLint + Prettier
- **提交**: Conventional Commits

### 分支策略

- `main`: 生产环境
- `develop`: 开发环境
- `feature/*`: 功能分支
- `hotfix/*`: 紧急修复

## 📊 数据更新策略

- **历史数据**: 长期缓存 (1 周+)
- **当前赛季**: 中期缓存 (1 天)
- **比赛日**: 短期缓存 (5 分钟)
- **实时数据**: WebSocket 推送

## 🚀 部署

### 生产环境

- **后端**: Railway/Render
- **前端**: Vercel
- **数据库**: PostgreSQL (云服务)
- **缓存**: Redis (云服务)

## 📝 许可证

MIT License

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📞 联系方式

如有问题，请通过以下方式联系：

- 项目 Issues
- 邮箱: [your-email@example.com]
