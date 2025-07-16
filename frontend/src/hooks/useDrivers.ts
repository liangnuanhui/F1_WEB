import { useQuery } from "@tanstack/react-query";
import { driversApi } from "@/lib/api";

interface UseDriversOptions {
  page?: number;
  size?: number;
  enabled?: boolean;
}

export const useDrivers = (options: UseDriversOptions = {}) => {
  const { page = 1, size = 30, enabled = true } = options;

  const {
    data: drivers,
    isLoading,
    error,
  } = useQuery({
    queryKey: ["drivers", page, size],
    queryFn: () => driversApi.getAll({ page, size }),
    enabled,
  });

  return {
    drivers: drivers,
    isLoading,
    error,
  };
};
