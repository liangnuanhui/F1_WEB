"use client";

import { Driver, DriverStanding, MergedDriver } from "@/types";
import { DriverCard } from "@/components/DriverCard";
import {
  useDriverStandings,
  useConstructorStandings,
  useDrivers,
} from "@/hooks";

export default function DriversPage() {
  const year = 2025;

  // 使用统一的hooks
  const {
    standings: driverStandingsData,
    isLoading: isLoadingStandings,
    error: errorStandings,
  } = useDriverStandings({ year });

  const {
    drivers: driversData,
    isLoading: isLoadingDrivers,
    error: errorDrivers,
  } = useDrivers({ size: 30 });

  const {
    standings: constructorStandingsData,
    isLoading: isLoadingConstructors,
    error: errorConstructors,
  } = useConstructorStandings({ year });

  const isLoading =
    isLoadingStandings || isLoadingDrivers || isLoadingConstructors;
  const error = errorStandings || errorDrivers || errorConstructors;

  if (isLoading) {
    return (
      <div className="flex min-h-[60vh] items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary mx-auto mb-4"></div>
          <p className="text-muted-foreground">加载 {year} 赛季车手信息中...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="text-center py-8">
        <p className="text-red-500">加载车手信息失败，请稍后重试</p>
      </div>
    );
  }

  const driversMap =
    driversData?.reduce(
      (acc: Record<string, Driver>, driver: Driver) => {
        acc[driver.driver_id] = driver;
        return acc;
      },
      {} as Record<string, Driver>
    ) ?? {};

  const mergedDrivers = driverStandingsData
    ?.map((standing: DriverStanding) => {
      const driverDetails = driversMap[standing.driver_id];
      return {
        ...standing,
        ...driverDetails,
      };
    })
    .filter(
      (driver: any) => driver.driver_id && driver.forename
    ) as MergedDriver[];

  const orderedConstructorIds =
    constructorStandingsData?.map((c: any) => c.constructor_id) ?? [];

  const sortedDrivers = mergedDrivers
    .filter((driver) => driver.driver_id !== "doohan")
    .sort((a, b) => {
      const teamAIndex = orderedConstructorIds.indexOf(a.constructor_id!);
      const teamBIndex = orderedConstructorIds.indexOf(b.constructor_id!);

      if (teamAIndex === -1) return 1;
      if (teamBIndex === -1) return -1;
      if (teamAIndex !== teamBIndex) {
        return teamAIndex - teamBIndex;
      }

      return (b.points ?? 0) - (a.points ?? 0);
    });

  return (
    <div className="container mx-auto p-4">
      <div className="mb-8">
        <h1 className="text-4xl font-black tracking-tight">
          F1 DRIVERS {year}
        </h1>
        <p className="text-lg text-muted-foreground">
          Meet the 2025 Formula 1 drivers
        </p>
      </div>
      {sortedDrivers.length > 0 ? (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
          {sortedDrivers.map((driver, index) => (
            <DriverCard
              key={driver.driver_id}
              driver={driver}
              priority={index < 4}
            />
          ))}
        </div>
      ) : (
        <div className="text-center py-8">
          <p className="text-muted-foreground">暂无 {year} 赛季的车手数据</p>
        </div>
      )}
    </div>
  );
}
