"use client";

import Link from "next/link";
import Image from "next/image";
import { useUpcomingRaces } from "@/hooks/use-races";
import { getRaceDisplayName, getRaceNationality } from "@/lib/utils";
import { CountryFlag } from "@/components/CountryFlag";
import { usePathname } from "next/navigation";

// 自定义日期格式化函数：只显示月和日
function formatMonthDay(dateStr?: string) {
  if (!dateStr) return "-";
  const date = new Date(dateStr);
  // 中文格式：6月27日
  return `${date.getMonth() + 1}月${date.getDate()}日`;
}

export function Header() {
  // 获取即将到来的比赛
  const { data: upcoming, isLoading } = useUpcomingRaces();
  const nextRace = upcoming?.[0];
  const pathname = usePathname();

  return (
    <header className="sticky top-0 z-50 w-full bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
      <div className="container pt-6 flex h-14 items-center">
        {/* Logo */}
        <Link href="/" className="flex items-center pl-4">
          <Image
            src="/LOGO-race_car.png"
            alt="F1 Logo"
            width={70}
            height={70}
            className="rounded-lg transition-transform duration-300 hover:scale-110 hover:rotate-6 drop-shadow-lg"
            priority
          />
        </Link>

        {/* 导航菜单 */}
        <nav className="hidden md:flex items-center space-x-6 ml-6">
          <Link
            href="/races"
            className={`text-xl font-semibold tracking-wider px-2 py-1 transition-all border-b-2 ${
              pathname === "/races"
                ? "border-[rgb(225,6,0)] text-primary"
                : "border-transparent hover:border-current hover:text-primary"
            }`}
          >
            赛程
          </Link>
          <Link
            href="/drivers"
            className={`text-xl font-semibold tracking-wider px-2 py-1 transition-all border-b-2 ${
              pathname === "/drivers"
                ? "border-[rgb(225,6,0)] text-primary"
                : "border-transparent hover:border-current hover:text-primary"
            }`}
          >
            车手
          </Link>
          <Link
            href="/constructors"
            className={`text-xl font-semibold tracking-wider px-2 py-1 transition-all border-b-2 ${
              pathname === "/constructors"
                ? "border-[rgb(225,6,0)] text-primary"
                : "border-transparent hover:border-current hover:text-primary"
            }`}
          >
            车队
          </Link>
          <Link
            href="/standings"
            className={`text-xl font-semibold tracking-wider px-2 py-1 transition-all border-b-2 ${
              pathname === "/standings"
                ? "border-[rgb(225,6,0)] text-primary"
                : "border-transparent hover:border-current hover:text-primary"
            }`}
          >
            排行榜
          </Link>
        </nav>
      </div>
      {/* 顶部下一站信息栏 */}
      <div
        className="w-full  flex items-center justify-center"
        style={{ minHeight: 38 }}
      >
        {isLoading ? (
          <span className="text-sm text-zinc-400 px-2 py-1">
            加载下一站信息...
          </span>
        ) : nextRace ? (
          <div className="flex items-center space-x-2 py-1 pt-4 pb-2">
            <span className="bg-[rgb(225,6,0)] text-white text-base font-bold px-3 py-1 rounded-lg tracking-wide">
              下一站
            </span>
            <Link
              href={`/races/${nextRace.id}`}
              className="text-lg font-bold text-zinc-900 flex items-center hover:text-[rgb(225,6,0)] transition-colors duration-200 cursor-pointer group"
            >
              <CountryFlag
                nationality={getRaceNationality(nextRace)}
                size="1.4em"
                className="mr-1.5"
              />
              <span className="ml-1 border-b-2 border-transparent group-hover:border-[rgb(225,6,0)] transition-all duration-200">
                {getRaceDisplayName(nextRace)}
              </span>
            </Link>
            <span className="bg-zinc-200 text-zinc-700 rounded-lg px-3 py-1 text-base font-medium ml-2">
              {formatMonthDay(nextRace.event_date)}
            </span>
          </div>
        ) : (
          <span className="text-sm text-zinc-400 px-2 py-1">
            暂无下一站信息
          </span>
        )}
      </div>
    </header>
  );
}
