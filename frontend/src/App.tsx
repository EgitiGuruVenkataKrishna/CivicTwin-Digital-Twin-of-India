import "./App.css";

function App() {
  return (
    <div className="app">
      <header className="app-header">
        <h1>🌡️ CivicTwin</h1>
        <p>AI-Powered Climate Digital Twin — Hyderabad</p>
      </header>
      <main className="app-main">
        <div className="placeholder-map">
          {/* TODO: Replace with MapContainer (Deck.gl + MapLibre) */}
          <p>Map viewport will render here</p>
          <p className="tech-note">Deck.gl + MapLibre GL JS</p>
        </div>
        <aside className="placeholder-sidebar">
          {/* TODO: Replace with ZonePanel + ScenarioBuilder */}
          <h2>Scenario Builder</h2>
          <p>Select a zone on the map to begin simulation.</p>
        </aside>
      </main>
    </div>
  );
}

export default App;
