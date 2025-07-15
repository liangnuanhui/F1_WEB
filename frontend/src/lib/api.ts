import axiosInstance from "./axios";
import type { AxiosRequestConfig } from "axios";
import {
  PaginatedResponse,
  Season,
  Circuit,
  Race,
  Driver,
  Constructor,
  Result,
  QualifyingResult,
  SprintResult,
  DriverStanding,
  ConstructorStanding,
} from "@/types";

// 通用 API 请求函数
async function apiRequest<T>(
  endpoint: string,
  config: AxiosRequestConfig = {}
): Promise<T> {
  try {
    const response = await axiosInstance.get(endpoint, config);

    // 如果响应数据为空
    if (!response.data) {
      return {} as T;
    }

    // 检查是否为 ApiResponse 格式
    if (
      response.data &&
      typeof response.data === "object" &&
      "success" in response.data
    ) {
      // 如果是 ApiResponse 格式，提取 data 字段
      if (response.data.success) {
        // 确保返回的是有效数据
        if (response.data.data !== undefined && response.data.data !== null) {
          return response.data.data;
        } else {
          return response.data.data; // 即使为null/undefined也返回，让调用方处理
        }
      } else {
        // 处理业务错误
        throw new Error(response.data.message || "API 请求失败");
      }
    }

    // 如果不是 ApiResponse 格式，直接返回数据
    return response.data;
  } catch (error) {
    if (error instanceof Error) {
      throw error;
    }
    throw new Error("请求失败");
  }
}

// 赛季相关 API
export const seasonsApi = {
  // 获取所有赛季
  getAll: async (): Promise<Season[]> => {
    const response = await apiRequest<Season[]>("/seasons/");
    return response;
  },

  // 获取单个赛季
  getById: async (id: number): Promise<Season> => {
    const response = await apiRequest<Season>(`/seasons/${id}/`);
    return response;
  },

  // 获取当前赛季
  getCurrent: async (): Promise<Season> => {
    const response = await apiRequest<Season>("/seasons/active");
    return response;
  },
};

// 赛道相关 API
export const circuitsApi = {
  // 获取所有赛道
  getAll: async (params?: {
    page?: number;
    size?: number;
  }): Promise<PaginatedResponse<Circuit>> => {
    const searchParams = new URLSearchParams();
    if (params?.page) searchParams.append("page", params.page.toString());
    if (params?.size) searchParams.append("size", params.size.toString());

    const query = searchParams.toString();
    return apiRequest<PaginatedResponse<Circuit>>(
      `/circuits/${query ? `?${query}` : ""}`
    );
  },

  // 获取单个赛道
  getById: async (id: number): Promise<Circuit> => {
    const response = await apiRequest<Circuit>(`/circuits/${id}/`);
    return response;
  },
};

// 比赛相关 API
export const racesApi = {
  // 获取所有比赛
  getAll: async (params?: {
    season?: number;
    page?: number;
    size?: number;
  }): Promise<Race[]> => {
    const searchParams = new URLSearchParams();
    if (params?.season) searchParams.append("season", params.season.toString());
    if (params?.page) searchParams.append("page", params.page.toString());
    if (params?.size) searchParams.append("size", params.size.toString());

    const query = searchParams.toString();
    return apiRequest<Race[]>(`/races/${query ? `?${query}` : ""}`);
  },

  // 获取单个比赛
  getById: async (id: number): Promise<Race> => {
    return apiRequest<Race>(`/races/${id}/`);
  },

  // 获取即将到来的比赛
  getUpcoming: async (): Promise<Race[]> => {
    return apiRequest<Race[]>("/races/upcoming/");
  },
};

// 车手相关 API
export const driversApi = {
  // 获取所有车手
  getAll: async (params?: {
    page?: number;
    size?: number;
  }): Promise<PaginatedResponse<Driver>> => {
    const searchParams = new URLSearchParams();
    if (params?.page) searchParams.append("page", params.page.toString());
    if (params?.size) searchParams.append("size", params.size.toString());

    const query = searchParams.toString();
    return apiRequest<PaginatedResponse<Driver>>(
      `/drivers/${query ? `?${query}` : ""}`
    );
  },

  // 获取单个车手
  getById: async (id: number): Promise<Driver> => {
    const response = await apiRequest<Driver>(`/drivers/${id}/`);
    return response;
  },

  // 搜索车手
  search: async (query: string): Promise<Driver[]> => {
    const response = await apiRequest<Driver[]>(
      `/drivers/search/?q=${encodeURIComponent(query)}`
    );
    return response;
  },
};

