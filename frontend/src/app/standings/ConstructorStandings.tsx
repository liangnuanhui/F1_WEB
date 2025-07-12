"use client";

import Image from "next/image";
import { useQuery } from "@tanstack/react-query";
import { useConstructorStandings } from "@/hooks/use-constructor-standings";
import { constructorsApi } from "@/lib/api";
import { getTeamLogoFilename } from "@/lib/team-logo-map";
import { Constructor, ConstructorStanding } from "@/types";

export function ConstructorStandings() {
  const {
    standings: standingsData,
    isLoading,
    error,
  } = useConstructorStandings();

  // 获取完整的车队数据以获得维基百科链接
  const {
    data: constructorsData,
    isLoading: isLoadingConstructors,
    error: errorConstructors,
  } = useQuery({
    queryKey: ["constructors"],
    queryFn: () => constructorsApi.getConstructors(),
  });

  const loading = isLoading || isLoadingConstructors;
  const hasError = error || errorConstructors;

  if (loading) {
    return <div className="text-center py-12">加载中...</div>;
  }
  if (hasError || !standingsData) {
    return (
      <div className="text-center py-12 text-red-500">加载车队积分榜失败</div>
    );
  }

  // 创建车队数据映射
  const constructorsMap =
    constructorsData?.data.reduce(
      (acc, constructor) => {
        acc[constructor.constructor_id] = constructor;
        return acc;
      },
      {} as Record<string, Constructor>
    ) ?? {};

  // 合并车队积分榜数据和完整车队数据
  const mergedConstructors = standingsData.map((standing) => {
    const constructorDetails = constructorsMap[standing.constructor_id];
    return {
      ...standing,
      ...constructorDetails,
    };
  }) as (ConstructorStanding & Constructor)[];

  return (
    <div className="bg-white rounded-lg shadow-sm">
      <div className="grid grid-cols-12 gap-4 px-6 py-3 font-bold text-sm text-zinc-500 border-b">
        <div className="col-span-1">POS.</div>
        <div className="col-span-10 pl-38">TEAM</div>
        <div className="col-span-1 text-right">PTS.</div>
      </div>
      <div>
        {mergedConstructors.map((item) => {
          const hasValidUrl =
            item.constructor_url && item.constructor_url.trim() !== "";

          const handleConstructorClick = () => {
            if (hasValidUrl) {
              window.open(item.constructor_url, "_blank");
            }
          };

          return (
            <div
              key={item.constructor_id}
              className="grid grid-cols-12 gap-4 px-6 py-3 items-center border-b border-zinc-100 last:border-b-0 hover:bg-zinc-50 transition-colors"
            >
              <div className="col-span-1 font-bold text-lg">
                {item.position}
              </div>
              <div
                className={`col-span-10 flex items-center gap-4 pl-38 transition-transform duration-300 hover:scale-105 ${hasValidUrl ? "cursor-pointer" : ""}`}
                onClick={handleConstructorClick}
                aria-label={
                  hasValidUrl
                    ? `查看 ${item.constructor_name} 的维基百科页面`
                    : undefined
                }
                role={hasValidUrl ? "button" : undefined}
              >
                <Image
                  src={`/team_logos/${getTeamLogoFilename(
                    item.constructor_id
                  )}.svg`}
                  alt={item.constructor_name || "Team"}
                  width={32}
                  height={32}
                  className="h-8 w-auto"
                />
                <span className="font-bold">
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
