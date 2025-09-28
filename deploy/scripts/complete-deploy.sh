#!/bin/bash

# F1 Web Complete Deployment Script
# 完整的VPS部署流程自动化脚本

set -e

# 配置变量
F1_USER="f1web"
F1_HOME="/var/www/f1-web"
REPO_URL="https://github.com/liangnuanhui/F1_WEB.git"
BRANCH="vps-deployment"

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

print_header() {
    echo -e "${BLUE}================================================${NC}"
    echo -e "${BLUE} $1${NC}"
    echo -e "${BLUE}================================================${NC}"
}

print_step() {
    echo -e "${GREEN}[STEP]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
    exit 1
}

# 检查是否为root用户
if [[ $EUID -ne 0 ]]; then
   print_error "请使用root权限运行此脚本: sudo $0"
fi

print_header "F1 Web Application 完整部署开始"

print_step "🔍 1. 运行基础环境设置..."
if [ -f "/tmp/deploy/scripts/vps-setup.sh" ]; then
    bash /tmp/deploy/scripts/vps-setup.sh
else
    print_error "找不到基础设置脚本，请先上传deploy目录到/tmp/"
fi

print_step "📂 2. 克隆项目代码..."
if [ -d "$F1_HOME/backend" ]; then
    print_warning "后端目录已存在，更新代码..."
    cd "$F1_HOME/backend"
    sudo -u "$F1_USER" git pull origin "$BRANCH"
else
    print_step "克隆后端代码..."
    sudo -u "$F1_USER" git clone -b "$BRANCH" "$REPO_URL" "$F1_HOME/temp"
    sudo -u "$F1_USER" mv "$F1_HOME/temp/backend" "$F1_HOME/"
    sudo -u "$F1_USER" mv "$F1_HOME/temp/frontend" "$F1_HOME/"
    sudo -u "$F1_USER" rm -rf "$F1_HOME/temp"
fi

print_step "🐍 3. 安装Python依赖..."
cd "$F1_HOME/backend"

# 检查Poetry是否可用
POETRY_PATH=$(which poetry 2>/dev/null || echo "/home/$F1_USER/.local/bin/poetry")
if [ ! -x "$POETRY_PATH" ]; then
    print_error "Poetry未安装或不可执行，请先运行基础设置脚本"
fi

# 检查pyproject.toml文件
if [ ! -f "pyproject.toml" ]; then
    print_error "未找到pyproject.toml文件，请确认代码已正确克隆"
fi

print_step "使用Poetry安装依赖: $POETRY_PATH"
sudo -u "$F1_USER" "$POETRY_PATH" install --no-dev

print_step "🗄️ 4. 运行数据库迁移..."
# 检查数据库连接
if ! sudo -u postgres psql -d "$DB_NAME" -c "SELECT 1;" > /dev/null 2>&1; then
    print_error "无法连接数据库 $DB_NAME，请检查PostgreSQL配置"
fi

# 检查alembic配置
if [ ! -f "alembic.ini" ]; then
    print_error "未找到alembic.ini文件，无法运行数据库迁移"
fi

sudo -u "$F1_USER" "$POETRY_PATH" run alembic upgrade head

print_step "🎨 5. 构建前端应用..."
if [ ! -f "/tmp/deploy/scripts/build-frontend.sh" ]; then
    print_error "前端构建脚本不存在: /tmp/deploy/scripts/build-frontend.sh"
fi

bash /tmp/deploy/scripts/build-frontend.sh

print_step "⚙️ 6. 启动systemd服务..."
systemctl enable f1-api f1-worker f1-beat
systemctl start f1-api f1-worker f1-beat

# 等待服务启动
sleep 5

print_step "🔍 7. 检查服务状态..."
for service in f1-api f1-worker f1-beat; do
    if systemctl is-active --quiet "$service"; then
        echo -e "  ✅ $service: ${GREEN}运行中${NC}"
    else
        echo -e "  ❌ $service: ${RED}未运行${NC}"
        print_warning "查看服务日志: journalctl -u $service -f"
    fi
done

print_step "🌐 8. 配置Caddy反向代理..."
# 备份现有配置
cp /etc/caddy/Caddyfile /etc/caddy/Caddyfile.backup.$(date +%Y%m%d_%H%M%S)

# 添加F1配置到Caddyfile
cat /tmp/deploy/config/f1-caddy.conf >> /etc/caddy/Caddyfile

# 重新加载Caddy
systemctl reload caddy

print_step "🧪 9. 运行部署测试..."
sleep 3

# 测试API端点
if curl -f -s http://localhost:8000/api/v1/health > /dev/null; then
    echo -e "  ✅ API服务: ${GREEN}正常${NC}"
else
    echo -e "  ❌ API服务: ${RED}异常${NC}"
fi

# 测试Redis连接
if redis-cli ping | grep -q PONG; then
    echo -e "  ✅ Redis服务: ${GREEN}正常${NC}"
else
    echo -e "  ❌ Redis服务: ${RED}异常${NC}"
fi

# 测试数据库连接
if sudo -u postgres psql -d f1_web_db -c "SELECT 1;" > /dev/null 2>&1; then
    echo -e "  ✅ 数据库: ${GREEN}正常${NC}"
else
    echo -e "  ❌ 数据库: ${RED}异常${NC}"
fi

print_header "部署完成！"

echo
echo "🎉 F1 Web应用部署成功！"
echo
echo "📋 访问信息："
echo "  🌐 网站地址: https://f1.251125.xyz"
echo "  🔧 API文档: https://f1.251125.xyz/api/v1/docs"
echo
echo "📊 服务管理命令："
echo "  状态检查: systemctl status f1-api f1-worker f1-beat"
echo "  重启服务: systemctl restart f1-api f1-worker f1-beat"
echo "  查看日志: journalctl -f -u f1-api"
echo "  Caddy日志: tail -f /var/log/caddy/f1.251125.xyz.log"
echo
echo "🔧 常用维护命令："
echo "  更新代码: cd $F1_HOME/backend && sudo -u $F1_USER git pull"
echo "  重新构建: bash /tmp/deploy/scripts/build-frontend.sh"
echo "  数据迁移: cd $F1_HOME/backend && sudo -u $F1_USER poetry run alembic upgrade head"
echo
echo "📈 监控地址："
echo "  系统监控: htop"
echo "  Redis监控: redis-cli monitor"
echo "  数据库监控: sudo -u postgres psql -d f1_web_db"
echo
echo "✅ 部署完成，F1应用已可正常访问！"