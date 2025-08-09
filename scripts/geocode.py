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

error_count = 0

def build_query(row, which="low"):
    """
    Build a geocoding query for the low or high address of a segment.
    """
    addr = row["ADDRESS RANGE - LOW"] if which == "low" else row["ADDRESS RANGE - HIGH"]
    direction = row["STREET DIRECTION"]
    name = row["STREET NAME"]
    st_type = row["STREET TYPE"]
    return f"{addr} {direction} {name} {st_type}, Chicago, IL"

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
        logger.info(resp.json()[0])
        return resp.json()[0]
    else:
        logger.error(f"Geocode error - status: {resp.status_code}, content: {resp.content}")
        error_count += 1
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
        if error_count > 3:
            logger.critical(f"TOO MANY ERRORS: {error_count}. TERMINATING")
            return
        seg_id = f"{row['STREET DIRECTION']}|{row['STREET NAME']}|{row['STREET TYPE']}|{row['ADDRESS RANGE - LOW']}|{row['ADDRESS RANGE - HIGH']}"
        if seg_id in cache:
            result_low, result_high = cache[seg_id]
        else:
            query_low = build_query(row, "low")
            query_high = build_query(row, "high")
            logger.info(f"[{i+1}/{len(segments)}] Geocoding: {query_low} and {query_high}")
            result_low = geocode(query_low)
            time.sleep(1)
            result_high = geocode(query_high)
            cache[seg_id] = (result_low, result_high)
            save_cache(cache)
            time.sleep(1)  # Be polite to the API

        logger.info(f"LOW: {result_low}")
        logger.info(f"HIGH: {result_high}")
        if result_low and result_high:
            try:
                lat1 = float(result_low["lat"])
                lon1 = float(result_low["lon"])
                lat2 = float(result_high["lat"])
                lon2 = float(result_high["lon"])
                features.append({
                    "type": "Feature",
                    "geometry": {
                        "type": "LineString",
                        "coordinates": [[lon1, lat1], [lon2, lat2]]
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
        else:
            logger.warning("One or both geocoding results missing, skipping segment.")

    geojson = {
        "type": "FeatureCollection",
        "features": features
    }
    with open(GEOJSON_FILE, "w", encoding="utf-8") as f:
        json.dump(geojson, f, indent=2)
    logger.info(f"Saved {len(features)} features to {GEOJSON_FILE}")

if __name__ == "__main__":
    main()
