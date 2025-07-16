import Image from "next/image";
import { getTeamColor } from "@/lib/team-colors";
import { CountryFlag } from "@/components/CountryFlag";
import {
  formatNameForImage,
  splitDriverName,
  mapConstructorIdForDriverNumber,
  fixDriverNameForImage,
  getDriverNumberForImage,
} from "@/lib/formatters";
import { MergedDriver } from "@/types";

interface DriverCardProps {
  driver: MergedDriver;
  priority?: boolean;
}

export const DriverCard = ({ driver, priority = false }: DriverCardProps) => {
  const teamColor = getTeamColor(driver.constructor_id || "");
  const cardStyle = {
    background: `linear-gradient(135deg, ${teamColor} 40%, rgba(0,0,0,0.7) 100%)`,
    color: "#fff",
  };

  const driverPhoto = formatNameForImage(driver.driver_name);

  // 使用正确的车队名称映射和车手名称修复
  const mappedConstructorId = mapConstructorIdForDriverNumber(
    driver.constructor_id || ""
  );
  const fixedDriverName = fixDriverNameForImage(driver.driver_name);

  // 使用正确的号码映射
  const correctNumber = getDriverNumberForImage(
    driver.driver_name,
    driver.number || 0
  );

  const driverNumberPath = `/driver_number/2025_${mappedConstructorId}_${fixedDriverName}_${correctNumber}.avif`;

  const { firstName, lastName } = splitDriverName(driver.driver_name);

  // 检查是否有有效的维基百科链接
  const hasValidUrl = driver.driver_url && driver.driver_url.trim() !== "";

  // 处理卡片点击事件
  const handleCardClick = () => {
    if (hasValidUrl) {
      window.open(driver.driver_url, "_blank");
    }
  };

  return (
    <div
      className={`group relative flex h-52 w-full flex-col overflow-hidden rounded-xl p-5 shadow-lg transition-transform hover:scale-110 ${
        hasValidUrl ? "cursor-pointer" : ""
      }`}
      style={cardStyle}
      onClick={handleCardClick}
      aria-label={
        hasValidUrl ? `查看 ${driver.driver_name} 的维基百科页面` : undefined
      }
      role={hasValidUrl ? "button" : undefined}
    >
      <div className="relative z-10 flex h-full flex-col justify-between">
        <div>
          <div className="relative inline-block">
            <div>
              <h2 className="text-2xl font-light leading-tight">{firstName}</h2>
              <h2 className="text-2xl font-extrabold leading-tight">
                {lastName.toUpperCase()}
              </h2>
            </div>
            {/* 自定义下划线 */}
            <span className="absolute bottom-0 left-0 h-px w-0 transition-all duration-300 group-hover:w-full bg-white" />
          </div>
          <p className="mt-1 text-sm font-light text-white/80">
            {driver.constructor_name}
          </p>
          {driver.nationality && (
            <div className="flex items-center justify-start mt-2">
              <CountryFlag nationality={driver.nationality} size="2em" />
            </div>
          )}
        </div>
        <div className="flex flex-col items-end justify-end"></div>
      </div>
      <div className="absolute -bottom-8 -right-4 h-60 w-60 z-20">
        <Image
          src={`/driver_photo_avif/${driverPhoto}.avif`}
          alt={driver.driver_name}
          fill
          sizes="(max-width: 768px) 50vw, (max-width: 1200px) 25vw, 240px"
          priority={priority}
          style={{ objectFit: "cover", objectPosition: "center top" }}
          className="transition-transform duration-300 group-hover:scale-105"
        />
      </div>
      {driver.number && (
        <div className="absolute -bottom-4 right-32 h-40 w-40 z-10 flex items-center justify-center">
          <Image
            src={driverNumberPath}
            alt={`${driver.driver_name} number`}
            width={120}
            height={120}
            sizes="(max-width: 768px) 25vw, (max-width: 1200px) 15vw, 120px"
            style={{
              objectFit: "contain",
              opacity: 0.3,
              filter: "brightness(1.5) contrast(0.8)",
              maxWidth: "120px",
              maxHeight: "120px",
            }}
            className="transition-transform duration-300 group-hover:scale-105"
          />
        </div>
      )}
    </div>
  );
};
