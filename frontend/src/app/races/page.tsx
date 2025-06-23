"use client";

import { useRaces } from "@/hooks/use-races";
import { formatDate, formatRaceName, formatTime } from "@/lib/utils";
import { Calendar, MapPin, Clock } from "lucide-react";
import { Race } from "@/types";

export default function RacesPage() {
  const {
    data: races,
    isLoading,
    error,
  } = useRaces({ season: 2025, size: 30 });

  if (isLoading) {
    return (
      <div className="flex items-center justify-center py-8">
        <div className="text-center">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary mx-auto mb-4"></div>
          <p className="text-muted-foreground">加载赛程中...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="text-center py-8">
        <p className="text-red-500">加载赛程失败，请稍后重试</p>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center space-x-2">
        <Calendar className="h-6 w-6 text-primary" />
        <h1 className="text-3xl font-bold">赛程</h1>
      </div>

      {races?.data && races.data.length > 0 ? (
        <div className="grid gap-4">
          {races.data.map((race: Race) => (
            <div
              key={race.id}
              className="rounded-lg border bg-card p-6 hover:shadow-md transition-shadow"
            >
              <div className="flex items-start justify-between">
                <div className="space-y-2">
                  <div className="flex items-center space-x-2">
                    <h2 className="text-xl font-semibold">
                      {formatRaceName(race.official_event_name)}
                    </h2>
                    <span className="rounded-full bg-primary/10 px-2 py-1 text-xs font-medium text-primary">
                      第 {race.round_number} 站
                    </span>
                  </div>

                  <div className="flex items-center space-x-4 text-sm text-muted-foreground">
                    <div className="flex items-center space-x-1">
                      <MapPin className="h-4 w-4" />
                      <span>{race.circuit_name}</span>
                    </div>
                    <div className="flex items-center space-x-1">
                      <Clock className="h-4 w-4" />
                      <span>{formatDate(race.event_date, "long")}</span>
                    </div>
                  </div>
                </div>
              </div>

              {/* 练习赛和排位赛时间 */}
              {(race.session1_date ||
                race.session2_date ||
                race.session3_date ||
                race.session4_date ||
                race.session5_date) && (
                <div className="mt-4 pt-4 border-t">
                  <h3 className="text-sm font-medium mb-2">详细时间安排</h3>
                  <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-2 text-xs">
                    {race.session1_date && (
                      <div className="flex justify-between">
                        <span>{race.session1 || "Session1"}:</span>
                        <span>{formatDate(race.session1_date)}</span>
                      </div>
                    )}
                    {race.session2_date && (
                      <div className="flex justify-between">
                        <span>{race.session2 || "Session2"}:</span>
                        <span>{formatDate(race.session2_date)}</span>
                      </div>
                    )}
                    {race.session3_date && (
                      <div className="flex justify-between">
                        <span>{race.session3 || "Session3"}:</span>
                        <span>{formatDate(race.session3_date)}</span>
                      </div>
                    )}
                    {race.session4_date && (
                      <div className="flex justify-between">
                        <span>{race.session4 || "Session4"}:</span>
                        <span>{formatDate(race.session4_date)}</span>
                      </div>
                    )}
                    {race.session5_date && (
                      <div className="flex justify-between">
                        <span>{race.session5 || "Session5"}:</span>
                        <span>{formatDate(race.session5_date)}</span>
                      </div>
                    )}
                  </div>
                </div>
              )}
            </div>
          ))}
        </div>
      ) : (
        <div className="text-center py-8">
          <p className="text-muted-foreground">暂无赛程数据</p>
        </div>
      )}
    </div>
  );
}
