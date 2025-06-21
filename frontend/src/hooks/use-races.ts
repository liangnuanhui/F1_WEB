import { useQuery } from "@tanstack/react-query";
import { racesApi } from "@/lib/api";
import { queryKeys } from "@/lib/query-client";

// 获取所有比赛
export function useRaces(params?: {
  season?: number;
  page?: number;
  size?: number;
}) {
  const filters = JSON.stringify(params);

  return useQuery({
    queryKey: queryKeys.races.list(filters),
    queryFn: () => racesApi.getAll(params),
  });
}

// 获取单个比赛
export function useRace(id: number) {
  return useQuery({
    queryKey: queryKeys.races.detail(id),
    queryFn: () => racesApi.getById(id),
    enabled: !!id,
  });
}

// 获取即将到来的比赛
export function useUpcomingRaces() {
  return useQuery({
    queryKey: queryKeys.races.upcoming(),
    queryFn: () => racesApi.getUpcoming(),
  });
}
