#!/bin/bash

# F1 Web Application 真正的一键部署脚本
# 基于VPS实际环境优化: Ubuntu 24.04, Node 22.20, Python 3.12

set -e

# 配置变量
F1_USER="f1web"
F1_HOME="/var/www/f1-web"
DB_NAME="f1_web_db"
DB_USER="f1_web_user"
DB_PASSWORD=$(openssl rand -base64 32 | tr -d '=+/' | cut -c1-25)
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

print_header "F1 Web Application 一键部署开始"

print_step "🔍 1. 验证环境依赖..."
# 检查必要命令
for cmd in python3 node npm git curl; do
    if ! command -v $cmd &> /dev/null; then
        print_error "$cmd 未安装，请先安装"
    fi
done

# 检查版本兼容性
PYTHON_VERSION=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
NODE_VERSION=$(node -v | sed 's/v//' | cut -d'.' -f1)

if (( $(echo "$PYTHON_VERSION < 3.9" | bc -l) )); then
    print_error "Python版本过低，需要3.9+，当前: $PYTHON_VERSION"
fi

if [ "$NODE_VERSION" -lt 18 ]; then
    print_error "Node.js版本过低，需要18+，当前: $(node -v)"
fi

# 检查PostgreSQL版本（16.x兼容）
if command -v psql &> /dev/null; then
    PG_VERSION=$(sudo -u postgres psql -t -c "SELECT version();" | grep -oP 'PostgreSQL \K[0-9]+')
    if [ "$PG_VERSION" -lt 12 ]; then
        print_error "PostgreSQL版本过低，需要12+，当前: $PG_VERSION"
    fi
    print_step "✅ PostgreSQL $PG_VERSION 兼容"
else
    print_error "PostgreSQL未安装"
fi

# 检查Redis版本（7.x兼容）
if command -v redis-cli &> /dev/null; then
    REDIS_VERSION=$(redis-cli --version | grep -oP 'redis-cli \K[0-9]+\.[0-9]+')
    print_step "✅ Redis $REDIS_VERSION 兼容"
else
    print_error "Redis未安装"
fi

# 检查服务状态
if ! systemctl is-active --quiet postgresql; then
    print_error "PostgreSQL未运行，请启动: systemctl start postgresql"
fi

if ! systemctl is-active --quiet redis-server; then
    print_error "Redis未运行，请启动: systemctl start redis-server"
fi

print_step "✅ 环境检查通过"

print_step "👤 2. 创建F1项目用户..."
if ! id "$F1_USER" &>/dev/null; then
    useradd -m -s /bin/bash "$F1_USER"
    usermod -aG www-data "$F1_USER"
    print_step "✅ 用户 $F1_USER 创建成功"
else
    print_warning "用户 $F1_USER 已存在"
fi

print_step "📁 3. 创建项目目录..."
mkdir -p "$F1_HOME"/{backend,frontend,logs,data}
mkdir -p "$F1_HOME/data/fastf1_cache"
chown -R "$F1_USER":www-data "$F1_HOME"
chmod -R 755 "$F1_HOME"

print_step "🗄️ 4. 配置PostgreSQL数据库..."
# 创建数据库用户和数据库
if ! sudo -u postgres psql -c "SELECT 1 FROM pg_user WHERE usename='$DB_USER';" | grep -q 1; then
    sudo -u postgres psql -c "CREATE USER $DB_USER WITH PASSWORD '$DB_PASSWORD';"
    print_step "✅ 数据库用户创建成功"
else
    print_warning "数据库用户已存在，更新密码"
    sudo -u postgres psql -c "ALTER USER $DB_USER WITH PASSWORD '$DB_PASSWORD';"
fi

if ! sudo -u postgres psql -lqt | cut -d \| -f 1 | grep -qw "$DB_NAME"; then
    sudo -u postgres psql -c "CREATE DATABASE $DB_NAME OWNER $DB_USER;"
    print_step "✅ 数据库创建成功"
else
    print_warning "数据库已存在"
fi

sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE $DB_NAME TO $DB_USER;"
sudo -u postgres psql -c "ALTER USER $DB_USER CREATEDB;"

print_step "🐍 5. 安装Poetry..."
if ! sudo -u "$F1_USER" test -f "/home/$F1_USER/.local/bin/poetry"; then
    curl -sSL https://install.python-poetry.org | sudo -u "$F1_USER" python3 -
    print_step "✅ Poetry安装成功"
else
    print_warning "Poetry已安装"
fi

print_step "📂 6. 克隆项目代码..."
if [ -d "$F1_HOME/backend" ]; then
    print_warning "代码目录已存在，更新代码..."
    cd "$F1_HOME/backend"
    sudo -u "$F1_USER" git pull origin "$BRANCH"
