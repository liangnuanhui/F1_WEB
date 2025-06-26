"use client";

import { useRaces } from "@/hooks/use-races";
import { formatDate, formatRaceName, getCountryFlag } from "@/lib/utils";
import { Calendar } from "lucide-react";
import { Race } from "@/types";
import { useQuery } from "@tanstack/react-query";
import axios, { type AxiosResponse } from "axios";

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

// 修正版：保证服务端和客户端一致的日期解析
function parseDateToUTC(dateStr?: string) {
  if (!dateStr) return undefined;
  // 兼容 '2025-06-01 13:00:00' 和 '2025-06-01T13:00:00Z'
  let iso = dateStr.includes("T") ? dateStr : dateStr.replace(" ", "T");
  if (!iso.endsWith("Z")) iso += "Z";
  const d = new Date(iso);
  return isNaN(d.getTime()) ? undefined : d;
}

function getRaceWeekendRange(race: Race) {
  // 收集所有合法 session 日期
  const sessionDates = [
    race.session1_date,
    race.session2_date,
    race.session3_date,
    race.session4_date,
    race.session5_date,
  ]
    .map(parseDateToUTC)
    .filter(Boolean) as Date[];

  if (sessionDates.length === 0) return "-";
  if (sessionDates.length === 1) {
    const d = sessionDates[0];
    return `${d.getMonth() + 1}月${d.getDate()}日`;
  }
  const minDate = new Date(Math.min(...sessionDates.map((d) => d.getTime())));
  const maxDate = new Date(Math.max(...sessionDates.map((d) => d.getTime())));
  // 跨年情况
  if (minDate.getFullYear() !== maxDate.getFullYear()) {
    return `${minDate.getFullYear()}年${minDate.getMonth() + 1}月${minDate.getDate()}日-${maxDate.getFullYear()}年${maxDate.getMonth() + 1}月${maxDate.getDate()}日`;
  }
  // 跨月
  if (minDate.getMonth() !== maxDate.getMonth()) {
    return `${minDate.getMonth() + 1}月${minDate.getDate()}日-${maxDate.getMonth() + 1}月${maxDate.getDate()}日`;
  }
  // 同月
  return `${minDate.getMonth() + 1}月${minDate.getDate()}日-${maxDate.getDate()}日`;
}

// SVG旗帜组件
const CheckerFlag = () => (
  <svg
    xmlns="http://www.w3.org/2000/svg"
    width="1.2em"
    height="1.2em"
    fill="none"
    viewBox="0 0 24 24"
  >
    <title>Chequered Flag</title>
    <path
      fill="currentColor"
      d="M9 6h2V4H9zm4 0V4h2v2zm-4 8v-2h2v2zm8-4V8h2v2zm0 4v-2h2v2zm-4 0v-2h2v2zm4-8V4h2v2zm-6 2V6h2v2zM5 20V4h2v2h2v2H7v2h2v2H7v8zm10-8v-2h2v2zm-4 0v-2h2v2zm-2-2V8h2v2zm4 0V8h2v2zm2-2V6h2v2z"
    ></path>
  </svg>
);

