import 'maplibre-gl/dist/maplibre-gl.css';
import maplibregl from 'maplibre-gl';

const MAPTILER_KEY = import.meta.env.VITE_MAPTILER_KEY

// Create the map container
const mapDiv = document.createElement('div');
mapDiv.id = 'map';
mapDiv.style.width = '100vw';
mapDiv.style.height = '100vh';
document.body.appendChild(mapDiv);

// Initialize MapLibre map
const map = new maplibregl.Map({
  container: 'map',
  style: `https://api.maptiler.com/maps/basic/style.json?key=${MAPTILER_KEY}`, // Open, no-auth, minimal vector style
  center: [-87.6298, 41.8781], // Chicago
  zoom: 11
});

// Add navigation controls
map.addControl(new maplibregl.NavigationControl(), 'top-right');

import type { DataDrivenPropertyValueSpecification } from 'maplibre-gl';

// Color palette for zones
const palette = [
  "#e6194b", "#3cb44b", "#ffe119", "#4363d8", "#f58231", "#911eb4", "#46f0f0",
  "#f032e6", "#bcf60c", "#fabebe", "#008080", "#e6beff", "#9a6324", "#fffac8",
  "#800000", "#aaffc3", "#808000", "#ffd8b1", "#000075", "#808080", "#ffffff", "#000000"
];

// Simple hash function to assign a color to a zone
function getZoneColor(zone: string): string {
  let hash = 0;
  for (let i = 0; i < zone.length; i++) {
    hash = zone.charCodeAt(i) + ((hash << 5) - hash);
  }
  return palette[Math.abs(hash) % palette.length];
}

/* Load and add the parking segments as a line layer */
map.on('load', () => {
  fetch('output_segments.geojson')
    .then(resp => resp.json())
    .then((geojson) => {
      // Add the GeoJSON as a source
      map.addSource('zones', {
        type: 'geojson',
        data: geojson
      });

      // Build a match expression for line color by zone
      const uniqueZones = Array.from(new Set(geojson.features.map((f: any) => f.properties.zone))) as string[];
      const zoneColors = [
        'match',
        ['get', 'zone'],
        ...uniqueZones.flatMap((zone) => [zone, getZoneColor(String(zone))]),
        '#888'
      ];

      // Add the line layer
      map.addLayer({
        id: 'zone-lines',
        type: 'line',
        source: 'zones',
        paint: {
          'line-color': zoneColors as unknown as DataDrivenPropertyValueSpecification<string>,
          'line-width': 4,
          'line-opacity': 0.8
        }
      });

      // Add popups on click
      map.on('click', 'zone-lines', (e) => {
        const feature = e.features && e.features[0];
        if (feature) {
          const p = feature.properties;
          new maplibregl.Popup()
            .setLngLat(e.lngLat)
            .setHTML(
              `<b>Zone:</b> ${p.zone}<br>
               <b>Address Range:</b> ${p.address_low} - ${p.address_high}<br>
               <b>Street:</b> ${p.direction} ${p.name} ${p.type}<br>
               <b>Odd/Even:</b> ${p.odd_even}`
            )
            .addTo(map);
        }
      });

      // Change cursor on hover
      map.on('mouseenter', 'zone-lines', () => {
        map.getCanvas().style.cursor = 'pointer';
      });
      map.on('mouseleave', 'zone-lines', () => {
        map.getCanvas().style.cursor = '';
      });
    })
    .catch(() => {
      alert("Could not load parking_segments.geojson. Please ensure the file is present.");
    });
});
