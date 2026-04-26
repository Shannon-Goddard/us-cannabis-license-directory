"""
State verified cleanup:
1. Rebuild all slugs from name
2. Add dba_slug column from dba
3. Fix MA zip codes — pad to 5 digits with leading zeros
"""

import csv
import re

PATH = r"c:\Users\uthin\Desktop\NEW-SEEDS-LAW\pipeline\04_human_in_the_loop\output\state-verified.csv"


def slugify(name: str) -> str:
    if not name or not name.strip():
        return ""
    name = name.lower().strip()
    if name.startswith("the "):
        name = name[4:]
    name = re.sub(r"[^\w\s-]", "", name)
    name = re.sub(r"[\s_]+", "-", name)
    return name.strip("-")


# Load
with open(PATH, newline="", encoding="utf-8-sig", errors="replace") as f:
    reader = csv.DictReader(f)
    fieldnames = list(reader.fieldnames)
    rows = list(reader)

# Add dba_slug column after dba if not present
if "dba_slug" not in fieldnames:
    dba_idx = fieldnames.index("dba") + 1 if "dba" in fieldnames else fieldnames.index("slug") + 1
    fieldnames.insert(dba_idx + 1, "dba_slug")

slug_rebuilt = 0
dba_slug_added = 0
ma_zips_fixed = 0

for row in rows:
    # Rebuild slug
    row["slug"] = slugify(row.get("name", ""))
    slug_rebuilt += 1

    # Build dba_slug
    dba = row.get("dba", "").strip()
    row["dba_slug"] = slugify(dba) if dba else ""
    if row["dba_slug"]:
        dba_slug_added += 1

    # Fix MA zip codes — pad to 5 digits
    state = row.get("state", "").strip()
    zip_code = row.get("zip_code", "").strip()
    if zip_code and len(zip_code) < 5 and zip_code.isdigit():
        row["zip_code"] = zip_code.zfill(5)
        if row["zip_code"] != zip_code:
            ma_zips_fixed += 1

# Write back
with open(PATH, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
    writer.writeheader()
    writer.writerows(rows)

print(f"Rows: {len(rows)}")
print(f"Slugs rebuilt: {slug_rebuilt}")
print(f"DBA slugs added: {dba_slug_added}")
print(f"Zip codes padded: {ma_zips_fixed}")
