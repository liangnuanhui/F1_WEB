"use client";

import { useQuery } from "@tanstack/react-query";
import { circuitsApi } from "@/lib/api";
import { getCountryFlag } from "@/lib/utils";
import { MapPin, Flag, Navigation } from "lucide-react";
import { Circuit } from "@/types";

export default function CircuitsPage() {
  const {
    data: circuits,
    isLoading,
    error,
  } = useQuery({
    queryKey: ["circuits"],
    queryFn: () => circuitsApi.getAll(),
  });

  if (isLoading) {
    return (
      <div className="flex items-center justify-center py-8">
        <div className="text-center">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary mx-auto mb-4"></div>
          <p className="text-muted-foreground">加载赛道信息中...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="text-center py-8">
        <p className="text-red-500">加载赛道信息失败，请稍后重试</p>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center space-x-2">
        <MapPin className="h-6 w-6 text-primary" />
        <h1 className="text-3xl font-bold">赛道</h1>
      </div>

      {circuits?.data && circuits.data.length > 0 ? (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {circuits.data.map((circuit: Circuit) => (
            <div
              key={circuit.id}
              className="rounded-lg border bg-card p-6 hover:shadow-md transition-shadow"
            >
              <div className="flex items-start justify-between mb-4">
                <div className="space-y-2">
                  <h2 className="text-xl font-semibold">{circuit.name}</h2>
                  <p className="text-sm text-muted-foreground">
                    {circuit.location}
                  </p>
                </div>

                <div className="flex items-center space-x-1 text-lg">
                  <span>{getCountryFlag(circuit.country)}</span>
                </div>
              </div>

              <div className="space-y-2 text-sm text-muted-foreground">
                <div className="flex items-center space-x-2">
                  <Flag className="h-4 w-4" />
                  <span>{circuit.country}</span>
                </div>

                <div className="flex items-center space-x-2">
                  <Navigation className="h-4 w-4" />
                  <span>海拔: {circuit.altitude}m</span>
                </div>

                <div className="flex items-center space-x-2">
                  <MapPin className="h-4 w-4" />
                  <span>
                    {circuit.latitude.toFixed(4)},{" "}
                    {circuit.longitude.toFixed(4)}
                  </span>
                </div>
              </div>

              <div className="mt-4 pt-4 border-t">
                <p className="text-xs text-muted-foreground">
                  赛道代码: {circuit.circuit_ref}
                </p>
              </div>
            </div>
          ))}
        </div>
      ) : (
        <div className="text-center py-8">
          <p className="text-muted-foreground">暂无赛道数据</p>
        </div>
      )}
    </div>
  );
}
