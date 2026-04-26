"""
MA Facilities Builder
Written by Amazon Q for Loyal9 / poweredby.ci

Sources:
  comm-ops.csv       - Primary: email, phone, GPS, active status, dates
  hmwt-yiqy.csv      - Enrichment: expiration, suspension, revocation dates

Output:
  MA-facilities.csv        - All retailers (Active + Expired + Surrendered)
  MA-facilities-active.csv - Active only
"""

import csv
import os

BASE_DIR  = os.path.dirname(os.path.abspath(__file__))
CSV_DIR   = os.path.abspath(os.path.join(BASE_DIR, "..", "csv"))
STATE_DIR = os.path.abspath(os.path.join(BASE_DIR, ".."))

COMM_OPS  = os.path.join(CSV_DIR, "comm-ops.csv")
HMWT      = os.path.join(CSV_DIR, "hmwt-yiqy.csv")
OUT_ALL    = os.path.join(STATE_DIR, "MA-facilities.csv")
OUT_ACTIVE = os.path.join(STATE_DIR, "MA-facilities-active.csv")

RETAIL_TYPES = {"Marijuana Retailer", "Medical Marijuana Retailer"}

HEADERS = [
    "Business_Name", "License_Number", "License_Type", "License_Status",
    "Establishment_Address_1", "Establishment_Address_2",
    "Establishment_City", "Establishment_State", "Establishment_ZIP",
    "Business_Email", "Business_Phone",
    "County", "Latitude", "Longitude",
    "Lic_Start_Date", "Lic_Expiration_Date", "Commence_Operations_Date",
    "Suspension_Start_Date", "Suspension_End_Date",
    "Revocation_Date", "Surrendered_Date",
    "Priority_Status", "EIN_TIN",
]


def load_hmwt(path):
    """Build lookup dict from hmwt-yiqy.csv keyed on LICENSE_NUMBER."""
    lookup = {}
    with open(path, encoding="utf-8") as f:
        for row in csv.DictReader(f):
            ln = row.get("LICENSE_NUMBER", "").strip()
            if ln:
                lookup[ln] = row
    return lookup


def main():
    hmwt = load_hmwt(HMWT)

    rows = []
    with open(COMM_OPS, encoding="utf-8-sig") as f:
        for row in csv.DictReader(f):
            if row["LICENSE_TYPE"].strip() not in RETAIL_TYPES:
                continue

            ln = row["LICENSE_NUMBER"].strip()
            h  = hmwt.get(ln, {})

            rows.append({
                "Business_Name":           row["BUSINESS_NAME"].strip(),
                "License_Number":          ln,
                "License_Type":            row["LICENSE_TYPE"].strip(),
                "License_Status":          row["LIC_STATUS"].strip(),
                "Establishment_Address_1": row["ESTABLISHMENT_ADDRESS_1"].strip(),
                "Establishment_Address_2": row["ESTABLISHMENT_ADDRESS_2"].strip(),
                "Establishment_City":      row["ESTABLISHMENT_CITY"].strip(),
                "Establishment_State":     row["ESTABLISHMENT_STATE"].strip(),
                "Establishment_ZIP":       row["ESTABLISHMENT_ZIP_CODE"].strip(),
                "Business_Email":          row["BUSINESS_EMAIL"].strip(),
                "Business_Phone":          row["BUSINESS_PHONE"].strip(),
                "County":                  row["county"].strip(),
                "Latitude":                row["latitude"].strip(),
                "Longitude":               row["longitude"].strip(),
                "Lic_Start_Date":          row["LIC_START_DATE"].strip(),
                "Lic_Expiration_Date":     row["LIC_EXPIRATION_DATE"].strip(),
                "Commence_Operations_Date": row["COMMENCE_OPERATIONS_DATE"].strip(),
                "Suspension_Start_Date":   h.get("LICENSE_SUSPENSION_START_DATE", "").strip(),
                "Suspension_End_Date":     h.get("LICENSE_SUSPENSION_END_DATE", "").strip(),
                "Revocation_Date":         h.get("LICENSE_REVOCATION_DATE", "").strip(),
                "Surrendered_Date":        h.get("LICENSE_SURRENDERED_DATE", "").strip(),
                "Priority_Status":         row["APPLICATION_CLASSIFICATION"].strip(),
                "EIN_TIN":                 row["EIN_TIN"].strip(),
            })

    active = [r for r in rows if r["License_Status"] == "Active"]

    for path, data in [(OUT_ALL, rows), (OUT_ACTIVE, active)]:
        with open(path, "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=HEADERS)
            w.writeheader()
            w.writerows(data)

    print(f"{len(rows)} total retailers  -> MA-facilities.csv")
    print(f"{len(active)} active retailers -> MA-facilities-active.csv")


if __name__ == "__main__":
    main()
