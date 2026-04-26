"""
WA Facilities Builder
Written by Amazon Q for Loyal9 / poweredby.ci

Sources:
  retailers.csv     - Primary: 1,209 records, all statuses, address + phone
  se-retailers.csv  - Enrichment: 9 active SE retailers with legal name,
                      expiration date, mailing address

Output:
  WA-facilities.csv        - All retailers (all statuses)
  WA-facilities-active.csv - ACTIVE (ISSUED) only
"""

import csv
import os

BASE_DIR  = os.path.dirname(os.path.abspath(__file__))
CSV_DIR   = os.path.abspath(os.path.join(BASE_DIR, "..", "csv"))
STATE_DIR = os.path.abspath(os.path.join(BASE_DIR, ".."))

RETAILERS = os.path.join(CSV_DIR, "retailers.csv")
SE_FILE   = os.path.join(CSV_DIR, "se-retailers.csv")
OUT_ALL    = os.path.join(STATE_DIR, "WA-facilities.csv")
OUT_ACTIVE = os.path.join(STATE_DIR, "WA-facilities-active.csv")

HEADERS = [
    "License_Number", "UBI", "Trade_Name", "Licensee",
    "Privilege_Status", "Privilege_Type",
    "Street", "Suite", "City", "State", "ZIP", "County",
    "Phone", "Expiration_Date", "Mailing_Address", "SE_Retailer",
]


def load_se(path):
    lookup = {}
    with open(path, encoding="cp1252") as f:
        for row in csv.DictReader(f):
            ln = row["License #"].strip()
            if ln and row["Status"].strip():
                lookup[ln] = row
    return lookup


def main():
    se = load_se(SE_FILE)

    rows = []
    with open(RETAILERS, encoding="cp1252") as f:
        for row in csv.DictReader(f):
            ln = row["License "].strip()
            if not ln:
                continue
            s = se.get(ln, {})
            mail = ""
            if s:
                mail = " ".join(filter(None, [
                    s.get("Mail Address", "").strip(),
                    s.get("Room#", "").strip(),
                    s.get("City", "").strip(),
                    s.get("St", "").strip(),
                    s.get("zip", "").strip(),
                ])).strip()

            rows.append({
                "License_Number":   ln,
                "UBI":              row["UBI"].strip(),
                "Trade_Name":       row["Tradename"].strip(),
                "Licensee":         s.get("Licensee", "").strip(),
                "Privilege_Status": row["Privilege Status"].strip(),
                "Privilege_Type":   row["Priv Desc"].strip(),
                "Street":           row["Street Address"].strip(),
                "Suite":            row["Suite Rm"].strip(),
                "City":             row["City"].strip(),
                "State":            row["State"].strip(),
                "ZIP":              row["Zip Code"].strip(),
                "County":           row["county"].strip(),
                "Phone":            row["Day Phone"].strip(),
                "Expiration_Date":  s.get("Expire", "").strip(),
                "Mailing_Address":  mail,
                "SE_Retailer":      "1" if s else "",
            })

    active = [r for r in rows if r["Privilege_Status"] == "ACTIVE (ISSUED)"]

    for path, data in [(OUT_ALL, rows), (OUT_ACTIVE, active)]:
        with open(path, "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=HEADERS)
            w.writeheader()
            w.writerows(data)

    print(f"{len(rows)} total retailers  -> WA-facilities.csv")
    print(f"{len(active)} active           -> WA-facilities-active.csv")
    print(f"  SE retailers joined: {sum(1 for r in rows if r['SE_Retailer'])}")


if __name__ == "__main__":
    main()
