import 'maplibre-gl/dist/maplibre-gl.css';
import maplibregl from 'maplibre-gl';

// Create the map container
const mapDiv = document.createElement('div');
mapDiv.id = 'map';
mapDiv.style.width = '100vw';
mapDiv.style.height = '100vh';
document.body.appendChild(mapDiv);

// Initialize MapLibre map
const map = new maplibregl.Map({
  container: 'map',
  style: 'https://demotiles.maplibre.org/style.json', // Free open source style
  center: [-87.6298, 41.8781], // Chicago
  zoom: 11
});

// Add navigation controls
map.addControl(new maplibregl.NavigationControl(), 'top-right');

// TODO: Load and display parking_segments.geojson as polygons/lines
