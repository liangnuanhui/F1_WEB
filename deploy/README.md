# F1 Web Application VPS 部署指南

## 📋 部署概述

本项目支持在已有Caddy、MySQL、VPN服务的VPS上部署F1 Web应用，包含：
- FastAPI后端API服务
- React前端SPA应用
- Celery任务队列和定时调度器
- PostgreSQL数据库
- Redis缓存

## 🏗️ 系统架构

```
Internet
    ↓
Caddy (反向代理)
    ↓
f1.251125.xyz
    ├── /api/* → FastAPI (localhost:8000)
    └── /* → React SPA (静态文件)

后台服务:
├── f1-api.service     (FastAPI后端)
├── f1-worker.service  (Celery Worker)
└── f1-beat.service    (Celery Beat调度器)

数据层:
├── PostgreSQL (5432) - F1数据存储
└── Redis (6379)      - 任务队列和缓存
```

## ⚡ 快速部署

### 1. 准备工作

确保您的VPS已有：
- ✅ Caddy反向代理
- ✅ MySQL (用于WordPress等)
- ✅ 基础的Linux环境
- ✅ 域名DNS解析 (`f1.251125.xyz` → VPS IP)

### 📋 部署信息
在使用自定义SSH端口(13578)的环境中，需要注意：

1. **防火墙配置**: 脚本会自动开放端口13578
2. **SSH连接**: 使用 `ssh -p 13578 root@172.245.39.166`
3. **文件传输**: 使用 `scp -P 13578` (注意大写P)

### 2. 上传部署文件

```bash
# 在本地打包部署文件
cd F1-web
tar -czf f1-deploy.tar.gz deploy/

# 上传到VPS (使用自定义端口)
scp -P 13578 f1-deploy.tar.gz root@172.245.39.166:/tmp/

# 连接到VPS并解压
ssh -p 13578 root@172.245.39.166
cd /tmp
tar -xzf f1-deploy.tar.gz
```

### 3. 一键部署

```bash
# 运行完整部署脚本
chmod +x /tmp/deploy/scripts/*.sh
bash /tmp/deploy/scripts/complete-deploy.sh
```

### 4. 验证部署

```bash
# 检查服务状态
systemctl status f1-api f1-worker f1-beat

# 测试API访问
curl https://f1.251125.xyz/api/v1/health

# 检查网站访问
curl -I https://f1.251125.xyz
```

## 📁 部署文件说明

```
deploy/
├── systemd/                 # systemd服务配置
│   ├── f1-api.service      # FastAPI后端服务
│   ├── f1-worker.service   # Celery Worker
│   └── f1-beat.service     # Celery Beat调度器
├── config/                 # 配置文件
│   ├── .env.vps           # VPS环境变量模板
│   └── f1-caddy.conf      # Caddy配置
└── scripts/               # 部署脚本
    ├── vps-setup.sh       # 基础环境设置
    ├── build-frontend.sh  # 前端构建
    └── complete-deploy.sh # 完整部署流程
```

## 🔧 手动部署步骤

如果需要分步骤部署：

### 步骤1: 基础环境设置
```bash
bash /tmp/deploy/scripts/vps-setup.sh
```

### 步骤2: 克隆代码
```bash
cd /var/www/f1-web
sudo -u f1web git clone -b vps-deployment https://github.com/liangnuanhui/F1_WEB.git temp
sudo -u f1web mv temp/backend ./
sudo -u f1web mv temp/frontend ./
sudo -u f1web rm -rf temp
```

### 步骤3: 安装依赖
```bash
cd /var/www/f1-web/backend
sudo -u f1web poetry install --no-dev
```

### 步骤4: 数据库迁移
```bash
sudo -u f1web poetry run alembic upgrade head
```

### 步骤5: 构建前端
```bash
bash /tmp/deploy/scripts/build-frontend.sh
```