else
    sudo -u "$F1_USER" git clone -b "$BRANCH" "$REPO_URL" "$F1_HOME/temp"
    sudo -u "$F1_USER" mv "$F1_HOME/temp/backend" "$F1_HOME/"
    sudo -u "$F1_USER" mv "$F1_HOME/temp/frontend" "$F1_HOME/"
    sudo -u "$F1_USER" rm -rf "$F1_HOME/temp"
    print_step "✅ 代码克隆成功"
fi

print_step "📦 7. 安装Python依赖..."
cd "$F1_HOME/backend"
sudo -u "$F1_USER" /home/"$F1_USER"/.local/bin/poetry install --no-dev

print_step "📝 8. 创建环境配置..."
cat > "$F1_HOME/.env" << EOF
# F1 Web Application - Production Environment
DATABASE_URL=postgresql://$DB_USER:$DB_PASSWORD@localhost:5432/$DB_NAME
DB_HOST=localhost
DB_PORT=5432
DB_NAME=$DB_NAME
DB_USER=$DB_USER
DB_PASSWORD=$DB_PASSWORD

REDIS_URL=redis://localhost:6379/0
CELERY_BROKER_URL=redis://localhost:6379/1
CELERY_RESULT_BACKEND=redis://localhost:6379/1

APP_ENV=production
DEBUG=false
SECRET_KEY=$(openssl rand -base64 32 | tr -d '=+/' | cut -c1-50)
API_V1_STR=/api/v1

CORS_ORIGINS=https://f1.251125.xyz
CORS_ALLOW_CREDENTIALS=true

FASTF1_CACHE_DIR=$F1_HOME/data/fastf1_cache
FASTF1_LOG_LEVEL=INFO

LOG_LEVEL=INFO
LOG_FILE=$F1_HOME/logs/app.log
ACCESS_LOG=$F1_HOME/logs/access.log

TRUSTED_HOSTS=f1.251125.xyz,localhost
MAX_REQUEST_SIZE=10485760
EOF

chown "$F1_USER":www-data "$F1_HOME/.env"
chmod 600 "$F1_HOME/.env"

print_step "🗄️ 9. 运行数据库迁移..."
sudo -u "$F1_USER" /home/"$F1_USER"/.local/bin/poetry run alembic upgrade head

print_step "🎨 10. 构建前端应用..."
cd "$F1_HOME/frontend"
npm ci --production=false

# 创建生产环境配置
cat > .env.local << EOF
NEXT_PUBLIC_API_URL=/api/v1
NODE_ENV=production
EOF

npm run build
chown -R "$F1_USER":www-data dist/

print_step "⚙️ 11. 安装systemd服务..."
cp /tmp/deploy/systemd/*.service /etc/systemd/system/
systemctl daemon-reload
systemctl enable f1-api f1-worker f1-beat

print_step "🌐 12. 配置Caddy..."
# 备份现有配置
if [ -f /etc/caddy/Caddyfile ]; then
    cp /etc/caddy/Caddyfile /etc/caddy/Caddyfile.backup.$(date +%Y%m%d_%H%M%S)
fi

# 添加F1配置
cat /tmp/deploy/config/f1-caddy.conf >> /etc/caddy/Caddyfile

print_step "🚀 13. 启动服务..."
systemctl start f1-api f1-worker f1-beat
systemctl reload caddy

print_step "🧪 14. 验证部署..."
sleep 5

# 检查服务状态
for service in f1-api f1-worker f1-beat; do
    if systemctl is-active --quiet "$service"; then
        echo -e "  ✅ $service: ${GREEN}运行中${NC}"
    else
        echo -e "  ❌ $service: ${RED}未运行${NC}"
    fi
done

# 测试API
if curl -f -s http://localhost:8000/api/v1/health > /dev/null; then
    echo -e "  ✅ API服务: ${GREEN}正常${NC}"
else
    echo -e "  ❌ API服务: ${RED}异常${NC}"
fi

print_header "部署完成！"

echo
echo "🎉 F1 Web应用部署成功！"
echo
echo "📋 访问信息："
echo "  🌐 网站地址: https://f1.251125.xyz"
echo "  🔧 API文档: https://f1.251125.xyz/api/v1/docs"
echo
echo "🔑 数据库信息："
echo "  数据库密码已保存到: $F1_HOME/.env"
echo "  密码: $DB_PASSWORD"
echo
echo "📊 服务管理："
echo "  状态检查: systemctl status f1-api f1-worker f1-beat"
echo "  重启服务: systemctl restart f1-api f1-worker f1-beat"
echo "  查看日志: journalctl -f -u f1-api"
echo
echo "✅ 部署完成，F1应用已可正常访问！"