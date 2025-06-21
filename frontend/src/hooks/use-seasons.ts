import { useQuery } from "@tanstack/react-query";
import { seasonsApi } from "@/lib/api";
import { queryKeys } from "@/lib/query-client";

// 获取所有赛季
export function useSeasons() {
  return useQuery({
    queryKey: queryKeys.seasons.lists(),
    queryFn: () => seasonsApi.getAll(),
  });
}

// 获取单个赛季
export function useSeason(id: number) {
  return useQuery({
    queryKey: queryKeys.seasons.detail(id),
    queryFn: () => seasonsApi.getById(id),
    enabled: !!id,
  });
}

// 获取当前活跃赛季
export function useActiveSeason() {
  return useQuery({
    queryKey: queryKeys.seasons.active(),
    queryFn: () => seasonsApi.getActive(),
  });
}
