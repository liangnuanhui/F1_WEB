"use client";

import { useActiveSeason } from "@/hooks/use-seasons";
import { useUpcomingRaces } from "@/hooks/use-races";
import { formatDate, formatRaceName } from "@/lib/utils";
import {
  Calendar,
  Users,
  Building2,
  MapPin,
  Trophy,
  TrendingUp,
} from "lucide-react";
import Link from "next/link";
import { Race } from "@/types";

export default function HomePage() {
  const { data: activeSeason, isLoading: seasonLoading } = useActiveSeason();
  const { data: upcomingRaces, isLoading: racesLoading } = useUpcomingRaces();

  const stats = [
    {
      title: "当前赛季",
      value: activeSeason?.data?.year || "2024",
      icon: TrendingUp,
      href: "/races",
    },
    {
      title: "即将比赛",
      value: upcomingRaces?.data?.length || 0,
      icon: Calendar,
      href: "/races",
    },
    {
      title: "车手数量",
      value: "20",
      icon: Users,
      href: "/drivers",
    },
    {
      title: "车队数量",
      value: "10",
      icon: Building2,
      href: "/constructors",
    },
    {
      title: "赛道数量",
      value: "24",
      icon: MapPin,
      href: "/circuits",
    },
    {
      title: "积分榜",
      value: "实时",
      icon: Trophy,
      href: "/standings",
    },
  ];

  return (
    <div className="space-y-8">
      {/* 欢迎区域 */}
      <div className="text-center space-y-4">
        <h1 className="text-4xl font-bold tracking-tight">
          欢迎来到 F1 赛事数据
        </h1>
        <p className="text-xl text-muted-foreground max-w-2xl mx-auto">
          探索一级方程式赛车的精彩世界，获取最新的赛程、车手、车队和积分榜信息
        </p>
      </div>

      {/* 统计卡片 */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {stats.map((stat) => (
          <Link
            key={stat.title}
            href={stat.href}
            className="group relative overflow-hidden rounded-lg border bg-card p-6 hover:shadow-lg transition-all duration-200"
          >
            <div className="flex items-center space-x-4">
              <div className="flex h-12 w-12 items-center justify-center rounded-lg bg-primary/10">
                <stat.icon className="h-6 w-6 text-primary" />
              </div>
              <div>
                <p className="text-sm font-medium text-muted-foreground">
                  {stat.title}
                </p>
                <p className="text-2xl font-bold">{stat.value}</p>
              </div>
            </div>
          </Link>
        ))}
      </div>

      {/* 即将到来的比赛 */}
      {!racesLoading &&
        upcomingRaces?.data &&
        upcomingRaces.data.length > 0 && (
          <div className="space-y-4">
            <h2 className="text-2xl font-bold">即将到来的比赛</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              {upcomingRaces.data.slice(0, 3).map((race: Race) => (
                <div
                  key={race.id}
                  className="rounded-lg border bg-card p-4 hover:shadow-md transition-shadow"
                >
                  <div className="flex items-center justify-between mb-2">
                    <h3 className="font-semibold">
                      {formatRaceName(race.name)}
                    </h3>
                    <span className="text-sm text-muted-foreground">
                      第 {race.round} 站
                    </span>
                  </div>
                  <div className="space-y-1 text-sm text-muted-foreground">
                    <p>{race.circuit?.name}</p>
                    <p>{formatDate(race.date, "long")}</p>
                    {race.time && <p>时间: {race.time.substring(0, 5)}</p>}
                  </div>
                </div>
              ))}
            </div>
            <div className="text-center">
              <Link
                href="/races"
                className="inline-flex items-center justify-center rounded-md bg-primary px-4 py-2 text-sm font-medium text-primary-foreground hover:bg-primary/90 transition-colors"
              >
                查看所有赛程
              </Link>
            </div>
          </div>
        )}

      {/* 快速导航 */}
      <div className="space-y-4">
        <h2 className="text-2xl font-bold">快速导航</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          <Link
            href="/races"
            className="flex items-center space-x-3 rounded-lg border bg-card p-4 hover:shadow-md transition-shadow"
          >
            <Calendar className="h-6 w-6 text-primary" />
            <div>
              <h3 className="font-semibold">赛程</h3>
              <p className="text-sm text-muted-foreground">查看比赛日程</p>
            </div>
          </Link>

          <Link
            href="/drivers"
            className="flex items-center space-x-3 rounded-lg border bg-card p-4 hover:shadow-md transition-shadow"
          >
            <Users className="h-6 w-6 text-primary" />
            <div>
              <h3 className="font-semibold">车手</h3>
              <p className="text-sm text-muted-foreground">浏览车手信息</p>
            </div>
          </Link>

          <Link
            href="/constructors"
            className="flex items-center space-x-3 rounded-lg border bg-card p-4 hover:shadow-md transition-shadow"
          >
            <Building2 className="h-6 w-6 text-primary" />
            <div>
              <h3 className="font-semibold">车队</h3>
              <p className="text-sm text-muted-foreground">了解车队详情</p>
            </div>
          </Link>

          <Link
            href="/standings"
            className="flex items-center space-x-3 rounded-lg border bg-card p-4 hover:shadow-md transition-shadow"
          >
            <Trophy className="h-6 w-6 text-primary" />
            <div>
              <h3 className="font-semibold">积分榜</h3>
              <p className="text-sm text-muted-foreground">查看排名情况</p>
            </div>
          </Link>
        </div>
      </div>

      {/* 加载状态 */}
      {(seasonLoading || racesLoading) && (
        <div className="flex items-center justify-center py-8">
          <div className="text-center">
            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary mx-auto mb-4"></div>
            <p className="text-muted-foreground">加载中...</p>
          </div>
        </div>
      )}
    </div>
  );
}
