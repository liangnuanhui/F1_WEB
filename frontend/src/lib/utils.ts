import { type ClassValue, clsx } from "clsx";
import { twMerge } from "tailwind-merge";
import { countryCodeMap } from "./country-code-map";
import { nationalityToFlagCode } from "./nationality-to-flag-code";

// 合并 Tailwind CSS 类名的工具函数
export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

// 格式化日期
export function formatDate(
  date: string | Date,
  format: "short" | "long" | "time" = "short"
): string {
  const d = new Date(date);

  switch (format) {
    case "short":
      return d.toLocaleDateString("zh-CN", {
        year: "numeric",
        month: "short",
        day: "numeric",
      });
    case "long":
      return d.toLocaleDateString("zh-CN", {
        year: "numeric",
        month: "long",
        day: "numeric",
        weekday: "long",
      });
    case "time":
      return d.toLocaleTimeString("zh-CN", {
        hour: "2-digit",
        minute: "2-digit",
      });
    default:
      return d.toLocaleDateString("zh-CN");
  }
}

// 格式化时间
export function formatTime(time: string): string {
  if (!time) return "";
  return time.substring(0, 5); // 只显示 HH:MM
}

// 格式化比赛名称
export function formatRaceName(name: string): string {
  return name.replace("Grand Prix", "大奖赛");
}

// 获取国家/地区三位码
export function getCountryCode(country: string): string | undefined {
  if (!country) return undefined;
  // 完全匹配
  if (countryCodeMap[country]) {
    return countryCodeMap[country];
  }
  // 模糊匹配 (例如 "UK" 匹配 "United Kingdom")
  const lowerCountry = country.toLowerCase();
  for (const key in countryCodeMap) {
    if (key.toLowerCase().includes(lowerCountry)) {
      return countryCodeMap[key];
    }
  }
  return undefined;
}

// 新增：根据国籍获取两位字母的国旗代码
export function getFlagCodeByNationality(
  nationality: string
): string | undefined {
  return nationalityToFlagCode[nationality];
}

// 新增：根据国家名称获取国旗 emoji
export function getCountryFlag(country: string): string {
  const countryCode = getCountryCode(country);
  if (!countryCode) return "🏴"; // 默认旗帜

  // 将国家代码转换为 emoji 旗帜
  // 例如 "GB" -> 🇬🇧
  const codePoints = countryCode
    .toUpperCase()
    .split("")
    .map((char) => 127397 + char.charCodeAt(0));
  return String.fromCodePoint(...codePoints);
}

// 处理比赛地点特殊显示名称
export function getCountryName(race: {
  round_number: number;
  location?: string;
  circuit?: { country?: string };
  country?: string;
}): string {
  const specialLocRounds = [0, 6, 7, 22]; // e.g., Testing, Miami, Imola
  if (specialLocRounds.includes(race.round_number) && race.location) {
    return race.location;
  }
  return race.circuit?.country || race.country || "Unknown";
}

// 格式化车手姓名
export function formatDriverName(forename: string, surname: string): string {
  return `${forename} ${surname}`;
}

// 格式化车队名称
export function formatConstructorName(name: string): string {
  const nameMap: Record<string, string> = {
    "Red Bull Racing": "红牛",
    Mercedes: "梅赛德斯",
    Ferrari: "法拉利",
    McLaren: "迈凯伦",
    "Aston Martin": "阿斯顿马丁",
    Alpine: "阿尔派",
    Williams: "威廉姆斯",
    "Haas F1 Team": "哈斯",
    "Alfa Romeo": "阿尔法罗密欧",
    AlphaTauri: "阿尔法塔里",
  };

  return nameMap[name] || name;
}

// 延迟函数
export function delay(ms: number): Promise<void> {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

// 防抖函数
export function debounce<T extends (...args: unknown[]) => unknown>(
  func: T,
  wait: number
): (...args: Parameters<T>) => void {
  let timeout: NodeJS.Timeout;

  return (...args: Parameters<T>) => {
    clearTimeout(timeout);
    timeout = setTimeout(() => func(...args), wait);
  };
}

// 节流函数
export function throttle<T extends (...args: unknown[]) => unknown>(
  func: T,
  limit: number
): (...args: Parameters<T>) => void {
  let inThrottle: boolean;

  return (...args: Parameters<T>) => {
    if (!inThrottle) {
      func(...args);
      inThrottle = true;
      setTimeout(() => (inThrottle = false), limit);
    }
  };
}

// 生成唯一 ID
export function generateId(): string {
  return Math.random().toString(36).substr(2, 9);
}

// 检查是否为移动设备
export function isMobile(): boolean {
  if (typeof window === "undefined") return false;
  return window.innerWidth < 768;
}

// 检查是否为平板设备
export function isTablet(): boolean {
  if (typeof window === "undefined") return false;
  return window.innerWidth >= 768 && window.innerWidth < 1024;
}

// 检查是否为桌面设备
export function isDesktop(): boolean {
  if (typeof window === "undefined") return false;
  return window.innerWidth >= 1024;
}

// 通用的错误处理工具
export interface ErrorState {
  message: string;
  code?: string;
  statusCode?: number;
  timestamp?: Date;
}

export function createErrorState(error: unknown): ErrorState {
  if (error instanceof Error) {
    return {
      message: error.message,
      timestamp: new Date(),
    };
  }

  if (typeof error === "string") {
    return {
      message: error,
      timestamp: new Date(),
    };
  }

  return {
    message: "发生了未知错误",
    timestamp: new Date(),
  };
}

export function getErrorMessage(error: unknown): string {
  if (error instanceof Error) {
    return error.message;
  }

  if (typeof error === "string") {
    return error;
  }

  return "发生了未知错误";
}

// 通用的加载状态管理工具
export interface LoadingState {
  isLoading: boolean;
  message?: string;
  progress?: number;
}

export function createLoadingState(
  isLoading: boolean,
  message?: string,
  progress?: number
): LoadingState {
  return {
    isLoading,
    message,
    progress,
  };
}

// 通用的数据状态管理工具
export interface DataState<T> {
  data?: T;
  isLoading: boolean;
  error?: ErrorState;
  isSuccess: boolean;
  isEmpty: boolean;
}

export function createDataState<T>(options: {
  data?: T;
  isLoading: boolean;
  error?: unknown;
}): DataState<T> {
  const { data, isLoading, error } = options;

  return {
    data,
    isLoading,
    error: error ? createErrorState(error) : undefined,
    isSuccess: !isLoading && !error && data !== undefined,
    isEmpty:
      !isLoading &&
      !error &&
      (data === undefined ||
        data === null ||
        (Array.isArray(data) && data.length === 0)),
  };
}

// 合并多个数据状态
export function mergeDataStates<
  T extends Record<
    string,
    {
      isLoading: boolean;
      error?: ErrorState;
      isSuccess: boolean;
      isEmpty: boolean;
    }
  >,
>(
  states: T
): {
  isLoading: boolean;
  error?: ErrorState;
  hasError: boolean;
  isSuccess: boolean;
  isEmpty: boolean;
} {
  const stateValues = Object.values(states);

  const isLoading = stateValues.some((state) => state.isLoading);
  const errors = stateValues
    .filter((state) => state.error)
    .map((state) => state.error);
  const hasError = errors.length > 0;
  const isSuccess =
    !isLoading && !hasError && stateValues.every((state) => state.isSuccess);
  const isEmpty =
    !isLoading && !hasError && stateValues.every((state) => state.isEmpty);

  return {
    isLoading,
    error: errors[0], // 返回第一个错误
    hasError,
    isSuccess,
    isEmpty,
  };
}
