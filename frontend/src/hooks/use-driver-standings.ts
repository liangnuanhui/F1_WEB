import { useQuery } from "@tanstack/react-query";
import { seasonsApi, standingsApi } from "@/lib/api";
import { DriverStanding } from "@/types";

interface UseDriverStandingsOptions {
  year?: number;
  seasonId?: number;
  enabled?: boolean;
}

export const useDriverStandings = (options: UseDriverStandingsOptions = {}) => {
  const { year, seasonId, enabled = true } = options;

  // 如果未提供年份或赛季ID，获取活跃赛季
  const { data: season, isLoading: seasonLoading } = useQuery({
    queryKey: ["active-season"],
    queryFn: () => seasonsApi.getActive(),
    enabled: enabled && !year && !seasonId,
  });

  const finalYear = year || season?.data?.year;
  const finalSeasonId = seasonId || season?.data?.id;

  const {
    data: standings,
    isLoading: standingsLoading,
    error,
  } = useQuery({
    queryKey: ["driver-standings", finalYear, finalSeasonId],
    queryFn: () =>
      finalYear
        ? standingsApi.getDriverStandings({ year: finalYear })
        : Promise.resolve(null),
    enabled: enabled && !!finalYear,
  });

  // 过滤掉 'doohan' 车手
  const standingsData = standings?.data
    ? (standings.data as DriverStanding[]).filter(
        (driver) => driver.driver_id !== "doohan"
      )
    : undefined;

  return {
    standings: standingsData,
    isLoading: seasonLoading || standingsLoading,
    error,
    seasonYear: finalYear,
    seasonId: finalSeasonId,
  };
};
