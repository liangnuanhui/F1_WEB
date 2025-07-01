"use client";

import Image from "next/image";
import { useConstructorStandings } from "@/hooks/use-constructor-standings";
import { getTeamLogoFilename } from "@/lib/team-logo-map";

export function ConstructorStandings() {
  const {
    standings: standingsData,
    isLoading,
    error,
  } = useConstructorStandings();

  if (isLoading) {
    return <div className="text-center py-12">加载中...</div>;
  }
  if (error || !standingsData) {
    return (
      <div className="text-center py-12 text-red-500">加载车队积分榜失败</div>
    );
  }

  return (
    <div className="bg-white rounded-lg shadow-sm">
      <div className="grid grid-cols-12 gap-4 px-6 py-3 font-bold text-sm text-zinc-500 border-b">
        <div className="col-span-1">POS.</div>
        <div className="col-span-10 pl-38">TEAM</div>
        <div className="col-span-1 text-right">PTS.</div>
      </div>
      <div>
        {standingsData.map((item) => (
          <div
            key={item.constructor_id}
            className="grid grid-cols-12 gap-4 px-6 py-3 items-center border-b border-zinc-100 last:border-b-0 hover:bg-zinc-50 transition-colors"
          >
            <div className="col-span-1 font-bold text-lg">{item.position}</div>
            <div className="col-span-10 flex items-center gap-4 pl-38">
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
        ))}
      </div>
    </div>
  );
}