// 车队相关 API
export const constructorsApi = {
  // 获取所有车队
  getConstructors: async (
    params: {
      page?: number;
      size?: number;
    } = { page: 1, size: 50 }
  ): Promise<PaginatedResponse<Constructor>> => {
    const searchParams = new URLSearchParams();
    if (params.page) searchParams.append("page", params.page.toString());
    if (params.size) searchParams.append("size", params.size.toString());

    const query = searchParams.toString();
    const data = await apiRequest<Constructor[]>(`/constructors/?${query}`);

    // 由于后端车队API不返回分页信息，构造基本的分页响应
    return {
      data: data,
      total: data.length,
      page: params.page || 1,
      size: params.size || 50,
      pages: 1,
    };
  },

  // 获取单个车队
  getById: async (id: number): Promise<Constructor> => {
    const response = await apiRequest<Constructor>(`/constructors/${id}/`);
    return response;
  },

  // 搜索车队
  search: async (query: string): Promise<Constructor[]> => {
    const response = await apiRequest<Constructor[]>(
      `/constructors/search/?q=${encodeURIComponent(query)}`
    );
    return response;
  },
};

// 比赛结果相关 API
export const resultsApi = {
  // 获取比赛结果
  getByRace: async (raceId: number): Promise<Result[]> => {
    const response = await apiRequest<Result[]>(`/results/race/${raceId}/`);
    return response;
  },

  // 获取车手结果
  getByDriver: async (
    driverId: number,
    params?: { season?: number }
  ): Promise<Result[]> => {
    const searchParams = new URLSearchParams();
    if (params?.season) searchParams.append("season", params.season.toString());

    const query = searchParams.toString();
    const response = await apiRequest<Result[]>(
      `/results/driver/${driverId}/${query ? `?${query}` : ""}`
    );
    return response;
  },

  // 获取车队结果
  getByConstructor: async (
    constructorId: number,
    params?: { season?: number }
  ): Promise<Result[]> => {
    const searchParams = new URLSearchParams();
    if (params?.season) searchParams.append("season", params.season.toString());

    const query = searchParams.toString();
    const response = await apiRequest<Result[]>(
      `/results/constructor/${constructorId}/${query ? `?${query}` : ""}`
    );
    return response;
  },
};

// 排位赛结果相关 API
export const qualifyingResultsApi = {
  // 获取排位赛结果
  getByRace: async (raceId: number): Promise<QualifyingResult[]> => {
    const response = await apiRequest<QualifyingResult[]>(
      `/qualifying/${raceId}/`
    );
    return response;
  },
};

// 短距离赛结果相关 API
export const sprintResultsApi = {
  // 获取短距离赛结果
  getByRace: async (raceId: number): Promise<SprintResult[]> => {
    const response = await apiRequest<SprintResult[]>(`/sprint/${raceId}/`);
    return response;
  },
};

// 积分榜相关 API
export const standingsApi = {
  // 获取车手积分榜
  getDriverStandings: async (
    year: number = new Date().getFullYear()
  ): Promise<DriverStanding[]> => {
    const response = await apiRequest<DriverStanding[]>(
      `/standings/drivers?year=${year}`
    );
    return response;
  },

  // 获取车队积分榜
  getConstructorStandings: async (
    year: number = new Date().getFullYear()
  ): Promise<ConstructorStanding[]> => {
    const response = await apiRequest<ConstructorStanding[]>(
      `/standings/constructors?year=${year}`
    );
    return response;
  },
};

// 数据初始化相关 API
export const dataInitApi = {
  // 初始化数据
  init: async (): Promise<unknown> => {
    const response = await apiRequest<unknown>("/data-init/");
    return response;
  },
};

// 导出所有 API
export const api = {
  seasons: seasonsApi,
  races: racesApi,
  drivers: driversApi,
  constructors: constructorsApi,
  results: resultsApi,
  qualifying: qualifyingResultsApi,
  sprint: sprintResultsApi,
  standings: standingsApi,
  circuits: circuitsApi,
  dataInit: dataInitApi,
};
