// src/lib/path-helpers.ts

/**
 * 从车手全名生成头像文件的路径
 * @param fullName - 车手全名 (e.g., "Max Verstappen")
 * @returns 头像文件的相对路径
 */
export const getAvatarPath = (fullName: string): string => {
  if (!fullName) return "/driver_photo_avif/default.avif";
  // 规范化名称，移除音标并替换空格
  const normalizedName = fullName
    .normalize("NFD")
    .replace(/[\u0300-\u036f]/g, "");
  const sanitizedName = normalizedName.replace(/ /g, "_");
  return `/driver_photo_avif/${sanitizedName}.avif`;
};

/**
 * 根据车队ID获取车辆图片的路径
 * @param constructorId - 车队ID (e.g., "red_bull")
 * @returns 车辆图片的相对路径
 */
export const getConstructorCarPath = (constructorId: string): string => {
  const carMapping: Record<string, string> = {
    mercedes: "mercedes.png",
    ferrari: "ferrari.png",
    red_bull: "red_bull.png",
    mclaren: "mclaren.png",
    aston_martin: "aston_martin.png",
    alpine: "alpine.png",
    williams: "williams.png",
    haas: "haas.png",
    rb: "rb.png",
    sauber: "sauber.png",
  };
  // 提供一个默认图片以防找不到匹配项
  return `/2025_constructor_car_photo/${carMapping[constructorId] || "mercedes.png"}`;
};
