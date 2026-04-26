"""
Pipeline 02 — State License Clean Export
Maps master-facilities-active.csv to plan-a schema.
Classifies License_Type into: dispensary, cultivator, academic, other.
Keeps both Business_Name (as name) and Legal_Name (as dba).
Output: state-clean.csv
"""

import csv
import re
import os

BASE   = os.path.dirname(os.path.abspath(__file__))
INPUT  = os.path.join(BASE, "../master-facilities-active.csv")
OUTPUT = os.path.join(BASE, "../state-clean.csv")

SCHEMA_HEADERS = [
    "name",
    "dba",
    "slug",
    "type",
    "url",
    "is_bad_url",
    "street_address",
    "city",
    "state",
    "zip_code",
    "country",
    "lat",
    "lng",
    "phone",
    "email",
    "license_state",
]

# Type classification keywords
DISPENSARY_KW = [
    "retail", "store", "dispensary", "dispensing", "retailer",
]
CULTIVATOR_KW = [
    "cultiv", "grow", "nursery", "outdoor", "indoor", "mixed-light",
    "small outdoor", "medium outdoor", "small indoor", "specialty",
]
ACADEMIC_KW = [
    "university", "research", "academic", "college",
]


def classify_type(license_type: str) -> str:
    lt = license_type.lower()
    types = set()

    for kw in DISPENSARY_KW:
        if kw in lt:
            types.add("dispensary")
            break
    for kw in CULTIVATOR_KW:
        if kw in lt:
            types.add("cultivator")
            break
    for kw in ACADEMIC_KW:
        if kw in lt:
            types.add("academic")
            break

    if not types:
        types.add("other")

    return "|".join(sorted(types))


def slugify(name: str) -> str:
    name = name.lower().strip()
    if name.startswith("the "):
        name = name[4:]
    name = re.sub(r"[^\w\s-]", "", name)
    name = re.sub(r"[\s_]+", "-", name)
    return name.strip("-")


def main():
    with open(INPUT, newline="", encoding="utf-8-sig", errors="replace") as f:
        rows = list(csv.DictReader(f))

    print(f"Loaded: {len(rows)} active state records")

    output = []
    type_counts = {}

    for r in rows:
        biz_name   = r["Business_Name"].strip()
        legal_name = r.get("Legal_Name", "").strip()
        license_type = r.get("License_Type", "").strip()

        entity_type = classify_type(license_type)
        type_counts[entity_type] = type_counts.get(entity_type, 0) + 1

        dba = legal_name if legal_name and legal_name.lower() != biz_name.lower() else ""

        # State code fallback if bad
        state = r.get("State_Code", "").strip()
        if len(state) != 2:
            state = r.get("Source_State", "").strip()

        output.append({
            "name":           biz_name,
            "dba":            dba,
            "slug":           slugify(biz_name),
            "type":           entity_type,
            "url":            r.get("Website", "").strip(),
            "is_bad_url":     "",
            "street_address": r.get("Street", "").strip(),
            "city":           r.get("City", "").strip(),
            "state":          state,
            "zip_code":       r.get("ZIP", "").strip(),
            "country":        "US",
            "lat":            r.get("Latitude", "").strip(),
            "lng":            r.get("Longitude", "").strip(),
            "phone":          r.get("Phone", "").strip(),
            "email":          r.get("Email", "").strip(),
            "license_state":  r.get("License_Number", "").strip(),
        })

    with open(OUTPUT, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=SCHEMA_HEADERS)
        writer.writeheader()
        writer.writerows(output)

    has_addr  = sum(1 for r in output if r["street_address"])
    has_phone = sum(1 for r in output if r["phone"])
    has_email = sum(1 for r in output if r["email"])
    has_url   = sum(1 for r in output if r["url"])
    has_lat   = sum(1 for r in output if r["lat"])
    has_dba   = sum(1 for r in output if r["dba"])
    states    = len(set(r["state"] for r in output))

    print(f"\nOutput: {OUTPUT}")
    print(f"  Rows:       {len(output)}")
    print(f"  States:     {states}")
    print(f"  Has address: {has_addr}")
    print(f"  Has phone:   {has_phone}")
    print(f"  Has email:   {has_email}")
    print(f"  Has website: {has_url}")
    print(f"  Has lat/lng: {has_lat}")
    print(f"  Has DBA:     {has_dba}")
    print(f"\nType breakdown:")
    for t, c in sorted(type_counts.items(), key=lambda x: -x[1]):
        print(f"  {t}: {c}")


if __name__ == "__main__":
    main()
