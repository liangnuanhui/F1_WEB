"use client";

import { useQuery } from "@tanstack/react-query";
import { constructorsApi } from "@/lib/api";
import { formatConstructorName, getCountryFlag } from "@/lib/utils";
import { Building2, Flag, Globe } from "lucide-react";
import { Constructor } from "@/types";

export default function ConstructorsPage() {
  const {
    data: constructors,
    isLoading,
    error,
  } = useQuery({
    queryKey: ["constructors"],
    queryFn: () => constructorsApi.getAll(),
  });

  if (isLoading) {
    return (
      <div className="flex items-center justify-center py-8">
        <div className="text-center">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary mx-auto mb-4"></div>
          <p className="text-muted-foreground">加载车队信息中...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="text-center py-8">
        <p className="text-red-500">加载车队信息失败，请稍后重试</p>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center space-x-2">
        <Building2 className="h-6 w-6 text-primary" />
        <h1 className="text-3xl font-bold">车队</h1>
      </div>

      {constructors?.data && constructors.data.length > 0 ? (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {constructors.data.map((constructor: Constructor) => (
            <div
              key={constructor.id}
              className="rounded-lg border bg-card p-6 hover:shadow-md transition-shadow"
            >
              <div className="flex items-start justify-between mb-4">
                <div className="space-y-2">
                  <h2 className="text-xl font-semibold">
                    {formatConstructorName(constructor.name)}
                  </h2>
                  <p className="text-sm text-muted-foreground">
                    {constructor.name}
                  </p>
                </div>

                <div className="flex items-center space-x-1 text-lg">
                  <span>{getCountryFlag(constructor.nationality)}</span>
                </div>
              </div>

              <div className="space-y-2 text-sm text-muted-foreground">
                <div className="flex items-center space-x-2">
                  <Flag className="h-4 w-4" />
                  <span>{constructor.nationality}</span>
                </div>

                <div className="flex items-center space-x-2">
                  <Globe className="h-4 w-4" />
                  <span>车队代码: {constructor.constructor_ref}</span>
                </div>
              </div>

              <div className="mt-4 pt-4 border-t">
                <a
                  href={constructor.url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-xs text-primary hover:underline"
                >
                  访问官网 →
                </a>
              </div>
            </div>
          ))}
        </div>
      ) : (
        <div className="text-center py-8">
          <p className="text-muted-foreground">暂无车队数据</p>
        </div>
      )}
    </div>
  );
}