// 已完成比赛卡片
function RaceResultCard({ race }: { race: Race }) {
  // 特殊location显示
  const specialLoc = [0, 6, 7, 22];
  const showLoc =
    specialLoc.includes(race.round_number) && race.location
      ? race.location
      : race.circuit?.country || race.country || "-";
  // 日期范围（英文简写）
  const getShortMonth = (date: Date) =>
    date.toLocaleString("en-US", { month: "short" }).toUpperCase();
  const sessionDates = [
    race.session1_date,
    race.session2_date,
    race.session3_date,
    race.session4_date,
    race.session5_date,
  ]
    .map(parseDateToUTC)
    .filter(Boolean) as Date[];
  let dateStr = "-";
  if (sessionDates.length) {
    const minDate = sessionDates.reduce((a, b) => (a < b ? a : b));
    const maxDate = sessionDates.reduce((a, b) => (a > b ? a : b));
    if (minDate.getMonth() === maxDate.getMonth()) {
      dateStr = `${minDate.getDate()} – ${maxDate.getDate()} ${getShortMonth(minDate)}`;
    } else {
      dateStr = `${minDate.getDate()} ${getShortMonth(minDate)} – ${maxDate.getDate()} ${getShortMonth(maxDate)}`;
    }
  }
  // 拉取真实前三名数据
  const { data, isLoading } = useQuery({
    queryKey: ["race-podium", race.id],
    queryFn: async (): Promise<
      {
        position: number;
        driver_code: string;
        driver_name: string;
        result_time: string;
      }[]
    > => {
      const res: AxiosResponse<any> = await axios.get(
        `/api/v1/races/${race.id}/podium`
      );
      return res.data.data;
    },
    staleTime: 60 * 1000,
  });
  // 占位数据
  const podium: {
    position: number;
    driver_code: string;
    driver_name: string;
    result_time: string;
  }[] =
    data && data.length === 3
      ? data
      : [
          { position: 1, driver_code: "-", driver_name: "-", result_time: "-" },
          { position: 2, driver_code: "-", driver_name: "-", result_time: "-" },
          { position: 3, driver_code: "-", driver_name: "-", result_time: "-" },
        ];
  return (
    <div className="relative rounded-2xl bg-[#FFFFFF] p-6 shadow flex flex-col gap-6 min-h-[220px]">
      {/* 头部信息 */}
      <div className="flex justify-between items-start">
        <div>
          <div className="text-base font-bold text-zinc-600 mb-2">
            {race.round_number === 0 ? "TESTING" : `ROUND ${race.round_number}`}
          </div>
          <div className="flex items-center gap-2 mb-2">
            <span className="text-xl">
              {getCountryFlag(race.circuit?.country || race.country || "")}
            </span>
            <span className="text-3xl font-extrabold text-zinc-900">
              {showLoc}
            </span>
          </div>
          <div className="text-lg font-bold text-zinc-500 mb-2">
            {race.official_event_name}
          </div>
        </div>
        <div className="flex items-center gap-2 bg-[#F7F4F1] rounded-lg px-4 py-2 text-zinc-700 font-bold text-lg">
          <CheckerFlag />
          <span>{dateStr}</span>
        </div>
      </div>
      {/* 前三名 */}
      <div className="flex gap-3">
        {isLoading
          ? // 骨架屏
            [1, 2, 3].map((i) => (
              <div
                key={i}
                className={`flex-1 rounded-xl bg-zinc-100 animate-pulse flex items-center gap-2 px-3 py-2 min-w-[100px] h-[56px]`}
              />
            ))
          : podium.map(
              (p: {
                position: number;
                driver_code: string;
                driver_name: string;
                result_time: string;
              }) => (
                <div
                  key={p.position}
                  className={`flex-1 rounded-xl ${p.position === 1 ? "bg-[#F7F4F1]" : p.position === 2 ? "bg-orange-100" : "bg-cyan-100"} flex items-center gap-2 px-3 py-2 min-w-[100px]`}
                >
                  <div className="flex flex-col items-center mr-2">
                    <span className="text-xl font-extrabold text-zinc-700 leading-none">
                      {p.position}
                      <span className="text-xs align-super font-bold">
                        {p.position === 1
                          ? "ST"
                          : p.position === 2
                            ? "ND"
                            : "RD"}
                      </span>
                    </span>
                  </div>
                  {/* 头像占位 */}
                  <div className="w-10 h-10 rounded-full bg-zinc-300 flex items-center justify-center font-bold text-lg text-zinc-500">
                    {p.driver_code ? p.driver_code[0] : "-"}
                  </div>
                  <div className="flex flex-col ml-1">
                    <span className="font-extrabold text-lg text-zinc-900">
                      {p.driver_code}
                    </span>
                    <span className="text-xs text-zinc-500 font-medium truncate max-w-[80px]">
                      {p.driver_name}
                    </span>
                    <span className="text-zinc-700 font-mono font-bold text-base">
                      {p.result_time}
                    </span>
                  </div>
                </div>
              )
            )}
      </div>
    </div>
  );
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
          {getRaceWeekendRange(race)}
        </div>
      </div>
    </div>
  );
}

// 下一场比赛卡片
function NextRaceCard({ race }: { race: Race }) {
  // 特殊location显示
  const specialLoc = [0, 6, 7, 22];
  const showLoc =
    specialLoc.includes(race.round_number) && race.location
      ? race.location
      : race.circuit?.country || race.country || "-";
  // 日期范围（英文简写）
  const getShortMonth = (date: Date) =>
    date.toLocaleString("en-US", { month: "short" }).toUpperCase();
  const sessionDates = [
    race.session1_date,
    race.session2_date,
    race.session3_date,
    race.session4_date,
    race.session5_date,
  ]
    .map(parseDateToUTC)
    .filter(Boolean) as Date[];
  let dateStr = "-";
  if (sessionDates.length) {
    const minDate = sessionDates.reduce((a, b) => (a < b ? a : b));
    const maxDate = sessionDates.reduce((a, b) => (a > b ? a : b));
    if (minDate.getMonth() === maxDate.getMonth()) {
      dateStr = `${minDate.getDate()} – ${maxDate.getDate()} ${getShortMonth(minDate)}`;
    } else {
      dateStr = `${minDate.getDate()} ${getShortMonth(minDate)} – ${maxDate.getDate()} ${getShortMonth(maxDate)}`;
    }
  }
  return (
    <div className="relative rounded-2xl bg-gradient-to-br from-[#FF1E00] to-[#B80000] p-6 shadow flex flex-col min-h-[220px] overflow-hidden">
      {/* 头部信息 */}
      <div className="flex justify-between items-start">
        <div>
          <div className="text-base font-bold text-white mb-2">
            {race.round_number === 0 ? "TESTING" : `ROUND ${race.round_number}`}
          </div>
          <div className="flex items-center gap-2 mb-2">
            <span className="text-xl">
              {getCountryFlag(race.circuit?.country || race.country || "")}
            </span>
            <span className="text-3xl font-extrabold text-white drop-shadow">
              {showLoc}
            </span>
          </div>
          <div className="text-lg font-bold text-white mb-2 drop-shadow">
            {race.official_event_name}
          </div>
        </div>
        <div className="flex items-center gap-2 bg-white rounded-lg px-4 py-2 text-[#B80000] font-extrabold text-lg shadow cursor-pointer select-none">
          NEXT RACE
          <span className="ml-1">&rarr;</span>
        </div>
      </div>
      {/* 左下角日期 */}
      <div className="absolute left-6 bottom-6 text-3xl font-extrabold text-white drop-shadow">
        {dateStr}
      </div>
      {/* 右下角赞助商Logo占位 */}
      <div className="absolute right-6 bottom-6 opacity-80">
        <span className="font-logo text-white text-lg tracking-widest">
          LOGO占位符
        </span>
      </div>
    </div>
  );
}

