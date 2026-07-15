import { useEffect, useState } from 'react';
import Sidebar from './components/Sidebar';
import MapComponent from './components/Map';
import Metrics from './components/Metrics';
import { Layers, Award } from 'lucide-react';
import { apiClient, simulationWs } from './services/api';
import { InfoModal } from './components/InfoModal';
import { useAppStore } from './store/appStore';

function App() {
  const [isInfoOpen, setIsInfoOpen] = useState(false);
  const { setZones, setObservations } = useAppStore();

  useEffect(() => {
    // Initialize WebSockets on mount
    simulationWs.connect();
    
    // Load initial database data
    const loadInitialData = async () => {
      try {
        const zonesResp = await apiClient.get('/zones');
        setZones(zonesResp.data);
      } catch (err) {
        console.warn("Failed to load planning zones:", err);
      }

      try {
        const obsResp = await apiClient.get('/climate/snapshot?west=78.2&south=17.2&east=78.7&north=17.6');
        setObservations(obsResp.data.observations || []);
      } catch (err) {
        console.warn("Failed to load climate observations:", err);
      }
    };
    
    loadInitialData();
    
    // Clean up on unmount
    return () => {
      simulationWs.disconnect();
    };
  }, []);

  return (
    <div className="relative w-full h-screen overflow-hidden bg-slate-950 font-sans text-slate-100 selection:bg-emerald-500/30">
      {/* Deck.GL Map Background */}
      <MapComponent />

      {/* Top Header Panel */}
      <header className="absolute top-0 left-0 right-0 h-16 backdrop-blur-xl bg-slate-950/50 border-b border-slate-800/80 z-20 flex items-center px-6 justify-between shadow-lg">
        <div className="flex items-center gap-4">
          <div className="w-9 h-9 rounded-xl bg-gradient-to-br from-emerald-400 to-teal-600 flex items-center justify-center shadow-[0_0_15px_rgba(52,211,153,0.3)]">
            <Layers className="w-5 h-5 text-white" />
          </div>
          <h1 className="text-2xl font-black tracking-tight bg-clip-text text-transparent bg-gradient-to-r from-slate-100 to-slate-400">
            CivicTwin
          </h1>
          <span className="ml-3 px-2.5 py-1 rounded-md bg-slate-800/80 border border-slate-700/80 text-[11px] font-bold text-emerald-400 uppercase tracking-widest shadow-inner">
            Phase 5
          </span>
        </div>
        
        <div className="flex items-center gap-4">
          <button 
            onClick={() => setIsInfoOpen(true)}
            className="flex items-center gap-2 px-3 py-1.5 rounded-lg bg-emerald-500/10 hover:bg-emerald-500/20 border border-emerald-500/20 hover:border-emerald-500/30 text-emerald-400 text-xs font-bold transition-all shadow-md active:scale-95"
          >
            <Award className="w-3.5 h-3.5" /> Project Info
          </button>
          
          <div className="flex items-center gap-3 bg-slate-900/60 border border-slate-700/50 rounded-full px-4 py-1.5 backdrop-blur-md">
            <div className="w-2.5 h-2.5 rounded-full bg-emerald-500 animate-pulse shadow-[0_0_8px_rgba(16,185,129,0.8)]"></div>
            <span className="text-xs font-bold text-slate-300 tracking-wide uppercase">System Online</span>
          </div>
        </div>
      </header>

      {/* Floating UI Overlay */}
      <Sidebar />
      <Metrics />

      {/* Info Modal Overlay */}
      <InfoModal isOpen={isInfoOpen} onClose={() => setIsInfoOpen(false)} />
    </div>
  );
}

export default App;
