"use client";

import { useQuery } from "@tanstack/react-query";
import { standingsApi, seasonsApi } from "@/lib/api";
import { ConstructorStanding } from "@/types";
import { getTeamLogoFilename } from "@/lib/team-logo-map";
import { getCountryCode } from "@/lib/utils";
import Image from "next/image";

export default function ConstructorStandingPage() {
  const { data: season, isLoading: seasonLoading } = useQuery({
    queryKey: ["active-season"],
    queryFn: () => seasonsApi.getActive(),
  });

  const seasonId = season?.data?.id;
  const {
    data: standings,
    isLoading,
    error,
  } = useQuery({
    queryKey: ["constructor-standings", seasonId],
    queryFn: () =>
      seasonId
        ? standingsApi.getConstructorStandings(seasonId)
        : Promise.resolve(null),
    enabled: !!seasonId,
  });

  if (seasonLoading || isLoading) {
    return <div className="text-center py-12">加载中...</div>;
  }
  if (error || !standings?.data) {
    return (
      <div className="text-center py-12 text-red-500">加载车队积分榜失败</div>
    );
  }

  const standingsData = standings.data as ConstructorStanding[];

  return (
    <div className="container mx-auto px-4 py-8 bg-[#F7F4F1]">
      <h1 className="text-3xl font-extrabold mb-6 tracking-wider">
        2025 CONSTRUCTOR'S STANDINGS
      </h1>
      <div className="bg-white rounded-lg shadow-sm">
        <div className="grid grid-cols-12 gap-4 px-6 py-3 font-bold text-sm text-zinc-500 border-b">
          <div className="col-span-1">POS.</div>
          <div className="col-span-6">TEAM</div>
          <div className="col-span-4">NATIONALITY</div>
          <div className="col-span-1 text-right">PTS.</div>
        </div>
        <div>
          {standingsData.map((item) => (
            <div
              key={item.constructor_id}
              className="grid grid-cols-12 gap-4 px-6 py-3 items-center border-b border-zinc-100 last:border-b-0 hover:bg-zinc-50 transition-colors"
            >
              <div className="col-span-1 font-bold text-lg">
                {item.position}
              </div>
              <div className="col-span-6 flex items-center gap-4">
                <Image
                  src={`/team_logos/${getTeamLogoFilename(item.constructor_id)}.svg`}
                  alt={item.constructor_name || "Team"}
                  width={32}
                  height={32}
                  className="h-8 w-auto"
                />
                <span className="font-bold">
                  {item.constructor_name || "Unknown Team"}
                </span>
              </div>
              <div className="col-span-4 font-medium text-zinc-600">
                {getCountryCode(item.nationality || "")?.toUpperCase() || "N/A"}
              </div>
              <div className="col-span-1 text-right font-bold text-lg">
                {item.points}
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
