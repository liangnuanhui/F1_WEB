"use client";

import { useQuery } from "@tanstack/react-query";
import { standingsApi, seasonsApi } from "@/lib/api";
import { Building2 } from "lucide-react";
import { ConstructorStanding } from "@/types";
import { useEffect } from "react";

type ConstructorStandingWithNames = ConstructorStanding & {
  constructor_name: string;
};

export default function ConstructorStandingPage() {
  // 1. 获取当前活跃赛季
  const {
    data: season,
    isLoading: seasonLoading,
    error: seasonError,
  } = useQuery({
    queryKey: ["active-season"],
    queryFn: () => seasonsApi.getActive(),
  });

  // 2. 用当前赛季 id 获取车队积分榜
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
        : Promise.resolve({ data: [], success: true }),
    enabled: !!seasonId, // 只有拿到 seasonId 后才请求
  });

  useEffect(() => {
    if (standings?.data) {
      console.log("constructor_standings.data", standings.data);
    }
  }, [standings]);

  if (seasonLoading || isLoading) {
    return <div className="text-center py-8">加载中...</div>;
  }
  if (seasonError || error) {
    return <div className="text-center py-8 text-red-500">加载失败</div>;
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center space-x-2">
        <Building2 className="h-6 w-6 text-primary" />
        <h1 className="text-3xl font-bold">车队排行榜</h1>
      </div>
      {standings?.data && standings.data.length > 0 ? (
        <div className="overflow-x-auto">
          <table className="min-w-full border rounded-lg text-center">
            <thead>
              <tr className="bg-muted">
                <th className="px-4 py-2">排名</th>
                <th className="px-4 py-2">车队</th>
                <th className="px-4 py-2">积分</th>
                <th className="px-4 py-2">胜场</th>
              </tr>
            </thead>
            <tbody>
              {(standings.data as ConstructorStandingWithNames[]).map(
                (item) => (
                  <tr
                    key={item.constructor_id}
                    className="border-b hover:bg-accent"
                  >
                    <td className="px-4 py-2">{item.position}</td>
                    <td className="px-4 py-2">{item.constructor_name}</td>
                    <td className="px-4 py-2">{item.points}</td>
                    <td className="px-4 py-2">{item.wins}</td>
                  </tr>
                )
              )}
            </tbody>
          </table>
        </div>
      ) : (
        <div className="text-center py-8">
          <p className="text-muted-foreground">暂无车队积分榜数据</p>
        </div>
      )}
    </div>
  );
}
