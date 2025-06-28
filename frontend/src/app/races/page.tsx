"use client";

import { useRaces } from "@/hooks/use-races";
import { formatDate, formatRaceName, getCountryName } from "@/lib/utils";
import { Calendar } from "lucide-react";
import { Race } from "@/types";
import { useQuery } from "@tanstack/react-query";
import axios, { type AxiosResponse } from "axios";
import { CountryFlag } from "@/components/CountryFlag";
import Image from "next/image";
import React from "react";

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

// 赛道图渲染组件，自动处理懒加载和onError
const CircuitImage = React.memo(function CircuitImage({
  src,
  alt,
  className,
}: {
  src: string;
  alt: string;
  className?: string;
}) {
  return (
    <Image
      src={src}
      alt={alt}
      width={120}
      height={72}
      className={className || "h-[72px] w-auto"}
      loading="lazy"
      onError={(e) => {
        const target = e.target as HTMLImageElement;
        target.style.display = "none";
      }}
    />
  );
});

// 已完成比赛卡片
const RaceResultCard = React.memo(function RaceResultCard({
  race,
}: {
  race: Race;
}) {
  // 特殊location显示
  const displayName = getCountryName(race);

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
    <div className="relative rounded-2xl bg-white p-6 shadow flex flex-col justify-between sm:h-64 h-[320px] min-h-[220px]">
      {/* 头部信息 */}
      <div className="flex justify-between items-start">
        <div>
          <p className="text-xs text-zinc-400 font-semibold tracking-wider mb-1">
            {race.round_number === 0 ? "TESTING" : `ROUND ${race.round_number}`}
          </p>
          <div className="flex items-center gap-3">
            <CountryFlag country={displayName} className="w-8 h-6 rounded" />
            <h2 className="text-3xl font-extrabold text-zinc-900">
              {displayName}
            </h2>
          </div>
          <p className="text-sm text-zinc-500 font-medium mt-1 min-h-[2.5rem] line-clamp-2">
            {race.official_event_name}
          </p>
        </div>
        <div className="flex items-center gap-2 rounded-lg px-3 py-1.5 text-zinc-500 font-semibold text-xs whitespace-nowrap flex-row bg-[#F7F4F1]">
          <CheckerFlag />
          <span>{dateStr}</span>
        </div>
      </div>
      {/* 前三名 */}
      <div className="flex flex-col sm:flex-row gap-2 sm:gap-1 w-full overflow-hidden">
        {isLoading
          ? // 骨架屏
            [1, 2, 3].map((i) => (
              <div
                key={i}
                className={`w-full sm:flex-1 rounded-xl bg-zinc-100 animate-pulse flex items-center gap-1 px-1 py-1 h-[48px]`}
              />
            ))
          : podium.map(
              (
                p: {
                  position: number;
                  driver_code: string;
                  driver_name: string;
                  result_time: string;
                },
                idx: number
              ) => {
                // 小屏下前三名卡片宽度错落
                let baseClass =
                  "rounded-xl bg-[#F7F4F1] flex items-center gap-1 p-1 min-w-0 overflow-hidden ";
                let widthClass = "";
                if (typeof window !== "undefined" && window.innerWidth < 640) {
                  if (idx === 0) widthClass = "w-full";
                  else if (idx === 1) widthClass = "w-[90%] self-end";
                  else if (idx === 2) widthClass = "w-[80%] self-end";
                } else {
                  widthClass = "w-full sm:flex-1";
                }
                // SSR/CSR兼容，tailwind建议直接写class
                return (
                  <div
                    key={p.position}
                    className={
                      (idx === 0
                        ? "w-full sm:w-auto sm:flex-1"
                        : idx === 1
                          ? "w-full ml-6 sm:w-auto sm:ml-0 sm:flex-1"
                          : idx === 2
                            ? "w-full ml-12 sm:w-auto sm:ml-0 sm:flex-1"
                            : "sm:w-auto sm:flex-1") + baseClass
                    }
                  >
                    <div className="flex flex-col items-center justify-center w-6 text-zinc-500">
                      <span className="text-lg font-bold leading-none">
                        {p.position}
                      </span>
                      <span className="text-[10px] font-semibold leading-none">
                        {["ST", "ND", "RD"][p.position - 1] || "TH"}
                      </span>
                    </div>
                    {/* 头像占位 */}
                    <div className="w-7 h-7 rounded-full flex-shrink-0 bg-zinc-300 flex items-center justify-center overflow-hidden">
                      {p.driver_name && p.driver_name !== "-" ? (
                        <img
                          src={`/driver_avatar/${p.driver_name.replace(/ /g, "_")}.png`}
                          alt={p.driver_name}
                          width={30}
                          height={30}
                          className="object-cover w-7 h-7 rounded-full"
                          style={{ objectPosition: "center" }}
                          loading="lazy"
                          onError={(e) => {
                            const img = e.target as HTMLImageElement;
                            img.style.display = "none";
                            if (img.parentElement) {
                              img.parentElement.textContent = p.driver_code
                                ? p.driver_code[0]
                                : "-";
                            }
                          }}
                        />
                      ) : p.driver_code ? (
                        p.driver_code[0]
                      ) : (
                        "-"
                      )}
                    </div>
                    <div className="flex flex-col ml-1 min-w-0 overflow-hidden">
                      <span className="font-bold text-[13px] text-zinc-900 truncate">
                        {p.driver_code}
                      </span>
                      <span className="text-zinc-500 font-mono font-medium text-[11px] truncate">
                        {p.result_time}
                      </span>
                    </div>
                  </div>
                );
              }
            )}
      </div>
    </div>
  );
});

