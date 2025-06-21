"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import {
  Calendar,
  Users,
  Building2,
  MapPin,
  Trophy,
  Home,
  X,
} from "lucide-react";
import { cn } from "@/lib/utils";
import { useAppStore } from "@/store";

const navigation = [
  { name: "首页", href: "/", icon: Home },
  { name: "赛程", href: "/races", icon: Calendar },
  { name: "车手", href: "/drivers", icon: Users },
  { name: "车队", href: "/constructors", icon: Building2 },
  { name: "赛道", href: "/circuits", icon: MapPin },
  { name: "积分榜", href: "/standings", icon: Trophy },
];

export function Sidebar() {
  const pathname = usePathname();
  const { sidebarOpen, setSidebarOpen } = useAppStore();

  return (
    <>
      {/* 移动端遮罩 */}
      {sidebarOpen && (
        <div
          className="fixed inset-0 z-40 bg-background/80 backdrop-blur-sm md:hidden"
          onClick={() => setSidebarOpen(false)}
        />
      )}

      {/* 侧边栏 */}
      <div
        className={cn(
          "fixed left-0 top-14 z-50 h-[calc(100vh-3.5rem)] w-64 transform border-r bg-background transition-transform duration-200 ease-in-out md:translate-x-0",
          sidebarOpen ? "translate-x-0" : "-translate-x-full"
        )}
      >
        <div className="flex h-full flex-col">
          {/* 移动端关闭按钮 */}
          <div className="flex items-center justify-between p-4 md:hidden">
            <h2 className="text-lg font-semibold">导航菜单</h2>
            <button
              onClick={() => setSidebarOpen(false)}
              className="rounded-md p-1 hover:bg-accent"
            >
              <X className="h-5 w-5" />
            </button>
          </div>

          {/* 导航菜单 */}
          <nav className="flex-1 space-y-1 p-4">
            {navigation.map((item) => {
              const isActive = pathname === item.href;
              return (
                <Link
                  key={item.name}
                  href={item.href}
                  className={cn(
                    "flex items-center space-x-3 rounded-lg px-3 py-2 text-sm font-medium transition-colors",
                    isActive
                      ? "bg-primary text-primary-foreground"
                      : "text-muted-foreground hover:bg-accent hover:text-accent-foreground"
                  )}
                  onClick={() => setSidebarOpen(false)}
                >
                  <item.icon className="h-5 w-5" />
                  <span>{item.name}</span>
                </Link>
              );
            })}
          </nav>

          {/* 底部信息 */}
          <div className="border-t p-4">
            <div className="text-xs text-muted-foreground">
              <p>F1 赛事数据</p>
              <p>实时更新</p>
            </div>
          </div>
        </div>
      </div>
    </>
  );
}
