import { create } from "zustand";
import { devtools } from "zustand/middleware";
import { Season, Circuit, Race, Driver, Constructor } from "@/types";

// 应用状态接口
interface AppState {
  // 当前选中的赛季
  currentSeason: Season | null;
  // 当前选中的赛道
  selectedCircuit: Circuit | null;
  // 当前选中的比赛
  selectedRace: Race | null;
  // 当前选中的车手
  selectedDriver: Driver | null;
  // 当前选中的车队
  selectedConstructor: Constructor | null;
  // 侧边栏是否打开
  sidebarOpen: boolean;
  // 主题模式
  theme: "light" | "dark" | "system";
  // 加载状态
  loading: boolean;
  // 错误信息
  error: string | null;
}

// 应用动作接口
interface AppActions {
  // 设置当前赛季
  setCurrentSeason: (season: Season | null) => void;
  // 设置选中的赛道
  setSelectedCircuit: (circuit: Circuit | null) => void;
  // 设置选中的比赛
  setSelectedRace: (race: Race | null) => void;
  // 设置选中的车手
  setSelectedDriver: (driver: Driver | null) => void;
  // 设置选中的车队
  setSelectedConstructor: (constructor: Constructor | null) => void;
  // 切换侧边栏
  toggleSidebar: () => void;
  // 设置侧边栏状态
  setSidebarOpen: (open: boolean) => void;
  // 设置主题
  setTheme: (theme: "light" | "dark" | "system") => void;
  // 设置加载状态
  setLoading: (loading: boolean) => void;
  // 设置错误信息
  setError: (error: string | null) => void;
  // 清除错误
  clearError: () => void;
  // 重置所有状态
  reset: () => void;
}

// 应用 Store 类型
type AppStore = AppState & AppActions;

// 初始状态
const initialState: AppState = {
  currentSeason: null,
  selectedCircuit: null,
  selectedRace: null,
  selectedDriver: null,
  selectedConstructor: null,
  sidebarOpen: false,
  theme: "system",
  loading: false,
  error: null,
};

// 创建应用 Store
export const useAppStore = create<AppStore>()(
  devtools(
    (set, get) => ({
      ...initialState,

      setCurrentSeason: (season) => set({ currentSeason: season }),

      setSelectedCircuit: (circuit) => set({ selectedCircuit: circuit }),

      setSelectedRace: (race) => set({ selectedRace: race }),

      setSelectedDriver: (driver) => set({ selectedDriver: driver }),

      setSelectedConstructor: (constructor) =>
        set({ selectedConstructor: constructor }),

      toggleSidebar: () =>
        set((state) => ({ sidebarOpen: !state.sidebarOpen })),

      setSidebarOpen: (open) => set({ sidebarOpen: open }),

      setTheme: (theme) => {
        set({ theme });
        // 保存到 localStorage
        if (typeof window !== "undefined") {
          localStorage.setItem("theme", theme);
        }
      },

      setLoading: (loading) => set({ loading }),

      setError: (error) => set({ error }),

      clearError: () => set({ error: null }),

      reset: () => set(initialState),
    }),
    {
      name: "f1-app-store",
    }
  )
);

// 从 localStorage 恢复主题设置
if (typeof window !== "undefined") {
  const savedTheme = localStorage.getItem("theme") as
    | "light"
    | "dark"
    | "system";
  if (savedTheme) {
    useAppStore.getState().setTheme(savedTheme);
  }
}
