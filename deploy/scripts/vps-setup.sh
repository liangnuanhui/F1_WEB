#!/bin/bash

# F1 Web Application VPS Deployment Script
# 适用于已有Caddy、MySQL、VPN服务的VPS环境

set -e

echo "🚀 开始F1项目VPS部署..."

# 配置变量
F1_USER="f1web"
F1_HOME="/var/www/f1-web"
DB_NAME="f1_web_db"
DB_USER="f1_web_user"
# 从环境变量读取密码，或提示用户输入
DB_PASSWORD="${F1_DB_PASSWORD:-$(openssl rand -base64 32 | tr -d '=+/' | cut -c1-25)}"

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

print_step() {
    echo -e "${GREEN}[STEP]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# 检查是否为root用户
if [[ $EUID -ne 0 ]]; then
   print_error "请使用root权限运行此脚本: sudo $0"
   exit 1
fi

print_step "🔧 1. 更新系统并安装依赖..."
apt update && apt upgrade -y
apt install -y curl wget git python3 python3-pip python3-venv nodejs npm postgresql postgresql-contrib redis-server supervisor htop

print_step "👤 2. 创建F1项目专用用户..."
if ! id "$F1_USER" &>/dev/null; then
    useradd -m -s /bin/bash "$F1_USER"
    usermod -aG www-data "$F1_USER"
    print_step "✅ 用户 $F1_USER 创建成功"
else
    print_warning "用户 $F1_USER 已存在"
fi

print_step "📁 3. 创建项目目录结构..."
mkdir -p "$F1_HOME"/{backend,frontend,logs,data,scripts}
mkdir -p "$F1_HOME/data/fastf1_cache"
chown -R "$F1_USER":www-data "$F1_HOME"
chmod -R 755 "$F1_HOME"

print_step "🗄️ 4. 配置PostgreSQL数据库..."
# 启动PostgreSQL服务
systemctl enable postgresql
systemctl start postgresql

# 创建数据库和用户
echo "生成的数据库密码: $DB_PASSWORD" > /tmp/f1_db_password.txt
echo "请保存此密码到安全位置！"
sudo -u postgres psql -c "CREATE USER $DB_USER WITH PASSWORD '$DB_PASSWORD';" 2>/dev/null || print_warning "用户 $DB_USER 可能已存在"
sudo -u postgres psql -c "CREATE DATABASE $DB_NAME OWNER $DB_USER;" 2>/dev/null || print_warning "数据库 $DB_NAME 可能已存在"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE $DB_NAME TO $DB_USER;"
sudo -u postgres psql -c "ALTER USER $DB_USER CREATEDB;"

print_step "📦 5. 配置Redis服务..."
systemctl enable redis-server
systemctl start redis-server

# 优化Redis配置
echo "maxmemory 256mb" >> /etc/redis/redis.conf
echo "maxmemory-policy allkeys-lru" >> /etc/redis/redis.conf
systemctl restart redis-server

print_step "🐍 6. 设置Python环境..."
# 安装Poetry (用于依赖管理)
curl -sSL https://install.python-poetry.org | sudo -u "$F1_USER" python3 -
export PATH="/home/$F1_USER/.local/bin:$PATH"

# 创建Python虚拟环境
sudo -u "$F1_USER" python3 -m venv "$F1_HOME/backend/.venv"

print_step "📋 7. 安装systemd服务文件..."
# 这些文件需要从deploy目录复制
cp /tmp/deploy/systemd/*.service /etc/systemd/system/
systemctl daemon-reload

print_step "📝 8. 创建环境配置文件..."
cp /tmp/deploy/config/.env.vps "$F1_HOME/.env"
chown "$F1_USER":www-data "$F1_HOME/.env"
chmod 600 "$F1_HOME/.env"

print_step "🔐 9. 配置防火墙..."
# 开放必要端口
ufw allow 22    # SSH
ufw allow 80    # HTTP
ufw allow 443   # HTTPS
ufw allow 8000  # F1 API (仅内部访问)

print_step "📊 10. 检查端口占用..."
netstat -tlnp | grep -E ':3000|:8000' || print_step "✅ 端口 3000 和 8000 可用"

print_step "✅ VPS基础环境配置完成！"
echo
echo "📋 下一步操作："
echo "1. 将项目代码克隆到 $F1_HOME/backend"
echo "2. 安装Python依赖: cd $F1_HOME/backend && poetry install"
echo "3. 运行数据库迁移: poetry run alembic upgrade head"
echo "4. 构建前端应用并部署"
echo "5. 启动systemd服务"
echo "6. 配置Caddy反向代理"
echo
echo "🔗 数据库连接信息："
echo "  Host: localhost:5432"
echo "  Database: $DB_NAME"
echo "  User: $DB_USER"
echo "  Password: $DB_PASSWORD"
echo
echo "🎯 服务管理命令："
echo "  启动: systemctl start f1-api f1-worker f1-beat"
echo "  状态: systemctl status f1-api f1-worker f1-beat"
echo "  日志: journalctl -f -u f1-api"