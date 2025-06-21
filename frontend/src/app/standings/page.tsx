"use client";

import { useState } from "react";
import { useActiveSeason } from "@/hooks/use-seasons";
import { useQuery } from "@tanstack/react-query";
import { standingsApi } from "@/lib/api";
import { getCountryFlag } from "@/lib/utils";
import { Trophy, Users, Building2 } from "lucide-react";

type StandingsType = "drivers" | "constructors";

export default function StandingsPage() {
  const [type, setType] = useState<StandingsType>("drivers");
  const { data: activeSeason } = useActiveSeason();

  const {
    data: standings,
    isLoading,
    error,
  } = useQuery({
    queryKey: ["standings", type, activeSeason?.data?.id],
    queryFn: () => {
      if (!activeSeason?.data?.id) return null;
      return type === "drivers"
        ? standingsApi.getDriverStandings(activeSeason.data.id)
        : standingsApi.getConstructorStandings(activeSeason.data.id);
    },
    enabled: !!activeSeason?.data?.id,
  });

  if (isLoading) {
    return (
      <div className="flex items-center justify-center py-8">
        <div className="text-center">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary mx-auto mb-4"></div>
          <p className="text-muted-foreground">加载积分榜中...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="text-center py-8">
        <p className="text-red-500">加载积分榜失败，请稍后重试</p>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div className="flex items-center space-x-2">
          <Trophy className="h-6 w-6 text-primary" />
          <h1 className="text-3xl font-bold">积分榜</h1>
        </div>

        <div className="flex items-center space-x-2">
          <span className="text-sm text-muted-foreground">
            {activeSeason?.data?.year} 赛季
          </span>
        </div>
      </div>

      {/* 切换按钮 */}
      <div className="flex space-x-2">
        <button
          onClick={() => setType("drivers")}
          className={`flex items-center space-x-2 px-4 py-2 rounded-lg transition-colors ${
            type === "drivers"
              ? "bg-primary text-primary-foreground"
              : "bg-secondary text-secondary-foreground hover:bg-secondary/80"
          }`}
        >
          <Users className="h-4 w-4" />
          <span>车手积分榜</span>
        </button>

        <button
          onClick={() => setType("constructors")}
          className={`flex items-center space-x-2 px-4 py-2 rounded-lg transition-colors ${
            type === "constructors"
              ? "bg-primary text-primary-foreground"
              : "bg-secondary text-secondary-foreground hover:bg-secondary/80"
          }`}
        >
          <Building2 className="h-4 w-4" />
          <span>车队积分榜</span>
        </button>
      </div>

      {/* 积分榜表格 */}
      {standings?.data && standings.data.length > 0 ? (
        <div className="rounded-lg border bg-card">
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead>
                <tr className="border-b bg-muted/50">
                  <th className="px-4 py-3 text-left font-medium">排名</th>
                  <th className="px-4 py-3 text-left font-medium">
                    {type === "drivers" ? "车手" : "车队"}
                  </th>
                  <th className="px-4 py-3 text-left font-medium">国籍</th>
                  <th className="px-4 py-3 text-right font-medium">积分</th>
                  <th className="px-4 py-3 text-right font-medium">胜场</th>
                </tr>
              </thead>
              <tbody>
                {standings.data.map((standing, index) => (
                  <tr key={standing.id} className="border-b hover:bg-muted/50">
                    <td className="px-4 py-3 font-medium">
                      {standing.position}
                    </td>
                    <td className="px-4 py-3">
                      <div className="flex items-center space-x-2">
                        {type === "drivers" ? (
                          <>
                            <span className="font-medium">
                              {standing.driver?.forename}{" "}
                              {standing.driver?.surname}
                            </span>
                            {standing.driver?.number && (
                              <span className="text-sm text-muted-foreground">
                                #{standing.driver.number}
                              </span>
                            )}
                          </>
                        ) : (
                          <span className="font-medium">
                            {standing.constructor?.name}
                          </span>
                        )}
                      </div>
                    </td>
                    <td className="px-4 py-3">
                      <div className="flex items-center space-x-1">
                        <span>
                          {type === "drivers"
                            ? getCountryFlag(standing.driver?.nationality || "")
                            : getCountryFlag(
                                standing.constructor?.nationality || ""
                              )}
                        </span>
                        <span className="text-sm text-muted-foreground">
                          {type === "drivers"
                            ? standing.driver?.nationality
                            : standing.constructor?.nationality}
                        </span>
                      </div>
                    </td>
                    <td className="px-4 py-3 text-right font-medium">
                      {standing.points}
                    </td>
                    <td className="px-4 py-3 text-right">{standing.wins}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      ) : (
        <div className="text-center py-8">
          <p className="text-muted-foreground">暂无积分榜数据</p>
        </div>
      )}
    </div>
  );
}
