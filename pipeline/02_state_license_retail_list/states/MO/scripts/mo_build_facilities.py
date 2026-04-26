"""
MO Facilities Builder
Written by Amazon Q for Loyal9 / poweredby.ci

Source: dispensary_map_arcgis_current.csv
  - ArcGIS map data export from Missouri DHSS dispensary map
  - Already clean: name, license, full address, county, GPS, phone, last updated

Output: MO-facilities.csv
"""

import csv
import os

BASE_DIR  = os.path.dirname(os.path.abspath(__file__))
CSV_DIR   = os.path.abspath(os.path.join(BASE_DIR, "..", "csv"))
STATE_DIR = os.path.abspath(os.path.join(BASE_DIR, ".."))

INPUT  = os.path.join(CSV_DIR, "dispensary_map_arcgis_current.csv")
OUTPUT = os.path.join(STATE_DIR, "MO-facilities.csv")

HEADERS = [
    "Business_Name", "License_Number", "Street", "City", "State", "ZIP",
    "County", "Phone", "Latitude", "Longitude", "Last_Updated",
]


def main():
    rows = []
    with open(INPUT, encoding="utf-8-sig") as f:
        for row in csv.DictReader(f):
            rows.append({
                "Business_Name":  row["Dispensary"].strip(),
                "License_Number": row["License"].strip(),
                "Street":         row["Address"].strip(),
                "City":           row["City"].strip(),
                "State":          "MO",
                "ZIP":            row["Zip code"].strip(),
                "County":         row["County"].strip(),
                "Phone":          row["Phone Number"].strip(),
                "Latitude":       row["latitude"].strip(),
                "Longitude":      row["longitude"].strip(),
                "Last_Updated":   row["Last updated"].strip(),
            })

    with open(OUTPUT, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=HEADERS)
        w.writeheader()
        w.writerows(rows)

    print(f"{len(rows)} dispensaries -> MO-facilities.csv")


if __name__ == "__main__":
    main()
