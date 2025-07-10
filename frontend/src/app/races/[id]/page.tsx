"use client";

import { useRace } from "@/hooks/use-races";
import { formatDate, getCountryName } from "@/lib/utils";
import { CountryFlag } from "@/components/CountryFlag";
import { Calendar, MapPin, Clock, Flag } from "lucide-react";
import Image from "next/image";
import React, { useState } from "react";

// 国家/地点到时区的映射
const LOCATION_TIMEZONE_MAP: Record<string, string> = {
  // 根据F1比赛地点映射时区
  Bahrain: "Asia/Bahrain",
  "Saudi Arabia": "Asia/Riyadh",
  Jeddah: "Asia/Riyadh",
  Australia: "Australia/Melbourne",
  Melbourne: "Australia/Melbourne",
  Japan: "Asia/Tokyo",
  Suzuka: "Asia/Tokyo",
  China: "Asia/Shanghai",
  Shanghai: "Asia/Shanghai",
  "Chinese Grand Prix": "Asia/Shanghai",
  上海: "Asia/Shanghai",
  Miami: "America/New_York",
  "United States": "America/New_York",
  "Emilia-Romagna": "Europe/Rome",
  Imola: "Europe/Rome",
  Italy: "Europe/Rome",
  Monaco: "Europe/Monaco",
  "Monte-Carlo": "Europe/Monaco",
  Canada: "America/Toronto",
  Montreal: "America/Toronto",
  Spain: "Europe/Madrid",
  Barcelona: "Europe/Madrid",
  Austria: "Europe/Vienna",
  Spielberg: "Europe/Vienna",
  "United Kingdom": "Europe/London",
  "Great Britain": "Europe/London",
  Silverstone: "Europe/London",
  Hungary: "Europe/Budapest",
  Budapest: "Europe/Budapest",
  Belgium: "Europe/Brussels",
  Spa: "Europe/Brussels",
  "Spa-Francorchamps": "Europe/Brussels",
  Netherlands: "Europe/Amsterdam",
  Zandvoort: "Europe/Amsterdam",
  Azerbaijan: "Asia/Baku",
  Baku: "Asia/Baku",
  Singapore: "Asia/Singapore",
  Mexico: "America/Mexico_City",
  "Mexico City": "America/Mexico_City",
  Brazil: "America/Sao_Paulo",
  "São Paulo": "America/Sao_Paulo",
  Interlagos: "America/Sao_Paulo",
  "Las Vegas": "America/Los_Angeles",
  Nevada: "America/Los_Angeles",
  Qatar: "Asia/Qatar",
  Losail: "Asia/Qatar",
  "Abu Dhabi": "Asia/Dubai",
  UAE: "Asia/Dubai",
  "Yas Marina": "Asia/Dubai",
  // 历史赛道
  Turkey: "Europe/Istanbul",
  Istanbul: "Europe/Istanbul",
  Russia: "Europe/Moscow",
  Sochi: "Europe/Moscow",
  Portugal: "Europe/Lisbon",
  Portimao: "Europe/Lisbon",
  "South Africa": "Africa/Johannesburg",
  // 添加更多映射...
};

// 获取比赛所在地时区
const getTrackTimezone = (race: any): string => {
  // 尝试从多个字段获取地理信息
  const country = race.country || "";
  const location = race.location || "";
  const circuitName = race.circuit?.circuit_name || "";
  const eventName = race.official_event_name || "";

  // 创建搜索候选列表（按优先级排序）
  const searchCandidates = [
    location, // 优先使用location
    country, // 然后country
    circuitName, // 赛道名称
    eventName, // 事件名称
  ].filter(Boolean); // 过滤空值

  // 在映射中搜索匹配项
  for (const candidate of searchCandidates) {
    if (LOCATION_TIMEZONE_MAP[candidate]) {
      const timezone = LOCATION_TIMEZONE_MAP[candidate];
      // console.log(`🌍 时区匹配成功: "${candidate}" -> ${timezone}`);
      return timezone;
    }

    // 尝试部分匹配（比如 "Formula 1 Rolex Australian Grand Prix 2025" 匹配 "Australia"）
    for (const [key, timezone] of Object.entries(LOCATION_TIMEZONE_MAP)) {
      if (
        candidate.toLowerCase().includes(key.toLowerCase()) ||
        key.toLowerCase().includes(candidate.toLowerCase())
      ) {
        // console.log(`🌍 时区部分匹配成功: "${candidate}" 包含 "${key}" -> ${timezone}`);
        return timezone;
      }
    }
  }

  // 默认返回UTC
  console.warn(`🌍 无法确定比赛地点的时区，使用UTC。比赛信息:`, {
    country,
    location,
    circuitName,
    eventName,
    searchCandidates,
  });
  return "UTC";
};

