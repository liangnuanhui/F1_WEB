import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  // 输出配置 - 仅在生产环境使用静态导出
  ...(process.env.NODE_ENV === 'production' && {
    output: 'export',
    trailingSlash: true,
    distDir: 'dist',
  }),

  // 性能优化配置
  turbopack: {
    rules: {
      "*.svg": {
        loaders: ["@svgr/webpack"],
        as: "*.js",
      },
    },
  },

  // 图片优化
  images: {
    // 静态导出时禁用优化，开发环境保持优化
    ...(process.env.NODE_ENV === 'production'
      ? { unoptimized: true }
      : {
          remotePatterns: [
            {
              protocol: "http",
              hostname: "localhost",
              port: "3000",
              pathname: "/**",
            },
            {
              protocol: "http",
              hostname: "127.0.0.1",
              port: "3000",
              pathname: "/**",
            },
          ],
          formats: ["image/webp", "image/avif"],
          deviceSizes: [640, 750, 828, 1080, 1200, 1920, 2048, 3840],
          imageSizes: [16, 32, 48, 64, 96, 128, 256, 384],
        }
    ),
  },

  // 减少不必要的文件监控
  webpack: (config, { dev, isServer }) => {
    if (dev && !isServer) {
      // 开发环境优化
      config.watchOptions = {
        poll: 1000,
        aggregateTimeout: 300,
        ignored: ["**/node_modules", "**/.git", "**/.next"],
      };
    }

    return config;
  },

  async rewrites() {
    // 仅在开发环境启用API重写
    if (process.env.NODE_ENV === "development") {
      return [
        {
          source: "/api/:path*",
          destination: "http://127.0.0.1:8000/api/:path*", // 开发环境后端地址
        },
      ];
    }
    return []; // 生产环境不使用重写，由Caddy处理
  },
};

export default nextConfig;
