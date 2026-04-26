"""
Pipeline 05 — Seed Breeders Export
Merges seedfinder-names.csv (2,059 names) with seedfinder-verified.csv (487 with homepage URLs).
Outputs to full schema with slugs.
"""

import csv
import re
import os

BASE     = os.path.dirname(os.path.abspath(__file__))
NAMES    = os.path.join(BASE, "../input/seedfinder-names.csv")
VERIFIED = os.path.join(BASE, "../input/seedfinder-verified.csv")
OUTPUT   = os.path.join(BASE, "../output/breeders-clean.csv")

SCHEMA_HEADERS = [
    "name", "dba", "slug", "dba_slug", "type",
    "is_breeder", "is_bank", "is_cultivator", "is_dispensary", "is_academic",
    "url", "is_bad_url", "reason_code",
    "street_address", "city", "state", "zip_code", "country",
    "lat", "lng", "phone", "email",
    "license_usda", "license_state", "license_other",
    "is_licensed", "schema_complete",
    "last_verified", "verified_by", "submitted_at", "submitted_by",
    "evidence_url",
]


def slugify(name: str) -> str:
    if not name or not name.strip():
        return ""
    name = name.lower().strip()
    if name.startswith("the "):
        name = name[4:]
    name = re.sub(r"[^\w\s-]", "", name)
    name = re.sub(r"[\s_]+", "-", name)
    return name.strip("-")


# Load verified homepage lookup
homepage_lookup = {}
with open(VERIFIED, newline="", encoding="utf-8-sig", errors="replace") as f:
    for row in csv.DictReader(f):
        key = row["name"].strip().lower()
        homepage_lookup[key] = row["homepage"].strip()

# Load all names
with open(NAMES, newline="", encoding="utf-8-sig", errors="replace") as f:
    names = list(csv.DictReader(f))

print(f"Names: {len(names)}")
print(f"Verified homepages: {len(homepage_lookup)}")

# Build output
output = []
has_url = 0

for row in names:
    name = row["name"].strip()
    key = name.lower()
    homepage = homepage_lookup.get(key, "")

    if homepage:
        has_url += 1

    rec = {h: "" for h in SCHEMA_HEADERS}
    rec["name"] = name
    rec["slug"] = slugify(name)
    rec["url"] = homepage
    rec["is_bad_url"] = "false" if homepage else ""

    output.append(rec)

with open(OUTPUT, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=SCHEMA_HEADERS)
    writer.writeheader()
    writer.writerows(output)

print(f"\nOutput: {OUTPUT}")
print(f"  Rows: {len(output)}")
print(f"  Has URL: {has_url}")
print(f"  No URL: {len(output) - has_url}")