// 简化的时区转换函数
const convertToTimezone = (
  dateStr: string | undefined,
  targetTimezone: string,
  sourceTimezone: string
): { date: string; time: string } => {
  if (!dateStr) return { date: "-", time: "-" };

  try {
    // 标准化时间格式
    let isoString = dateStr;
    if (!isoString.includes("T")) {
      isoString = isoString.replace(" ", "T");
    }
    if (!isoString.endsWith("Z")) {
      isoString += "Z"; // 确保被识别为UTC时间
    }

    // 创建UTC时间的Date对象
    const utcDate = new Date(isoString);

    // 调试输出
    console.log(
      `🕐 时区转换: 原始UTC时间: ${dateStr} -> Date对象: ${utcDate.toISOString()} -> 目标时区: ${targetTimezone}`
    );

    // 根据目标时区格式化显示
    const dateOptions: Intl.DateTimeFormatOptions = {
      month: "short",
      day: "numeric",
      timeZone: targetTimezone,
    };

    const timeOptions: Intl.DateTimeFormatOptions = {
      hour: "2-digit",
      minute: "2-digit",
      hour12: false,
      timeZone: targetTimezone,
    };

    const formattedDate = utcDate.toLocaleDateString("en-US", dateOptions);
    const formattedTime = utcDate.toLocaleTimeString("en-US", timeOptions);

    console.log(
      `🕐 转换结果: ${formattedDate} ${formattedTime} (${targetTimezone})`
    );

    return {
      date: formattedDate,
      time: formattedTime,
    };
  } catch (error) {
    console.warn("时区转换失败:", error, "输入:", dateStr);

    // fallback: 直接显示原始时间
    try {
      const date = new Date(dateStr);
      return {
        date: date.toLocaleDateString("en-US", {
          month: "short",
          day: "numeric",
        }),
        time: date.toLocaleTimeString("en-US", {
          hour: "2-digit",
          minute: "2-digit",
          hour12: false,
        }),
      };
    } catch {
      return { date: "-", time: "-" };
    }
  }
};

// 简化的时区偏移映射 - 考虑夏令时
const getTimezoneOffsetHours = (timezone: string): number => {
  // 这个函数现在不再需要，因为我们使用浏览器原生的时区转换
  const now = new Date();
  const month = now.getMonth() + 1; // 1-12

  const offsets: Record<string, { winter: number; summer: number }> = {
    "Europe/London": { winter: 0, summer: 1 }, // UTC+0/+1
    "Asia/Shanghai": { winter: 8, summer: 8 }, // UTC+8 (无夏令时)
    "America/New_York": { winter: -5, summer: -4 }, // UTC-5/-4
    "America/Los_Angeles": { winter: -8, summer: -7 }, // UTC-8/-7
    "Asia/Tokyo": { winter: 9, summer: 9 }, // UTC+9 (无夏令时)
    "Asia/Bahrain": { winter: 3, summer: 3 }, // UTC+3
    "Asia/Riyadh": { winter: 3, summer: 3 }, // UTC+3
    "Australia/Melbourne": { winter: 10, summer: 11 }, // UTC+10/+11
    "Asia/Baku": { winter: 4, summer: 4 }, // UTC+4
    "Asia/Singapore": { winter: 8, summer: 8 }, // UTC+8
    "America/Mexico_City": { winter: -6, summer: -5 }, // UTC-6/-5
    "America/Sao_Paulo": { winter: -3, summer: -3 }, // UTC-3
    "Asia/Qatar": { winter: 3, summer: 3 }, // UTC+3
    "Asia/Dubai": { winter: 4, summer: 4 }, // UTC+4
  };

  const tzConfig = offsets[timezone];
  if (!tzConfig) return 0;

  // 简化的夏令时判断 (3月-10月为夏季)
  const isSummer = month >= 3 && month <= 10;
  return isSummer ? tzConfig.summer : tzConfig.winter;
};

// 方格旗组件
const CheckerFlag = () => (
  <svg
    xmlns="http://www.w3.org/2000/svg"
    width="1.2em"
    height="1.2em"
    fill="currentColor"
    viewBox="0 0 24 24"
    className="mr-2"
  >
    <title>Chequered Flag</title>
    <path d="M9 6h2V4H9zm4 0V4h2v2zm-4 8v-2h2v2zm8-4V8h2v2zm0 4v-2h2v2zm-4 0v-2h2v2zm4-8V4h2v2zm-6 2V6h2v2zM5 20V4h2v2h2v2H7v2h2v2H7v8zm10-8v-2h2v2zm-4 0v-2h2v2zm-2-2V8h2v2zm4 0V8h2v2zm2-2V6h2v2z" />
  </svg>
);

