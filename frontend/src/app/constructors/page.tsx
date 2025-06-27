"use client";

import { useQuery } from "@tanstack/react-query";
import { standingsApi, constructorsApi } from "@/lib/api";
import { getTeamColor } from "@/lib/team-colors";
import { Constructor, ConstructorStanding, DriverStanding } from "@/types";
import Image from "next/image";
import { ChevronRight } from "lucide-react";
import { teamLogoMap } from "@/lib/team-logo-map";
import { availableAvatarSet } from "@/lib/available-avatars";

// Helper to format driver names for avatar lookup
const formatAvatarName = (driverName: string) => {
  // Normalize to handle special characters (e.g., ü -> u) and replace spaces with underscores.
  const normalizedName = driverName
    .normalize("NFD")
    .replace(/[\u0300-\u036f]/g, "");
  return normalizedName.replace(/ /g, "_");
};

// Helper to format driver names for display (bold surname)
const formatDriverDisplayName = (driverName: string) => {
  const parts = driverName.split(" ");
  if (parts.length > 1) {
    const firstName = parts.slice(0, -1).join(" ");
    const lastName = parts[parts.length - 1];
    return (
      <>
        {firstName} <span className="font-bold">{lastName.toUpperCase()}</span>
      </>
    );
  }
  return <span className="font-bold">{driverName.toUpperCase()}</span>;
};

const TeamCard = ({
  constructor,
  drivers,
}: {
  constructor: ConstructorStanding;
  drivers: DriverStanding[];
}) => {
  const color = getTeamColor(constructor.constructor_id);
  const logoFilename = teamLogoMap[constructor.constructor_id] || null;
  const logoUrl = logoFilename ? `/team_logos/${logoFilename}.svg` : null;

  const cardStyle = {
    background: `linear-gradient(135deg, ${color} 40%, rgba(0,0,0,0.5) 100%)`,
    color: "#fff",
  };

  const handleCardClick = () => {
    if (constructor.constructor_url) {
      window.open(constructor.constructor_url, "_blank");
    }
  };

  return (
    <div
      className="group relative flex cursor-pointer flex-col overflow-hidden rounded-2xl transition-transform duration-300 hover:scale-105"
      style={cardStyle}
      onClick={handleCardClick}
    >
      <div className="relative z-10 p-6">
        <div className="flex items-start justify-between">
          <div>
            <h2 className="text-3xl font-bold mb-2">
              {constructor.constructor_name}
            </h2>
            <div className="flex space-x-4">
              {drivers.map((driver) => {
                const avatarName = formatAvatarName(driver.driver_name);
                const hasAvatar = availableAvatarSet.has(avatarName);
                const avatarUrl = hasAvatar
                  ? `/driver_avatar/${avatarName}.png`
                  : `/driver_avatar/default.svg`;

                return (
                  <div
                    key={driver.driver_id}
                    className="flex items-center space-x-2"
                  >
                    <div
                      className="rounded-full w-8 h-8 flex-shrink-0"
                      style={{ backgroundColor: color }}
                    >
                      <Image
                        src={avatarUrl}
                        alt={driver.driver_name}
                        width={32}
                        height={32}
                        className="rounded-full"
                      />
                    </div>
                    <p className="text-sm tracking-wide">
                      {formatDriverDisplayName(driver.driver_name)}
                    </p>
                  </div>
                );
              })}
            </div>
          </div>
          {logoUrl && (
            <div className="bg-white/20 rounded-full p-2">
              <Image
                src={logoUrl}
                alt={`${constructor.constructor_name} logo`}
                width={24}
                height={24}
                className="opacity-80"
              />
            </div>
          )}
        </div>
      </div>

      <div className="relative mt-4 px-6 pb-4">
        <Image
          src={`/2025_constructor_car_photo/${constructor.constructor_id}.png`}
          alt={`${constructor.constructor_name} car`}
          width={450}
          height={225}
          className="transform-gpu opacity-90 transition-transform duration-500 group-hover:scale-110"
        />
      </div>

      <div className="absolute right-4 top-1/2 -translate-y-1/2 cursor-pointer rounded-full bg-black/30 p-2 opacity-0 transition-opacity group-hover:opacity-100">
        <ChevronRight className="h-6 w-6" />
      </div>

      <div className="absolute inset-0 bg-black/10 opacity-50 group-hover:opacity-0 transition-opacity duration-300"></div>
    </div>
  );
};

export default function ConstructorPage() {
  const year = 2025;

  const {
    data: constructorStandings,
    isLoading: isLoadingConstructors,
    error: errorConstructors,
  } = useQuery({
    queryKey: ["constructorStandings", year],
    queryFn: () => standingsApi.getConstructorStandings({ year }),
  });

  const {
    data: driverStandings,
    isLoading: isLoadingDrivers,
    error: errorDrivers,
  } = useQuery({
    queryKey: ["driverStandings", year],
    queryFn: () => standingsApi.getDriverStandings({ year }),
  });

  const {
    data: constructors,
    isLoading: isLoadingConstructorsData,
    error: errorConstructorsData,
  } = useQuery({
    queryKey: ["constructors"],
    queryFn: () => constructorsApi.getConstructors(),
  });

  const isLoading =
    isLoadingConstructors || isLoadingDrivers || isLoadingConstructorsData;
  const error = errorConstructors || errorDrivers || errorConstructorsData;

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

  const constructorMap = constructors?.data.reduce(
    (acc, constructor) => {
      acc[constructor.constructor_id] = constructor;
      return acc;
    },
    {} as Record<string, Constructor>
  );

  const driversByConstructor = driverStandings?.data.reduce(
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
    {} as Record<string, DriverStanding[]>
  );

  const mergedConstructorStandings = constructorStandings?.data.map(
    (standing) => ({
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
          {mergedConstructorStandings.map((constructor) => (
            <TeamCard
              key={constructor.constructor_id}
              constructor={constructor}
              drivers={driversByConstructor?.[constructor.constructor_id] || []}
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
