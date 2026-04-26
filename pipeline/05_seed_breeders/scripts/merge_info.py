"""
Pipeline 05 — Merge breeder_info.csv into breeders-master.csv
Match on URL (normalized). Info fills blank fields in master, never overwrites.
New breeders from info (no URL match) get appended.
"""

import csv
import re
import os

BASE   = os.path.dirname(os.path.abspath(__file__))
MASTER = os.path.join(BASE, "../breeders-master.csv")
INFO   = os.path.join(BASE, "../breeder_info.csv")

# Field mapping: info column -> master column
FIELD_MAP = {
    "street_add": "street_address",
    "city": "city",
    "state": "state",
    "zip_code": "zip_code",
    "country": "country",
    "phone": "phone",
    "email": "email",
}


def clean_url(u):
    u = u.strip().lower().rstrip("/")
    for prefix in ["https://www.", "http://www.", "https://", "http://"]:
        if u.startswith(prefix):
            u = u[len(prefix):]
    return u


def slugify(name):
    if not name or not name.strip():
        return ""
    name = name.lower().strip()
    if name.startswith("the "):
        name = name[4:]
    name = re.sub(r"[^\w\s-]", "", name)
    name = re.sub(r"[\s_]+", "-", name)
    return name.strip("-")


# Load master
with open(MASTER, newline="", encoding="utf-8-sig", errors="replace") as f:
    reader = csv.DictReader(f)
    master_headers = list(reader.fieldnames)
    master_rows = list(reader)

# Load info
with open(INFO, newline="", encoding="utf-8-sig", errors="replace") as f:
    info_rows = list(csv.DictReader(f))

# Build info lookup by cleaned URL
info_lookup = {}
for r in info_rows:
    url = r.get("url", "").strip()
    if url:
        info_lookup[clean_url(url)] = r

print(f"Master rows: {len(master_rows)}")
print(f"Info rows: {len(info_rows)}")
print(f"Info URLs: {len(info_lookup)}")

# Pass 1: Fill blanks in master from info where URL matches
filled = 0
matched = 0

for row in master_rows:
    master_url = clean_url(row.get("url", ""))
    if not master_url:
        continue

    info = info_lookup.pop(master_url, None)
    if not info:
        continue

    matched += 1

    for info_col, master_col in FIELD_MAP.items():
        info_val = info.get(info_col, "").strip()
        master_val = row.get(master_col, "").strip()
        if info_val and not master_val:
            row[master_col] = info_val
            filled += 1

# Pass 2: Append new rows from info that didn't match any master URL
new_rows = 0
for url_key, info in info_lookup.items():
    new_row = {h: "" for h in master_headers}
    new_row["name"] = info.get("name", "").strip()
    new_row["slug"] = slugify(new_row["name"])
    new_row["url"] = info.get("url", "").strip()
    new_row["is_bad_url"] = "false" if new_row["url"] else ""

    for info_col, master_col in FIELD_MAP.items():
        val = info.get(info_col, "").strip()
        if val:
            new_row[master_col] = val

    master_rows.append(new_row)
    new_rows += 1

# Write back
with open(MASTER, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=master_headers, extrasaction="ignore")
    writer.writeheader()
    writer.writerows(master_rows)

print(f"\nResults:")
print(f"  URL matches: {matched}")
print(f"  Fields filled: {filled}")
print(f"  New rows appended: {new_rows}")
print(f"  Master total now: {len(master_rows)}")
