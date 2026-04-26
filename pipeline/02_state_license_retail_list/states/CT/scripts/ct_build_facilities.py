"""
CT Facilities Builder
Written by Amazon Q for Loyal9 / poweredby.ci

Source: Connecticut.csv
  - CT Dept of Consumer Protection license export
  - 55 adult-use cannabis retailer records

Output: CT-facilities.csv
"""

import csv
import os
import re

BASE_DIR  = os.path.dirname(os.path.abspath(__file__))
CSV_DIR   = os.path.abspath(os.path.join(BASE_DIR, "..", "csv"))
STATE_DIR = os.path.abspath(os.path.join(BASE_DIR, ".."))

INPUT  = os.path.join(CSV_DIR, "Connecticut.csv")
OUTPUT = os.path.join(STATE_DIR, "CT-facilities.csv")

HEADERS = [
    "License_Number", "Business_Name", "DBA", "License_Type", "License_Status",
    "Street", "City", "State", "ZIP",
    "Effective_Date", "Expiration_Date", "Application_Type",
]

# "169 East St\nNew Haven, CT 06511"
ADDR_RE = re.compile(r'^(.+)\n(.+),\s+CT\s+(\d{5})', re.DOTALL)


def parse_license_address(raw):
    raw = raw.strip()
    m = ADDR_RE.match(raw)
    if m:
        return m.group(1).strip(), m.group(2).strip(), "CT", m.group(3).strip()
    return raw, "", "CT", ""


def main():
    rows = []
    with open(INPUT, encoding="utf-8-sig") as f:
        for row in csv.DictReader(f):
            if not row["Name"].strip():
                continue
            street, city, state, zip_code = parse_license_address(row["License Address"])
            rows.append({
                "License_Number":  row["Credential"].strip(),
                "Business_Name":   row["Name"].strip(),
                "DBA":             row["DBA"].strip(),
                "License_Type":    row["License Type"].strip(),
                "License_Status":  row["Status"].strip(),
                "Street":          street,
                "City":            city,
                "State":           state,
                "ZIP":             zip_code,
                "Effective_Date":  row["Effective Date"].strip(),
                "Expiration_Date": row["Expiration Date"].strip(),
                "Application_Type": row["Application Type"].strip(),
            })

    with open(OUTPUT, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=HEADERS)
        w.writeheader()
        w.writerows(rows)

    active = sum(1 for r in rows if r["License_Status"] == "ACTIVE")
    print(f"{len(rows)} total / {active} active -> CT-facilities.csv")


if __name__ == "__main__":
    main()
