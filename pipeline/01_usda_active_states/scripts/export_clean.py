"""
Pipeline 01 — USDA Clean Export
Filters USDA_geocoded.csv to Active + Active on CAP only.
Maps to plan-a schema. Drops Regulatory Body and Status.
Output: csv/usda-clean.csv
"""

import csv
import re
import os

BASE   = os.path.dirname(os.path.abspath(__file__))
INPUT  = os.path.join(BASE, "../csv/USDA_geocoded.csv")
OUTPUT = os.path.join(BASE, "../csv/usda-clean.csv")

ACTIVE_STATUSES = {"active", "active on cap"}

STATE_TO_CODE = {
    "alabama": "AL", "alaska": "AK", "arizona": "AZ", "arkansas": "AR",
    "california": "CA", "colorado": "CO", "connecticut": "CT", "delaware": "DE",
    "florida": "FL", "georgia": "GA", "hawaii": "HI", "idaho": "ID",
    "illinois": "IL", "indiana": "IN", "iowa": "IA", "kansas": "KS",
    "kentucky": "KY", "louisiana": "LA", "maine": "ME", "maryland": "MD",
    "massachusetts": "MA", "michigan": "MI", "minnesota": "MN", "mississippi": "MS",
    "missouri": "MO", "montana": "MT", "nebraska": "NE", "nevada": "NV",
    "new hampshire": "NH", "new jersey": "NJ", "new mexico": "NM", "new york": "NY",
    "north carolina": "NC", "north dakota": "ND", "ohio": "OH", "oklahoma": "OK",
    "oregon": "OR", "pennsylvania": "PA", "puerto rico": "PR", "rhode island": "RI",
    "south carolina": "SC", "south dakota": "SD", "tennessee": "TN", "texas": "TX",
    "utah": "UT", "vermont": "VT", "virginia": "VA", "washington": "WA",
    "west virginia": "WV", "wisconsin": "WI", "wyoming": "WY",
    "district of columbia": "DC", "guam": "GU", "u.s. virgin islands": "VI",
    "american samoa": "AS", "northern mariana islands": "MP",
}

SCHEMA_HEADERS = [
    "name",
    "dba",
    "slug",
    "type",
    "url",
    "is_bad_url",
    "city",
    "state",
    "zip_code",
    "country",
    "lat",
    "lng",
    "phone",
    "email",
    "license_usda",
]


def slugify(name: str) -> str:
    name = name.lower().strip()
    if name.startswith("the "):
        name = name[4:]
    name = re.sub(r"[^\w\s-]", "", name)
    name = re.sub(r"[\s_]+", "-", name)
    return name.strip("-")


def main():
    with open(INPUT, newline="", encoding="utf-8-sig") as f:
        rows = list(csv.DictReader(f))

    print(f"Loaded: {len(rows)} total USDA records")

    active = [r for r in rows if r["Status"].strip().lower() in ACTIVE_STATUSES]
    print(f"Active: {len(active)}")

    output = []
    for r in active:
        state_full = r["State"].strip()
        state_code = STATE_TO_CODE.get(state_full.lower(), state_full)

        output.append({
            "name":         r["Business or License Holder Name"].strip(),
            "dba":          "",
            "slug":         slugify(r["Business or License Holder Name"]),
            "type":         "cultivator",
            "url":          "",
            "is_bad_url":   "",
            "city":         r["City"].strip(),
            "state":        state_code,
            "zip_code":     r["Zip Code"].strip(),
            "country":      "US",
            "lat":          r["Latitude"].strip(),
            "lng":          r["Longitude"].strip(),
            "phone":        "",
            "email":        "",
            "license_usda": r["License Number"].strip(),
        })

    with open(OUTPUT, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=SCHEMA_HEADERS)
        writer.writeheader()
        writer.writerows(output)

    # Summary
    has_lat = sum(1 for r in output if r["lat"])
    states = len(set(r["state"] for r in output))
    print(f"\nOutput: {OUTPUT}")
    print(f"  Rows:       {len(output)}")
    print(f"  States:     {states}")
    print(f"  Geocoded:   {has_lat}")


if __name__ == "__main__":
    main()
