import React from 'react';
import { useAppStore } from '../store/appStore';
import { ThermometerSnowflake, Wind } from 'lucide-react';

const Metrics: React.FC = () => {
  const { overallMetrics } = useAppStore();

  return (
    <div className="absolute top-24 right-6 flex flex-col gap-4 z-10">
      <div className="backdrop-blur-2xl bg-slate-900/60 border border-slate-700/50 rounded-2xl shadow-[0_8px_30px_rgb(0,0,0,0.4)] p-5 w-64 glass-panel flex items-center gap-5 transform transition-all hover:scale-105">
        <div className="p-3.5 bg-blue-500/20 rounded-xl shadow-inner border border-blue-500/30">
          <ThermometerSnowflake className="w-7 h-7 text-blue-400" />
        </div>
        <div>
          <p className="text-xs font-bold text-slate-400 uppercase tracking-wider mb-1">Temp Drop</p>
          <p className="text-3xl font-black text-white drop-shadow-md">
            {overallMetrics.tempDrop.toFixed(1)} <span className="text-lg font-bold text-slate-300">°C</span>
          </p>
        </div>
      </div>

      <div className="backdrop-blur-2xl bg-slate-900/60 border border-slate-700/50 rounded-2xl shadow-[0_8px_30px_rgb(0,0,0,0.4)] p-5 w-64 glass-panel flex items-center gap-5 transform transition-all hover:scale-105">
        <div className="p-3.5 bg-teal-500/20 rounded-xl shadow-inner border border-teal-500/30">
          <Wind className="w-7 h-7 text-teal-400" />
        </div>
        <div>
          <p className="text-xs font-bold text-slate-400 uppercase tracking-wider mb-1">AQI Impr.</p>
          <p className="text-3xl font-black text-white drop-shadow-md">
            {overallMetrics.aqiImp.toFixed(0)} <span className="text-lg font-bold text-slate-300">pts</span>
          </p>
        </div>
      </div>
    </div>
  );
};

export default Metrics;
