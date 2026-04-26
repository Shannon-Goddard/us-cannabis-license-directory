"""
MI Facilities Builder
Written by Amazon Q for Loyal9 / poweredby.ci

Sources:
  RecordList20260418-adult-use.csv  - Marihuana Retailer + Microbusiness
  RecordList20260418-medical.csv    - Provisioning Center

Output:
  MI-facilities.csv        - All retail license types (all statuses)
  MI-facilities-active.csv - Active only
"""

import csv
import os
import re

BASE_DIR  = os.path.dirname(os.path.abspath(__file__))
CSV_DIR   = os.path.abspath(os.path.join(BASE_DIR, "..", "csv"))
STATE_DIR = os.path.abspath(os.path.join(BASE_DIR, ".."))

AU_FILE  = os.path.join(CSV_DIR, "RecordList20260418-adult-use.csv")
MED_FILE = os.path.join(CSV_DIR, "RecordList20260418-medical.csv")
OUT_ALL    = os.path.join(STATE_DIR, "MI-facilities.csv")
OUT_ACTIVE = os.path.join(STATE_DIR, "MI-facilities-active.csv")

AU_RETAIL_TYPES = {
    "Marihuana Retailer - License",
    "Marihuana Microbusiness - License",
    "Class A Marihuana Microbusiness - License",
}
MED_RETAIL_TYPES = {"Provisioning Center - License"}

HEADERS = [
    "License_Number", "Business_Name", "License_Type", "License_Status",
    "Street", "City", "State", "ZIP",
    "Expiration_Date", "Home_Delivery", "Disciplinary_Action", "Notes",
    "Source",
]

# "123 Main St, Anytown MI 49000"
ADDR_RE = re.compile(r'^(.+),\s+(.+?)\s+MI\s+(\d{5})', re.IGNORECASE)


def parse_address(raw):
    m = ADDR_RE.match(raw.strip())
    if m:
        return m.group(1).strip(), m.group(2).strip(), "MI", m.group(3).strip()
    return raw.strip(), "", "MI", ""


def load_file(path, name_field, retail_types, source_label, home_delivery=False):
    rows = []
    with open(path, encoding="utf-8-sig") as f:
        for row in csv.DictReader(f):
            if row["Record Type"].strip() not in retail_types:
                continue
            street, city, state, zip_code = parse_address(row.get("Address", ""))
            rows.append({
                "License_Number":    row["Record Number"].strip(),
                "Business_Name":     row[name_field].strip(),
                "License_Type":      row["Record Type"].strip(),
                "License_Status":    row["Status"].strip(),
                "Street":            street,
                "City":              city,
                "State":             state,
                "ZIP":               zip_code,
                "Expiration_Date":   row.get("Expiration Date", "").strip(),
                "Home_Delivery":     row.get("Home Delivery", "").strip() if home_delivery else "",
                "Disciplinary_Action": row.get("Disciplinary Action", "").strip(),
                "Notes":             row.get("Notes", "").strip(),
                "Source":            source_label,
            })
    return rows


def main():
    au  = load_file(AU_FILE,  "License Name",  AU_RETAIL_TYPES,  "adult-use")
    med = load_file(MED_FILE, "Licensee Name", MED_RETAIL_TYPES, "medical", home_delivery=True)

    rows   = au + med
    active = [r for r in rows if r["License_Status"] == "Active"]

    for path, data in [(OUT_ALL, rows), (OUT_ACTIVE, active)]:
        with open(path, "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=HEADERS)
            w.writeheader()
            w.writerows(data)

    au_active  = sum(1 for r in au  if r["License_Status"] == "Active")
    med_active = sum(1 for r in med if r["License_Status"] == "Active")

    print(f"{len(rows)} total retail records  -> MI-facilities.csv")
    print(f"{len(active)} active               -> MI-facilities-active.csv")
    print(f"  Adult-use active:  {au_active}")
    print(f"  Medical active:    {med_active}")


if __name__ == "__main__":
    main()
