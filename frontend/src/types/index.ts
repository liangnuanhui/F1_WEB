// F1 项目类型定义

// 基础响应类型
export interface ApiResponse<T> {
  data: T;
  message?: string;
  success: boolean;
}

// 分页响应类型
export interface PaginatedResponse<T> {
  data: T[];
  total: number;
  page: number;
  size: number;
  pages: number;
}

// 赛季类型
export interface Season {
  id: number;
  year: number;
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

// 赛道类型
export interface Circuit {
  id: number;
  name: string;
  location: string;
  country: string;
  latitude: number;
  longitude: number;
  altitude: number;
  url: string;
  circuit_ref: string;
  created_at: string;
  updated_at: string;
}

// 比赛类型
export interface Race {
  id: number;
  season_id: number;
  circuit_id: number;
  name: string;
  date: string;
  time: string;
  url: string;
  round: number;
  fp1_date?: string;
  fp1_time?: string;
  fp2_date?: string;
  fp2_time?: string;
  fp3_date?: string;
  fp3_time?: string;
  quali_date?: string;
  quali_time?: string;
  sprint_date?: string;
  sprint_time?: string;
  created_at: string;
  updated_at: string;
  season?: Season;
  circuit?: Circuit;
}

// 车手类型
export interface Driver {
  id: number;
  driver_ref: string;
  number?: number;
  code?: string;
  forename: string;
  surname: string;
  date_of_birth?: string;
  nationality: string;
  url: string;
  created_at: string;
  updated_at: string;
}

// 车队类型
export interface Constructor {
  id: number;
  constructor_ref: string;
  name: string;
  nationality: string;
  url: string;
  created_at: string;
  updated_at: string;
}

// 比赛结果类型
export interface Result {
  id: number;
  race_id: number;
  driver_id: number;
  constructor_id: number;
  number?: number;
  grid: number;
  position?: number;
  position_text: string;
  position_order: number;
  points: number;
  laps: number;
  time?: string;
  milliseconds?: number;
  fastest_lap?: number;
  rank?: number;
  fastest_lap_time?: string;
  fastest_lap_speed?: number;
  status_id: number;
  created_at: string;
  updated_at: string;
  race?: Race;
  driver?: Driver;
  constructor?: Constructor;
}

// 排位赛结果类型
export interface QualifyingResult {
  id: number;
  race_id: number;
  driver_id: number;
  constructor_id: number;
  number: number;
  position: number;
  q1?: string;
  q2?: string;
  q3?: string;
  created_at: string;
  updated_at: string;
  race?: Race;
  driver?: Driver;
  constructor?: Constructor;
}

// 冲刺赛结果类型
export interface SprintResult {
  id: number;
  race_id: number;
  driver_id: number;
  constructor_id: number;
  number: number;
  grid: number;
  position?: number;
  position_text: string;
  position_order: number;
  points: number;
  laps: number;
  time?: string;
  milliseconds?: number;
  fastest_lap?: number;
  fastest_lap_time?: string;
  status_id: number;
  created_at: string;
  updated_at: string;
  race?: Race;
  driver?: Driver;
  constructor?: Constructor;
}

// 积分榜类型
export interface Standings {
  id: number;
  season_id: number;
  driver_id?: number;
  constructor_id?: number;
  position: number;
  points: number;
  wins: number;
  created_at: string;
  updated_at: string;
  season?: Season;
  driver?: Driver;
  constructor?: Constructor;
}

// 导航菜单类型
export interface NavItem {
  label: string;
  href: string;
  icon?: string;
  children?: NavItem[];
}

// 图表数据类型
export interface ChartData {
  name: string;
  value: number;
  [key: string]: any;
}

// 筛选器类型
export interface FilterOptions {
  season?: number;
  circuit?: number;
  driver?: number;
  constructor?: number;
  [key: string]: any;
}

// 排序类型
export interface SortOptions {
  field: string;
  direction: "asc" | "desc";
}