// 赛道图组件
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
      width={300}
      height={200}
      className={className || "h-48 w-auto"}
      loading="lazy"
      onError={(e) => {
        const target = e.target as HTMLImageElement;
        target.style.display = "none";
      }}
    />
  );
});

interface SessionCardProps {
  sessionName: string;
  sessionDate?: string;
  isCompleted: boolean;
  timezone: string;
}

const SessionCard: React.FC<SessionCardProps> = ({
  sessionName,
  sessionDate,
  isCompleted,
  timezone,
}) => {
  // 从UTC转换到目标时区
  const { date, time } = convertToTimezone(
    sessionDate,
    timezone,
    "UTC" // 原始数据始终是UTC
  );

  return (
    <div className="bg-white rounded-lg p-4 border border-gray-200 hover:shadow-md transition-shadow">
      <div className="flex items-center justify-between">
        <div className="flex items-center">
          {isCompleted && <CheckerFlag />}
          <div>
            <h3 className="font-bold text-lg text-gray-900">{sessionName}</h3>
            <div className="flex items-center text-sm text-gray-600 mt-1">
              <Calendar className="w-4 h-4 mr-1" />
              {date}
            </div>
          </div>
        </div>
        <div className="text-right">
          <div className="flex items-center text-lg font-mono font-bold text-gray-900">
            <Clock className="w-4 h-4 mr-1" />
            {time}
          </div>
        </div>
      </div>
    </div>
  );
};

