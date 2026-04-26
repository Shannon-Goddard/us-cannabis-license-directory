"""
NV Facilities Builder
Written by Amazon Q for Loyal9 / poweredby.ci

Source: 3-tab Excel workbook saved as 3 CSVs by Shannon
  - active-license-list.csv
  - conditional-licenses.csv
  - surrendered-revoked-licenses.csv

Filters: Retail Dispensary + Medical Dispensary only
Skips:   fully empty rows (Excel padding)

Output:
  NV-facilities.csv        - All dispensary records (all statuses)
  NV-facilities-active.csv - Active only
"""

import csv
import os

BASE_DIR  = os.path.dirname(os.path.abspath(__file__))
CSV_DIR   = os.path.abspath(os.path.join(BASE_DIR, "..", "csv"))
STATE_DIR = os.path.abspath(os.path.join(BASE_DIR, ".."))

FILES = [
    "active-license-list.csv",
    "conditional-licenses.csv",
    "surrendered-revoked-licenses.csv",
]

DISPENSARY_TYPES = {"Retail Dispensary", "Medical Dispensary"}

HEADERS = [
    "License_Number", "CE_ID", "Business_Name",
    "License_Type", "License_Status", "County", "State", "Source_File",
]


def main():
    rows = []
    for fn in FILES:
        path = os.path.join(CSV_DIR, fn)
        with open(path, encoding="utf-8-sig") as f:
            for row in csv.DictReader(f):
                if not row["LicenseName"].strip():
                    continue  # skip empty Excel padding rows
                if row["LicenseType"].strip() not in DISPENSARY_TYPES:
                    continue
                rows.append({
                    "License_Number": row["LicenseNumber"].strip(),
                    "CE_ID":          row["CE ID"].strip(),
                    "Business_Name":  row["LicenseName"].strip(),
                    "License_Type":   row["LicenseType"].strip(),
                    "License_Status": row["LicenseStatus"].strip(),
                    "County":         row["County"].strip(),
                    "State":          "NV",
                    "Source_File":    fn,
                })

    active = [r for r in rows if r["License_Status"] == "Active"]

    for path, data in [
        (os.path.join(STATE_DIR, "NV-facilities.csv"), rows),
        (os.path.join(STATE_DIR, "NV-facilities-active.csv"), active),
    ]:
        with open(path, "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=HEADERS)
            w.writeheader()
            w.writerows(data)

    statuses = {}
    for r in rows:
        statuses[r["License_Status"]] = statuses.get(r["License_Status"], 0) + 1

    print(f"{len(rows)} total dispensary records -> NV-facilities.csv")
    print(f"{len(active)} active                  -> NV-facilities-active.csv")
    for s, c in sorted(statuses.items(), key=lambda x: -x[1]):
        print(f"  {c:3d}  {s}")


if __name__ == "__main__":
    main()
