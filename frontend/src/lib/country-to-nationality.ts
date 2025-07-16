// 将比赛的 country 字段映射到 nationality 格式
// 这样可以复用车手国旗的渲染逻辑（react-country-flag）
export const countryToNationality: Record<string, string> = {
  // 数据库中实际的 country 值映射到 nationality 格式
  USA: "American",
  "United States": "American",
  Monaco: "Monegasque",
  Spain: "Spanish",
  UK: "British",
  "United Kingdom": "British",
  Belgium: "Belgian",
  China: "Chinese",
  Japan: "Japanese",
  Australia: "Australian",
  Austria: "Austrian",
  Azerbaijan: "Azerbaijani", // 需要添加到 nationalityToFlagCode
  Bahrain: "Bahraini", // 需要添加
  Brazil: "Brazilian",
  Canada: "Canadian",
  France: "French",
  Germany: "German",
  Hungary: "Hungarian",
  Italy: "Italian",
  Mexico: "Mexican",
  Netherlands: "Dutch",
  Qatar: "Qatari", // 需要添加
  "Saudi Arabia": "Saudi", // 需要添加
  Singapore: "Singaporean", // 需要添加
  "United Arab Emirates": "Emirati", // 需要添加

  // 特殊地点映射（用于Testing等）
  Sakhir: "Bahraini", // Bahrain
  Imola: "Italian", // Italy
  "Las Vegas": "American", // USA
  Miami: "American", // USA
  Austin: "American", // USA
  Silverstone: "British", // UK
  Barcelona: "Spanish", // Spain
  "Spa-Francorchamps": "Belgian", // Belgium
  Suzuka: "Japanese", // Japan
  Shanghai: "Chinese", // China
};
