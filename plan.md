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

### 3.1. Choose Mapping Library
- Use a modern web mapping library:
    - [Leaflet.js](https://leafletjs.com/) (open source, easy to use)
    - [Mapbox GL JS](https://docs.mapbox.com/mapbox-gl-js/) (more advanced, free tier available)
    - [Google Maps JS API] (if preferred, but may have cost/usage limits)

### 3.2. Render Zone Segments
- For each geocoded street segment, draw a polyline or point on the map.
- Color-code or style lines/points by zone.
- Optionally, group contiguous segments into polygons if possible (advanced).

### 3.3. Interactivity
- On hover/click: show zone number, street info, and any relevant restrictions.
- Search bar: allow users to enter an address, geocode it, and highlight the corresponding zone.
- Filter: allow users to select a zone and highlight all its segments.

### 3.4. Legend & UI
- Add a legend explaining colors/styles.
- Provide instructions for searching and interpreting the map.

## 4. Web Application Structure

### 4.1. Frontend
- Framework: Vanilla JS, React, or Vue (depending on complexity and preference).
- Components:
    - Map display
    - Search/filter controls
    - Info popups/tooltips
    - Legend

### 4.2. Backend (Optional)
- If geocoding on-the-fly or handling user uploads, a backend (Node.js, Python Flask, etc.) may be needed.
- For a static site, pre-process all geocoding and serve as static assets.

## 5. Deployment

- Host as a static site (GitHub Pages, Netlify, Vercel) if all data is pre-processed.
- If a backend is needed, deploy to a suitable platform (Heroku, Render, etc.).
- Ensure API keys (if used) are secured and not exposed in the frontend.

## 6. Technical Challenges & Solutions

- **Geocoding Accuracy:** Street segments may not always geocode cleanly; implement error handling and manual correction for problematic segments.
- **API Limits:** Use open/free geocoding services where possible; cache results.
- **Performance:** Pre-process and serve only necessary data to the frontend.
- **Data Updates:** Document the process for updating the map when new CSVs are released.

## 7. Stretch Goals

- Allow users to draw/select an area and see all zones intersecting it.
- Show permit rules, costs, and links to city resources.
- Mobile-friendly/responsive design.

---

## Next Steps

1. Parse and inspect the CSV to understand data quirks.
2. Prototype geocoding for a sample of street segments.
3. Choose mapping library and set up a basic map.
4. Develop data pipeline for geocoding and GeoJSON generation.
5. Build out the interactive frontend.
6. Deploy and test with real users.
