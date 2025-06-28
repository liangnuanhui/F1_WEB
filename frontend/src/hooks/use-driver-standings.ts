import { useQuery } from "@tanstack/react-query";
import { seasonsApi, standingsApi } from "@/lib/api";
import { DriverStanding } from "@/types";

export const useDriverStandings = () => {
  const { data: season, isLoading: seasonLoading } = useQuery({
    queryKey: ["active-season"],
    queryFn: () => seasonsApi.getActive(),
  });

  const seasonYear = season?.data?.year;

  const {
    data: standings,
    isLoading: standingsLoading,
    error,
  } = useQuery({
    queryKey: ["driver-standings", seasonYear],
    queryFn: () =>
      seasonYear
        ? standingsApi.getDriverStandings({ year: seasonYear })
        : Promise.resolve(null),
    enabled: !!seasonYear,
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
    seasonYear: seasonYear,
  };
};
