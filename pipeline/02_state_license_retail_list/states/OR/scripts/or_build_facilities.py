"""
OR Facilities Builder
Written by Amazon Q for Loyal9 / poweredby.ci

Source: Cannabis Business Licenses & Endorsements.csv
  - Oregon Liquor and Cannabis Commission (OLCC)
  - UTF-16 encoded, tab-delimited inside a .csv wrapper
  - 3,526 records across all license types

Filters: RECREATIONAL RETAILER, ACTIVE status only for active CSV
Output:
  OR-facilities.csv        - All recreational retailers (all statuses)
  OR-facilities-active.csv - Active only
"""

import csv
import os
import re

BASE_DIR  = os.path.dirname(os.path.abspath(__file__))
CSV_DIR   = os.path.abspath(os.path.join(BASE_DIR, "..", "csv"))
STATE_DIR = os.path.abspath(os.path.join(BASE_DIR, ".."))

INPUT      = os.path.join(CSV_DIR, "Cannabis Business Licenses & Endorsements.csv")
OUT_ALL    = os.path.join(STATE_DIR, "OR-facilities.csv")
OUT_ACTIVE = os.path.join(STATE_DIR, "OR-facilities-active.csv")

RETAIL_TYPES = {"RECREATIONAL RETAILER"}

HEADERS = [
    "License_Number", "Business_Name", "Legal_Name",
    "License_Type", "Status", "Expiration_Date",
    "Street", "City", "State", "ZIP",
    "County", "Endorsement", "SOS_Registration_Number",
]

# "3005 SW MULTNOMAH BLVD PORTLAND OR  97219-3701"
ADDR_RE = re.compile(r'^(.+?)\s+([A-Z\s]+?)\s+OR\s+(\d{5}(?:-\d{4})?)\s*$')


def parse_address(raw):
    raw = raw.strip()
    m = ADDR_RE.match(raw)
    if m:
        return m.group(1).strip(), m.group(2).strip().title(), "OR", m.group(3).strip()
    return raw, "", "OR", ""


def main():
    raw_rows = []
    with open(INPUT, encoding="utf-16") as f:
        for line in csv.reader(f):
            if line:
                raw_rows.append(line[0].split('\t'))

    headers = raw_rows[0]
    data = [dict(zip(headers, r + [''] * (len(headers) - len(r)))) for r in raw_rows[1:] if len(r) > 1]

    rows = []
    for r in data:
        if r.get("License Type", "").strip() not in RETAIL_TYPES:
            continue
        if not r.get("Business Name", "").strip():
            continue
        street, city, state, zip_code = parse_address(r.get("PhysicalAddress", ""))
        rows.append({
            "License_Number":        r["License Number"].strip(),
            "Business_Name":         r["Business Name"].strip(),
            "Legal_Name":            r["Business Licenses"].strip(),
            "License_Type":          r["License Type"].strip(),
            "Status":                r["Status"].strip(),
            "Expiration_Date":       r["Expiration Date"].strip(),
            "Street":                street,
            "City":                  city,
            "State":                 state,
            "ZIP":                   zip_code,
            "County":                r["County"].strip(),
            "Endorsement":           r["Endorsement"].strip(),
            "SOS_Registration_Number": r["SOS Registration Number"].strip(),
        })

    active = [r for r in rows if r["Status"] == "ACTIVE"]

    for path, data in [(OUT_ALL, rows), (OUT_ACTIVE, active)]:
        with open(path, "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=HEADERS)
            w.writeheader()
            w.writerows(data)

    delivery = sum(1 for r in active if "Delivery" in r["Endorsement"])
    print(f"{len(rows)} total retailers  -> OR-facilities.csv")
    print(f"{len(active)} active           -> OR-facilities-active.csv")
    print(f"  Home delivery endorsed: {delivery}")


if __name__ == "__main__":
    main()
