import { useQuery } from "@tanstack/react-query";
import { seasonsApi, standingsApi } from "@/lib/api";
import { ConstructorStanding } from "@/types";

interface UseConstructorStandingsOptions {
  year?: number;
  seasonId?: number;
  enabled?: boolean;
}

export const useConstructorStandings = (options: UseConstructorStandingsOptions = {}) => {
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
    queryKey: ["constructor-standings", finalYear, finalSeasonId],
    queryFn: () =>
      finalYear
        ? standingsApi.getConstructorStandings({ year: finalYear })
        : Promise.resolve(null),
    enabled: enabled && !!finalYear,
  });

  const standingsData = standings?.data as ConstructorStanding[] | undefined;

  return {
    standings: standingsData,
    isLoading: seasonLoading || standingsLoading,
    error,
    seasonYear: finalYear,
    seasonId: finalSeasonId,
  };
};
