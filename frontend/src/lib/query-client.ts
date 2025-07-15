import { QueryClient } from "@tanstack/react-query";

// 创建 React Query 客户端
export const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      // 默认缓存时间：5分钟
      staleTime: 5 * 60 * 1000,
      // 默认垃圾回收时间：10分钟
      gcTime: 10 * 60 * 1000,
      // 重试次数
      retry: 3,
      // 重试延迟
      retryDelay: (attemptIndex) => Math.min(1000 * 2 ** attemptIndex, 30000),
      // 错误时重试
      retryOnMount: true,
      // 窗口重新获得焦点时重新获取数据
      refetchOnWindowFocus: false,
      // 网络重新连接时重新获取数据
      refetchOnReconnect: true,
    },
    mutations: {
      // 重试次数
      retry: 1,
      // 重试延迟
      retryDelay: 1000,
    },
  },
});

// 查询键常量
export const queryKeys = {
  // 赛季相关
  seasons: {
    all: ["seasons"] as const,
    lists: () => [...queryKeys.seasons.all, "list"] as const,
    list: (filters: string) =>
      [...queryKeys.seasons.lists(), { filters }] as const,
    details: () => [...queryKeys.seasons.all, "detail"] as const,
    detail: (id: number) => [...queryKeys.seasons.details(), id] as const,
    active: () => [...queryKeys.seasons.all, "active"] as const,
    current: () => [...queryKeys.seasons.all, "current"] as const,
  },

  // 赛道相关
  circuits: {
    all: ["circuits"] as const,
    lists: () => [...queryKeys.circuits.all, "list"] as const,
    list: (filters: string) =>
      [...queryKeys.circuits.lists(), { filters }] as const,
    details: () => [...queryKeys.circuits.all, "detail"] as const,
    detail: (id: number) => [...queryKeys.circuits.details(), id] as const,
  },

  // 比赛相关
  races: {
    all: ["races"] as const,
    lists: () => [...queryKeys.races.all, "list"] as const,
    list: (filters: string) =>
      [...queryKeys.races.lists(), { filters }] as const,
    details: () => [...queryKeys.races.all, "detail"] as const,
    detail: (id: number) => [...queryKeys.races.details(), id] as const,
    upcoming: () => [...queryKeys.races.all, "upcoming"] as const,
    recent: () => [...queryKeys.races.all, "recent"] as const,
  },

  // 车手相关
  drivers: {
    all: ["drivers"] as const,
    lists: () => [...queryKeys.drivers.all, "list"] as const,
    list: (filters: string) =>
      [...queryKeys.drivers.lists(), { filters }] as const,
    details: () => [...queryKeys.drivers.all, "detail"] as const,
    detail: (id: number) => [...queryKeys.drivers.details(), id] as const,
    search: (query: string) =>
      [...queryKeys.drivers.all, "search", query] as const,
  },

  // 车队相关
  constructors: {
    all: ["constructors"] as const,
    lists: () => [...queryKeys.constructors.all, "list"] as const,
    list: (filters: string) =>
      [...queryKeys.constructors.lists(), { filters }] as const,
    details: () => [...queryKeys.constructors.all, "detail"] as const,
    detail: (id: number) => [...queryKeys.constructors.details(), id] as const,
    search: (query: string) =>
      [...queryKeys.constructors.all, "search", query] as const,
  },

  // 比赛结果相关
  results: {
    all: ["results"] as const,
    byRace: (raceId: number) =>
      [...queryKeys.results.all, "race", raceId] as const,
    byDriver: (driverId: number, filters: string) =>
      [...queryKeys.results.all, "driver", driverId, { filters }] as const,
    byConstructor: (constructorId: number, filters: string) =>
      [
        ...queryKeys.results.all,
        "constructor",
        constructorId,
        { filters },
      ] as const,
  },

  // 排位赛结果相关
  qualifying: {
    all: ["qualifying"] as const,
    byRace: (raceId: number) =>
      [...queryKeys.qualifying.all, "race", raceId] as const,
    byDriver: (driverId: number, filters: string) =>
      [...queryKeys.qualifying.all, "driver", driverId, { filters }] as const,
  },

  // 冲刺赛结果相关
  sprint: {
    all: ["sprint"] as const,
    byRace: (raceId: number) =>
      [...queryKeys.sprint.all, "race", raceId] as const,
    byDriver: (driverId: number, filters: string) =>
      [...queryKeys.sprint.all, "driver", driverId, { filters }] as const,
  },

  // 积分榜相关
  standings: {
    all: ["standings"] as const,
    drivers: (year: number) =>
      [...queryKeys.standings.all, "drivers", year] as const,
    constructors: (year: number) =>
      [...queryKeys.standings.all, "constructors", year] as const,
    driversBySeasonId: (seasonId: number) =>
      [...queryKeys.standings.all, "drivers", "season", seasonId] as const,
    constructorsBySeasonId: (seasonId: number) =>
      [...queryKeys.standings.all, "constructors", "season", seasonId] as const,
  },
};
