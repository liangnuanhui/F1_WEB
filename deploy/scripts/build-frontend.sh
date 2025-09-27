#!/bin/bash

# F1 Frontend Build and Deploy Script for VPS

set -e

# 配置变量
F1_HOME="/var/www/f1-web"
FRONTEND_DIR="$F1_HOME/frontend"
BACKEND_DIR="$F1_HOME/backend"
BUILD_DIR="$FRONTEND_DIR/dist"

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

print_step() {
    echo -e "${GREEN}[BUILD]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
    exit 1
}

print_step "🏗️ 开始构建F1前端应用..."

# 检查Node.js版本
if ! command -v node &> /dev/null; then
    print_error "Node.js 未安装，请先安装 Node.js 18+"
fi

NODE_VERSION=$(node -v | cut -d 'v' -f 2 | cut -d '.' -f 1)
if [ "$NODE_VERSION" -lt 18 ]; then
    print_error "Node.js 版本过低，需要 18+，当前版本: $(node -v)"
fi

# 进入前端目录
cd "$FRONTEND_DIR" || print_error "前端目录不存在: $FRONTEND_DIR"

print_step "📦 安装依赖..."
npm ci --production=false

# 配置生产环境变量
print_step "🔧 配置生产环境变量..."
# 从环境变量读取API地址
API_BASE_URL="${VITE_API_BASE_URL:-https://f1.251125.xyz/api/v1}"

# 创建生产环境配置文件
cat > .env.production << EOF
# 生产环境配置
VITE_API_BASE_URL=$API_BASE_URL
VITE_APP_TITLE=F1 Web
VITE_APP_DESCRIPTION=Formula 1 Data Hub
VITE_APP_VERSION=1.0.0

# 生产优化
VITE_BUILD_SOURCEMAP=false
VITE_BUILD_MINIFY=true
VITE_CHUNK_SIZE_LIMIT=1000

# 静态资源CDN (可选)
# VITE_CDN_BASE_URL=https://cdn.yourdomain.com
EOF

print_step "🏗️ 构建生产版本..."
# 检查是否是Next.js项目
if [ -f "package.json" ] && grep -q "next" package.json; then
    npm run build
else
    # 如果是Vite项目
    npm run build
fi

# 检查构建结果
if [ ! -d "$BUILD_DIR" ]; then
    print_error "构建失败：未找到 dist 目录"
fi

# 检查构建文件
if [ ! -f "$BUILD_DIR/index.html" ]; then
    print_error "构建失败：未找到 index.html"
fi

print_step "📊 构建统计..."
BUILD_SIZE=$(du -sh "$BUILD_DIR" | cut -f1)
FILE_COUNT=$(find "$BUILD_DIR" -type f | wc -l)
echo "  构建大小: $BUILD_SIZE"
echo "  文件数量: $FILE_COUNT"
echo "  构建目录: $BUILD_DIR"

print_step "🔐 设置文件权限..."
chown -R f1web:www-data "$BUILD_DIR"
find "$BUILD_DIR" -type f -exec chmod 644 {} \;
find "$BUILD_DIR" -type d -exec chmod 755 {} \;

print_step "🧪 运行构建测试..."
# 检查关键文件
CRITICAL_FILES=("index.html" "assets")
for file in "${CRITICAL_FILES[@]}"; do
    if [ ! -e "$BUILD_DIR/$file" ]; then
        print_error "关键文件缺失: $file"
    fi
done

print_step "✅ 前端构建完成！"
echo
echo "📋 部署信息："
echo "  构建目录: $BUILD_DIR"
echo "  Caddy配置: root * $BUILD_DIR"
echo "  访问地址: https://f1.251125.xyz"
echo
echo "🚀 下一步："
echo "  1. 重新加载Caddy配置: systemctl reload caddy"
echo "  2. 检查网站访问: curl -I https://f1.251125.xyz"
echo "  3. 查看Caddy日志: tail -f /var/log/caddy/f1.251125.xyz.log"