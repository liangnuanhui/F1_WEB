import axios from "axios";

// 配置API基础URL
const getBaseURL = () => {
  // 优先使用环境变量中的API URL（VPS部署时设置此变量）
  if (process.env.NEXT_PUBLIC_API_URL) {
    return process.env.NEXT_PUBLIC_API_URL;
  }

  // 生产环境：前后端同部署在VPS时，使用相对路径或同域名
  if (process.env.NODE_ENV === "production") {
    // VPS部署建议：设置NEXT_PUBLIC_API_URL环境变量为你的VPS地址
    // 例如: https://your-vps-domain.com/api/v1 或 https://your-ip:8000/api/v1
    return "/api/v1"; // 默认使用相对路径，适合同域名部署
  }

  // 开发环境使用本地API
  return process.env.NEXT_PUBLIC_API_BASE_URL || "http://localhost:8000/api/v1";
};

const axiosInstance = axios.create({
  baseURL: getBaseURL(),
  timeout: 30000, // 30秒超时，因为Render免费服务可能需要冷启动
});

// 添加请求拦截器
axiosInstance.interceptors.request.use(
  (config) => {
    if (process.env.NODE_ENV === "development") {
      console.log(`🚀 API请求: ${config.method?.toUpperCase()} ${config.url}`);
    }
    return config;
  },
  (error) => {
    if (process.env.NODE_ENV === "development") {
      console.error("❌ API请求错误:", error);
    }
    return Promise.reject(error);
  }
);

// 添加响应拦截器
axiosInstance.interceptors.response.use(
  (response) => {
    if (process.env.NODE_ENV === "development") {
      console.log(`✅ API响应: ${response.status} ${response.config.url}`);
    }
    return response;
  },
  (error) => {
    if (process.env.NODE_ENV === "development") {
      console.error(
        "❌ API响应错误:",
        error.response?.status,
        error.response?.data
      );
    }
    return Promise.reject(error);
  }
);

export default axiosInstance;
