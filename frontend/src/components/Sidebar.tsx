import React from 'react';
import { useAppStore } from '../store/appStore';
import { Settings, Leaf, Sun, Car, Activity } from 'lucide-react';
import { runScenario, simulationWs } from '../services/api';

const Sidebar: React.FC = () => {
  const { params, setParams, interventionType, setInterventionType, setSimulationResults } = useAppStore();

  const handleRunSimulation = async () => {
    try {
      // Setup WS listener for simulation updates
      simulationWs.onMessage((data) => {
        if (data.type === 'simulation_update' || data.type === 'simulation_complete') {
           setSimulationResults(data.results, data.metrics);
        }
      });

      // Ensure WS is connected before triggering API
      if (!simulationWs['ws'] || simulationWs['ws']?.readyState !== WebSocket.OPEN) {
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
        <h2 className="text-xl font-bold text-slate-100 tracking-wide">Interventions</h2>
      </div>

      <div className="flex flex-col gap-5">
        <div className="flex flex-col gap-2">
          <label className="text-xs font-semibold text-slate-400 uppercase tracking-wider flex items-center gap-2">
            <Activity className="w-4 h-4 text-blue-400" /> Type
          </label>
          <select 
            value={interventionType}
            onChange={(e) => setInterventionType(e.target.value)}
            className="bg-slate-800/80 border border-slate-600 rounded-lg p-3 text-slate-200 outline-none focus:ring-2 focus:ring-emerald-500/50 transition-all font-medium"
          >
            <option value="green_roofs">Green Roofs</option>
            <option value="cool_pavements">Cool Pavements</option>
            <option value="traffic_reduction">Traffic Reduction</option>
          </select>
        </div>

        <div className="flex flex-col gap-3 group">
          <label className="text-xs font-semibold text-slate-400 uppercase tracking-wider flex justify-between items-center">
            <span className="flex items-center gap-2"><Leaf className="w-4 h-4 text-emerald-400" /> Add Green Space</span>
            <span className="text-emerald-400 font-mono bg-emerald-400/10 px-2 py-0.5 rounded">{params.greenSpaceAdded}%</span>
          </label>
          <input 
            type="range" 
            min="0" max="50" 
            value={params.greenSpaceAdded}
            onChange={(e) => setParams({ greenSpaceAdded: parseInt(e.target.value) })}
            className="w-full h-2 bg-slate-700 rounded-lg appearance-none cursor-pointer accent-emerald-500"
          />
        </div>

        <div className="flex flex-col gap-3 group">
          <label className="text-xs font-semibold text-slate-400 uppercase tracking-wider flex justify-between items-center">
            <span className="flex items-center gap-2"><Sun className="w-4 h-4 text-amber-400" /> Change Albedo</span>
            <span className="text-amber-400 font-mono bg-amber-400/10 px-2 py-0.5 rounded">+{params.albedoChange}</span>
          </label>
          <input 
            type="range" 
            min="0" max="0.5" step="0.05"
            value={params.albedoChange}
            onChange={(e) => setParams({ albedoChange: parseFloat(e.target.value) })}
            className="w-full h-2 bg-slate-700 rounded-lg appearance-none cursor-pointer accent-amber-500"
          />
        </div>

        <div className="flex flex-col gap-3 group">
          <label className="text-xs font-semibold text-slate-400 uppercase tracking-wider flex justify-between items-center">
            <span className="flex items-center gap-2"><Car className="w-4 h-4 text-rose-400" /> Traffic Reduction</span>
            <span className="text-rose-400 font-mono bg-rose-400/10 px-2 py-0.5 rounded">{params.trafficReduction}%</span>
          </label>
          <input 
            type="range" 
            min="0" max="100" 
            value={params.trafficReduction}
            onChange={(e) => setParams({ trafficReduction: parseInt(e.target.value) })}
            className="w-full h-2 bg-slate-700 rounded-lg appearance-none cursor-pointer accent-rose-500"
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
