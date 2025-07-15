// 工具函数，从全名生成头像路径
export const getAvatarPath = (fullName: string) => {
  if (!fullName) return "/driver_photo_avif/default.avif";
  const normalizedName = fullName
    .normalize("NFD")
    .replace(/[̀-ͯ]/g, "");
  const sanitizedName = normalizedName.replace(/ /g, "_");
  return `/driver_photo_avif/${sanitizedName}.avif`;
};

// 获取车队车辆图片路径
export const getConstructorCarPath = (constructorId: string) => {
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
  return `/2025_constructor_car_photo/${carMapping[constructorId] || "mercedes.png"}`;
};
