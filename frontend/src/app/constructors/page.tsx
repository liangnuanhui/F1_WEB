"use client";

import { Constructor } from "@/types";

import {
  Constructor,
  ConstructorStanding,
  DriverStanding,
  Driver,
  MergedDriver,
} from "@/types";
import { TeamCard } from "@/components/TeamCard";
import {
  useDriverStandings,
  useConstructorStandings,
  useDrivers,
  useConstructors,
} from "@/hooks";

export default function ConstructorPage() {
  const year = 2025;

  // 使用统一的hooks
  const {
    standings: constructorStandings,
    isLoading: isLoadingConstructors,
    error: errorConstructors,
  } = useConstructorStandings({ year });

  const {
    standings: driverStandings,
    isLoading: isLoadingDrivers,
    error: errorDrivers,
  } = useDriverStandings({ year });

  const {
    constructors,
    isLoading: isLoadingConstructorsData,
    error: errorConstructorsData,
  } = useConstructors();

  const {
    drivers: driversData,
    isLoading: isLoadingDriversData,
    error: errorDriversData,
  } = useDrivers({ size: 30 });

  const isLoading =
    isLoadingConstructors ||
    isLoadingDrivers ||
    isLoadingConstructorsData ||
    isLoadingDriversData;
  const error =
    errorConstructors ||
    errorDrivers ||
    errorConstructorsData ||
    errorDriversData;

  if (isLoading) {
    return (
      <div className="flex items-center justify-center py-8">
        <div className="text-center">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary mx-auto mb-4"></div>
          <p className="text-muted-foreground">加载 {year} 赛季车队信息中...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="text-center py-8">
        <p className="text-red-500">加载车队信息失败，请稍后重试</p>
      </div>
    );
  }

  const constructorMap = constructors?.reduce(
    (acc: Record<string, Constructor>, constructor: Constructor) => {
      acc[constructor.constructor_id] = constructor;
      return acc;
    },
    {} as Record<string, Constructor>
  ) ?? {};

  // 创建车手数据映射
  const driversMap =
    driversData?.reduce(
      (acc: Record<string, Driver>, driver: Driver) => {
        acc[driver.driver_id] = driver;
        return acc;
      },
      {} as Record<string, Driver>
    ) ?? {};

  // 合并车手积分榜数据和完整车手数据
  const mergedDrivers = (driverStandings
    ?.map((standing: DriverStanding) => {
      const driverDetails = driversMap[standing.driver_id];
      return {
        ...standing,
        ...driverDetails,
      };
    })
    .filter(
      (driver: MergedDriver) => driver.driver_id && driver.forename
    ) ?? []) as MergedDriver[];

  const driversByConstructor = mergedDrivers.reduce(
    (acc, driver) => {
      if (driver.constructor_id) {
        if (!acc[driver.constructor_id]) {
          acc[driver.constructor_id] = [];
        }
        // Temporary fix: Exclude Jack Doohan from Alpine
        if (
          driver.constructor_id === "alpine" &&
          driver.driver_id === "doohan"
        ) {
          return acc;
        }
        acc[driver.constructor_id].push(driver);
      }
      return acc;
    },
    {} as Record<string, MergedDriver[]>
  );

  const mergedConstructorStandings = constructorStandings?.map(
    (standing: ConstructorStanding) => ({
      ...standing,
      constructor_url:
        constructorMap?.[standing.constructor_id]?.constructor_url || null,
    })
  );

  return (
    <div className="container mx-auto p-4">
      <div className="mb-8">
        <h1 className="text-4xl font-black tracking-tight">F1 TEAMS {year}</h1>
        <p className="text-lg text-muted-foreground">
          Find the current Formula 1 teams for the {year} season
        </p>
      </div>

      {mergedConstructorStandings && mergedConstructorStandings.length > 0 ? (
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {mergedConstructorStandings.map((constructor: Constructor, index: number) => (
            <TeamCard
              key={constructor.constructor_id}
              constructor={constructor}
              drivers={driversByConstructor?.[constructor.constructor_id] || []}
              priority={index < 2}
            />
          ))}
        </div>
      ) : (
        <div className="text-center py-8">
          <p className="text-muted-foreground">暂无 {year} 赛季的车队数据</p>
        </div>
      )}
    </div>
  );
}
