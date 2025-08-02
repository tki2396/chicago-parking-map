# Chicago Parking Zone Map

An interactive map to visualize Chicago's residential parking permit zones, using open data and open source tools.

## Project Overview

This project helps residents and visitors understand where they can park in Chicago by visualizing the boundaries and coverage of each parking permit zone. It uses official city data and displays the results on an interactive web map.

## Directory Structure

```
.
├── data/
│   └── Parking_Permit_Zones_20250802.csv   # Source CSV from City of Chicago
├── parse_zones.py                          # CSV parsing utilities
├── geocode_all.py                          # Geocode segments and output GeoJSON
├── geocoded_segments.json                   # Geocoding cache (auto-generated)
├── parking_segments.geojson                 # GeoJSON for map (auto-generated)
├── index.html                              # Interactive Leaflet map
├── plan.md                                 # Full project plan and workflow
├── .venv/                                  # Python virtual environment (created by uv)
└── README.md                               # This file
```

## Setup Instructions

1. **Install Python 3.13** (recommended for compatibility).
2. **Install [uv](https://github.com/astral-sh/uv)** for fast Python environment management.
3. **Create a virtual environment:**
   ```
   uv venv .venv --python=3.13
   ```
4. **Install dependencies:**
   ```
   uv pip install requests
   ```

## Data Processing Workflow

1. **Place the latest CSV in `data/`**  
   Download from [City of Chicago Data Portal](https://data.cityofchicago.org/Transportation/Parking-Permit-Zones/u9xt-hiju/data_preview).

2. **Parse and geocode street segments:**
   ```
   uv pip run python geocode_all.py
   ```
   - This will read the CSV, geocode each street segment (start and end), and output `parking_segments.geojson`.
   - Results are cached in `geocoded_segments.json` to avoid redundant API calls.

3. **Map Visualization:**
   - Open `index.html` in a browser to view the interactive map.
   - For local development, serve the directory with:
     ```
     uv pip run python -m http.server 8000
     ```
     Then visit [http://localhost:8000/index.html](http://localhost:8000/index.html).

   - Each zone is shown as a colored line segment. Click a segment for details.

## Updating Data

- To update for a new CSV, replace the file in `data/`, then re-run `geocode_all.py`.
- The cache will be used for previously geocoded segments; new segments will be geocoded as needed.

## Project Plan

See [plan.md](plan.md) for the full technical plan, design decisions, and stretch goals.

## License

This project is open source and uses only open data and open source tools.
