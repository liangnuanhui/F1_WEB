import { useQuery } from "@tanstack/react-query";
import { constructorsApi } from "@/lib/api";
import { Constructor } from "@/types";

interface UseConstructorsOptions {
  page?: number;
  size?: number;
  enabled?: boolean;
}

export const useConstructors = (options: UseConstructorsOptions = {}) => {
  const { page = 1, size = 50, enabled = true } = options;

  const {
    data: constructors,
    isLoading,
    error,
  } = useQuery({
    queryKey: ["constructors", page, size],
    queryFn: () => constructorsApi.getConstructors({ page, size }),
    enabled,
  });

  return {
    constructors: constructors?.data,
    isLoading,
    error,
  };
};
