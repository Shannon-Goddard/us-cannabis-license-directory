"""
Pipeline 05 — Breeder vs State Slug Match (re-run with updated master)
Matches breeders-master.csv slug against state-verified.csv slug and dba_slug.
Exact match only.
Output: breeders_states.csv
"""

import csv
import re
import os

BASE     = os.path.dirname(os.path.abspath(__file__))
BREEDERS = os.path.join(BASE, "../breeders-master.csv")
STATE    = os.path.join(BASE, "../../04_human_in_the_loop/output/state-verified.csv")
OUTPUT   = os.path.join(BASE, "../output/breeders_states.csv")


def slugify(name):
    if not name or not name.strip():
        return ""
    name = name.lower().strip()
    if name.startswith("the "):
        name = name[4:]
    name = re.sub(r"[^\w\s-]", "", name)
    name = re.sub(r"[\s_]+", "-", name)
    return name.strip("-")


# Load breeders
with open(BREEDERS, newline="", encoding="utf-8-sig", errors="replace") as f:
    breeders = list(csv.DictReader(f))

# Rebuild slugs to be safe
for b in breeders:
    b["slug"] = slugify(b.get("name", ""))

# Load state
with open(STATE, newline="", encoding="utf-8-sig", errors="replace") as f:
    state_rows = list(csv.DictReader(f))

slug_lookup = {}
dba_slug_lookup = {}

for r in state_rows:
    s = r.get("slug", "").strip()
    ds = r.get("dba_slug", "").strip()
    if s:
        if s not in slug_lookup:
            slug_lookup[s] = []
        slug_lookup[s].append(r)
    if ds:
        if ds not in dba_slug_lookup:
            dba_slug_lookup[ds] = []
        dba_slug_lookup[ds].append(r)

print(f"Breeders: {len(breeders)}")
print(f"State rows: {len(state_rows)}")
print(f"Unique state slugs: {len(slug_lookup)}")
print(f"Unique state dba_slugs: {len(dba_slug_lookup)}")

OUTPUT_HEADERS = [
    "breeder_name", "breeder_slug", "breeder_url",
    "match_type",
    "state_name", "state_dba", "state_slug", "state_dba_slug",
    "state_type", "state_street_address", "state_city", "state_state",
    "state_zip_code", "state_phone", "state_email", "state_url",
    "state_license", "state_lat", "state_lng",
    "verified",
]

matches = []

for b in breeders:
    bslug = b.get("slug", "").strip()
    if not bslug:
        continue

    if bslug in slug_lookup:
        for sr in slug_lookup[bslug]:
            matches.append({
                "breeder_name": b["name"],
                "breeder_slug": bslug,
                "breeder_url": b.get("url", ""),
                "match_type": "slug",
                "state_name": sr.get("name", ""),
                "state_dba": sr.get("dba", ""),
                "state_slug": sr.get("slug", ""),
                "state_dba_slug": sr.get("dba_slug", ""),
                "state_type": sr.get("type", ""),
                "state_street_address": sr.get("street_address", ""),
                "state_city": sr.get("city", ""),
                "state_state": sr.get("state", ""),
                "state_zip_code": sr.get("zip_code", ""),
                "state_phone": sr.get("phone", ""),
                "state_email": sr.get("email", ""),
                "state_url": sr.get("url", ""),
                "state_license": sr.get("license_state", ""),
                "state_lat": sr.get("lat", ""),
                "state_lng": sr.get("lng", ""),
                "verified": "",
            })

    if bslug in dba_slug_lookup and bslug not in slug_lookup:
        for sr in dba_slug_lookup[bslug]:
            matches.append({
                "breeder_name": b["name"],
                "breeder_slug": bslug,
                "breeder_url": b.get("url", ""),
                "match_type": "dba_slug",
                "state_name": sr.get("name", ""),
                "state_dba": sr.get("dba", ""),
                "state_slug": sr.get("slug", ""),
                "state_dba_slug": sr.get("dba_slug", ""),
                "state_type": sr.get("type", ""),
                "state_street_address": sr.get("street_address", ""),
                "state_city": sr.get("city", ""),
                "state_state": sr.get("state", ""),
                "state_zip_code": sr.get("zip_code", ""),
                "state_phone": sr.get("phone", ""),
                "state_email": sr.get("email", ""),
                "state_url": sr.get("url", ""),
                "state_license": sr.get("license_state", ""),
                "state_lat": sr.get("lat", ""),
                "state_lng": sr.get("lng", ""),
                "verified": "",
            })

with open(OUTPUT, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=OUTPUT_HEADERS)
    writer.writeheader()
    writer.writerows(matches)

unique_breeders = len(set(m["breeder_slug"] for m in matches))
slug_matches = sum(1 for m in matches if m["match_type"] == "slug")
dba_matches = sum(1 for m in matches if m["match_type"] == "dba_slug")

print(f"\nMatches: {len(matches)} total rows")
print(f"  Unique breeders matched: {unique_breeders}")
print(f"  Via slug: {slug_matches}")
print(f"  Via dba_slug: {dba_matches}")
print(f"\nOutput: {OUTPUT}")
