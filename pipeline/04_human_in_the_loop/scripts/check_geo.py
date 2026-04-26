"""
Double-check geo for rows with missing/bad zip codes.
Finds rows where double-check-geo = 'X', then verifies the lat/lng
is in the correct state by checking if the coordinates are reasonable
for the listed city/state.

Uses Google Maps reverse geocoding to verify.
"""

import csv
import os
import time
import requests

VERIFIED = r"c:\Users\uthin\Desktop\NEW-SEEDS-LAW\pipeline\04_human_in_the_loop\output\usda-verified.csv"
GOOGLE_URL = "https://maps.googleapis.com/maps/api/geocode/json"
GOOGLE_API_KEY = "<YOUR_GOOGLE_API_KEY>"

# Load
with open(VERIFIED, newline="", encoding="utf-8-sig", errors="replace") as f:
    reader = csv.DictReader(f)
    fieldnames = reader.fieldnames
    rows = list(reader)

# Find the flag column
flag_col = None
for h in fieldnames:
    if "double" in h.lower() or "check" in h.lower():
        flag_col = h
        break

if not flag_col:
    print("Could not find double-check-geo column")
    print(f"Headers: {fieldnames}")
    exit(1)

flagged = [(i, r) for i, r in enumerate(rows) if r.get(flag_col, "").strip().upper() == "X"]
print(f"Flagged rows: {len(flagged)}")
print(f"Flag column: '{flag_col}'")

# For each flagged row, re-geocode using just city + state (no zip)
# Compare new lat/lng against existing lat/lng
# If they're far apart (>50km), flag as bad

import math

def haversine(lat1, lon1, lat2, lon2):
    """Distance in km between two lat/lng points."""
    R = 6371
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat/2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon/2)**2
    return R * 2 * math.asin(math.sqrt(a))


def geocode_city_state(city, state):
    """Geocode using just city + state. Returns (lat, lng) or (None, None)."""
    parts = [p for p in [city, state] if p.strip()]
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
            return loc["lat"], loc["lng"]
    except Exception:
        pass
    return None, None


bad = []
ok = []
no_coords = []

for idx, row in flagged:
    name  = row.get("name", "")
    city  = row.get("city", "").strip()
    state = row.get("state", "").strip()
    lat   = row.get("lat", "").strip()
    lng   = row.get("lng", "").strip()

    if not lat or not lng:
        no_coords.append((idx, name, city, state))
        continue

    old_lat = float(lat)
    old_lng = float(lng)

    new_lat, new_lng = geocode_city_state(city, state)
    time.sleep(0.05)

    if new_lat is None:
        no_coords.append((idx, name, city, state))
        continue

    dist = haversine(old_lat, old_lng, new_lat, new_lng)

    if dist > 50:
        bad.append((idx, name, city, state, dist, old_lat, old_lng, new_lat, new_lng))
        # Update to correct coordinates
        rows[idx]["lat"] = str(new_lat)
        rows[idx]["lng"] = str(new_lng)
    else:
        ok.append((idx, name, city, state, dist))

print(f"\nResults:")
print(f"  OK (within 50km): {len(ok)}")
print(f"  BAD (>50km off, corrected): {len(bad)}")
print(f"  No coordinates: {len(no_coords)}")

if bad:
    print(f"\n=== Corrected rows ===")
    for idx, name, city, state, dist, olat, olng, nlat, nlng in bad:
        print(f"  {name} ({city}, {state}): was {olat},{olng} -> now {nlat},{nlng} ({dist:.0f}km off)")

if no_coords:
    print(f"\n=== No coordinates ===")
    for idx, name, city, state in no_coords:
        print(f"  {name} ({city}, {state})")

# Write back
with open(VERIFIED, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)

print(f"\nUpdated: {VERIFIED}")
