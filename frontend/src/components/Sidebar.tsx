import React from 'react';
import { useAppStore } from '../store/appStore';
import { Settings, Thermometer, CloudRain, Activity } from 'lucide-react';
import { runScenario, simulationWs } from '../services/api';

const Sidebar: React.FC = () => {
  const { params, setParams, interventionType, setSimulationResults } = useAppStore();

  const handleRunSimulation = async () => {
    try {
      // Setup WS listener for simulation updates
      simulationWs.onMessage((data) => {
        if (data.type === 'simulation_update' || data.type === 'simulation_complete') {
           setSimulationResults(data.results, data.metrics);
        }
      });

      // Ensure WS is connected before triggering API
      if (!simulationWs.isConnected()) {
        simulationWs.connect();
      }

      // Trigger the backend API
      await runScenario({
        interventionType,
        parameters: params,
      });

    } catch (error) {
      console.error("Failed to run scenario", error);
    }
  };

  return (
    <div className="absolute top-24 left-6 w-80 backdrop-blur-2xl bg-slate-900/60 border border-slate-700/50 rounded-2xl shadow-[0_8px_30px_rgb(0,0,0,0.4)] p-6 flex flex-col gap-6 z-10 glass-panel">
      <div className="flex items-center gap-3 border-b border-slate-700/50 pb-4">
        <Settings className="w-6 h-6 text-emerald-400" />
        <h2 className="text-xl font-bold text-slate-100 tracking-wide">Climate Twin</h2>
      </div>

      <div className="flex flex-col gap-5">
        <div className="flex flex-col gap-2">
          <label className="text-xs font-semibold text-slate-400 uppercase tracking-wider flex items-center gap-2">
            <Activity className="w-4 h-4 text-blue-400" /> Sector Focus
          </label>
          <select 
            value={params.sectorFocus}
            onChange={(e) => setParams({ sectorFocus: e.target.value as any })}
            className="bg-slate-800/80 border border-slate-600 rounded-lg p-3 text-slate-200 outline-none focus:ring-2 focus:ring-emerald-500/50 transition-all font-medium"
          >
            <option value="agriculture">Agriculture & Crop Health</option>
            <option value="water_security">Water Security & Reservoirs</option>
            <option value="disaster_risk">Disaster Risk & Wet-Bulb</option>
          </select>
        </div>

        <div className="flex flex-col gap-3 group">
          <label className="text-xs font-semibold text-slate-400 uppercase tracking-wider flex justify-between items-center">
            <span className="flex items-center gap-2"><Thermometer className="w-4 h-4 text-orange-400" /> Temp Anomaly</span>
            <span className="text-orange-400 font-mono bg-orange-400/10 px-2 py-0.5 rounded">
              {params.tempAnomaly > 0 ? `+${params.tempAnomaly}` : params.tempAnomaly}°C
            </span>
          </label>
          <input 
            type="range" 
            min="-1.0" max="4.5" step="0.1"
            value={params.tempAnomaly}
            onChange={(e) => setParams({ tempAnomaly: parseFloat(e.target.value) })}
            className="w-full h-2 bg-slate-700 rounded-lg appearance-none cursor-pointer accent-orange-500"
          />
        </div>

        <div className="flex flex-col gap-3 group">
          <label className="text-xs font-semibold text-slate-400 uppercase tracking-wider flex justify-between items-center">
            <span className="flex items-center gap-2"><CloudRain className="w-4 h-4 text-cyan-400" /> Monsoon Deviation</span>
            <span className="text-cyan-400 font-mono bg-cyan-400/10 px-2 py-0.5 rounded">
              {params.rainfallAnomaly > 0 ? `+${params.rainfallAnomaly}` : params.rainfallAnomaly}%
            </span>
          </label>
          <input 
            type="range" 
            min="-50" max="50" step="5"
            value={params.rainfallAnomaly}
            onChange={(e) => setParams({ rainfallAnomaly: parseInt(e.target.value) })}
            className="w-full h-2 bg-slate-700 rounded-lg appearance-none cursor-pointer accent-cyan-500"
          />
        </div>
      </div>

      <button 
        onClick={handleRunSimulation}
        className="mt-2 w-full bg-gradient-to-r from-emerald-500 to-teal-600 hover:from-emerald-400 hover:to-teal-500 text-white font-bold py-3 px-4 rounded-xl shadow-lg shadow-emerald-500/20 transform transition-all active:scale-95 flex justify-center items-center gap-2"
      >
        <Activity className="w-5 h-5" /> Run Simulation
      </button>
    </div>
  );
};

export default Sidebar;
