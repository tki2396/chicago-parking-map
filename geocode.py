import time
import logging
import requests
import json
import os

from parse_zones import load_parking_zones, get_unique_street_segments

logger = logging.getLogger()

NOMINATIM_URL = os.getenv("NOMINATIM_URL")
USER_AGENT = os.getenv("USER_AGENT")
CACHE_FILE = os.getenv("CACHE_FILE")
GEOJSON_FILE = os.getenv("GEOJSON_FILE")


def build_query(row):
    addr_low = row["ADDRESS RANGE - LOW"]
    direction = row["STREET DIRECTION"]
    name = row["STREET NAME"]
    st_type = row["STREET TYPE"]
    return f"{addr_low} {direction} {name} {st_type}, Chicago, IL"

def geocode(query):
    params = {
        "q": query,
        "format": "json",
        "addressdetails": 1,
        "limit": 1,
    }
    headers = {"User-Agent": USER_AGENT}
    resp = requests.get(NOMINATIM_URL, params=params, headers=headers)
    if resp.status_code == 200 and resp.json():
        return resp.json()[0]
    return None

def load_cache():
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_cache(cache):
    with open(CACHE_FILE, "w", encoding="utf-8") as f:
        json.dump(cache, f, indent=2)

def main():
    rows = load_parking_zones()
    segments = get_unique_street_segments(rows)
    cache = load_cache()
    features = []

    for i, row in enumerate(segments):
        seg_id = f"{row['STREET DIRECTION']}|{row['STREET NAME']}|{row['STREET TYPE']}|{row['ADDRESS RANGE - LOW']}"
        if seg_id in cache:
            result = cache[seg_id]
        else:
            query = build_query(row)
            logger.info(f"[{i+1}/{len(segments)}] Geocoding: {query}")
            result = geocode(query)
            cache[seg_id] = result
            save_cache(cache)
            time.sleep(1)  # Be polite to the API

        if result:
            try:
                lat = float(result["lat"])
                lon = float(result["lon"])
                features.append({
                    "type": "Feature",
                    "geometry": {
                        "type": "Point",
                        "coordinates": [lon, lat]
                    },
                    "properties": {
                        "zone": row["ZONE"],
                        "address_low": row["ADDRESS RANGE - LOW"],
                        "address_high": row["ADDRESS RANGE - HIGH"],
                        "direction": row["STREET DIRECTION"],
                        "name": row["STREET NAME"],
                        "type": row["STREET TYPE"],
                        "odd_even": row["ODD_EVEN"]
                    }
                })
            except Exception as e:
                logger.error(f"Error parsing result: {e}")

    geojson = {
        "type": "FeatureCollection",
        "features": features
    }
    with open(GEOJSON_FILE, "w", encoding="utf-8") as f:
        json.dump(geojson, f, indent=2)
    logger.info(f"Saved {len(features)} features to {GEOJSON_FILE}")

if __name__ == "__main__":
    main()
