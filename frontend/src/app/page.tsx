"use client";

import { DriverStanding, ConstructorStanding } from "@/types";

import { useState } from "react";
import Image from "next/image";
import { useDriverStandings } from "@/hooks/use-driver-standings";
import { useConstructorStandings } from "@/hooks/use-constructor-standings";
import { getTeamColor } from "@/lib/team-colors";
import { getTeamLogoFilename } from "@/lib/team-logo-map";
import { CountryFlag } from "@/components/CountryFlag";

// 工具函数，从全名生成头像路径
const getAvatarPath = (fullName: string) => {
  if (!fullName) return "/driver_photo_avif/default.avif";
  const normalizedName = fullName
    .normalize("NFD")
    .replace(/[\u0300-\u036f]/g, "");
  const sanitizedName = normalizedName.replace(/ /g, "_");
  return `/driver_photo_avif/${sanitizedName}.avif`;
};

// 获取车队车辆图片路径
const getConstructorCarPath = (constructorId: string) => {
  const carMapping: Record<string, string> = {
    mercedes: "mercedes.png",
    ferrari: "ferrari.png",
    red_bull: "red_bull.png",
    mclaren: "mclaren.png",
    aston_martin: "aston_martin.png",
    alpine: "alpine.png",
    williams: "williams.png",
    haas: "haas.png",
    rb: "rb.png",
    sauber: "sauber.png",
  };
  return `/2025_constructor_car_photo/${carMapping[constructorId] || "mercedes.png"}`;
};

// 获取名次后缀
const getPositionSuffix = (position: number) => {
  switch (position) {
    case 1:
      return "ST";
    case 2:
      return "ND";
    case 3:
      return "RD";
    default:
      return "TH";
  }
};

// 车手卡片组件
function DriverCard({
  driver,
  position,
  className,
}: {
  driver: DriverStanding;
  position: number;
  className?: string;
}) {
  const teamColor = getTeamColor(driver.constructor_id || "");

  // 解析车手姓名，假设格式是 "Forename Surname"
  const nameParts = driver.driver_name.split(" ");
  const surname = nameParts[nameParts.length - 1];
  const forename = nameParts.slice(0, -1).join(" ");

  return (
    <div
      className={`relative rounded-lg overflow-hidden shadow-lg ${className}`}
      style={{ backgroundColor: teamColor }}
    >
      {/* 渐变覆盖层 */}
      <div className="absolute inset-0 bg-gradient-to-r from-black/30 to-transparent" />

      {/* 内容 */}
      <div className="relative p-6 h-full flex flex-col justify-between text-white">
        {/* 左上角信息 */}
        <div className="space-y-2">
          <div className="text-4xl font-bold">
            {position}
            <span className="text-2xl font-normal">
              {getPositionSuffix(position)}
            </span>
          </div>
          <div className="space-y-1">
            <div className="text-xl font-medium">
              {forename} <span className="font-bold">{surname}</span>
            </div>
            <div className="text-sm opacity-90">{driver.constructor_name}</div>
            {driver.nationality && (
              <div className="flex items-center justify-start">
                <CountryFlag nationality={driver.nationality} size="2em" />
              </div>
            )}
          </div>
        </div>

        {/* 左下角积分 */}
        <div className="text-2xl font-bold">
          {driver.points} <span className="text-lg font-normal">PTS</span>
        </div>
      </div>

      {/* 右侧车手头像 */}
      <div className="absolute right-0 top-0 bottom-0 w-48 overflow-hidden">
        <Image
          src={getAvatarPath(driver.driver_name)}
          alt={driver.driver_name}
          width={192}
          height={384}
          className="object-cover w-full h-full scale-110"
          style={{ objectPosition: "center -10%" }}
        />
      </div>
    </div>
  );
}

// 车队卡片组件
function ConstructorCard({
  constructor,
  position,
  className,
  drivers,
}: {
  constructor: ConstructorStanding;
  position: number;
  className?: string;
  drivers?: string[];
}) {
  const teamColor = getTeamColor(constructor.constructor_id);

  // 格式化车手名字，family name加粗
  const formatDriverName = (fullName: string) => {
    const nameParts = fullName.split(" ");
    const surname = nameParts[nameParts.length - 1];
    const forename = nameParts.slice(0, -1).join(" ");

    return (
      <span>
        {forename} <span className="font-bold">{surname}</span>
      </span>
    );
  };

  return (
    <div
      className={`relative rounded-lg overflow-hidden shadow-lg ${className}`}
      style={{ backgroundColor: teamColor }}
    >
      {/* 渐变覆盖层 */}
      <div className="absolute inset-0 bg-gradient-to-r from-black/30 to-transparent" />

      {/* 车队logo - 右上角 */}
      <div className="absolute top-4 right-4 z-10">
        <Image
          src={`/team_logos/${getTeamLogoFilename(constructor.constructor_id)}.svg`}
          alt={constructor.constructor_name}
          width={48}
          height={48}
          className="drop-shadow-lg"
        />
      </div>

      {/* 内容 */}
      <div className="relative p-6 h-full flex flex-col justify-between text-white">
        {/* 左上角信息 */}
        <div className="space-y-2">
          <div className="text-4xl font-bold">
            {position}
            <span className="text-2xl font-normal">
              {getPositionSuffix(position)}
            </span>
          </div>
          <div className="space-y-1">
            <div className="text-xl font-bold">
              {constructor.constructor_name}
            </div>
            <div className="text-2xl font-bold">
              {constructor.points}{" "}
              <span className="text-lg font-normal">PTS</span>
            </div>
            {drivers && drivers.length > 0 && (
              <div className="text-sm opacity-90 space-y-1">
                {drivers.map((driverName, index) => (
                  <div key={index}>{formatDriverName(driverName)}</div>
                ))}
              </div>
            )}
          </div>
        </div>
      </div>

      {/* 底部车辆图片 */}
      <div className="absolute bottom-3 right-5 w-4/5 h-3/5 -translate-x-4">
        <Image
          src={getConstructorCarPath(constructor.constructor_id)}
          alt={`${constructor.constructor_name} car`}
          fill
          className="object-contain object-bottom-right opacity-80 scale-110"
        />
      </div>
    </div>
  );
}

