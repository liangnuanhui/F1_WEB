import { useQuery } from "@tanstack/react-query";
import { seasonsApi, standingsApi } from "@/lib/api";
import { ConstructorStanding } from "@/types";

export const useConstructorStandings = () => {
  const { data: season, isLoading: seasonLoading } = useQuery({
    queryKey: ["active-season"],
    queryFn: () => seasonsApi.getActive(),
  });

  const seasonId = season?.data?.id;

  const {
    data: standings,
    isLoading: standingsLoading,
    error,
  } = useQuery({
    queryKey: ["constructor-standings", seasonId],
    queryFn: () =>
      seasonId
        ? standingsApi.getConstructorStandings({ seasonId })
        : Promise.resolve(null),
    enabled: !!seasonId,
  });

  const standingsData = standings?.data as ConstructorStanding[] | undefined;

  return {
    standings: standingsData,
    isLoading: seasonLoading || standingsLoading,
    error,
    seasonId: seasonId,
  };
};
