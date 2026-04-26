"""
NJ Facilities Builder
Written by Amazon Q for Loyal9 / poweredby.ci

Source: nj-dispensaries.csv
  - Extracted from NJ Cannabis Regulatory Commission map page
  - 302 dispensaries with name, address, and type tags

Notes:
  - Values are wrapped in single quotes (JS map data artifact)
  - Type field uses pipe + literal \\n as delimiter
  - Address format: "Street, City, NJ ZIP, USA"
  - No license numbers or expiration dates in this source

Output: NJ-facilities.csv
"""

import csv
import os
import re

BASE_DIR  = os.path.dirname(os.path.abspath(__file__))
CSV_DIR   = os.path.abspath(os.path.join(BASE_DIR, "..", "csv"))
STATE_DIR = os.path.abspath(os.path.join(BASE_DIR, ".."))

INPUT  = os.path.join(CSV_DIR, "nj-dispensaries.csv")
OUTPUT = os.path.join(STATE_DIR, "NJ-facilities.csv")

HEADERS = [
    "Business_Name", "Street", "City", "State", "ZIP",
    "Recreational", "Medical", "Delivery", "Microbusiness",
    "Consumption_Area", "Raw_Type",
]

# "394 Communipaw Ave, Jersey City, NJ 07304, USA"
ADDR_RE = re.compile(r'^(.+),\s+(.+),\s+NJ\s+(\d{5})', re.IGNORECASE)


def parse_address(raw):
    m = ADDR_RE.match(raw.strip())
    if m:
        return m.group(1).strip(), m.group(2).strip(), "NJ", m.group(3).strip()
    return raw.strip(), "", "NJ", ""


def parse_type(raw):
    tags = [t.strip() for t in re.split(r'\|\\n|\\n|\|', raw)]
    tags = [t for t in tags if t]
    return {
        "Recreational":    "1" if any("Recreational" in t for t in tags) else "",
        "Medical":         "1" if any("Medicinal" in t or "Medical" in t for t in tags) else "",
        "Delivery":        "1" if any("delivery" in t.lower() for t in tags) else "",
        "Microbusiness":   "1" if any("Microbusiness" in t for t in tags) else "",
        "Consumption_Area":"1" if any("Consumption" in t for t in tags) else "",
    }


def main():
    rows = []
    with open(INPUT, encoding="cp1252") as f:
        for row in csv.DictReader(f):
            name = row["Business Name"].strip().strip("'")
            if not name:
                continue
            addr  = row["Address"].strip().strip("'")
            rtype = row["Type"].strip().strip("'")

            street, city, state, zip_code = parse_address(addr)
            flags = parse_type(rtype)

            rows.append({
                "Business_Name": name,
                "Street":        street,
                "City":          city,
                "State":         state,
                "ZIP":           zip_code,
                **flags,
                "Raw_Type":      rtype,
            })

    with open(OUTPUT, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=HEADERS)
        w.writeheader()
        w.writerows(rows)

    rec  = sum(1 for r in rows if r["Recreational"])
    med  = sum(1 for r in rows if r["Medical"])
    delv = sum(1 for r in rows if r["Delivery"])
    mb   = sum(1 for r in rows if r["Microbusiness"])

    print(f"{len(rows)} dispensaries -> NJ-facilities.csv")
    print(f"  Recreational: {rec}  Medical: {med}  Delivery: {delv}  Microbusiness: {mb}")


if __name__ == "__main__":
    main()
