"use client";

import { useQuery } from "@tanstack/react-query";
import { driversApi } from "@/lib/api";
import { Users, Flag, Calendar } from "lucide-react";
import { Driver } from "@/types";

export default function DriversPage() {
  const {
    data: drivers,
    isLoading,
    error,
  } = useQuery({
    queryKey: ["drivers"],
    queryFn: () => driversApi.getAll({ size: 30 }),
  });

  if (isLoading) {
    return (
      <div className="flex items-center justify-center py-8">
        <div className="text-center">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary mx-auto mb-4"></div>
          <p className="text-muted-foreground">加载车手信息中...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="text-center py-8">
        <p className="text-red-500">加载车手信息失败，请稍后重试</p>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center space-x-2">
        <Users className="h-6 w-6 text-primary" />
        <h1 className="text-3xl font-bold">车手简介</h1>
      </div>

      {drivers?.data && drivers.data.length > 0 ? (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {drivers.data.map((driver: Driver) => (
            <div
              key={driver.driver_id}
              className="rounded-lg border bg-card p-6 hover:shadow-md transition-shadow"
            >
              <div className="flex items-start justify-between mb-4">
                <div className="space-y-2">
                  <h2 className="text-xl font-semibold">
                    {driver.forename} {driver.surname}
                  </h2>
                  {driver.number && (
                    <div className="flex items-center space-x-2">
                      <span className="text-2xl font-bold text-primary">
                        #{driver.number}
                      </span>
                      {driver.code && (
                        <span className="text-sm text-muted-foreground">
                          {driver.code}
                        </span>
                      )}
                    </div>
                  )}
                </div>

                <div className="flex items-center space-x-1 text-lg">
                  <span>{driver.nationality}</span>
                </div>
              </div>

              <div className="space-y-2 text-sm text-muted-foreground">
                <div className="flex items-center space-x-2">
                  <Flag className="h-4 w-4" />
                  <span>{driver.nationality}</span>
                </div>

                {driver.date_of_birth && (
                  <div className="flex items-center space-x-2">
                    <Calendar className="h-4 w-4" />
                    <span>{new Date(driver.date_of_birth).getFullYear()}</span>
                  </div>
                )}
              </div>
            </div>
          ))}
        </div>
      ) : (
        <div className="text-center py-8">
          <p className="text-muted-foreground">暂无车手数据</p>
        </div>
      )}
    </div>
  );
}
