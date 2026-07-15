import React, { useMemo } from 'react';
import { DeckGL } from '@deck.gl/react';
import { HeatmapLayer } from '@deck.gl/aggregation-layers';
import { GeoJsonLayer, ScatterplotLayer } from '@deck.gl/layers';
import { Map as MapGL } from 'react-map-gl/maplibre';
import 'maplibre-gl/dist/maplibre-gl.css';
import { useAppStore } from '../store/appStore';

const INITIAL_VIEW_STATE = {
  longitude: 78.4867, // Hyderabad center
  latitude: 17.3850,
  zoom: 11.5,
  pitch: 30,
  bearing: 0
};

const MAP_STYLE = 'https://basemaps.cartocdn.com/gl/dark-matter-gl-style/style.json';

const MapComponent: React.FC = () => {
  const { simulationResults, zones, observations } = useAppStore();

  // Construct GeoJSON FeatureCollection for planning zones
  const zonesGeoJson = useMemo(() => {
    return {
      type: 'FeatureCollection',
      features: (zones || []).map((z) => ({
        type: 'Feature',
        geometry: z.geojson,
        properties: {
          id: z.id,
          name: z.name,
          zone_type: z.zone_type,
          ...z.properties
        }
      }))
    };
  }, [zones]);

  const layers = useMemo(() => {
    const list: any[] = [];

    // 1. Planning Zones Layer
    if (zones && zones.length > 0) {
      list.push(
        new GeoJsonLayer({
          id: 'zones-layer',
          data: zonesGeoJson,
          pickable: true,
          stroked: true,
          filled: true,
          lineWidthScale: 1,
          lineWidthMinPixels: 2,
          getFillColor: (f: any) => {
            const type = f.properties.zone_type;
            if (type === 'water_body') return [59, 130, 246, 50]; // blue
            if (type === 'green_space') return [16, 185, 129, 60]; // green
            if (type === 'commercial') return [245, 158, 11, 40]; // orange
            if (type === 'industrial') return [239, 68, 68, 40]; // red
            return [100, 116, 139, 30]; // slate
          },
          getLineColor: (f: any) => {
            const type = f.properties.zone_type;
            if (type === 'water_body') return [59, 130, 246, 180];
            if (type === 'green_space') return [16, 185, 129, 180];
            if (type === 'commercial') return [245, 158, 11, 180];
            if (type === 'industrial') return [239, 68, 68, 180];
            return [100, 116, 139, 150];
          },
          getLineWidth: 2
        })
      );
    }

    // 2. Heatmap Layer (Simulation deltas)
    if (simulationResults && simulationResults.length > 0) {
      list.push(
        new HeatmapLayer({
          id: 'heatmap-layer',
          data: simulationResults,
          getPosition: (d: any) => d.position,
          getWeight: (d: any) => Math.abs(d.temperatureDelta),
          radiusPixels: 45,
          intensity: 1.5,
          threshold: 0.05,
          colorRange: [
            [33, 102, 172, 120],  
            [67, 147, 195, 150],  
            [244, 165, 130, 180], 
            [214, 96, 77, 210],   
            [178, 24, 43, 240]    
          ]
        })
      );
    }

    // 3. Climate Ground Observations / Satellites Layer
    if (observations && observations.length > 0) {
      list.push(
        new ScatterplotLayer({
          id: 'observations-layer',
          data: observations,
          pickable: true,
          opacity: 0.9,
          stroked: true,
          filled: true,
          radiusScale: 15,
          radiusMinPixels: 6,
          radiusMaxPixels: 12,
          lineWidthMinPixels: 1.5,
          getPosition: (d: any) => [d.lon, d.lat],
          getFillColor: (d: any) => {
            if (d.dataset === 'cpcb_aq') return [20, 184, 166]; // teal (CPCB AQI)
            if (d.dataset === 'imd_stations') return [168, 85, 247]; // purple (IMD Stations)
            if (d.dataset === 'gee_lst') return [239, 68, 68]; // red (GEE Landsat LST)
            return [249, 115, 22]; // orange (MOSDAC INSAT)
          },
          getLineColor: [255, 255, 255, 225],
          getLineWidth: 1
        })
      );
    }

    return list;
  }, [simulationResults, zonesGeoJson, observations]);

  return (
    <div className="absolute inset-0 w-full h-full z-0">
      <DeckGL
        initialViewState={INITIAL_VIEW_STATE}
        controller={true}
        layers={layers}
        getTooltip={({ object }) => {
          if (!object) return null;
          // If it's a planning zone feature
          if (object.properties && object.properties.zone_type) {
            const typeFormatted = object.properties.zone_type.replace('_', ' ');
            return {
              html: `<div class="bg-slate-900 border border-slate-700/50 p-3 rounded-xl shadow-xl text-slate-100 text-xs font-sans">
                      <p class="font-bold text-emerald-400 text-sm mb-1">${object.properties.name}</p>
                      <p class="capitalize"><strong class="text-slate-400">Type:</strong> ${typeFormatted}</p>
                      <p class="mt-1 text-slate-300 font-medium">${object.properties.description || ''}</p>
                    </div>`,
              style: { padding: '0', backgroundColor: 'transparent' }
            };
          }
          // If it's an observation point
          if (object.dataset) {
            const val = object.properties?.value || object.properties?.aqi || object.properties?.temp_c || 0;
            const unit = object.dataset === 'cpcb_aq' ? ' pts' : ' °C';
            const metric = object.dataset === 'cpcb_aq' ? 'Air Quality (AQI)' : 'Surface Temperature';
            const sensor = object.dataset === 'cpcb_aq' 
              ? 'CPCB Ground Station' 
              : object.dataset === 'imd_stations' 
                ? 'IMD AWS Station'
                : object.dataset === 'gee_lst'
                  ? 'Landsat-8 (GEE)'
                  : 'INSAT-3D (MOSDAC)';
            return {
              html: `<div class="bg-slate-900 border border-slate-700/50 p-3 rounded-xl shadow-xl text-slate-100 text-xs font-sans">
                      <p class="font-bold text-teal-400 text-sm mb-1">${sensor}</p>
                      <p><strong class="text-slate-400">${metric}:</strong> ${val.toFixed(1)}${unit}</p>
                      <p class="text-[10px] text-slate-500 mt-1">Coordinates: [${object.lon.toFixed(4)}, ${object.lat.toFixed(4)}]</p>
                    </div>`,
              style: { padding: '0', backgroundColor: 'transparent' }
            };
          }
          return null;
        }}
      >
        <MapGL mapStyle={MAP_STYLE} />
      </DeckGL>
    </div>
  );
};

export default MapComponent;

