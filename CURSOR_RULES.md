# F1 赛事数据网站开发规范

## 项目概述

开发一个全面展示 F1 比赛日程、赛道详情、车手与车队排行及比赛结果的网站。采用前后端分离架构，Python 处理数据，Next.js 构建用户界面。

## 技术栈规范

### 后端技术栈

- **框架**: FastAPI (推荐) 或 Flask
- **数据库**: PostgreSQL + SQLAlchemy ORM
- **缓存**: Redis (数据缓存 + Session 存储)
- **数据源**: FastF1 库 (官方 F1 数据)
- **任务队列**: Celery (定时数据更新)
- **WebSocket**: FastAPI 内置 或 Socket.IO
- **部署**: Docker + Railway/Render

### 前端技术栈

- **框架**: Next.js 14 + TypeScript
- **样式**: Tailwind CSS
- **状态管理**: React Query/SWR (服务端状态) + Zustand (客户端状态)
- **图表库**: Chart.js 或 Recharts
- **WebSocket**: 原生 WebSocket 或 Socket.IO Client
- **部署**: Vercel

### 开发工具

- **包管理**: pnpm (前端), poetry (后端)
- **代码规范**: ESLint + Prettier (前端), Black + isort (后端)
- **容器化**: Docker Compose (开发环境)
- **API 文档**: FastAPI 自动生成 Swagger

## 架构设计原则

### 1. 前后端分离

```
前端 (Next.js) ←→ REST API ←→ 后端 (FastAPI + FastF1)
```

### 2. 数据流向

```
FastF1 → 数据处理 → PostgreSQL → Redis 缓存 → API → 前端展示
```

### 3. 实时更新架构

```
Next.js ←→ WebSocket ←→ FastAPI ←→ Redis ←→ 数据更新服务
```

## 核心功能模块

### 后端 API 设计

```python
# 必需的 API 端点
GET /api/schedule          # 赛季赛程
GET /api/races/{race_id}   # 单场比赛详情
GET /api/drivers           # 车手列表和积分榜
GET /api/constructors      # 车队积分榜
GET /api/circuits          # 赛道信息
GET /api/results/{race_id} # 比赛结果
GET /api/standings         # 当前积分榜
WebSocket /ws/race/{race_id} # 实时比赛数据
```

### 前端页面结构

- **首页**: 赛季概览 + 下场比赛倒计时
- **赛程页**: 完整日程 + 多时区显示
- **赛道页**: 布局图 + 历史数据 + 特点介绍
- **车手页**: 积分榜 + 个人统计 + 生涯数据
- **车队页**: 车队积分 + 车手组合 + 历史成绩
- **比赛结果页**: 详细成绩 + 圈速分析

## 开发注意事项

### 1. 数据管理

- **缓存策略**: 历史数据长期缓存(1 周+)，当前赛季中期缓存(1 天)，比赛日短期缓存(5 分钟)
- **数据更新频率**: 比赛周末每 5-10 分钟，非比赛期每日更新
- **错误处理**: FastF1 数据获取失败时的降级方案
- **数据一致性**: 使用事务确保数据完整性

### 2. 性能优化

- **前端**: Next.js SSG/ISR，图片优化，代码分割
- **后端**: 数据库索引优化，API 响应缓存，连接池管理
- **CDN**: 静态资源加速，图片压缩
- **懒加载**: 大数据表格和图表按需加载

### 3. 用户体验

- **响应式设计**: 移动端优先，适配各种屏幕
- **加载状态**: 骨架屏，进度条，错误边界
- **多时区支持**: 自动检测用户时区，比赛时间本地化
- **PWA 功能**: 离线缓存，推送通知

### 4. 实时功能

- **WebSocket 管理**: 连接状态监控，断线重连机制
- **消息格式**: 统一的消息结构，版本控制
- **房间管理**: 按比赛分组，用户状态跟踪
- **性能控制**: 连接数限制，消息频率控制

## 代码规范

### 后端 (Python)

- 使用 `async/await` 异步编程
- Pydantic 模型验证所有输入输出
- 依赖注入管理数据库连接
- 错误处理使用 HTTPException
- 日志记录使用 structlog

### 前端 (TypeScript)

- 严格的 TypeScript 配置
- 自定义 hooks 封装复杂逻辑
- 组件按功能模块组织
- 使用 React.memo 优化渲染
- Error Boundary 全局错误处理

### API 设计原则

- RESTful 设计，资源导向
- 统一的响应格式
- 适当的 HTTP 状态码
- API 版本控制 (`/api/v1/`)
- 分页、排序、过滤支持

## 部署和运维

### 开发环境

```bash
# 后端
cd backend && poetry install && poetry run uvicorn main:app --reload

# 前端
cd frontend && pnpm install && pnpm dev

# 数据库
docker-compose up postgres redis
```

### 生产环境

- **后端**: Railway/Render + PostgreSQL + Redis
- **前端**: Vercel (自动 CI/CD)
- **监控**: 日志聚合，性能监控，错误跟踪
- **备份**: 数据库定期备份，静态资源 CDN

## 安全考虑

- API 限流和防护
- 输入验证和 SQL 注入防护
- CORS 配置
- 敏感信息环境变量管理
- HTTPS 强制使用

## 测试策略

- **后端**: pytest + 数据库测试
- **前端**: Jest + React Testing Library
- **E2E**: Playwright 关键路径测试
- **API**: 自动化 API 测试

## 开发优先级

### Phase 1: 基础功能 (MVP)

1. 静态数据展示 (赛程、车手、车队)
2. 基础 API 和前端页面
3. 数据库设计和基础缓存

### Phase 2: 动态功能

1. 数据自动更新机制
2. 用户交互功能
3. 性能优化

### Phase 3: 实时功能

1. WebSocket 实时数据推送
2. 高级用户功能
3. 移动端优化

## 文件命名规范

### 后端

- 文件名: 小写字母 + 下划线 (snake_case)
- 类名: 大驼峰命名 (PascalCase)
- 函数名: 小写字母 + 下划线 (snake_case)
- 常量: 大写字母 + 下划线 (UPPER_SNAKE_CASE)

### 前端

- 文件名: 大驼峰命名 (PascalCase) 用于组件，小驼峰命名 (camelCase) 用于工具函数
- 组件名: 大驼峰命名 (PascalCase)
- 函数名: 小驼峰命名 (camelCase)
- 常量: 大写字母 + 下划线 (UPPER_SNAKE_CASE)

## 提交信息规范

使用 Conventional Commits 格式：

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

类型包括：

- `feat`: 新功能
- `fix`: 修复 bug
- `docs`: 文档更新
- `style`: 代码格式调整
- `refactor`: 代码重构
- `test`: 测试相关
- `chore`: 构建过程或辅助工具的变动

## 分支管理

- `main`: 生产环境分支
- `develop`: 开发环境分支
- `feature/*`: 功能开发分支
- `hotfix/*`: 紧急修复分支
- `release/*`: 发布准备分支

遵循以上规范开发，确保代码质量和项目可维护性。
