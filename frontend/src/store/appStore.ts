import { create } from 'zustand';

export interface ScenarioParams {
  tempAnomaly: number;       // Temperature anomaly: -1.0 to +4.5 °C
  rainfallAnomaly: number;   // Monsoon rainfall anomaly: -50% to +50%
  sectorFocus: 'agriculture' | 'water_security' | 'disaster_risk';
}

export interface SimulationResult {
  position: [number, number];
  temperatureDelta: number;
  aqiImprovement: number;
}

export interface OverallMetrics {
  cropYield: number;
  reservoirLevel: number;
  droughtIndex: string;
  tempMean: number;
}

interface AppState {
  interventionType: string;
  params: ScenarioParams;
  activeZone: string | null;
  simulationResults: SimulationResult[];
  overallMetrics: OverallMetrics;
  zones: any[];
  observations: any[];
  setInterventionType: (type: string) => void;
  setParams: (params: Partial<ScenarioParams>) => void;
  setActiveZone: (zone: string | null) => void;
  setSimulationResults: (results: SimulationResult[], metrics: OverallMetrics) => void;
  setZones: (zones: any[]) => void;
  setObservations: (observations: any[]) => void;
}

export const useAppStore = create<AppState>((set) => ({
  interventionType: 'agriculture',
  params: {
    tempAnomaly: 1.5,
    rainfallAnomaly: -10,
    sectorFocus: 'agriculture',
  },
  activeZone: null,
  simulationResults: [],
  overallMetrics: { cropYield: 0, reservoirLevel: 80, droughtIndex: 'Normal', tempMean: 32.5 },
  zones: [],
  observations: [],
  setInterventionType: (type) => set({ interventionType: type }),
  setParams: (newParams) => set((state) => ({ params: { ...state.params, ...newParams } })),
  setActiveZone: (zone) => set({ activeZone: zone }),
  setSimulationResults: (results, metrics) => set({ simulationResults: results, overallMetrics: metrics }),
  setZones: (zones) => set({ zones }),
  setObservations: (observations) => set({ observations }),
}));
