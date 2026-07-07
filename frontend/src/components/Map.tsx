import React, { useMemo } from 'react';
import DeckGL from '@deck.gl/react';
import { HeatmapLayer } from '@deck.gl/aggregation-layers';
import MapGL from 'react-map-gl/maplibre';
import 'maplibre-gl/dist/maplibre-gl.css';
import { useAppStore } from '../store/appStore';

const INITIAL_VIEW_STATE = {
  longitude: 77.2090, // New Delhi center
  latitude: 28.6139,
  zoom: 11,
  pitch: 45,
  bearing: 0
};

const MAP_STYLE = 'https://basemaps.cartocdn.com/gl/dark-matter-gl-style/style.json';

const MapComponent: React.FC = () => {
  const { simulationResults } = useAppStore();

  const layers = useMemo(() => {
    const data = simulationResults || [];
    
    return [
      new HeatmapLayer({
        id: 'heatmap-layer',
        data,
        getPosition: (d: any) => d.position,
        getWeight: (d: any) => Math.abs(d.temperatureDelta), // Weight visualization by magnitude of drop
        radiusPixels: 60,
        intensity: 2,
        threshold: 0.1,
        // Vibrant dark-theme heatmap palette (cool blue to vibrant red)
        colorRange: [
          [33, 102, 172, 150],  
          [67, 147, 195, 180],  
          [244, 165, 130, 200], 
          [214, 96, 77, 220],   
          [178, 24, 43, 255]    
        ]
      })
    ];
  }, [simulationResults]);

  return (
    <div className="absolute inset-0 w-full h-full z-0">
      <DeckGL
        initialViewState={INITIAL_VIEW_STATE}
        controller={true}
        layers={layers}
      >
        <MapGL mapStyle={MAP_STYLE} />
      </DeckGL>
    </div>
  );
};

export default MapComponent;
