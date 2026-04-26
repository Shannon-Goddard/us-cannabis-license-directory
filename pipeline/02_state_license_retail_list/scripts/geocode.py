"""
Geocoder — originally Pipeline 03, moved into Pipeline 02
Written by Amazon Q for Loyal9

1. Pulls records missing Latitude from master-facilities-active.csv
2. Geocodes via US Census Geocoder batch API (10k rows/batch, free, no key)
3. Falls back to Google Maps Geocoding API for failures and city/ZIP-only records
4. Writes lat/long back into both master-facilities.csv and master-facilities-active.csv

Dependencies: requests
Requires Google Maps API key for fallback geocoding.
"""

import csv
import io
import os
import time
import requests

BASE = os.path.dirname(os.path.abspath(__file__))
MASTER_ALL    = os.path.join(BASE, "../master-facilities.csv")
MASTER_ACTIVE = os.path.join(BASE, "../master-facilities-active.csv")

CENSUS_URL    = "https://geocoding.geo.census.gov/geocoder/locations/addressbatch"
GOOGLE_URL    = "https://maps.googleapis.com/maps/api/geocode/json"
GOOGLE_API_KEY = "<YOUR_GOOGLE_API_KEY>"
BATCH_SIZE    = 9999  # Census max is 10k rows including header

JUNK_STREET = {"not published", "not available", "data not available", "n/a", "none"}


def census_batch(records):
    """
    records: list of dicts with keys: id, street, city, state, zip
    Returns dict of {id: (lat, lon)} for matched results.
    """
    buf = io.StringIO()
    w = csv.writer(buf, quoting=csv.QUOTE_ALL)
    for r in records:
        w.writerow([r['id'], r['street'], r['city'], r['state'], r['zip']])
    payload = buf.getvalue().encode("utf-8")

    resp = requests.post(
        CENSUS_URL,
        files={"addressFile": ("batch.csv", io.BytesIO(payload), "text/csv")},
        data={"benchmark": "Public_AR_Current"},
        timeout=300,
    )
    resp.raise_for_status()

    results = {}
    for line in csv.reader(resp.text.strip().splitlines()):
        if len(line) < 6:
            continue
        uid, match, coords = line[0], line[2], line[5]
        if match.strip().upper() == "MATCH" and coords.strip():
            lon, lat = coords.strip().split(",")
            results[uid.strip()] = (lat.strip(), lon.strip())
    return results


def google_single(street, city, state, zip_code):
    """Google Maps Geocoding API fallback. Returns (lat, lon) or (None, None)."""
    parts = [p for p in [street, city, state, zip_code] if p and p.lower() not in JUNK_STREET]
    if not parts:
        return None, None
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
    return None, None


def load_csv(path):
    with open(path, encoding="utf-8") as f:
        return list(csv.DictReader(f)), csv.DictReader(open(path, encoding="utf-8")).fieldnames


def save_csv(path, rows, fieldnames):
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        w.writerows(rows)


def main():
    all_rows, headers = load_csv(MASTER_ALL)
    active_rows, _ = load_csv(MASTER_ACTIVE)

    missing = [
        (i, r) for i, r in enumerate(all_rows)
        if not r["Latitude"] and (r["Street"] or r["City"])
    ]
    print(f"Records to geocode: {len(missing)}")

    census_candidates = [
        (i, r) for i, r in missing
        if r["Street"] and r["Street"].lower().strip() not in JUNK_STREET
    ]
    print(f"  Census batch:   {len(census_candidates)}")

    geo_results = {}

    for batch_start in range(0, len(census_candidates), BATCH_SIZE):
        batch = census_candidates[batch_start:batch_start + BATCH_SIZE]
        batch_num = batch_start // BATCH_SIZE + 1
        total_batches = (len(census_candidates) - 1) // BATCH_SIZE + 1
        print(f"  Sending Census batch {batch_num}/{total_batches} ({len(batch)} rows)...", end=" ", flush=True)

        records = [
            {"id": str(i), "street": r["Street"], "city": r["City"],
             "state": r["State_Code"], "zip": r["ZIP"]}
            for i, r in batch
        ]
        try:
            matched = census_batch(records)
            for i, _ in batch:
                if str(i) in matched:
                    geo_results[i] = matched[str(i)]
            print(f"matched {len(matched)}/{len(batch)}")
        except Exception as e:
            print(f"ERROR: {e}")

    google_needed = [(i, r) for i, r in missing if i not in geo_results]
    print(f"  Google Maps fallback: {len(google_needed)}")

    for count, (i, r) in enumerate(google_needed, 1):
        lat, lon = google_single(r["Street"], r["City"], r["State_Code"], r["ZIP"])
        if lat:
            geo_results[i] = (lat, lon)
        if count % 500 == 0:
            print(f"    Google: {count}/{len(google_needed)} ({len(geo_results)} total matched)")
        time.sleep(0.05)

    print(f"\nTotal geocoded: {len(geo_results)} / {len(missing)}")

    for i, (lat, lon) in geo_results.items():
        all_rows[i]["Latitude"] = lat
        all_rows[i]["Longitude"] = lon

    updated_lookup = {}
    for r in all_rows:
        key = (r["Source_State"], r["License_Number"], r["Business_Name"])
        updated_lookup[key] = (r["Latitude"], r["Longitude"])

    for r in active_rows:
        key = (r["Source_State"], r["License_Number"], r["Business_Name"])
        if key in updated_lookup and not r["Latitude"]:
            r["Latitude"], r["Longitude"] = updated_lookup[key]

    save_csv(MASTER_ALL, all_rows, headers)
    save_csv(MASTER_ACTIVE, active_rows, headers)

    print("master-facilities.csv and master-facilities-active.csv updated.")


if __name__ == "__main__":
    main()
