/**
 * 格式化工具函数集合
 * 统一管理前端数据格式化逻辑
 */

/**
 * 格式化车手姓名用于图片文件名
 * 移除重音符号并将空格替换为下划线
 * @param name 车手姓名
 * @returns 格式化后的文件名
 */
export const formatNameForImage = (name: string): string => {
  return name
    .normalize("NFD")
    .replace(/[\u0300-\u036f]/g, "")
    .replace(/ /g, "_");
};

/**
 * 格式化车手姓名用于头像查找
 * 规范化特殊字符并替换空格为下划线
 * @param driverName 车手姓名
 * @returns 格式化后的头像文件名
 */
export const formatAvatarName = (driverName: string): string => {
  // 规范化处理特殊字符 (如 ü -> u) 并替换空格为下划线
  const normalizedName = driverName
    .normalize("NFD")
    .replace(/[\u0300-\u036f]/g, "");
  return normalizedName.replace(/ /g, "_");
};

/**
 * 分割车手姓名用于显示格式化
 * @param driverName 车手姓名
 * @returns 包含firstName和lastName的对象，用于组件中的显示格式化
 */
export const formatDriverDisplayName = (driverName: string) => {
  const parts = driverName.split(" ");
  if (parts.length > 1) {
    const firstName = parts.slice(0, -1).join(" ");
    const lastName = parts[parts.length - 1];
    return { firstName, lastName };
  }
  return { firstName: "", lastName: driverName };
};

/**
 * 分割车手姓名为名字和姓氏
 * @param driverName 车手姓名
 * @returns 包含firstName和lastName的对象
 */
export const splitDriverName = (driverName: string) => {
  const [firstName, ...lastNameParts] = driverName.split(" ");
  const lastName = lastNameParts.join(" ");
  return { firstName, lastName };
};

/**
 * 映射车队ID到车手号码图片文件名中使用的车队名称
 * @param constructorId 车队ID
 * @returns 对应的文件名中的车队名称
 */
export const mapConstructorIdForDriverNumber = (constructorId: string): string => {
  const mapping: Record<string, string> = {
    "aston_martin": "astonmartin",
    "red_bull": "redbullracing", 
    "rb": "racingbulls",
    "sauber": "kicksauber",
    "ferrari": "ferrari",
    "mercedes": "mercedes",
    "mclaren": "mclaren",
    "alpine": "alpine",
    "haas": "haas",
    "williams": "williams"
  };
  
  return mapping[constructorId] || constructorId;
};

/**
 * 修复特定车手名称的拼写错误
 * @param driverName 车手姓名
 * @returns 修复后的车手姓名
 */
export const fixDriverNameForImage = (driverName: string): string => {
  const nameMapping: Record<string, string> = {
    "Charles Leclerc": "chales_leclerc", // 保持文件中的拼写错误 chales
    "Andrea Kimi Antonelli": "kimi_antonelli", // 文件中使用的简化名称
    "Franco Colapinto": "franco_colapinto",
    "Pierre Gasly": "pierre_gasly", 
    "Fernando Alonso": "fernando_alonso",
    "Lance Stroll": "lance_stroll",
    "Lewis Hamilton": "lewis_hamilton",
    "Esteban Ocon": "esteban_ocon",
    "Oliver Bearman": "oliver_bearman",
    "Gabriel Bortoleto": "gabriel_bortoleto", 
    "Nico Hulkenberg": "nico_hulkenberg",
    "Lando Norris": "lando_norris",
    "Oscar Piastri": "oscar_piastri",
    "George Russell": "george_russell",
    "Isack Hadjar": "isack_hadjar",
    "Liam Lawson": "liam_lawson", 
    "Max Verstappen": "max_verstappen",
    "Yuki Tsunoda": "yuki_tsunoda",
    "Alexander Albon": "alexander_albon",
    "Carlos Sainz": "carlos_sainz"
  };
  
  return nameMapping[driverName] || formatNameForImage(driverName).toLowerCase();
};

/**
 * 获取车手在号码图片文件中使用的实际号码
 * @param driverName 车手姓名
 * @param databaseNumber 数据库中的号码
 * @returns 图片文件中使用的号码
 */
export const getDriverNumberForImage = (driverName: string, databaseNumber: number): number => {
  // 根据实际的图片文件映射正确的号码
  const numberMapping: Record<string, number> = {
    "Max Verstappen": 1,    // 文件: max_verstappen_1.avif
    "Lando Norris": 4,      // 文件: lando_norris_4.avif
    "Gabriel Bortoleto": 5, // 文件: gabriel_bortoleto_5.avif
    "Isack Hadjar": 6,      // 文件: isack_hadjar_6.avif
    "Pierre Gasly": 10,     // 文件: pierre_gasly_10.avif
    "Andrea Kimi Antonelli": 12, // 文件: kimi_antonelli_12.avif
    "Fernando Alonso": 14,  // 文件: fernando_alonso_14.avif
    "Charles Leclerc": 16,  // 文件: chales_leclerc_16.avif
    "Lance Stroll": 18,     // 文件: lance_stroll_18.avif
    "Yuki Tsunoda": 22,     // 文件: yuki_tsunoda_22.avif
    "Alexander Albon": 23,  // 文件: alexander_albon_23.avif
    "Nico Hulkenberg": 27,  // 文件: nico_hulkenberg_27.avif
    "Liam Lawson": 30,      // 文件: liam_lawson_30.avif
    "Esteban Ocon": 31,     // 文件: esteban_ocon_31.avif
    "Franco Colapinto": 43, // 文件: franco_colapinto_43.avif
    "Lewis Hamilton": 44,   // 文件: lewis_hamilton_44.avif
    "Carlos Sainz": 55,     // 文件: carlos_sainz_55.avif
    "George Russell": 63,   // 文件: george_russell_63.avif
    "Oscar Piastri": 81,    // 文件: oscar_piastri_81.avif
    "Oliver Bearman": 87    // 文件: oliver_bearman_87.avif
  };
  
  return numberMapping[driverName] || databaseNumber;
}; 