const RaceCard = React.memo(function RaceCard({
  race,
  wide = false,
  bgImageUrl,
}: {
  race: Race | null;
  wide?: boolean;
  bgImageUrl: string;
}) {
  if (!race)
    return (
      <div
        className={`rounded-xl bg-zinc-200 flex items-center justify-center text-zinc-400 h-80 w-full`}
      >
        暂无数据
      </div>
    );

  return (
    <div
      className={`relative rounded-xl shadow-md overflow-hidden flex flex-col justify-end text-white transition-all duration-200 h-80 w-full bg-cover bg-center`}
      style={{ backgroundImage: `url('${bgImageUrl}')` }}
    >
      {/* 半透明遮罩 */}
      <div className="absolute inset-0 bg-black/40" />
      <div className="relative z-10 p-6 flex flex-col h-full justify-between">
        <div>
          <div className="text-xs font-bold tracking-widest mb-1">
            ROUND {race.round_number}
          </div>
          <div className="text-3xl font-extrabold">{getCountryName(race)}</div>
          <div className="text-lg font-bold my-2">
            {getRaceWeekendRange(race)}
          </div>
        </div>
        {/* 左下角 logo 占位 */}
        <div className="absolute left-6 bottom-6 opacity-90">
          <span className="font-logo text-white text-lg tracking-widest"></span>
        </div>
      </div>
    </div>
  );
});

