import Image from "next/image";
import { ChevronRight } from "lucide-react";
import { getTeamColor } from "@/lib/team-colors";
import { teamLogoMap } from "@/lib/team-logo-map";
import { availableAvatarSet } from "@/lib/available-avatars";
import { formatAvatarName, formatDriverDisplayName } from "@/lib/formatters";
import { ConstructorStanding, MergedDriver } from "@/types";

interface TeamCardProps {
  constructor: ConstructorStanding;
  drivers: MergedDriver[];
  priority?: boolean;
}

export const TeamCard = ({
  constructor,
  drivers,
  priority = false,
}: TeamCardProps) => {
  const color = getTeamColor(constructor.constructor_id);
  const logoFilename = teamLogoMap[constructor.constructor_id] || null;
  const logoUrl = logoFilename ? `/team_logos/${logoFilename}.svg` : null;

  const cardStyle = {
    background: `linear-gradient(135deg, ${color} 40%, rgba(0,0,0,0.5) 100%)`,
    color: "#fff",
  };

  const handleCardClick = () => {
    if (constructor.constructor_url) {
      window.open(constructor.constructor_url, "_blank");
    }
  };

  return (
    <div
      className="group relative flex cursor-pointer flex-col overflow-hidden rounded-2xl transition-transform duration-300 hover:scale-105"
      style={cardStyle}
      onClick={handleCardClick}
    >
      <div className="relative z-10 p-6">
        <div className="flex items-start justify-between">
          <div>
            <div className="relative inline-block group mb-2">
              <h2 className="text-3xl font-bold">
                {constructor.constructor_name}
              </h2>
              {/* 自定义下划线 */}
              <span className="absolute bottom-0 left-0 h-px w-0 transition-all duration-300 group-hover:w-full bg-white" />
            </div>
            <div className="flex space-x-4">
              {drivers.map((driver) => {
                const avatarName = formatAvatarName(driver.driver_name);
                const hasAvatar = availableAvatarSet.has(avatarName);
                const avatarUrl = hasAvatar
                  ? `/driver_avatar/${avatarName}.png`
                  : `/driver_avatar/default.svg`;

                // 检查是否有有效的维基百科链接
                const hasValidUrl =
                  driver.driver_url && driver.driver_url.trim() !== "";

                const handleDriverClick = (e: React.MouseEvent) => {
                  e.stopPropagation(); // 阻止事件冒泡到父元素
                  if (hasValidUrl) {
                    window.open(driver.driver_url, "_blank");
                  }
                };

                return (
                  <div
                    key={driver.driver_id}
                    className={`flex items-center space-x-2 group transition-transform duration-300 hover:scale-110 ${
                      hasValidUrl ? "cursor-pointer" : ""
                    }`}
                    onClick={handleDriverClick}
                  >
                    <div
                      className="rounded-full w-8 h-8 flex-shrink-0"
                      style={{ backgroundColor: color }}
                    >
                      <Image
                        src={avatarUrl}
                        alt={driver.driver_name}
                        width={32}
                        height={32}
                        className="rounded-full"
                      />
                    </div>
                    {hasValidUrl ? (
                      <button
                        className="text-sm tracking-wide cursor-pointer text-left"
                        aria-label={`查看 ${driver.driver_name} 的维基百科页面`}
                      >
                        {(() => {
                          const { firstName, lastName } = formatDriverDisplayName(driver.driver_name);
                          return firstName ? (
                            <>
                              {firstName} <span className="font-bold">{lastName.toUpperCase()}</span>
                            </>
                          ) : (
                            <span className="font-bold">{lastName.toUpperCase()}</span>
                          );
                        })()}
                      </button>
                    ) : (
                      <p className="text-sm tracking-wide">
                        {(() => {
                          const { firstName, lastName } = formatDriverDisplayName(driver.driver_name);
                          return firstName ? (
                            <>
                              {firstName} <span className="font-bold">{lastName.toUpperCase()}</span>
                            </>
                          ) : (
                            <span className="font-bold">{lastName.toUpperCase()}</span>
                          );
                        })()}
                      </p>
                    )}
                  </div>
                );
              })}
            </div>
          </div>
          {logoUrl && (
            <div className="bg-white/20 rounded-full p-2">
              <Image
                src={logoUrl}
                alt={`${constructor.constructor_name} logo`}
                width={24}
                height={24}
                className="opacity-80"
              />
            </div>
          )}
        </div>
      </div>

      <div className="relative mt-4 px-6 pb-4">
        <Image
          src={`/2025_constructor_car_photo/${constructor.constructor_id}.png`}
          alt={`${constructor.constructor_name} car`}
          width={450}
          height={225}
          className="w-full h-auto transform-gpu opacity-90"
          priority={priority}
        />
      </div>

      <div className="absolute right-4 top-1/2 -translate-y-1/2 cursor-pointer rounded-full bg-black/30 p-2 opacity-0 transition-opacity group-hover:opacity-100">
        <ChevronRight className="h-6 w-6" />
      </div>

      <div className="absolute inset-0 bg-black/10 opacity-50 group-hover:opacity-0 transition-opacity duration-300"></div>
    </div>
  );
};