export default function HomePage() {
  const [activeTab, setActiveTab] = useState<"drivers" | "teams">("drivers");
  const { standings: driverStandings, isLoading: driversLoading } =
    useDriverStandings();
  const { standings: constructorStandings, isLoading: constructorsLoading } =
    useConstructorStandings();

  // 获取前三名数据
  const topDrivers = driverStandings?.slice(0, 3) || [];
  const topConstructors = constructorStandings?.slice(0, 3) || [];

  // 获取车队的车手信息
  const getConstructorDrivers = (constructorId: string) => {
    return (
      driverStandings
        ?.filter((driver) => driver.constructor_id === constructorId)
        .map((driver) => driver.driver_name) || []
    );
  };

  const renderDriverPodium = () => {
    if (driversLoading) {
      return <div className="text-center py-12">加载中...</div>;
    }

    if (topDrivers.length < 3) {
      return <div className="text-center py-12">数据不足</div>;
    }

    // 排列顺序：第二名(左)、第一名(中)、第三名(右)
    const podiumOrder = [topDrivers[1], topDrivers[0], topDrivers[2]];
    const heights = ["h-80", "h-96", "h-72"]; // 第二名、第一名、第三名的高度

    return (
      <div className="flex items-end justify-center gap-6 mb-8 px-4">
        {podiumOrder.map((driver, index) => (
          <div key={driver.driver_id} className="flex-1 max-w-md">
            <DriverCard
              driver={driver}
              position={index === 1 ? 1 : index === 0 ? 2 : 3}
              className={heights[index]}
            />
          </div>
        ))}
      </div>
    );
  };

  const renderConstructorPodium = () => {
    if (constructorsLoading) {
      return <div className="text-center py-12">加载中...</div>;
    }

    if (topConstructors.length < 3) {
      return <div className="text-center py-12">数据不足</div>;
    }

    // 排列顺序：第二名(左)、第一名(中)、第三名(右)
    const podiumOrder = [
      topConstructors[1],
      topConstructors[0],
      topConstructors[2],
    ];
    const heights = ["h-80", "h-96", "h-72"]; // 第二名、第一名、第三名的高度

    return (
      <div className="flex items-end justify-center gap-6 mb-8 px-4">
        {podiumOrder.map((constructor, index) => (
          <div key={constructor.constructor_id} className="flex-1 max-w-md">
            <ConstructorCard
              constructor={constructor}
              position={index === 1 ? 1 : index === 0 ? 2 : 3}
              className={heights[index]}
              drivers={getConstructorDrivers(constructor.constructor_id)}
            />
          </div>
        ))}
      </div>
    );
  };

  const getButtonClass = (tabName: "drivers" | "teams") => {
    return `px-6 py-3 text-lg font-bold rounded-md transition-colors ${
      activeTab === tabName
        ? "bg-zinc-800 text-white"
        : "bg-transparent text-zinc-600 hover:bg-zinc-200"
    }`;
  };

  return (
    <div className="min-h-screen bg-[#F7F4F1]">
      <div className="container mx-auto px-4 py-8">
        {/* 页面标题和选项卡 */}
        <div className="text-center mb-12">
          <h1 className="text-5xl font-black tracking-wider mb-8">
            2025 FORMULA 1
          </h1>
          <div className="flex justify-center">
            <div className="flex items-center p-1 bg-zinc-100 rounded-lg">
              <button
                onClick={() => setActiveTab("drivers")}
                className={getButtonClass("drivers")}
              >
                DRIVERS
              </button>
              <button
                onClick={() => setActiveTab("teams")}
                className={getButtonClass("teams")}
              >
                TEAMS
              </button>
            </div>
          </div>
        </div>

        {/* 内容区域 */}
        {activeTab === "drivers"
          ? renderDriverPodium()
          : renderConstructorPodium()}

        {/* 完整积分榜链接 */}
        <div className="text-center">
          <button
            onClick={() =>
              (window.location.href = `/standings?tab=${activeTab}`)
            }
            className="inline-flex items-center px-6 py-3 bg-zinc-800 text-white font-bold rounded-md hover:bg-zinc-700 transition-colors cursor-pointer"
          >
            Show all
            <svg
              className="ml-2 w-4 h-4"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M19 9l-7 7-7-7"
              />
            </svg>
          </button>
        </div>
      </div>
    </div>
  );
}
