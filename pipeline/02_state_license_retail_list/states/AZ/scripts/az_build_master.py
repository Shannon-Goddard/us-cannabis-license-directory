"""
AZ Master CSV Builder
Written by Amazon Q for Loyal9 / poweredby.ci

Combines all per-license inspection and enforcement CSVs into:
  - AZ-inspections-master.csv
  - AZ-enforcements-master.csv
"""

import csv
import os
import glob

BASE_DIR  = os.path.dirname(os.path.abspath(__file__))
STATE_DIR = os.path.abspath(os.path.join(BASE_DIR, ".."))

INSP_DIR  = os.path.join(STATE_DIR, "csv", "inspections")
ENF_DIR   = os.path.join(STATE_DIR, "csv", "enforcements")

INSP_MASTER = os.path.join(STATE_DIR, "AZ-inspections-master.csv")
ENF_MASTER  = os.path.join(STATE_DIR, "AZ-enforcements-master.csv")


def combine(folder, output):
    files = sorted(glob.glob(os.path.join(folder, "*.csv")))
    if not files:
        print(f"No files found in {folder}")
        return

    written = 0
    seen = set()

    with open(output, "w", newline="", encoding="utf-8") as out_f:
        writer = None
        for fpath in files:
            with open(fpath, newline="", encoding="utf-8-sig") as in_f:
                reader = csv.DictReader(in_f)
                if writer is None:
                    writer = csv.DictWriter(out_f, fieldnames=reader.fieldnames,
                                            extrasaction="ignore")
                    writer.writeheader()
                for row in reader:
                    # Deduplicate on all values combined
                    key = tuple(row.values())
                    if key not in seen:
                        seen.add(key)
                        writer.writerow(row)
                        written += 1

    print(f"  {written} unique rows → {output}")


print("Building AZ master CSVs...")
combine(INSP_DIR, INSP_MASTER)
combine(ENF_DIR,  ENF_MASTER)
print("Done.")