### 步骤6: 启动服务
```bash
systemctl enable f1-api f1-worker f1-beat
systemctl start f1-api f1-worker f1-beat
```

### 步骤7: 配置Caddy
```bash
cat /tmp/deploy/config/f1-caddy.conf >> /etc/caddy/Caddyfile
systemctl reload caddy
```

## 🔍 服务管理

### 查看服务状态
```bash
systemctl status f1-api f1-worker f1-beat
```

### 查看服务日志
```bash
# API服务日志
journalctl -f -u f1-api

# Worker日志
journalctl -f -u f1-worker

# Beat调度器日志
journalctl -f -u f1-beat

# Caddy访问日志
tail -f /var/log/caddy/f1.251125.xyz.log
```

### 重启服务
```bash
systemctl restart f1-api f1-worker f1-beat
```

## 📊 数据同步功能

部署完成后，系统会自动：

1. **每天凌晨2点** - 检查即将到来的F1比赛
2. **比赛结束后** - 自动安排3、6、12小时后的数据更新
3. **自动同步** - 5类F1数据：排位赛、比赛结果、冲刺赛、积分榜

### 手动触发数据同步
```bash
# 为2025年第10轮比赛安排同步
curl -X POST "https://f1.251125.xyz/api/v1/post-race-sync/2025/10/schedule"

# 查看同步计划
curl "https://f1.251125.xyz/api/v1/post-race-sync/schedules"

# 查看系统统计
curl "https://f1.251125.xyz/api/v1/post-race-sync/stats"
```

## 🛠️ 故障排除

### 常见问题

**1. 服务启动失败**
```bash
# 检查依赖服务
systemctl status postgresql redis-server

# 检查配置文件
cat /var/www/f1-web/.env

# 检查权限
ls -la /var/www/f1-web/
```

**2. API无法访问**
```bash
# 检查端口占用
netstat -tlnp | grep 8000

# 检查防火墙
ufw status

# 测试本地API
curl localhost:8000/api/v1/health
```

**3. 前端无法访问**
```bash
# 检查构建文件
ls -la /var/www/f1-web/frontend/dist/

# 检查Caddy配置
caddy validate --config /etc/caddy/Caddyfile

# 重新加载Caddy
systemctl reload caddy
```

**4. 数据库连接失败**
```bash
# 测试数据库连接
sudo -u postgres psql -d f1_web_db -c "SELECT 1;"

# 检查数据库用户权限
sudo -u postgres psql -c "\du"
```

## 🔄 更新部署

### 使用SSH自定义端口更新代码
```bash
# 连接到VPS
ssh -p 13578 root@172.245.39.166

# 更新后端代码
cd /var/www/f1-web/backend
sudo -u f1web git pull origin vps-deployment
sudo -u f1web poetry install --no-dev
systemctl restart f1-api f1-worker f1-beat
```

### 更新前端
```bash
bash /tmp/deploy/scripts/build-frontend.sh
systemctl reload caddy
```

### 数据库迁移
```bash
cd /var/www/f1-web/backend
sudo -u f1web poetry run alembic upgrade head
```

## 📈 性能监控

### 系统资源
```bash
# CPU和内存使用
htop

# 磁盘使用
df -h

# 服务资源使用
systemctl status f1-api f1-worker f1-beat
```

### 应用监控
```bash
# Redis监控
redis-cli info

# 数据库连接
sudo -u postgres psql -d f1_web_db -c "SELECT count(*) FROM pg_stat_activity;"

# API响应测试
curl -w "%{time_total}\n" -o /dev/null -s https://f1.251125.xyz/api/v1/health
```

---

## 📞 支持

如有问题：
1. 检查服务日志：`journalctl -f -u f1-api`
2. 查看Caddy日志：`tail -f /var/log/caddy/f1.251125.xyz.log`
3. 测试API健康检查：`curl https://f1.251125.xyz/api/v1/health`

**部署成功后，F1 Web应用将完全自动化运行，包括数据同步和更新！** 🏎️