export default function RaceDetailPage({
  params,
}: {
  params: Promise<{ id: string }>;
}) {
  const { id } = React.use(params);
  const raceId = parseInt(id);
  const { data: raceResponse, isLoading, error } = useRace(raceId);

  // 时区模式状态：'my' 表示用户本地时区，'track' 表示赛道时区
  const [timezoneMode, setTimezoneMode] = useState<"my" | "track">("my");

  // 获取race数据（在所有条件返回之前确保hooks调用顺序一致）
  const race = raceResponse?.data;

  // 确定要使用的时区（在条件返回之前）
  const currentTimezone =
    timezoneMode === "my"
      ? Intl.DateTimeFormat().resolvedOptions().timeZone // 用户本地时区
      : race
        ? getTrackTimezone(race) // 赛道时区
        : "UTC"; // 默认UTC

  // 调试：输出原始时间数据（必须在所有条件返回之前）
  React.useEffect(() => {
    if (race) {
      console.log("🕐 调试时间数据:", {
        比赛: race.official_event_name,
        地点: `${race.location}, ${race.country}`,
        识别的时区: getTrackTimezone(race),
        原始session时间: {
          session1_date: race.session1_date,
          session2_date: race.session2_date,
          session3_date: race.session3_date,
          session4_date: race.session4_date,
          session5_date: race.session5_date,
        },
        当前时区模式: timezoneMode,
        使用的时区: currentTimezone,
      });
    }
  }, [race, timezoneMode, currentTimezone]);

  if (isLoading) {
    return (
      <div className="flex items-center justify-center py-8 bg-background min-h-[60vh]">
        <div className="text-center">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary mx-auto mb-4"></div>
          <p className="text-muted-foreground">加载比赛详情中...</p>
        </div>
      </div>
    );
  }

  if (error || !raceResponse?.success) {
    return (
      <div className="text-center py-8 bg-background min-h-[60vh]">
        <p className="text-red-500">加载比赛详情失败，请稍后重试</p>
      </div>
    );
  }

  // race 和 currentTimezone 已在上面定义，不需要重复声明
  if (!race) {
    return (
      <div className="text-center py-8 bg-background min-h-[60vh]">
        <p className="text-red-500">找不到比赛数据</p>
      </div>
    );
  }

  const displayName = getCountryName(race);

  // 判断比赛是否已结束
  const now = new Date();
  const eventDate = race.event_date ? new Date(race.event_date) : null;
  const isPastRace = Boolean(eventDate && eventDate < now);

  // 根据event_format确定session名称
  const getSessionNames = () => {
    if (race.event_format === "sprint_qualifying") {
      return [
        "PRACTICE 1",
        "SPRINT QUALIFYING",
        "SPRINT",
        "QUALIFYING",
        "RACE",
      ];
    } else {
      return ["PRACTICE 1", "PRACTICE 2", "PRACTICE 3", "QUALIFYING", "RACE"];
    }
  };

  const sessionNames = getSessionNames();
  const sessions = [
    { name: sessionNames[0], date: race.session1_date },
    { name: sessionNames[1], date: race.session2_date },
    { name: sessionNames[2], date: race.session3_date },
    { name: sessionNames[3], date: race.session4_date },
    { name: sessionNames[4], date: race.session5_date },
  ]; // 显示所有5个session，即使某些没有具体日期

  return (
    <div className="min-h-screen bg-gray-50">
      {/* 头部横幅 */}
      <div className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 py-8">
          <div className="flex flex-col lg:flex-row gap-8">
            {/* 左侧：比赛信息 */}
            <div className="flex-1">
              <div className="flex items-center gap-2 text-sm text-gray-500 mb-2">
                <span className="font-semibold">
                  {race.round_number === 0
                    ? "TESTING"
                    : `ROUND ${race.round_number}`}
                </span>
              </div>

              <div className="flex items-center gap-4 mb-4">
                <CountryFlag
                  country={displayName}
                  className="w-12 h-8 rounded"
                />
                <h1 className="text-4xl font-extrabold text-gray-900 hover:underline hover:decoration-gray-900 hover:decoration-2 hover:underline-offset-4 transition-all duration-200 cursor-pointer">
                  {displayName}
                </h1>
              </div>

              <h2 className="text-2xl font-bold text-gray-700 mb-4">
                {race.official_event_name}
              </h2>

              <div className="flex flex-wrap gap-6 text-sm text-gray-600">
                <div className="flex items-center">
                  <MapPin className="w-4 h-4 mr-2" />
                  <span>{race.circuit?.circuit_name}</span>
                </div>
                <div className="flex items-center">
                  <Calendar className="w-4 h-4 mr-2" />
                  <span>{eventDate ? formatDate(eventDate) : "-"}</span>
                </div>
              </div>
            </div>

            {/* 右侧：赛道图 */}
            <div className="lg:w-80 flex justify-center lg:justify-end">
              {race.circuit_id ? (
                <CircuitImage
                  src={`/circuits_svg/${race.circuit_id}.svg`}
                  alt={race.circuit?.circuit_name || "赛道布局"}
                  className="h-48 w-auto"
                />
              ) : (
                <div className="h-48 w-64 bg-gray-200 rounded-lg flex items-center justify-center">
                  <span className="text-gray-500">暂无赛道图</span>
                </div>
              )}
            </div>
          </div>
        </div>
      </div>

      {/* 主要内容 */}
      <div className="max-w-7xl mx-auto px-4 py-8">
        {/* Schedule 标题部分 */}
        <div className="mb-8">
          <div className="flex items-center gap-4 mb-6">
            <h2 className="text-3xl font-extrabold text-gray-900">SCHEDULE</h2>
            <div className="flex gap-2">
              <button className="bg-red-600 text-white px-4 py-2 rounded font-semibold text-sm">
                Add F1 calendar
              </button>
              <div className="flex bg-gray-100 rounded">
                <button
                  className={`px-4 py-2 rounded text-sm font-semibold transition-colors ${
                    timezoneMode === "my"
                      ? "bg-black text-white"
                      : "text-gray-600 hover:text-gray-900"
                  }`}
                  onClick={() => setTimezoneMode("my")}
                >
                  My time
                </button>
                <button
                  className={`px-4 py-2 rounded text-sm font-semibold transition-colors ${
                    timezoneMode === "track"
                      ? "bg-black text-white"
                      : "text-gray-600 hover:text-gray-900"
                  }`}
                  onClick={() => setTimezoneMode("track")}
                >
                  Track time
                </button>
              </div>
            </div>
          </div>

          {/* 时区信息显示 */}
          <div className="mb-4 text-sm text-gray-600">
            <span>Showing times in: </span>
            <span className="font-semibold">
              {timezoneMode === "my"
                ? `${Intl.DateTimeFormat().resolvedOptions().timeZone} (Your local time)`
                : `${currentTimezone} (Track time)`}
            </span>
          </div>
        </div>

        {/* Session 卡片列表 */}
        <div className="space-y-4">
          {sessions.map((session, index) => (
            <SessionCard
              key={index}
              sessionName={session.name}
              sessionDate={session.date}
              isCompleted={isPastRace}
              timezone={currentTimezone}
            />
          ))}
        </div>
      </div>
    </div>
  );
}
