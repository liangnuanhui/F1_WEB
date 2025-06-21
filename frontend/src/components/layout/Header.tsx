"use client";

import { useState } from "react";
import Link from "next/link";
import { Menu, X, Sun, Moon, Monitor } from "lucide-react";
import { cn } from "@/lib/utils";
import { useAppStore } from "@/store";
import { useTheme } from "@/components/theme/ThemeProvider";

export function Header() {
  const { sidebarOpen, setSidebarOpen } = useAppStore();
  const { theme, setTheme } = useTheme();
  const [isThemeMenuOpen, setIsThemeMenuOpen] = useState(false);

  const toggleTheme = (newTheme: "light" | "dark" | "system") => {
    setTheme(newTheme);
    setIsThemeMenuOpen(false);
  };

  return (
    <header className="sticky top-0 z-50 w-full border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
      <div className="container flex h-14 items-center">
        {/* 移动端菜单按钮 */}
        <button
          className="mr-2 px-2 py-1 md:hidden"
          onClick={() => setSidebarOpen(!sidebarOpen)}
        >
          {sidebarOpen ? (
            <X className="h-5 w-5" />
          ) : (
            <Menu className="h-5 w-5" />
          )}
        </button>

        {/* Logo */}
        <Link href="/" className="flex items-center space-x-2">
          <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-red-600 text-white font-bold text-sm">
            F1
          </div>
          <span className="hidden font-bold sm:inline-block">F1 赛事数据</span>
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
            href="/constructors"
            className="text-sm font-medium transition-colors hover:text-primary"
          >
            车队
          </Link>
          <Link
            href="/circuits"
            className="text-sm font-medium transition-colors hover:text-primary"
          >
            赛道
          </Link>
          <Link
            href="/standings"
            className="text-sm font-medium transition-colors hover:text-primary"
          >
            积分榜
          </Link>
        </nav>

        {/* 右侧工具栏 */}
        <div className="ml-auto flex items-center space-x-2">
          {/* 主题切换 */}
          <div className="relative">
            <button
              className="flex h-9 w-9 items-center justify-center rounded-md border transition-colors hover:bg-accent hover:text-accent-foreground"
              onClick={() => setIsThemeMenuOpen(!isThemeMenuOpen)}
            >
              {theme === "light" && <Sun className="h-4 w-4" />}
              {theme === "dark" && <Moon className="h-4 w-4" />}
              {theme === "system" && <Monitor className="h-4 w-4" />}
            </button>

            {isThemeMenuOpen && (
              <div className="absolute right-0 top-full mt-1 w-32 rounded-md border bg-popover p-1 shadow-md">
                <button
                  className={cn(
                    "flex w-full items-center space-x-2 rounded-sm px-2 py-1.5 text-sm transition-colors hover:bg-accent",
                    theme === "light" && "bg-accent"
                  )}
                  onClick={() => toggleTheme("light")}
                >
                  <Sun className="h-4 w-4" />
                  <span>浅色</span>
                </button>
                <button
                  className={cn(
                    "flex w-full items-center space-x-2 rounded-sm px-2 py-1.5 text-sm transition-colors hover:bg-accent",
                    theme === "dark" && "bg-accent"
                  )}
                  onClick={() => toggleTheme("dark")}
                >
                  <Moon className="h-4 w-4" />
                  <span>深色</span>
                </button>
                <button
                  className={cn(
                    "flex w-full items-center space-x-2 rounded-sm px-2 py-1.5 text-sm transition-colors hover:bg-accent",
                    theme === "system" && "bg-accent"
                  )}
                  onClick={() => toggleTheme("system")}
                >
                  <Monitor className="h-4 w-4" />
                  <span>系统</span>
                </button>
              </div>
            )}
          </div>
        </div>
      </div>
    </header>
  );
}
