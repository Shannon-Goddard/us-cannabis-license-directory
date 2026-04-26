"""
USDA Geocoder — Stage 01 enrichment
Written by Amazon Q for Loyal9

Adds Latitude + Longitude to USDA_search_tool.csv using Google Maps API.
Input:  pipeline/01_usda_active_states/csv/USDA_search_tool.csv
Output: pipeline/01_usda_active_states/csv/USDA_geocoded.csv
"""

import csv
import os
import time
import requests

GOOGLE_API_KEY = "<YOUR_GOOGLE_API_KEY>"
GOOGLE_URL     = "https://maps.googleapis.com/maps/api/geocode/json"

BASE   = os.path.dirname(os.path.abspath(__file__))
INPUT  = os.path.join(BASE, "../csv/USDA_search_tool.csv")
OUTPUT = os.path.join(BASE, "../csv/USDA_geocoded.csv")


def geocode(city, state, zip_code):
    parts = [p for p in [city, state, zip_code] if p.strip()]
    if not parts:
        return "", ""
    try:
        resp = requests.get(
            GOOGLE_URL,
            params={"address": ", ".join(parts), "key": GOOGLE_API_KEY},
            timeout=10,
        )
        data = resp.json()
        if data["status"] == "OK":
            loc = data["results"][0]["geometry"]["location"]
            return str(loc["lat"]), str(loc["lng"])
    except Exception:
        pass
    return "", ""


def main():
    rows = list(csv.DictReader(open(INPUT, encoding="utf-8-sig")))
    print(f"Loaded {len(rows)} USDA records")

    # Cache by (city, state, zip) — many records share the same location
    cache = {}
    matched = 0

    for i, row in enumerate(rows, 1):
        key = (row["City"].strip(), row["State"].strip(), row["Zip Code"].strip())
        if key not in cache:
            lat, lon = geocode(*key)
            cache[key] = (lat, lon)
            time.sleep(0.05)  # 20 req/sec
        row["Latitude"], row["Longitude"] = cache[key]
        if row["Latitude"]:
            matched += 1
        if i % 1000 == 0:
            print(f"  {i}/{len(rows)} processed — {matched} geocoded — {len(cache)} unique locations")

    fieldnames = list(rows[0].keys())
    with open(OUTPUT, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        w.writerows(rows)

    print(f"\n{matched}/{len(rows)} geocoded")
    print(f"{len(cache)} unique city/ZIP combinations hit the API")
    print(f"Output -> {OUTPUT}")


if __name__ == "__main__":
    main()
