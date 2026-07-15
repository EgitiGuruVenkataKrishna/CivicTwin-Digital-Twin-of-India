import React, { useState } from 'react';
import { X, Users, Lightbulb, Cpu, DollarSign, Award, Database } from 'lucide-react';

interface InfoModalProps {
  isOpen: boolean;
  onClose: () => void;
}

export const InfoModal: React.FC<InfoModalProps> = ({ isOpen, onClose }) => {
  const [activeTab, setActiveTab] = useState<'overview' | 'team' | 'architecture' | 'datasets'>('overview');

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-slate-950/80 backdrop-blur-md p-4 animate-fadeIn">
      <div className="relative w-full max-w-4xl h-[80vh] bg-slate-900 border border-slate-700/50 rounded-3xl shadow-[0_20px_50px_rgba(0,0,0,0.5)] flex flex-col overflow-hidden text-slate-100">
        
        {/* Header */}
        <div className="flex items-center justify-between px-8 py-5 border-b border-slate-800 bg-slate-900/50">
          <div className="flex items-center gap-3">
            <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-emerald-400 to-teal-600 flex items-center justify-center">
              <Award className="w-5 h-5 text-white" />
            </div>
            <div>
              <h2 className="text-xl font-bold tracking-tight bg-clip-text text-transparent bg-gradient-to-r from-slate-100 to-slate-400">
                CivicTwin — Hackathon Proposal Details
              </h2>
              <p className="text-xs text-slate-400 uppercase tracking-widest font-semibold mt-0.5">
                Bharatiya Antariksh Hackathon 2026
              </p>
            </div>
          </div>
          <button 
            onClick={onClose}
            className="p-2 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-400 hover:text-slate-200 transition-colors"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Navigation Tabs */}
        <div className="flex border-b border-slate-800 bg-slate-900/20 px-8 py-3 gap-2">
          <button
            onClick={() => setActiveTab('overview')}
            className={`flex items-center gap-2 px-4 py-2 rounded-xl text-sm font-semibold transition-all ${
              activeTab === 'overview'
                ? 'bg-emerald-500/20 border border-emerald-500/30 text-emerald-400'
                : 'hover:bg-slate-800/50 text-slate-400 hover:text-slate-200'
            }`}
          >
            <Lightbulb className="w-4 h-4" /> Overview & Opportunity
          </button>
          <button
            onClick={() => setActiveTab('team')}
            className={`flex items-center gap-2 px-4 py-2 rounded-xl text-sm font-semibold transition-all ${
              activeTab === 'team'
                ? 'bg-emerald-500/20 border border-emerald-500/30 text-emerald-400'
                : 'hover:bg-slate-800/50 text-slate-400 hover:text-slate-200'
            }`}
          >
            <Users className="w-4 h-4" /> Team & Cost
          </button>
          <button
            onClick={() => setActiveTab('architecture')}
            className={`flex items-center gap-2 px-4 py-2 rounded-xl text-sm font-semibold transition-all ${
              activeTab === 'architecture'
                ? 'bg-emerald-500/20 border border-emerald-500/30 text-emerald-400'
                : 'hover:bg-slate-800/50 text-slate-450 hover:text-slate-200'
            }`}
          >
            <Cpu className="w-4 h-4" /> Architecture & Tech Stack
          </button>
          <button
            onClick={() => setActiveTab('datasets')}
            className={`flex items-center gap-2 px-4 py-2 rounded-xl text-sm font-semibold transition-all ${
              activeTab === 'datasets'
                ? 'bg-emerald-500/20 border border-emerald-500/30 text-emerald-400'
                : 'hover:bg-slate-800/50 text-slate-400 hover:text-slate-200'
            }`}
          >
            <Database className="w-4 h-4" /> ISRO Data Catalog
          </button>
        </div>

        {/* Content Area */}
        <div className="flex-1 overflow-y-auto p-8 bg-slate-900/30 scrollbar">
          
          {/* TAB 1: Overview */}
          {activeTab === 'overview' && (
            <div className="flex flex-col gap-6 animate-slideIn">
              <div>
                <h3 className="text-emerald-400 font-bold text-xs uppercase tracking-widest mb-2">Problem Statement</h3>
                <p className="text-slate-300 text-lg leading-relaxed font-medium">
                  AI-Powered Digital Twin of India’s Climate using India's National Data
                </p>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mt-2">
                <div className="p-5 rounded-2xl border border-slate-800 bg-slate-900/40">
                  <h4 className="text-slate-200 font-bold text-sm flex items-center gap-2 mb-2">
                    <span className="w-1.5 h-1.5 rounded-full bg-emerald-400"></span>
                    How is it different?
                  </h4>
                  <p className="text-slate-400 text-sm leading-relaxed">
                    Unlike standard models providing static snapshots, CivicTwin integrates heterogeneous national datasets 
                    (INSAT, IMD) into a dynamic, physics-informed AI framework, shifting from descriptive observation to 
                    interactive simulation.
                  </p>
                </div>

                <div className="p-5 rounded-2xl border border-slate-800 bg-slate-900/40">
                  <h4 className="text-slate-200 font-bold text-sm flex items-center gap-2 mb-2">
                    <span className="w-1.5 h-1.5 rounded-full bg-emerald-400"></span>
                    How does it solve the problem?
                  </h4>
                  <p className="text-slate-400 text-sm leading-relaxed">
                    By fusing multi-source data with physics-informed machine learning, CivicTwin reduces uncertainty in 
                    forecasting extreme weather and heat stress, enabling policymakers to run real-time "What-If" adaptation scenarios.
                  </p>
                </div>
              </div>

              <div className="p-5 rounded-2xl border border-emerald-500/20 bg-emerald-500/5 mt-2">
                <h4 className="text-emerald-400 font-bold text-sm flex items-center gap-2 mb-2">
                  🌟 USP of the proposed solution
                </h4>
                <p className="text-slate-300 text-sm leading-relaxed font-medium">
                  Physics-Informed Digital Interoperability. Our solution ensures predictions respect physical laws, providing 
                  high-fidelity, actionable intelligence specifically tuned to India’s national climate infrastructure.
                </p>
              </div>

              <div>
                <h3 className="text-emerald-400 font-bold text-xs uppercase tracking-widest mb-3">Key Features Offered</h3>
                <ul className="grid grid-cols-1 md:grid-cols-2 gap-2 text-sm text-slate-300">
                  <li className="flex items-center gap-2">
                    <div className="w-1.5 h-1.5 rounded-full bg-emerald-400"></div> Real-time heterogenous national data ingestion
                  </li>
                  <li className="flex items-center gap-2">
                    <div className="w-1.5 h-1.5 rounded-full bg-emerald-400"></div> Physics-Informed Neural Network (PINN) core solver
                  </li>
                  <li className="flex items-center gap-2">
                    <div className="w-1.5 h-1.5 rounded-full bg-emerald-400"></div> Interactive 3D visual deck.gl dashboard
                  </li>
                  <li className="flex items-center gap-2">
                    <div className="w-1.5 h-1.5 rounded-full bg-emerald-400"></div> Dynamic what-if scenarios (Albedo, Green Cover, Traffic)
                  </li>
                  <li className="flex items-center gap-2">
                    <div className="w-1.5 h-1.5 rounded-full bg-emerald-400"></div> Uncertainty quantification with MC-Dropout
                  </li>
                  <li className="flex items-center gap-2">
                    <div className="w-1.5 h-1.5 rounded-full bg-emerald-400"></div> Zero-penny scalable cloud deployment architecture
                  </li>
                </ul>
              </div>
            </div>
          )}

          {/* TAB 2: Team & Cost */}
          {activeTab === 'team' && (
            <div className="flex flex-col gap-6 animate-slideIn">
              <div>
                <h3 className="text-emerald-400 font-bold text-xs uppercase tracking-widest mb-4">Team Members</h3>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  
                  {/* Team Leader */}
                  <div className="p-4 rounded-xl border border-emerald-500/20 bg-slate-900/40 flex items-start gap-4">
                    <div className="p-2.5 bg-emerald-500/10 rounded-lg text-emerald-400 border border-emerald-500/20 font-bold text-xs uppercase">
                      LDR
                    </div>
                    <div>
                      <h4 className="font-bold text-slate-200">Guru Venkata Krishna Egiti</h4>
                      <p className="text-xs text-slate-400 mt-1">College: VIT-AP University</p>
                      <p className="text-[10px] text-emerald-400 font-bold uppercase tracking-wider mt-1">Team Leader</p>
                    </div>
                  </div>

                  {/* Member 1 */}
                  <div className="p-4 rounded-xl border border-slate-800 bg-slate-900/40 flex items-start gap-4">
                    <div className="p-2.5 bg-slate-800 rounded-lg text-slate-400 font-bold text-xs">
                      M1
                    </div>
                    <div>
                      <h4 className="font-bold text-slate-200">Prasad Mediboina</h4>
                      <p className="text-xs text-slate-400 mt-1">College: MVJ College of Engineering</p>
                      <p className="text-[10px] text-slate-500 font-bold uppercase tracking-wider mt-1">Developer</p>
                    </div>
                  </div>

                  {/* Member 2 */}
                  <div className="p-4 rounded-xl border border-slate-800 bg-slate-900/40 flex items-start gap-4">
                    <div className="p-2.5 bg-slate-800 rounded-lg text-slate-400 font-bold text-xs">
                      M2
                    </div>
                    <div>
                      <h4 className="font-bold text-slate-200">Shree Harsha R</h4>
                      <p className="text-xs text-slate-400 mt-1">College: VIT-AP University</p>
                      <p className="text-[10px] text-slate-500 font-bold uppercase tracking-wider mt-1">Developer</p>
                    </div>
                  </div>

                  {/* Member 3 */}
                  <div className="p-4 rounded-xl border border-slate-800 bg-slate-900/40 flex items-start gap-4">
                    <div className="p-2.5 bg-slate-800 rounded-lg text-slate-400 font-bold text-xs">
                      M3
                    </div>
                    <div>
                      <h4 className="font-bold text-slate-200">Sunayana Padhy</h4>
                      <p className="text-xs text-slate-400 mt-1">College: VIT-AP University</p>
                      <p className="text-[10px] text-slate-500 font-bold uppercase tracking-wider mt-1">Developer</p>
                    </div>
                  </div>

                </div>
              </div>

              <div className="p-6 rounded-2xl border border-slate-850 bg-slate-900/20 mt-2">
                <h3 className="text-emerald-400 font-bold text-xs uppercase tracking-widest flex items-center gap-2 mb-3">
                  <DollarSign className="w-4 h-4" /> Estimated Implementation Cost
                </h3>
                <div className="flex flex-col gap-4">
                  <div className="flex justify-between items-baseline border-b border-slate-800 pb-2">
                    <span className="text-sm font-semibold text-slate-300">Strategy</span>
                    <span className="text-emerald-400 font-black text-lg">Zero-Penny Infrastructure</span>
                  </div>
                  <p className="text-slate-400 text-sm leading-relaxed">
                    <strong>Approach:</strong> Utilising free tiers for all cloud services (GCP Research Credits, GEE NonCommercial, Render, Supabase, and Streamlit Cloud).
                  </p>
                  <p className="text-slate-400 text-sm leading-relaxed">
                    <strong>Focus:</strong> Investment is allocated to engineering time and open-source development, minimising overhead by leveraging managed open-source ecosystems.
                  </p>
                </div>
              </div>
            </div>
          )}

          {/* TAB 3: Architecture & Tech */}
          {activeTab === 'architecture' && (
            <div className="flex flex-col gap-6 animate-slideIn">
              
              {/* Technologies */}
              <div>
                <h3 className="text-emerald-400 font-bold text-xs uppercase tracking-widest mb-3">Technologies Used</h3>
                <div className="grid grid-cols-2 md:grid-cols-3 gap-3">
                  <div className="p-3 bg-slate-950/40 border border-slate-800 rounded-xl text-center">
                    <p className="text-xs text-slate-400 uppercase font-semibold">Data Ingestion</p>
                    <p className="text-sm font-bold text-slate-200 mt-1">Google Earth Engine</p>
                  </div>
                  <div className="p-3 bg-slate-950/40 border border-slate-800 rounded-xl text-center">
                    <p className="text-xs text-slate-400 uppercase font-semibold">Database</p>
                    <p className="text-sm font-bold text-slate-200 mt-1">PostgreSQL + PostGIS</p>
                  </div>
                  <div className="p-3 bg-slate-950/40 border border-slate-800 rounded-xl text-center">
                    <p className="text-xs text-slate-400 uppercase font-semibold">Data Format</p>
                    <p className="text-sm font-bold text-slate-200 mt-1">Cloud-Optimised GeoTIFF</p>
                  </div>
                  <div className="p-3 bg-slate-950/40 border border-slate-800 rounded-xl text-center">
                    <p className="text-xs text-slate-400 uppercase font-semibold">AI Framework</p>
                    <p className="text-sm font-bold text-slate-200 mt-1">PyTorch (PINNs)</p>
                  </div>
                  <div className="p-3 bg-slate-950/40 border border-slate-800 rounded-xl text-center">
                    <p className="text-xs text-slate-400 uppercase font-semibold">Infrastructure</p>
                    <p className="text-sm font-bold text-slate-200 mt-1">Docker & GH Actions</p>
                  </div>
                  <div className="p-3 bg-slate-950/40 border border-slate-800 rounded-xl text-center">
                    <p className="text-xs text-slate-400 uppercase font-semibold">Visualisation</p>
                    <p className="text-sm font-bold text-slate-200 mt-1">Deck.gl + React</p>
                  </div>
                </div>
              </div>

              {/* Architecture Diagram */}
              <div>
                <h3 className="text-emerald-400 font-bold text-xs uppercase tracking-widest mb-3">System Architecture</h3>
                <div className="w-full bg-slate-950/50 rounded-2xl p-4 border border-slate-800 overflow-x-auto flex justify-center">
                  <svg width="600" height="180" viewBox="0 0 600 180" className="max-w-full">
                    {/* Data Sources */}
                    <rect x="10" y="50" width="120" height="80" rx="10" fill="#1e293b" stroke="#334155" strokeWidth="2" />
                    <text x="70" y="80" textAnchor="middle" fill="#94a3b8" fontSize="10" fontWeight="bold">DATA SOURCES</text>
                    <text x="70" y="98" textAnchor="middle" fill="#e2e8f0" fontSize="11" fontWeight="bold">GEE & MOSDAC</text>
                    <text x="70" y="114" textAnchor="middle" fill="#e2e8f0" fontSize="11" fontWeight="bold">IMD / CPCB</text>

                    {/* Arrow 1 */}
                    <path d="M 130 90 L 170 90" stroke="#10b981" strokeWidth="2" fill="none" markerEnd="url(#arrow)" />

                    {/* Database */}
                    <rect x="180" y="50" width="120" height="80" rx="10" fill="#111827" stroke="#10b981" strokeWidth="2" />
                    <text x="240" y="80" textAnchor="middle" fill="#10b981" fontSize="10" fontWeight="bold">SPATIAL DB</text>
                    <text x="240" y="98" textAnchor="middle" fill="#e2e8f0" fontSize="11" fontWeight="bold">PostgreSQL</text>
                    <text x="240" y="114" textAnchor="middle" fill="#e2e8f0" fontSize="11" fontWeight="bold">+ PostGIS</text>

                    {/* Arrow 2 */}
                    <path d="M 300 90 L 340 90" stroke="#10b981" strokeWidth="2" fill="none" markerEnd="url(#arrow)" />

                    {/* ML Server */}
                    <rect x="350" y="50" width="100" height="80" rx="10" fill="#1e293b" stroke="#334155" strokeWidth="2" />
                    <text x="400" y="80" textAnchor="middle" fill="#94a3b8" fontSize="10" fontWeight="bold">AI PINN CORE</text>
                    <text x="400" y="102" textAnchor="middle" fill="#e2e8f0" fontSize="11" fontWeight="bold">PyTorch</text>

                    {/* Arrow 3 */}
                    <path d="M 450 90 L 490 90" stroke="#10b981" strokeWidth="2" fill="none" markerEnd="url(#arrow)" />

                    {/* Web Dashboard */}
                    <rect x="500" y="50" width="90" height="80" rx="10" fill="#1e293b" stroke="#3b82f6" strokeWidth="2" />
                    <text x="545" y="80" textAnchor="middle" fill="#3b82f6" fontSize="10" fontWeight="bold">DASHBOARD</text>
                    <text x="545" y="98" textAnchor="middle" fill="#e2e8f0" fontSize="11" fontWeight="bold">React</text>
                    <text x="545" y="114" textAnchor="middle" fill="#e2e8f0" fontSize="11" fontWeight="bold">+ Deck.gl</text>

                    {/* SVG Definitions */}
                    <defs>
                      <marker id="arrow" viewBox="0 0 10 10" refX="5" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
                        <path d="M 0 0 L 10 5 L 0 10 z" fill="#10b981" />
                      </marker>
                    </defs>
                  </svg>
                </div>
              </div>

              {/* Process Flow Diagram */}
              <div>
                <h3 className="text-emerald-400 font-bold text-xs uppercase tracking-widest mb-3">Simulation Process Flow</h3>
                <div className="w-full bg-slate-950/50 rounded-2xl p-4 border border-slate-800 overflow-x-auto flex justify-center">
                  <svg width="600" height="150" viewBox="0 0 600 150" className="max-w-full">
                    {/* Step 1 */}
                    <circle cx="50" cy="70" r="30" fill="#1e293b" stroke="#334155" strokeWidth="2" />
                    <text x="50" y="74" textAnchor="middle" fill="#e2e8f0" fontSize="10" fontWeight="bold">1. Parameters</text>

                    <path d="M 80 70 L 130 70" stroke="#10b981" strokeWidth="1.5" fill="none" markerEnd="url(#arrow)" />

                    {/* Step 2 */}
                    <circle cx="170" cy="70" r="30" fill="#1e293b" stroke="#334155" strokeWidth="2" />
                    <text x="170" y="70" textAnchor="middle" fill="#e2e8f0" fontSize="9" fontWeight="bold">2. Query</text>
                    <text x="170" y="82" textAnchor="middle" fill="#e2e8f0" fontSize="9" fontWeight="bold">PostGIS</text>

                    <path d="M 200 70 L 250 70" stroke="#10b981" strokeWidth="1.5" fill="none" markerEnd="url(#arrow)" />

                    {/* Step 3 */}
                    <circle cx="290" cy="70" r="30" fill="#111827" stroke="#10b981" strokeWidth="2" />
                    <text x="290" y="70" textAnchor="middle" fill="#10b981" fontSize="9" fontWeight="bold">3. Solve</text>
                    <text x="290" y="82" textAnchor="middle" fill="#10b981" fontSize="9" fontWeight="bold">PINN</text>

                    <path d="M 320 70 L 370 70" stroke="#10b981" strokeWidth="1.5" fill="none" markerEnd="url(#arrow)" />

                    {/* Step 4 */}
                    <circle cx="410" cy="70" r="30" fill="#1e293b" stroke="#334155" strokeWidth="2" />
                    <text x="410" y="70" textAnchor="middle" fill="#e2e8f0" fontSize="9" fontWeight="bold">4. Broadcast</text>
                    <text x="410" y="82" textAnchor="middle" fill="#e2e8f0" fontSize="9" fontWeight="bold">Websocket</text>

                    <path d="M 440 70 L 490 70" stroke="#10b981" strokeWidth="1.5" fill="none" markerEnd="url(#arrow)" />

                    {/* Step 5 */}
                    <circle cx="530" cy="70" r="30" fill="#1e293b" stroke="#3b82f6" strokeWidth="2" />
                    <text x="530" y="70" textAnchor="middle" fill="#3b82f6" fontSize="9" fontWeight="bold">5. Render</text>
                    <text x="530" y="82" textAnchor="middle" fill="#3b82f6" fontSize="9" fontWeight="bold">Deck.gl</text>
                  </svg>
                </div>
              </div>

            </div>
          )}

          {/* TAB 4: ISRO Data Catalog */}
          {activeTab === 'datasets' && (
            <div className="flex flex-col gap-6 animate-slideIn">
              <div>
                <h3 className="text-emerald-400 font-bold text-xs uppercase tracking-widest mb-3">Satellite Data Products (MOSDAC / NICES)</h3>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div className="p-4 rounded-xl border border-slate-800 bg-slate-900/40">
                    <p className="text-xs text-orange-400 font-bold uppercase tracking-wider mb-1">INSAT Land Surface Temp (LST)</p>
                    <p className="text-sm font-bold text-slate-200">Product: 3RIMG_L2B_LST</p>
                    <p className="text-xs text-slate-400 mt-1 leading-relaxed">
                      High-resolution thermal infrared bands used to compute land surface thermal anomalies and monitoring soil dehydration.
                    </p>
                  </div>
                  <div className="p-4 rounded-xl border border-slate-800 bg-slate-900/40">
                    <p className="text-xs text-cyan-400 font-bold uppercase tracking-wider mb-1">INSAT Ocean/Sea Surface Temp (SST)</p>
                    <p className="text-sm font-bold text-slate-200">Product: 3RIMG_L2B_SST</p>
                    <p className="text-xs text-slate-400 mt-1 leading-relaxed">
                      SST measurements to capture regional oceanic thermal states affecting monsoon wind cycles and coastal humidity.
                    </p>
                  </div>
                  <div className="p-4 rounded-xl border border-slate-800 bg-slate-900/40">
                    <p className="text-xs text-blue-400 font-bold uppercase tracking-wider mb-1">INSAT Multi-sensor Rainfall</p>
                    <p className="text-sm font-bold text-slate-200">Product: 3RIMG_L2B_IMC</p>
                    <p className="text-xs text-slate-400 mt-1 leading-relaxed">
                      Integrated multi-spectral precipitation estimate representing convective monsoon downpours at hourly steps.
                    </p>
                  </div>
                  <div className="p-4 rounded-xl border border-slate-800 bg-slate-900/40">
                    <p className="text-xs text-emerald-400 font-bold uppercase tracking-wider mb-1">NICES Climate Variables</p>
                    <p className="text-sm font-bold text-slate-200">Product: Soil Moisture & Water Bodies</p>
                    <p className="text-xs text-slate-400 mt-1 leading-relaxed">
                      Biogeochemical variables tracking catchment reservoir boundaries, soil hydration index, and vegetation metrics.
                    </p>
                  </div>
                </div>
              </div>

              <div>
                <h3 className="text-emerald-400 font-bold text-xs uppercase tracking-widest mb-3">IMD Gridded National Meteorological Datasets</h3>
                <div className="p-5 rounded-2xl border border-slate-850 bg-slate-900/20">
                  <div className="flex flex-col gap-3 text-sm text-slate-300">
                    <div className="flex justify-between items-baseline border-b border-slate-800 pb-2">
                      <span className="font-semibold text-slate-200">1. IMD Gridded Rainfall (0.25° x 0.25°)</span>
                      <a href="https://www.imdpune.gov.in/cmpg/Griddata/Rainfall_25_Bin.html" target="_blank" rel="noreferrer" className="text-emerald-400 hover:underline text-xs">imdpune.gov.in →</a>
                    </div>
                    <p className="text-xs text-slate-450 leading-relaxed">
                      High-resolution daily precipitation binary arrays interpolated from rain-gauge stations across India, serving as the baseline ground truth for rainfall anomalies.
                    </p>
                    <div className="flex justify-between items-baseline border-b border-slate-800 pb-2 mt-2">
                      <span className="font-semibold text-slate-200">2. IMD Gridded Temperature (1.0° x 1.0°)</span>
                      <a href="https://imdpune.gov.in/cmpg/Griddata/Max_1_Bin.html" target="_blank" rel="noreferrer" className="text-emerald-400 hover:underline text-xs">imdpune.gov.in →</a>
                    </div>
                    <p className="text-xs text-slate-450 leading-relaxed">
                      Gridded Maximum and Minimum daily temperatures used to compute standard climate indices and train physical thermal coefficients.
                    </p>
                  </div>
                </div>
              </div>

              <div>
                <h3 className="text-emerald-400 font-bold text-xs uppercase tracking-widest mb-2">Bhuvan Geospatial Services</h3>
                <p className="text-slate-350 text-sm leading-relaxed">
                  The digital twin integrates Bhuvan base map services (WMS/WMTS), including the digital elevation model (DEM) and thematic land use/land cover (LULC) maps, establishing the underlying topographical constraints for runoff and crop-health projections.
                </p>
              </div>
            </div>
          )}

        </div>

        {/* Footer */}
        <div className="flex items-center justify-between px-8 py-4 border-t border-slate-800 bg-slate-900/50 text-[10px] text-slate-500 font-bold uppercase tracking-wider">
          <span>ISRO Bhartiya Antariksh Hackathon 2026</span>
          <span className="text-emerald-400">Team CivicTwin — H2S</span>
        </div>

      </div>
    </div>
  );
};
