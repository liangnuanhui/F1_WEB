# 项目结构说明

```
F1-web/
├── README.md                    # 项目介绍和快速开始指南
├── CURSOR_RULES.md             # 开发规范和架构设计
├── PROJECT_STRUCTURE.md        # 项目结构说明 (本文件)
├── docker-compose.yml          # 开发环境 Docker 配置
├── .gitignore                  # Git 忽略文件
├── .env.example               # 环境变量示例
│
├── backend/                    # FastAPI 后端
│   ├── pyproject.toml         # Poetry 依赖管理
│   ├── alembic.ini           # 数据库迁移配置
│   ├── main.py               # FastAPI 应用入口
│   ├── requirements.txt      # 依赖列表 (备用)
│   │
│   ├── app/                  # 应用主目录
│   │   ├── __init__.py
│   │   ├── main.py          # FastAPI 应用实例
│   │   ├── core/            # 核心配置
│   │   │   ├── __init__.py
│   │   │   ├── config.py    # 应用配置
│   │   │   ├── database.py  # 数据库连接
│   │   │   ├── redis.py     # Redis 连接
│   │   │   └── security.py  # 安全相关
│   │   │
│   │   ├── api/             # API 路由
│   │   │   ├── __init__.py
│   │   │   ├── v1/         # API v1 版本
│   │   │   │   ├── __init__.py
│   │   │   │   ├── endpoints/
│   │   │   │   │   ├── __init__.py
│   │   │   │   │   ├── schedule.py    # 赛程 API
│   │   │   │   │   ├── races.py       # 比赛 API
│   │   │   │   │   ├── drivers.py     # 车手 API
│   │   │   │   │   ├── constructors.py # 车队 API
│   │   │   │   │   ├── circuits.py    # 赛道 API
│   │   │   │   │   ├── results.py     # 结果 API
│   │   │   │   │   └── standings.py   # 积分榜 API
│   │   │   │   └── websocket.py       # WebSocket 路由
│   │   │   └── deps.py      # 依赖注入
│   │   │
│   │   ├── models/          # 数据模型
│   │   │   ├── __init__.py
│   │   │   ├── base.py     # 基础模型
│   │   │   ├── schedule.py # 赛程模型
│   │   │   ├── race.py     # 比赛模型
│   │   │   ├── driver.py   # 车手模型
│   │   │   ├── constructor.py # 车队模型
│   │   │   ├── circuit.py  # 赛道模型
│   │   │   ├── result.py   # 结果模型
│   │   │   └── standing.py # 积分榜模型
│   │   │
│   │   ├── schemas/        # Pydantic 模式
│   │   │   ├── __init__.py
│   │   │   ├── schedule.py
│   │   │   ├── race.py
│   │   │   ├── driver.py
│   │   │   ├── constructor.py
│   │   │   ├── circuit.py
│   │   │   ├── result.py
│   │   │   └── standing.py
│   │   │
│   │   ├── services/       # 业务逻辑
│   │   │   ├── __init__.py
│   │   │   ├── fastf1_service.py  # FastF1 数据服务
│   │   │   ├── cache_service.py   # 缓存服务
│   │   │   ├── schedule_service.py
│   │   │   ├── race_service.py
│   │   │   ├── driver_service.py
│   │   │   ├── constructor_service.py
│   │   │   ├── circuit_service.py
│   │   │   ├── result_service.py
│   │   │   └── standing_service.py
│   │   │
│   │   ├── utils/          # 工具函数
│   │   │   ├── __init__.py
│   │   │   ├── timezone.py # 时区处理
│   │   │   ├── cache.py    # 缓存工具
│   │   │   ├── logger.py   # 日志工具
│   │   │   └── validators.py # 数据验证
│   │   │
│   │   └── tasks/          # Celery 任务
│   │       ├── __init__.py
│   │       ├── data_sync.py # 数据同步任务
│   │       └── cache_update.py # 缓存更新任务
│   │
│   ├── alembic/            # 数据库迁移
│   │   ├── versions/       # 迁移文件
│   │   ├── env.py         # 迁移环境
│   │   └── script.py.mako # 迁移模板
│   │
│   ├── tests/             # 测试
│   │   ├── __init__.py
│   │   ├── conftest.py   # 测试配置
│   │   ├── test_api/     # API 测试
│   │   ├── test_services/ # 服务测试
│   │   └── test_utils/   # 工具测试
│   │
│   └── init.sql          # 数据库初始化脚本
│
├── frontend/              # Next.js 前端
│   ├── package.json      # 依赖管理
│   ├── pnpm-lock.yaml   # 锁定文件
│   ├── next.config.js   # Next.js 配置
│   ├── tailwind.config.js # Tailwind 配置
│   ├── tsconfig.json    # TypeScript 配置
│   ├── .eslintrc.js     # ESLint 配置
│   ├── .prettierrc      # Prettier 配置
│   │
│   ├── public/          # 静态资源
│   │   ├── images/      # 图片资源
│   │   ├── icons/       # 图标资源
│   │   └── favicon.ico  # 网站图标
│   │
│   ├── src/             # 源代码
│   │   ├── app/         # App Router 页面
│   │   │   ├── layout.tsx      # 根布局
│   │   │   ├── page.tsx        # 首页
│   │   │   ├── schedule/       # 赛程页
│   │   │   │   └── page.tsx
│   │   │   ├── races/          # 比赛页
│   │   │   │   ├── page.tsx
│   │   │   │   └── [id]/       # 单场比赛
│   │   │   │       └── page.tsx
│   │   │   ├── drivers/        # 车手页
│   │   │   │   ├── page.tsx
│   │   │   │   └── [id]/       # 单个车手
│   │   │   │       └── page.tsx
│   │   │   ├── constructors/   # 车队页
│   │   │   │   ├── page.tsx
│   │   │   │   └── [id]/       # 单个车队
│   │   │   │       └── page.tsx
│   │   │   ├── circuits/       # 赛道页
│   │   │   │   ├── page.tsx
│   │   │   │   └── [id]/       # 单个赛道
│   │   │   │       └── page.tsx
│   │   │   └── standings/      # 积分榜页
│   │   │       └── page.tsx
│   │   │
│   │   ├── components/  # React 组件
│   │   │   ├── ui/      # 基础 UI 组件
│   │   │   │   ├── Button.tsx
│   │   │   │   ├── Card.tsx
│   │   │   │   ├── Table.tsx
│   │   │   │   ├── Modal.tsx
│   │   │   │   └── Loading.tsx
│   │   │   │
│   │   │   ├── layout/  # 布局组件
│   │   │   │   ├── Header.tsx
│   │   │   │   ├── Footer.tsx
│   │   │   │   ├── Sidebar.tsx
│   │   │   │   └── Navigation.tsx
│   │   │   │
│   │   │   ├── schedule/ # 赛程相关组件
│   │   │   │   ├── ScheduleCard.tsx
│   │   │   │   ├── CountdownTimer.tsx
│   │   │   │   └── TimezoneSelector.tsx
│   │   │   │
│   │   │   ├── race/     # 比赛相关组件
│   │   │   │   ├── RaceCard.tsx
│   │   │   │   ├── ResultsTable.tsx
│   │   │   │   ├── LapChart.tsx
│   │   │   │   └── LiveData.tsx
│   │   │   │
│   │   │   ├── driver/   # 车手相关组件
│   │   │   │   ├── DriverCard.tsx
│   │   │   │   ├── DriverStats.tsx
│   │   │   │   └── CareerTimeline.tsx
│   │   │   │
│   │   │   ├── constructor/ # 车队相关组件
│   │   │   │   ├── ConstructorCard.tsx
│   │   │   │   ├── TeamStats.tsx
│   │   │   │   └── DriverPair.tsx
│   │   │   │
│   │   │   ├── circuit/  # 赛道相关组件
│   │   │   │   ├── CircuitCard.tsx
│   │   │   │   ├── TrackLayout.tsx
│   │   │   │   └── CircuitStats.tsx
│   │   │   │
│   │   │   └── standings/ # 积分榜相关组件
│   │   │       ├── StandingsTable.tsx
│   │   │       ├── PointsChart.tsx
│   │   │       └── SeasonProgress.tsx
│   │   │
│   │   ├── hooks/        # 自定义 Hooks
│   │   │   ├── useApi.ts        # API 调用 Hook
│   │   │   ├── useWebSocket.ts  # WebSocket Hook
│   │   │   ├── useLocalStorage.ts # 本地存储 Hook
│   │   │   ├── useTimezone.ts   # 时区 Hook
│   │   │   └── useDebounce.ts   # 防抖 Hook
│   │   │
│   │   ├── lib/          # 工具库
│   │   │   ├── api.ts           # API 客户端
│   │   │   ├── websocket.ts     # WebSocket 客户端
│   │   │   ├── utils.ts         # 通用工具函数
│   │   │   ├── constants.ts     # 常量定义
│   │   │   └── types.ts         # TypeScript 类型
│   │   │
│   │   ├── store/        # 状态管理
│   │   │   ├── index.ts         # Store 入口
│   │   │   ├── appStore.ts      # 应用状态
│   │   │   ├── userStore.ts     # 用户状态
│   │   │   └── websocketStore.ts # WebSocket 状态
│   │   │
│   │   └── styles/       # 样式文件
│   │       ├── globals.css      # 全局样式
│   │       └── components.css   # 组件样式
│   │
│   └── tests/           # 测试
│       ├── __init__.py
│       ├── components/  # 组件测试
│       ├── hooks/       # Hook 测试
│       └── utils/       # 工具测试
│
├── docs/                # 文档
│   ├── api/            # API 文档
│   ├── deployment/     # 部署文档
│   └── development/    # 开发文档
│
└── scripts/            # 脚本文件
    ├── setup.sh        # 项目设置脚本
    ├── deploy.sh       # 部署脚本
    └── backup.sh       # 备份脚本
```

## 文件说明

### 核心配置文件

- `README.md`: 项目介绍、快速开始、部署指南
- `CURSOR_RULES.md`: 详细的开发规范和架构设计
- `docker-compose.yml`: 开发环境的基础设施配置
- `.gitignore`: Git 版本控制忽略文件

### 后端结构

- `backend/app/`: FastAPI 应用主目录
- `backend/app/api/`: API 路由定义
- `backend/app/models/`: SQLAlchemy 数据模型
- `backend/app/schemas/`: Pydantic 数据验证模式
- `backend/app/services/`: 业务逻辑服务层
- `backend/app/utils/`: 工具函数和辅助模块

### 前端结构

- `frontend/src/app/`: Next.js App Router 页面
- `frontend/src/components/`: React 组件库
- `frontend/src/hooks/`: 自定义 React Hooks
- `frontend/src/lib/`: 工具库和类型定义
- `frontend/src/store/`: 状态管理 (Zustand)

### 开发工具

- `docs/`: 项目文档
- `scripts/`: 自动化脚本
- `tests/`: 测试文件

这个结构遵循了现代全栈应用的最佳实践，确保了代码的可维护性和可扩展性。
