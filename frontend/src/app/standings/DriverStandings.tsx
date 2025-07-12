"use client";

import Image from "next/image";
import { useQuery } from "@tanstack/react-query";
import { useDriverStandings } from "@/hooks/use-driver-standings";
import { driversApi } from "@/lib/api";
import { getTeamColor } from "@/lib/team-colors";
import { availableAvatarSet } from "@/lib/available-avatars";
import { getTeamLogoFilename } from "@/lib/team-logo-map";
import { getCountryCode } from "@/lib/utils";
import { Driver, DriverStanding } from "@/types";

// 工具函数，从全名生成头像路径
const getAvatarPath = (fullName: string) => {
  if (!fullName) return "/driver_avatar/default.svg";
  // 规范化名称以处理特殊字符 (例如 ü -> u)
  const normalizedName = fullName
    .normalize("NFD")
    .replace(/[\u0300-\u036f]/g, "");
  const sanitizedName = normalizedName.replace(/ /g, "_");
  if (availableAvatarSet.has(sanitizedName)) {
    return `/driver_avatar/${sanitizedName}.png`;
  }
  return "/driver_avatar/default.svg";
};

export function DriverStandings() {
  const { standings: standingsData, isLoading, error } = useDriverStandings();

  // 获取完整的车手数据以获得维基百科链接
  const {
    data: driversData,
    isLoading: isLoadingDrivers,
    error: errorDrivers,
  } = useQuery({
    queryKey: ["drivers"],
    queryFn: () => driversApi.getAll({ size: 30 }),
  });

  const loading = isLoading || isLoadingDrivers;
  const hasError = error || errorDrivers;

  if (loading) {
    return <div className="text-center py-12">加载中...</div>;
  }
  if (hasError || !standingsData) {
    return (
      <div className="text-center py-12 text-red-500">加载车手积分榜失败</div>
    );
  }

  // 创建车手数据映射
  const driversMap =
    driversData?.data.reduce(
      (acc, driver) => {
        acc[driver.driver_id] = driver;
        return acc;
      },
      {} as Record<string, Driver>
    ) ?? {};

  // 合并车手积分榜数据和完整车手数据
  const mergedDrivers = standingsData
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

  return (
    <div className="bg-white rounded-lg shadow-sm">
      <div className="grid grid-cols-12 gap-4 px-6 py-3 font-bold text-sm text-zinc-500 border-b">
        <div className="col-span-1">POS.</div>
        <div className="col-span-4">DRIVER</div>
        <div className="col-span-2">NATIONALITY</div>
        <div className="col-span-4">TEAM</div>
        <div className="col-span-1 text-right">PTS.</div>
      </div>
      <div>
        {mergedDrivers.map((item) => {
          const hasValidUrl = item.driver_url && item.driver_url.trim() !== "";
          
          const handleDriverClick = () => {
            if (hasValidUrl) {
              window.open(item.driver_url, "_blank");
            }
          };

          return (
            <div
              key={item.driver_id}
              className="grid grid-cols-12 gap-4 px-6 py-3 items-center border-b border-zinc-100 last:border-b-0 hover:bg-zinc-50 transition-colors"
            >
              <div className="col-span-1 font-bold text-lg">{item.position}</div>
              <div 
                className={`col-span-4 flex items-center gap-4 transition-transform duration-300 hover:scale-105 ${hasValidUrl ? 'cursor-pointer' : ''}`}
                onClick={handleDriverClick}
                aria-label={hasValidUrl ? `查看 ${item.driver_name} 的维基百科页面` : undefined}
                role={hasValidUrl ? "button" : undefined}
              >
                <div
                  className="w-10 h-10 rounded-full flex-shrink-0 flex items-center justify-center overflow-hidden"
                  style={{
                    backgroundColor: getTeamColor(
                      item.constructor_id || undefined
                    ),
                  }}
                >
                  <Image
                    src={getAvatarPath(item.driver_name)}
                    alt={item.driver_name || "Driver"}
                    width={40}
                    height={40}
                    className="object-cover w-full h-full"
                  />
                </div>
                <span className="font-bold">
                  {item.driver_name || "Unknown Driver"}
                </span>
              </div>
              <div className="col-span-2 font-medium text-zinc-600">
                {getCountryCode(item.nationality || "")?.toUpperCase() || "N/A"}
              </div>
              <div className="col-span-4 flex items-center gap-3">
                <Image
                  src={`/team_logos/${getTeamLogoFilename(
                    item.constructor_id || ""
                  )}.svg`}
                  alt={item.constructor_name || "Team"}
                  width={28}
                  height={28}
                />
                <span className="font-medium">
                  {item.constructor_name || "Unknown Team"}
                </span>
              </div>
              <div className="col-span-1 text-right font-bold text-lg">
                {item.points}
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
