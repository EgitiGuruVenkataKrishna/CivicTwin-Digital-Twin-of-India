import { create } from 'zustand';

export interface ScenarioParams {
  greenSpaceAdded: number;
  albedoChange: number;
  trafficReduction: number;
}

export interface SimulationResult {
  position: [number, number];
  temperatureDelta: number;
  aqiImprovement: number;
}

interface AppState {
  interventionType: string;
  params: ScenarioParams;
  activeZone: string | null;
  simulationResults: SimulationResult[];
  overallMetrics: { tempDrop: number; aqiImp: number };
  setInterventionType: (type: string) => void;
  setParams: (params: Partial<ScenarioParams>) => void;
  setActiveZone: (zone: string | null) => void;
  setSimulationResults: (results: SimulationResult[], metrics: { tempDrop: number; aqiImp: number }) => void;
}

export const useAppStore = create<AppState>((set) => ({
  interventionType: 'green_roofs',
  params: {
    greenSpaceAdded: 10,
    albedoChange: 0.1,
    trafficReduction: 5,
  },
  activeZone: null,
  simulationResults: [],
  overallMetrics: { tempDrop: 0, aqiImp: 0 },
  setInterventionType: (type) => set({ interventionType: type }),
  setParams: (newParams) => set((state) => ({ params: { ...state.params, ...newParams } })),
  setActiveZone: (zone) => set({ activeZone: zone }),
  setSimulationResults: (results, metrics) => set({ simulationResults: results, overallMetrics: metrics }),
}));
