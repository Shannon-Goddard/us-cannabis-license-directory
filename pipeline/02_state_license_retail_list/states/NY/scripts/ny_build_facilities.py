"""
NY Facilities Builder
Written by Amazon Q for Loyal9 / poweredby.ci

Source: Search Active Licenses result.csv
  - NY Office of Cannabis Management (OCM) full license export
  - 2,204 records across all license types

Filters: Retail-facing license types only
Output:
  NY-facilities.csv        - All retail licenses (all operational statuses)
  NY-facilities-active.csv - Operational Status = Active only
"""

import csv
import os

BASE_DIR  = os.path.dirname(os.path.abspath(__file__))
CSV_DIR   = os.path.abspath(os.path.join(BASE_DIR, "..", "csv"))
STATE_DIR = os.path.abspath(os.path.join(BASE_DIR, ".."))

INPUT      = os.path.join(CSV_DIR, "Search Active Licenses result.csv")
OUT_ALL    = os.path.join(STATE_DIR, "NY-facilities.csv")
OUT_ACTIVE = os.path.join(STATE_DIR, "NY-facilities-active.csv")

RETAIL_TYPES = {
    "Adult-Use Retail Dispensary License",
    "Adult-Use Conditional Retail Dispensary License",
    "Adult-Use Microbusiness License",
    "Adult-Use Registered Organization Dispensary License",
    "Registered Organization",
}

HEADERS = [
    "License_Number", "Application_Number", "Entity_Name", "DBA",
    "License_Type", "License_Status", "Operational_Status",
    "Address_1", "Address_2", "City", "State", "ZIP", "County", "Region",
    "Latitude", "Longitude",
    "Effective_Date", "Issued_Date", "Expiration_Date", "Date_Opened_to_Public",
    "Business_Website", "Hours",
    "Drive_Thru", "SEE_Category", "Business_Purpose",
]


def main():
    rows = []
    with open(INPUT, encoding="utf-8-sig") as f:
        for row in csv.DictReader(f):
            if row["License Type"].strip() not in RETAIL_TYPES:
                continue
            rows.append({
                "License_Number":         row["License Number"].strip(),
                "Application_Number":     row["Application Number"].strip(),
                "Entity_Name":            row["Entity Name"].strip(),
                "DBA":                    row["DBA"].strip(),
                "License_Type":           row["License Type"].strip(),
                "License_Status":         row["License Status"].strip(),
                "Operational_Status":     row["Operational Status"].strip(),
                "Address_1":              row["Address Line 1"].strip(),
                "Address_2":              row["Address Line 2"].strip(),
                "City":                   row["City"].strip(),
                "State":                  row["State"].strip(),
                "ZIP":                    row["Zip"].strip(),
                "County":                 row["County"].strip(),
                "Region":                 row["Region"].strip(),
                "Latitude":               row["Latitude"].strip(),
                "Longitude":              row["Longitude"].strip(),
                "Effective_Date":         row["Effective Date"].strip(),
                "Issued_Date":            row["Issued Date"].strip(),
                "Expiration_Date":        row["Expiration Date"].strip(),
                "Date_Opened_to_Public":  row["Retail Date Opened to Public"].strip(),
                "Business_Website":       row["Business Website"].strip(),
                "Hours":                  row["Misc2"].strip(),
                "Drive_Thru":             row["Retail Activities Drive Thru"].strip(),
                "SEE_Category":           row["SEE Category"].strip(),
                "Business_Purpose":       row["Business Purpose"].strip(),
            })

    active = [r for r in rows if r["Operational_Status"] == "Active"]

    for path, data in [(OUT_ALL, rows), (OUT_ACTIVE, active)]:
        with open(path, "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=HEADERS)
            w.writeheader()
            w.writerows(data)

    types = {}
    for r in rows:
        types[r["License_Type"]] = types.get(r["License_Type"], 0) + 1

    print(f"{len(rows)} total retail records  -> NY-facilities.csv")
    print(f"{len(active)} active               -> NY-facilities-active.csv")
    for t, c in sorted(types.items(), key=lambda x: -x[1]):
        print(f"  {c:4d}  {t}")


if __name__ == "__main__":
    main()
