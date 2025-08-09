import csv
from collections import Counter

CSV_FILE = "public/data/Parking_Permit_Zones_20250802.csv"

def load_parking_zones(csv_file=CSV_FILE):
    """Load all rows from the parking zones CSV as a list of dicts."""
    rows = []
    with open(csv_file, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(row)
    return rows

def get_unique_street_segments(rows):
    """
    Return a list of unique (direction, name, type) tuples for ACTIVE segments.
    """
    seen = set()
    unique_segments = []
    for row in rows:
        if row["STATUS"] != "ACTIVE":
            continue
        seg = (row["STREET DIRECTION"], row["STREET NAME"], row["STREET TYPE"])
        if seg not in seen:
            seen.add(seg)
            unique_segments.append(row)
    return unique_segments

if __name__ == "__main__":
    rows = load_parking_zones()
    zones = set()
    streets = set()
    zone_counter = Counter()
    street_counter = Counter()
    for row in rows:
        zones.add(row["ZONE"])
        streets.add(f"{row['STREET DIRECTION']} {row['STREET NAME']} {row['STREET TYPE']}".strip())
        zone_counter[row["ZONE"]] += 1
        street_counter[row["STREET NAME"]] += 1

    print(f"Total rows: {len(rows)}")
    print(f"Unique zones: {len(zones)}")
    print(f"Unique street segments: {len(streets)}")
    print("\nSample rows:")
    for r in rows[:10]:
        print(r)

    print("\nMost common zones:")
    for zone, count in zone_counter.most_common(10):
        print(f"Zone {zone}: {count} segments")

    print("\nMost common street names:")
    for street, count in street_counter.most_common(10):
        print(f"{street}: {count} segments")