// 下一场比赛卡片
const NextRaceCard = React.memo(function NextRaceCard({
  race,
}: {
  race: Race;
}) {
  // 特殊location显示
  const displayName = getCountryName(race);

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
    <div className="relative rounded-2xl bg-gradient-to-br from-[#FF1E00] to-[#B80000] p-6 shadow flex flex-col min-h-[220px] h-64 overflow-hidden">
      {/* 头部信息 */}
      <div className="flex justify-between items-start">
        <div>
          <div className="text-base font-bold text-white mb-2">
            {race.round_number === 0 ? "TESTING" : `ROUND ${race.round_number}`}
          </div>
          <div className="flex items-center gap-2 mb-2">
            <CountryFlag country={displayName} className="w-8 h-6 rounded" />
            <span className="text-3xl font-extrabold text-white drop-shadow">
              {displayName}
            </span>
          </div>
          <div className="text-lg font-bold text-white mb-2 drop-shadow">
            {race.official_event_name}
          </div>
        </div>
        <div className="flex items-center gap-2 bg-white rounded-lg px-4 py-2 text-[#B80000] font-extrabold text-lg shadow cursor-pointer select-none whitespace-nowrap flex-row">
          NEXT RACE
          <span className="ml-1">&rarr;</span>
        </div>
      </div>
      {/* 左下角日期 */}
      <div className="absolute left-6 bottom-6 text-3xl font-extrabold text-white drop-shadow">
        {dateStr}
      </div>
      {/* 右下角赛道图 */}
      <div className="absolute right-6 bottom-6 opacity-90">
        {race.circuit_id ? (
          <CircuitImage
            src={`/circuits_svg/${race.circuit_id}.svg`}
            alt={race.circuit?.circuit_name || "赛道布局"}
            className="h-[72px] w-auto brightness-0 invert"
          />
        ) : (
          <span className="font-logo text-white text-lg tracking-widest">
            LOGO
          </span>
        )}
      </div>
    </div>
  );
});

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
const UpcomingRaceCard = React.memo(function UpcomingRaceCard({
  race,
}: {
  race: Race;
}) {
  // 特殊location显示
  const displayName = getCountryName(race);

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
    <div className="relative rounded-2xl bg-white p-6 shadow flex flex-col justify-between min-h-[220px] h-64">
      {/* 头部信息 */}
      <div>
        <p className="text-xs text-zinc-400 font-semibold tracking-wider mb-1">
          {race.round_number === 0 ? "TESTING" : `ROUND ${race.round_number}`}
        </p>
        <div className="flex items-center gap-3">
          <CountryFlag country={displayName} className="w-8 h-6 rounded" />
          <h2 className="text-3xl font-extrabold text-zinc-900">
            {displayName}
          </h2>
        </div>
        <p className="text-sm text-zinc-500 font-medium mt-1 min-h-[2.5rem] line-clamp-2">
          {race.official_event_name}
        </p>
      </div>

      {/* 底部信息 */}
      <div className="flex justify-between items-end">
        <div className="text-2xl font-bold text-zinc-900">{dateStr}</div>
        <div className="opacity-90">
          {race.circuit_id ? (
            <CircuitImage
              src={`/circuits_svg/${race.circuit_id}.svg`}
              alt={race.circuit?.circuit_name || "赛道布局"}
              className="h-[65px] w-auto"
            />
          ) : (
            <TrackPlaceholder />
          )}
        </div>
      </div>
    </div>
  );
});

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

  // 为顶部卡片准备随机背景图
  const backgroundImages = [
    "random_photo_1.jpg",
    "random_photo_2.jpg",
    "random_photo_3.jpg",
    "random_photo_4.jpg",
    "random_photo_5.jpg",
    "random_photo_6.jpg",
    "random_photo_7.jpg",
    "random_photo_8.jpg",
    "random_photo_9.jpg",
    "random_photo_10.jpg",
    "random_photo_11.jpg",
    "random_photo_12.jpg",
    "random_photo_13.jpg",
    "random_photo_14.jpg",
    "random_photo_15.jpg",
    "random_photo_16.jpg",
    "random_photo_17.jpg",
    "random_photo_18.jpg",
    "random_photo_19.jpg",
    "random_photo_20.jpg",
    "random_photo_21.jpg",
    "random_photo_22.jpg",
    "random_photo_23.jpg",
    "random_photo_24.jpg",
    "random_photo_25.jpg",
    "random_photo_26.jpg",
    "random_photo_27.jpg",
    "random_photo_28.jpg",
    "random_photo_29.jpg",
  ];

  const shuffle = (arr: string[]) => arr.sort(() => 0.5 - Math.random());
  const randomBgs = shuffle([...backgroundImages]).slice(0, 4);
  const bgUrls = randomBgs.map((img) => `/random_backgroud/${img}`);

  return (
    <div className="space-y-6 bg-background min-h-screen pb-10">
      <div className="relative w-screen ">
        <div className="w-[90vw] mx-auto px-2 pt-6 pb-8">
          {/* <div className="flex items-center space-x-2 justify-center mb-6">
            <img src="/calendar.png" alt="logo" className="h-10 w-10" />
            <span className="text-4xl font-extrabold tracking-tight">
              2025 赛历
            </span>
          </div> */}
          <div className="flex flex-row gap-x-6">
            {/* Previous */}
            <div className="flex flex-col flex-[1_1_0%]">
              <span className="mb-3 ml-2 text-2xl font-bold text-zinc-800">
                Previous
              </span>
              <RaceCard race={prevRace} wide={false} bgImageUrl={bgUrls[0]} />
            </div>
            {/* Next */}
            <div className="flex flex-col flex-[2_2_0%]">
              <span className="mb-3 ml-2 text-2xl font-bold text-zinc-800">
                Next
              </span>
              <RaceCard race={nextRace} wide={true} bgImageUrl={bgUrls[1]} />
            </div>
            {/* Upcoming1 */}
            <div className="flex flex-col flex-[1_1_0%]">
              <span className="mb-3 ml-2 text-2xl font-bold text-zinc-800">
                {upcoming.length > 0 ? "Upcoming" : ""}
              </span>
              {upcoming[0] && (
                <RaceCard
                  race={upcoming[0]}
                  wide={false}
                  bgImageUrl={bgUrls[2]}
                />
              )}
            </div>
            {/* Upcoming2 */}
            <div className="flex flex-col flex-[1_1_0%]">
              <span className="mb-3 ml-2 text-2xl font-bold text-zinc-800">
                &nbsp;
              </span>
              {upcoming[1] && (
                <RaceCard
                  race={upcoming[1]}
                  wide={false}
                  bgImageUrl={bgUrls[3]}
                />
              )}
            </div>
          </div>
        </div>
      </div>
      {raceArr.length > 0 ? (
        <div className="max-w-[90vw] mx-auto grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 px-2">
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
