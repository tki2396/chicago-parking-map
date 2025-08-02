# Plan for Building an Interactive Chicago Parking Zone Map

## 1. Project Overview

Create an interactive web map that visualizes Chicago's residential parking permit zones using the provided CSV data. The map should allow users to:
- View the boundaries/coverage of each parking zone.
- Search for an address or click on the map to see the zone.
- Filter or highlight specific zones.
- Understand the street-level applicability of each zone.

## 2. Data Processing

### 2.1. Parse the CSV
- Read and parse `Parking_Permit_Zones_20250802.csv`.
- Extract relevant fields: ZONE, ADDRESS RANGE - LOW/HIGH, STREET DIRECTION, STREET NAME, STREET TYPE, ODD_EVEN, etc.

### 2.2. Geocode Street Segments
- For each row, construct a street segment (e.g., "5900-5998 N Harding Ave").
- Use a geocoding API (e.g., OpenStreetMap Nominatim) to convert each segment into a polyline or set of coordinates.
    - Batch geocoding is recommended for efficiency.
    - Handle API rate limits and errors gracefully.
- Store geocoded results in a GeoJSON or similar format for efficient map rendering.

### 2.3. Data Normalization & Caching
- Normalize street names and directions for consistency.
- Cache geocoded results to avoid repeated API calls.
- Optionally, pre-process and store the geocoded data as a static file (GeoJSON) for fast loading.

## 3. Map Visualization

### 3.1. Mapping Library and Frontend Stack

- **Mapping Library:** Use [MapLibre GL JS](https://maplibre.org/projects/maplibre-gl-js/), a fully open source fork of Mapbox GL JS v1.x, for modern vector maps and advanced styling. No API key or vendor lock-in required.
- **Frontend:** Use TypeScript for all frontend code, organized in `src/`.
- **Build Tool:** Use [Vite](https://vitejs.dev/) for fast TypeScript/ESM builds and local development.
- **Deployment:** The output is static HTML/JS/CSS, compatible with GitHub Pages and other static hosts.

### 3.2. Project Structure

- `src/main.ts`: TypeScript entrypoint for the map UI.
- `index.html`: Loads the Vite/TS bundle as a module.
- `vite.config.js`, `tsconfig.json`: Build and TypeScript config.
- `data/`, `parking_segments.geojson`: Data files.

### 3.3. Rendering Zones

- For each geocoded street segment, draw a colored polyline on the map, colored by zone.
- **Next step:** To show the area/boundary of each zone, generate polygons (not just lines) for each zone. This may require:
    - Grouping contiguous segments by zone.
    - Using a polygonization algorithm or heuristics to "fill" the area.
    - Rendering polygons with semi-transparent fill and colored borders.

### 3.4. Interactivity

- On hover/click: show zone number, street info, and any relevant restrictions.
- Search bar: allow users to enter an address, geocode it, and highlight the corresponding zone.
- Filter: allow users to select a zone and highlight all its segments or area.

### 3.5. Legend & UI

- Add a legend explaining colors/styles.
- Provide instructions for searching and interpreting the map.

## 4. Web Application Structure

### 4.1. Frontend

- All frontend code is written in TypeScript and lives in `src/`.
- Use ES module imports and modern JS/TS features.
- Vite handles local dev server, hot reload, and builds for production.
- The map is initialized in `src/main.ts` using MapLibre GL JS.

### 4.2. Deployment

- The built site is static and can be deployed to GitHub Pages or any static host.
- Only the compiled JS (not raw TS) is deployed.
- No backend is required unless you want to add dynamic geocoding or user uploads.

## 5. Development and Deployment Workflow

- **Local development:** Use Vite for fast dev server and hot reload:
  ```
  npm run dev
  ```
- **Build for production:** 
  ```
  npm run build
  ```
  Output is in `dist/`.
- **Deploy:** Push the contents of `dist/` (and static files) to GitHub Pages or your preferred static host.
- **No API keys required** for MapLibre and open vector tiles.

## 6. Technical Challenges & Solutions

- **Geocoding Accuracy:** Street segments may not always geocode cleanly; implement error handling and manual correction for problematic segments.
- **API Limits:** Use open/free geocoding services where possible; cache results.
- **Performance:** Pre-process and serve only necessary data to the frontend.
- **Data Updates:** Document the process for updating the map when new CSVs are released.

## 7. Stretch Goals

- Allow users to draw/select an area and see all zones intersecting it.
- Show permit rules, costs, and links to city resources.
- Mobile-friendly/responsive design.
- Add address search and zone highlight.
- Generate and display polygons for full zone areas (not just lines).

---

## Next Steps

1. Parse and inspect the CSV to understand data quirks.
2. Prototype geocoding for a sample of street segments.
3. **Switch to MapLibre GL JS and TypeScript frontend (done).**
4. Develop data pipeline for geocoding and GeoJSON generation.
5. Build out the interactive frontend using Vite and MapLibre.
6. **Implement area coloring:** Generate polygons for each zone and render them with fill color.
7. Deploy and test with real users.
