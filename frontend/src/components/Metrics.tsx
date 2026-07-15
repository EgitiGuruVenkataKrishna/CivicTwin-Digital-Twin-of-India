import React from 'react';
import { useAppStore } from '../store/appStore';
import { Thermometer, Sprout, Droplets, Flame } from 'lucide-react';

const Metrics: React.FC = () => {
  const { overallMetrics } = useAppStore();

  const getDroughtColor = (index: string) => {
    const val = index.toLowerCase();
    if (val.includes('extreme')) return 'text-red-500';
    if (val.includes('severe')) return 'text-orange-500';
    if (val.includes('moderate')) return 'text-amber-500';
    return 'text-emerald-400';
  };

  const getDroughtBg = (index: string) => {
    const val = index.toLowerCase();
    if (val.includes('extreme')) return 'bg-red-500/10 border-red-500/30';
    if (val.includes('severe')) return 'bg-orange-500/10 border-orange-500/30';
    if (val.includes('moderate')) return 'bg-amber-500/10 border-amber-500/30';
    return 'bg-emerald-500/10 border-emerald-500/30';
  };

  return (
    <div className="absolute top-24 right-6 flex flex-col gap-4 z-10">
      {/* 1. Mean Temperature */}
      <div className="backdrop-blur-2xl bg-slate-900/60 border border-slate-700/50 rounded-2xl shadow-[0_8px_30px_rgb(0,0,0,0.4)] p-5 w-64 glass-panel flex items-center gap-5 transform transition-all hover:scale-105">
        <div className="p-3.5 bg-orange-500/20 rounded-xl shadow-inner border border-orange-500/30">
          <Thermometer className="w-7 h-7 text-orange-400" />
        </div>
        <div>
          <p className="text-xs font-bold text-slate-400 uppercase tracking-wider mb-1">Mean Temp</p>
          <p className="text-3xl font-black text-white drop-shadow-md">
            {overallMetrics.tempMean.toFixed(1)} <span className="text-lg font-bold text-slate-300">°C</span>
          </p>
        </div>
      </div>

      {/* 2. Crop Yield Impact */}
      <div className="backdrop-blur-2xl bg-slate-900/60 border border-slate-700/50 rounded-2xl shadow-[0_8px_30px_rgb(0,0,0,0.4)] p-5 w-64 glass-panel flex items-center gap-5 transform transition-all hover:scale-105">
        <div className="p-3.5 bg-emerald-500/20 rounded-xl shadow-inner border border-emerald-500/30">
          <Sprout className="w-7 h-7 text-emerald-400" />
        </div>
        <div>
          <p className="text-xs font-bold text-slate-400 uppercase tracking-wider mb-1">Crop Yield</p>
          <p className={`text-3xl font-black drop-shadow-md ${overallMetrics.cropYield >= 0 ? 'text-emerald-400' : 'text-red-400'}`}>
            {overallMetrics.cropYield >= 0 ? `+${overallMetrics.cropYield.toFixed(1)}` : overallMetrics.cropYield.toFixed(1)} <span className="text-lg font-bold text-slate-300">%</span>
          </p>
        </div>
      </div>

      {/* 3. Water Reserves */}
      <div className="backdrop-blur-2xl bg-slate-900/60 border border-slate-700/50 rounded-2xl shadow-[0_8px_30px_rgb(0,0,0,0.4)] p-5 w-64 glass-panel flex items-center gap-5 transform transition-all hover:scale-105">
        <div className="p-3.5 bg-cyan-500/20 rounded-xl shadow-inner border border-cyan-500/30">
          <Droplets className="w-7 h-7 text-cyan-400" />
        </div>
        <div>
          <p className="text-xs font-bold text-slate-400 uppercase tracking-wider mb-1">Water Reserves</p>
          <p className="text-3xl font-black text-white drop-shadow-md">
            {overallMetrics.reservoirLevel.toFixed(0)} <span className="text-lg font-bold text-slate-300">%</span>
          </p>
        </div>
      </div>

      {/* 4. Drought Index */}
      <div className="backdrop-blur-2xl bg-slate-900/60 border border-slate-700/50 rounded-2xl shadow-[0_8px_30px_rgb(0,0,0,0.4)] p-5 w-64 glass-panel flex items-center gap-5 transform transition-all hover:scale-105">
        <div className={`p-3.5 rounded-xl shadow-inner border ${getDroughtBg(overallMetrics.droughtIndex)}`}>
          <Flame className={`w-7 h-7 ${getDroughtColor(overallMetrics.droughtIndex)}`} />
        </div>
        <div>
          <p className="text-xs font-bold text-slate-400 uppercase tracking-wider mb-1">Drought Index</p>
          <p className={`text-2xl font-black drop-shadow-md ${getDroughtColor(overallMetrics.droughtIndex)}`}>
            {overallMetrics.droughtIndex}
          </p>
        </div>
      </div>
    </div>
  );
};

export default Metrics;
