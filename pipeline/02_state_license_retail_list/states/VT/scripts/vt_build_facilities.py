"""
VT Facilities Builder
Written by Amazon Q for Loyal9 / poweredby.ci

Source: licenses_4.15.csv
  - Vermont Cannabis Control Board (CCB) license export
  - 558 records across all license types

Filters: Retailer license type only
Output:  VT-facilities.csv
"""

import csv
import os

BASE_DIR  = os.path.dirname(os.path.abspath(__file__))
CSV_DIR   = os.path.abspath(os.path.join(BASE_DIR, "..", "csv"))
STATE_DIR = os.path.abspath(os.path.join(BASE_DIR, ".."))

INPUT  = os.path.join(CSV_DIR, "licenses_4.15.csv")
OUTPUT = os.path.join(STATE_DIR, "VT-facilities.csv")

HEADERS = [
    "License_Number", "Business_Name", "License_Type",
    "City", "State", "Expiration_Date",
]


def main():
    rows = []
    with open(INPUT, encoding="utf-8-sig") as f:
        for row in csv.DictReader(f):
            if row["License Type"].strip() != "Retailer":
                continue
            rows.append({
                "License_Number": row["License #"].strip(),
                "Business_Name":  row["Business Name"].strip(),
                "License_Type":   row["License Type"].strip(),
                "City":           row["City"].strip(),
                "State":          "VT",
                "Expiration_Date": row["Expiration Date"].strip(),
            })

    with open(OUTPUT, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=HEADERS)
        w.writeheader()
        w.writerows(rows)

    print(f"{len(rows)} retailers -> VT-facilities.csv")


if __name__ == "__main__":
    main()
