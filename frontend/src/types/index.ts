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

// 赛季类型 - 基于实际数据库模型
export interface Season {
  id: number;
  year: number;
  name: string;
  description?: string;
  start_date?: string;
  end_date?: string;
  is_active: boolean;
}

// 赛道类型 - 基于实际数据库模型
export interface Circuit {
  circuit_id: string;
  circuit_url?: string;
  circuit_name: string;
  lat?: number;
  long?: number;
  locality?: string;
  country?: string;
  length?: number;
  corners?: number;
  lap_record?: string;
  lap_record_driver?: string;
  lap_record_year?: number;
  description?: string;
  characteristics?: string;
  is_active: boolean;
  id: string;
  name: string;
}

// 比赛类型 - 基于实际数据库模型
export interface Race {
  id: number;
  season_id: number;
  circuit_id: string;
  round_number: number;
  country?: string;
  location?: string;
  official_event_name: string;
  event_date?: string;
  event_format?: string;
  is_sprint: boolean;
  session1?: string;
  session1_date?: string;
  session2?: string;
  session2_date?: string;
  session3?: string;
  session3_date?: string;
  session4?: string;
  session4_date?: string;
  session5?: string;
  session5_date?: string;
  season?: Season;
  circuit?: Circuit;
}

// 车手类型 - 与数据库一致
export interface Driver {
  driver_id: string;
  number?: number;
  code?: string;
  driver_url?: string;
  forename: string;
  surname: string;
  date_of_birth?: string;
  nationality?: string;
  id: string;
  driver_number: number;
  dob: string;
  url: string;
}

// 车队类型 - 与数据库一致
export interface Constructor {
  constructor_id: string;
  constructor_url?: string;
  name: string;
  nationality?: string;
  season_id: number;
  base?: string;
  team_chief?: string;
  technical_chief?: string;
  power_unit?: string;
  is_active?: boolean;
  championships: number;
  wins: number;
  podiums: number;
  poles: number;
  fastest_laps: number;
  id: string;
  url: string;
}

// 比赛结果类型 - 基于实际数据库模型
export interface Result {
  id: number;
  race_id: number;
  driver_id: string;
  constructor_id: string;
  driver_number?: number;
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
  race?: Race;
  driver?: Driver;
  constructor?: Constructor;
}

// 排位赛结果类型 - 基于实际数据库模型
export interface QualifyingResult {
  id: number;
  race_id: number;
  driver_id: string;
  constructor_id: string;
  driver_number: number;
  position: number;
  q1?: string;
  q2?: string;
  q3?: string;
  race?: Race;
  driver?: Driver;
  constructor?: Constructor;
}

// 冲刺赛结果类型 - 基于实际数据库模型
export interface SprintResult {
  id: number;
  race_id: number;
  driver_id: string;
  constructor_id: string;
  driver_number: number;
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
  race?: Race;
  driver?: Driver;
  constructor?: Constructor;
}

// 车手积分榜类型 - 与后端 schema/database 一致
export interface DriverStanding {
  position: number;
  points: number;
  wins: number;
  driver_id: string;
  driver_name: string;
  nationality: string | null;
  constructor_id: string | null;
  constructor_name: string | null;
}

// 车队积分榜类型 - 与后端 schema/database 一致
export interface ConstructorStanding {
  position: number;
  points: number;
  wins: number;
  constructor_id: string;
  constructor_name: string;
  nationality: string | null;
}

// 积分榜历史类型 - 与后端 schema/database 一致
export interface StandingHistory {
  id: number;
  season_id: number;
  position?: number;
  points: number;
  wins: number;
  driver_id: string;
  constructor_id: string;
  driver_name: string;
  driver_code: string;
  constructor_name: string;
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
  circuit?: string;
  driver?: string;
  constructor?: string;
  [key: string]: any;
}

// 排序选项类型
export interface SortOptions {
  field: string;
  direction: "asc" | "desc";
}