// 赛道图占位符SVG
const TrackPlaceholder = () => (
  <svg
    width="64"
    height="48"
    viewBox="0 0 64 48"
    fill="none"
    xmlns="http://www.w3.org/2000/svg"
  >
    <rect
      x="4"
      y="12"
      width="56"
      height="24"
      rx="12"
      stroke="#222"
      strokeWidth="3"
      fill="none"
    />
    <path d="M12 36 Q32 8 52 36" stroke="#222" strokeWidth="3" fill="none" />
  </svg>
);

// 未进行普通比赛卡片
function UpcomingRaceCard({ race }: { race: Race }) {
  // 特殊location显示
  const specialLoc = [0, 6, 7, 22];
  const showLoc =
    specialLoc.includes(race.round_number) && race.location
      ? race.location
      : race.circuit?.country || race.country || "-";
  // 日期范围（英文简写）
  const getShortMonth = (date: Date) =>
    date.toLocaleString("en-US", { month: "short" }).toUpperCase();
  const sessionDates = [
    race.session1_date,
    race.session2_date,
    race.session3_date,
    race.session4_date,
    race.session5_date,
  ]
    .map(parseDateToUTC)
    .filter(Boolean) as Date[];
  let dateStr = "-";
  if (sessionDates.length) {
    const minDate = sessionDates.reduce((a, b) => (a < b ? a : b));
    const maxDate = sessionDates.reduce((a, b) => (a > b ? a : b));
    if (minDate.getMonth() === maxDate.getMonth()) {
      dateStr = `${minDate.getDate()} – ${maxDate.getDate()} ${getShortMonth(minDate)}`;
    } else {
      dateStr = `${minDate.getDate()} ${getShortMonth(minDate)} – ${maxDate.getDate()} ${getShortMonth(maxDate)}`;
    }
  }
  return (
    <div className="relative rounded-2xl bg-white p-6 shadow flex flex-col min-h-[220px] overflow-hidden">
      {/* 头部信息 */}
      <div>
        <div className="text-base font-bold text-zinc-600 mb-2">
          {race.round_number === 0 ? "TESTING" : `ROUND ${race.round_number}`}
        </div>
        <div className="flex items-center gap-2 mb-2">
          <span className="text-xl">
            {getCountryFlag(race.circuit?.country || race.country || "")}
          </span>
          <span className="text-3xl font-extrabold text-zinc-900">
            {showLoc}
          </span>
        </div>
        <div className="text-lg font-bold text-zinc-500 mb-2">
          {race.official_event_name}
        </div>
      </div>
      {/* 左下角日期 */}
      <div className="absolute left-6 bottom-6 text-3xl font-extrabold text-zinc-900">
        {dateStr}
      </div>
      {/* 右下角赛道图占位符 */}
      <div className="absolute right-6 bottom-6 opacity-90">
        <TrackPlaceholder />
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
            <RaceCard race={nextRace} />
            {upcoming.map((race) => (
              <RaceCard key={race.id} race={race} />
            ))}
          </div>
        </div>
      </div>
      {raceArr.length > 0 ? (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 px-2">
          {raceArr.map((race: Race, idx) => {
            // 判断比赛状态
            const now = new Date();
            const eventDate = race.event_date
              ? new Date(race.event_date)
              : null;
            const isPast = eventDate && eventDate < now;
            // 下一场比赛判断
            const nextRace = raceArr.find(
              (r) => new Date(r.event_date || "") >= now
            );
            const isNext = nextRace && nextRace.id === race.id;
            // TESTING卡片始终用UpcomingRaceCard
            if (race.round_number === 0) {
              return <UpcomingRaceCard key={race.id} race={race} />;
            }
            if (isPast) {
              return <RaceResultCard key={race.id} race={race} />;
            }
            if (isNext) {
              return <NextRaceCard key={race.id} race={race} />;
            }
            return <UpcomingRaceCard key={race.id} race={race} />;
          })}
        </div>
      ) : (
        <div className="text-center py-8">
          <p className="text-muted-foreground">暂无赛程数据</p>
        </div>
      )}
    </div>
  );
}
