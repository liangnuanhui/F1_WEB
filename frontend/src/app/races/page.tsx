"use client";

import { useRaces } from "@/hooks/use-races";
import { formatDate, formatRaceName, getCountryFlag } from "@/lib/utils";
import { Calendar } from "lucide-react";
import { Race } from "@/types";

function formatF1DateRange(dateStr?: string) {
  if (!dateStr) return "-";
  const date = new Date(dateStr);
  const day = date.getDate();
  const month = date.toLocaleString("en-US", { month: "short" });
  // 取三天范围（F1 官网通常为周五-周日）
  const start = day - 2 > 0 ? day - 2 : day;
  return `${start} - ${day} ${month}`;
}

// 只显示月和日
function formatMonthDayRange(start?: string, end?: string) {
  if (!start) return "-";
  const startDate = new Date(start);
  const endDate = end ? new Date(end) : startDate;
  const month = startDate.getMonth() + 1;
  const startDay = startDate.getDate();
  const endDay = endDate.getDate();
  return `${month}月${startDay}${endDay !== startDay ? `-${endDay}` : ""}日`;
}

function RaceCard({
  race,
  wide = false,
}: {
  race: Race | null;
  wide?: boolean;
}) {
  if (!race)
    return (
      <div
        className={`rounded-xl bg-zinc-200 flex items-center justify-center text-zinc-400 ${wide ? "basis-[36%] min-w-[320px] max-w-xl" : "basis-[24%] min-w-[200px] max-w-sm"} h-56 mr-4 last:mr-0`}
      >
        暂无数据
      </div>
    );
  return (
    <div
      className={`relative rounded-xl shadow-md overflow-hidden flex flex-col justify-end text-white transition-all duration-200 ${
        wide
          ? "basis-[36%] min-w-[320px] max-w-xl"
          : "basis-[24%] min-w-[200px] max-w-sm"
      } h-56 bg-gradient-to-br from-zinc-400 to-zinc-600 mr-4 last:mr-0`}
    >
      {/* 占位背景，可替换为图片 */}
      <div className="absolute inset-0 bg-zinc-300/60" />
      <div className="relative z-10 p-4">
        <div className="text-xs font-bold tracking-widest mb-1">
          ROUND {race.round_number}
        </div>
        <div className="flex items-center mb-2">
          <span className="text-2xl mr-2">
            {getCountryFlag(race.circuit?.country || race.country || "")}
          </span>
          <span className="text-lg font-bold">
            {race.circuit?.country || race.country || "-"}
          </span>
        </div>
        <div className="text-base font-semibold mb-1">
          {formatMonthDayRange(race.event_date)}
        </div>
      </div>
    </div>
  );
}

export default function RacesPage() {
  const {
    data: races,
    isLoading,
    error,
  } = useRaces({ season: 2025, size: 30 });

  if (isLoading) {
    return (
      <div className="flex items-center justify-center py-8 bg-background min-h-[60vh]">
        <div className="text-center">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary mx-auto mb-4"></div>
          <p className="text-muted-foreground">加载赛程中...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="text-center py-8 bg-background min-h-[60vh]">
        <p className="text-red-500">加载赛程失败，请稍后重试</p>
      </div>
    );
  }

  // 赛程头部卡片区逻辑
  let prevRace: Race | null = null,
    nextRace: Race | null = null,
    upcoming: Race[] = [];
  const raceArr = races?.data || [];
  if (raceArr.length > 0) {
    const now = new Date();
    const sorted = [...raceArr].sort(
      (a, b) =>
        new Date(a.event_date || "").getTime() -
        new Date(b.event_date || "").getTime()
    );
    prevRace =
      sorted.filter((r) => new Date(r.event_date || "") < now).pop() || null;
    nextRace = sorted.find((r) => new Date(r.event_date || "") >= now) || null;
    if (nextRace) {
      const nextIdx = sorted.findIndex((r) => r.id === nextRace!.id);
      upcoming = sorted.slice(nextIdx + 1, nextIdx + 3);
    }
  }

  return (
    <div className="space-y-6 bg-background min-h-screen pb-10">
      <div
        className="w-screen max-w-none bg-white flex flex-col items-center justify-center"
        style={{
          marginLeft: "calc(50% - 50vw)",
          marginRight: "calc(50% - 50vw)",
        }}
      >
        <div className="w-full max-w-10xl mx-auto px-4 pt-6 pb-8">
          <div className="flex items-center space-x-2 justify-center mb-6">
            <Calendar className="h-7 w-7 text-primary" />
            <h1 className="text-4xl font-extrabold tracking-tight">
              2025 赛历
            </h1>
          </div>
          <div className="flex flex-row gap-6 justify-center">
            <RaceCard race={prevRace} />
            <RaceCard race={nextRace} wide />
            {upcoming.map((race) => (
              <RaceCard key={race.id} race={race} />
            ))}
          </div>
        </div>
      </div>
      {raceArr.length > 0 ? (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 px-2">
          {raceArr.map((race: Race) => (
            <div
              key={race.id}
              className="flex rounded-xl bg-white/90 dark:bg-zinc-900 border border-zinc-200 dark:border-zinc-800 shadow hover:shadow-lg transition-shadow min-h-[120px]"
            >
              {/* 左侧：轮次、国旗、城市 */}
              <div className="flex flex-col items-center justify-center w-24 bg-primary/10 rounded-l-xl py-4">
                <span className="text-xs text-primary font-bold mb-1">
                  ROUND {race.round_number}
                </span>
                <span className="text-2xl mb-1">
                  {getCountryFlag(race.circuit?.country || race.country || "")}
                </span>
                <span className="text-xs text-muted-foreground text-center">
                  {race.circuit?.country || race.country || "-"}
                </span>
                {race.circuit?.locality && (
                  <span className="text-[10px] text-zinc-400">
                    {race.circuit.locality}
                  </span>
                )}
              </div>
              {/* 中间：英文名、赛道名 */}
              <div className="flex-1 flex flex-col justify-center px-4 py-2">
                <div className="text-lg md:text-xl font-semibold text-zinc-900 dark:text-white mb-1">
                  {race.official_event_name}
                </div>
                <div className="text-xs text-zinc-500 dark:text-zinc-400">
                  {race.circuit?.circuit_name || "-"}
                </div>
              </div>
              {/* 右侧：日期 */}
              <div className="flex flex-col items-end justify-center w-28 pr-4">
                <span className="text-base font-bold text-primary">
                  {formatF1DateRange(race.event_date)}
                </span>
                {race.event_date && (
                  <span className="text-xs text-zinc-400 mt-1">
                    {formatDate(race.event_date, "long")}
                  </span>
                )}
              </div>
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
