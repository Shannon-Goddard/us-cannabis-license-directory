"""
CA Facilities Builder
Written by Amazon Q for Loyal9 / poweredby.ci

Combines all 9 California DCC CSV exports into:
  - CA-facilities.csv        — all records, all statuses
  - CA-facilities-active.csv — Active only (seed finder use)

Source files collected: April 18, 2026
Source: California Department of Cannabis Control
        https://www.cannabis.ca.gov/resources/search-for-licensed-business/
"""

import csv
import glob
import os

BASE_DIR   = os.path.dirname(os.path.abspath(__file__))
STATE_DIR  = os.path.abspath(os.path.join(BASE_DIR, ".."))
ALL_OUT    = os.path.join(STATE_DIR, "CA-facilities.csv")
ACTIVE_OUT = os.path.join(STATE_DIR, "CA-facilities-active.csv")

SEED_RELEVANT = {
    "Commercial -  Retailer",
    "Commercial -  Retailer - Non-Storefront",
    "Commercial -  Microbusiness",
    "Cultivation -  Nursery",
}

def main():
    files = sorted(glob.glob(os.path.join(STATE_DIR, "uls-export-04-18-2026*.csv")))
    print(f"Found {len(files)} source files")

    all_rows = []
    seen     = set()

    for fpath in files:
        fname = os.path.basename(fpath)
        with open(fpath, newline="", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)
            count  = 0
            for row in reader:
                key = row.get("licenseNumber", "").strip()
                if key and key not in seen:
                    seen.add(key)
                    all_rows.append(row)
                    count += 1
            print(f"  {fname}: {count} unique rows")

    all_rows.sort(key=lambda r: (r.get("licenseType",""), r.get("businessLegalName","")))
    headers = list(all_rows[0].keys()) if all_rows else []

    with open(ALL_OUT, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=headers, extrasaction="ignore")
        w.writeheader()
        w.writerows(all_rows)
    print(f"\nAll records:  {len(all_rows)} rows -> CA-facilities.csv")

    active = [r for r in all_rows if r.get("licenseStatus","").strip() == "Active"]
    with open(ACTIVE_OUT, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=headers, extrasaction="ignore")
        w.writeheader()
        w.writerows(active)
    print(f"Active only:  {len(active)} rows -> CA-facilities-active.csv")

    print("\nActive records by license type:")
    type_counts = {}
    for r in active:
        t = r.get("licenseType","Unknown").strip()
        type_counts[t] = type_counts.get(t, 0) + 1
    for t, c in sorted(type_counts.items(), key=lambda x: -x[1]):
        flag = " [seed finder]" if t in SEED_RELEVANT else ""
        print(f"  {c:>5}  {t}{flag}")

if __name__ == "__main__":
    main()
