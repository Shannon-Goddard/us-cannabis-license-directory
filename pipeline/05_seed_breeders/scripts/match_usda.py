"""
Pipeline 05 — Breeder vs USDA Slug Match
Matches breeders-clean.csv slug against usda-verified.csv slug.
Exact match only.
Output: breeders_usda.csv
"""

import csv
import os

BASE     = os.path.dirname(os.path.abspath(__file__))
BREEDERS = os.path.join(BASE, "../output/breeders-clean.csv")
USDA     = os.path.join(BASE, "../input/usda-verified.csv")
OUTPUT   = os.path.join(BASE, "../output/breeders_usda.csv")

# Load breeders
with open(BREEDERS, newline="", encoding="utf-8") as f:
    breeders = list(csv.DictReader(f))

# Load USDA — build lookup by slug
with open(USDA, newline="", encoding="utf-8-sig", errors="replace") as f:
    usda_reader = csv.DictReader(f)
    usda_headers = usda_reader.fieldnames
    usda_rows = list(usda_reader)

slug_lookup = {}
for r in usda_rows:
    s = r.get("slug", "").strip()
    if s:
        if s not in slug_lookup:
            slug_lookup[s] = []
        slug_lookup[s].append(r)

print(f"Breeders: {len(breeders)}")
print(f"USDA rows: {len(usda_rows)}")
print(f"Unique USDA slugs: {len(slug_lookup)}")

OUTPUT_HEADERS = [
    "breeder_name", "breeder_slug", "breeder_url",
    "usda_name", "usda_slug", "usda_city", "usda_state",
    "usda_zip_code", "usda_lat", "usda_lng", "usda_license",
    "verified",
]

matches = []

for b in breeders:
    bslug = b.get("slug", "").strip()
    if not bslug:
        continue

    if bslug in slug_lookup:
        for ur in slug_lookup[bslug]:
            matches.append({
                "breeder_name": b["name"],
                "breeder_slug": bslug,
                "breeder_url": b.get("url", ""),
                "usda_name": ur.get("name", ""),
                "usda_slug": ur.get("slug", ""),
                "usda_city": ur.get("city", ""),
                "usda_state": ur.get("state", ""),
                "usda_zip_code": ur.get("zip_code", ""),
                "usda_lat": ur.get("lat", ""),
                "usda_lng": ur.get("lng", ""),
                "usda_license": ur.get("license_usda", ""),
                "verified": "",
            })

with open(OUTPUT, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=OUTPUT_HEADERS)
    writer.writeheader()
    writer.writerows(matches)

unique_breeders = len(set(m["breeder_slug"] for m in matches))

print(f"\nMatches: {len(matches)} total rows")
print(f"  Unique breeders matched: {unique_breeders}")
print(f"\nOutput: {OUTPUT}")
