"use client";

import { useState } from "react";
import Link from "next/link";
import Image from "next/image";
import { useUpcomingRaces } from "@/hooks/use-races";
import { getCountryName } from "@/lib/utils";
import { CountryFlag } from "@/components/CountryFlag";

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
  const nextRace = upcoming?.data?.[0];

  return (
    <header className="sticky top-0 z-50 w-full border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
      <div className="container flex h-14 items-center">
        {/* Logo */}
        <Link href="/" className="flex items-center pl-4">
          <Image
            src="/LOGO-race_car.png"
            alt="F1 Logo"
            width={50}
            height={50}
            className="rounded-lg"
          />
        </Link>

        {/* 导航菜单 */}
        <nav className="hidden md:flex items-center space-x-6 ml-6">
          <Link
            href="/races"
            className="text-sm font-medium transition-colors hover:text-primary"
          >
            赛程
          </Link>
          <Link
            href="/drivers"
            className="text-sm font-medium transition-colors hover:text-primary"
          >
            车手
          </Link>
          <Link
            href="/driver_standing"
            className="text-sm font-medium transition-colors hover:text-primary"
          >
            车手排行榜
          </Link>
          <Link
            href="/constructors"
            className="text-sm font-medium transition-colors hover:text-primary"
          >
            车队
          </Link>
          <Link
            href="/constructor_standing"
            className="text-sm font-medium transition-colors hover:text-primary"
          >
            车队排行榜
          </Link>
          <Link
            href="/circuits"
            className="text-sm font-medium transition-colors hover:text-primary"
          >
            赛道
          </Link>
        </nav>
      </div>
      {/* 顶部下一站信息栏 */}
      <div
        className="w-full  flex items-center justify-center border-b border-zinc-200"
        style={{ minHeight: 38 }}
      >
        {isLoading ? (
          <span className="text-sm text-zinc-400 px-2 py-1">
            加载下一站信息...
          </span>
        ) : nextRace ? (
          <div className="flex items-center space-x-2 py-1">
            <span className="text-base font-medium text-zinc-700 tracking-wide">
              下一站
            </span>
            <span className="text-lg font-bold text-zinc-900 flex items-center">
              <CountryFlag
                country={getCountryName(nextRace)}
                className="w-5 mr-1.5"
              />
              <span className="ml-1">{getCountryName(nextRace)}</span>
            </span>
            <span className="bg-zinc-200 text-zinc-700 rounded px-2 py-0.5 text-sm font-semibold ml-2">
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
