"use client";

import { useState, Suspense } from "react";
import { useSearchParams } from "next/navigation";
import { DriverStandings } from "./DriverStandings";
import { ConstructorStandings } from "./ConstructorStandings";

type StandingType = "drivers" | "teams";

function StandingsContent() {
  const searchParams = useSearchParams();
  const tabParam = searchParams.get("tab") as StandingType;

  // 根据URL参数设置初始状态，如果参数是有效的，使用参数值，否则默认为"drivers"
  const [activeTab, setActiveTab] = useState<StandingType>(
    tabParam === "drivers" || tabParam === "teams" ? tabParam : "drivers"
  );

  const renderContent = () => {
    switch (activeTab) {
      case "drivers":
        return <DriverStandings />;
      case "teams":
        return <ConstructorStandings />;
      default:
        return null;
    }
  };

  const getButtonClass = (tabName: StandingType) => {
    return `px-4 py-2 text-sm font-semibold rounded-md transition-colors ${
      activeTab === tabName
        ? "bg-zinc-800 text-white"
        : "bg-transparent text-zinc-600 hover:bg-zinc-200"
    }`;
  };

  return (
    <div className="container mx-auto px-4 py-8 bg-[#F7F4F1]">
      <div className="flex items-center mb-6">
        <h1 className="text-3xl font-extrabold tracking-wider mr-6">
          2025 STANDINGS
        </h1>
        <div className="flex items-center p-1 bg-zinc-100 rounded-lg">
          <button
            onClick={() => setActiveTab("drivers")}
            className={getButtonClass("drivers")}
          >
            Drivers
          </button>
          <button
            onClick={() => setActiveTab("teams")}
            className={getButtonClass("teams")}
          >
            Teams
          </button>
        </div>
      </div>
      <div>{renderContent()}</div>
    </div>
  );
}

export default function StandingsPage() {
  return (
    <Suspense fallback={
      <div className="min-h-screen bg-gradient-to-br from-red-50 via-white to-red-50 p-4">
        <div className="max-w-7xl mx-auto">
          <div className="text-center py-8">
            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-red-600 mx-auto"></div>
            <p className="mt-2 text-gray-600">Loading standings...</p>
          </div>
        </div>
      </div>
    }>
      <StandingsContent />
    </Suspense>
  );
}
