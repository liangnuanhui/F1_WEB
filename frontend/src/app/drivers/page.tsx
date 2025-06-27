"use client";

import { useQuery } from "@tanstack/react-query";
import { driversApi, standingsApi } from "@/lib/api";
import { Driver, DriverStanding } from "@/types";
import Image from "next/image";
import { getTeamColor } from "@/lib/team-colors";
import { CountryFlag } from "@/components/CountryFlag";

const formatNameForImage = (name: string) => {
  return name
    .normalize("NFD")
    .replace(/[\u0300-\u036f]/g, "")
    .replace(/ /g, "_");
};

const DriverCard = ({
  driver,
  priority = false,
}: {
  driver: DriverStanding & Partial<Driver>;
  priority?: boolean;
}) => {
  const teamColor = getTeamColor(driver.constructor_id || "");
  const cardStyle = {
    background: `linear-gradient(135deg, ${teamColor} 40%, rgba(0,0,0,0.7) 100%)`,
    color: "#fff",
  };

  const driverPhoto = formatNameForImage(driver.driver_name);

  const driverNumberPath = `/driver_number/2025_${driver.constructor_id}_${formatNameForImage(driver.driver_name).toLowerCase()}_${driver.driver_number}.avif`;

  const [firstName, ...lastNameParts] = driver.driver_name.split(" ");
  const lastName = lastNameParts.join(" ");

  return (
    <div
      className="relative flex h-52 w-full flex-col overflow-hidden rounded-xl p-5 shadow-lg transition-transform hover:scale-105"
      style={cardStyle}
    >
      <div className="relative z-10 flex h-full flex-col justify-between">
        <div>
          <h2 className="text-2xl font-light leading-tight">{firstName}</h2>
          <h2 className="text-2xl font-extrabold leading-tight">
            {lastName.toUpperCase()}
          </h2>
          <p className="mt-1 text-sm font-light text-white/80">
            {driver.constructor_name}
          </p>
        </div>
        <div className="flex items-end justify-between">
          {driver.nationality && (
            <div className="h-8 w-8 overflow-hidden rounded-full">
              <CountryFlag
                nationality={driver.nationality}
                className="h-full w-full object-cover"
              />
            </div>
          )}
          {driver.driver_number && (
            <div className="relative h-12 w-20">
              <Image
                src={driverNumberPath}
                alt={`${driver.driver_name} number`}
                fill
                sizes="(max-width: 768px) 10vw, (max-width: 1200px) 5vw, 80px"
                style={{ objectFit: "contain" }}
              />
            </div>
          )}
        </div>
      </div>
      <div className="absolute -bottom-8 -right-4 h-60 w-60">
        <Image
          src={`/driver_photo_avif/${driverPhoto}.avif`}
          alt={driver.driver_name}
          fill
          sizes="(max-width: 768px) 50vw, (max-width: 1200px) 25vw, 240px"
          priority={priority}
          style={{ objectFit: "cover", objectPosition: "center top" }}
          className="transition-transform duration-300 group-hover:scale-105"
        />
      </div>
    </div>
  );
};

export default function DriversPage() {
  const year = 2025;
  const {
    data: driverStandingsData,
    isLoading: isLoadingStandings,
    error: errorStandings,
  } = useQuery({
    queryKey: ["driverStandings", year],
    queryFn: () => standingsApi.getDriverStandings({ year }),
  });

  const {
    data: driversData,
    isLoading: isLoadingDrivers,
    error: errorDrivers,
  } = useQuery({
    queryKey: ["drivers"],
    queryFn: () => driversApi.getAll({ size: 30 }),
  });

  const {
    data: constructorStandingsData,
    isLoading: isLoadingConstructors,
    error: errorConstructors,
  } = useQuery({
    queryKey: ["constructorStandings", year],
    queryFn: () => standingsApi.getConstructorStandings({ year }),
  });

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
    driversData?.data.reduce(
      (acc, driver) => {
        acc[driver.driver_id] = driver;
        return acc;
      },
      {} as Record<string, Driver>
    ) ?? {};

  const mergedDrivers = driverStandingsData?.data
    .map((standing) => {
      const driverDetails = driversMap[standing.driver_id];
      return {
        ...standing,
        ...driverDetails,
      };
    })
    .filter(
      (driver) => driver.driver_id && driver.forename
    ) as (DriverStanding & Driver)[];

  const orderedConstructorIds =
    constructorStandingsData?.data.map((c) => c.constructor_id) ?? [];

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
