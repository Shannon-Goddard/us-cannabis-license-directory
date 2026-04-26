"""
KY OMC Licensee Text Parser
Written by Amazon Q for Loyal9 / poweredby.ci

Parses the Kentucky Office of Medical Cannabis licensee page text
(copied from https://kymedcan.ky.gov/businesses/Pages/licensees.aspx)
into KY-facilities.csv

Source text is in notes.text — paste the raw page text into
pipeline/02_state_license_retail_list/states/KY/ky_licensees.txt
then run this script.

Structure:
  - Section headers (Safety Compliance, Cultivator Tier I/II/III, Processor, Dispensary)
  - Region headers for dispensaries (Region 1 Bluegrass, etc.)
  - Each entry: Company Name (DBA: Brand)*** (County Co.)
  - *** = approved to operate
  - Parenthetical notes = transfer/location history (ignored for CSV)
"""

import csv
import os
import re

BASE_DIR  = os.path.dirname(os.path.abspath(__file__))
STATE_DIR = os.path.abspath(os.path.join(BASE_DIR, ".."))
INPUT     = os.path.join(STATE_DIR, "ky_licensees.txt")
OUTPUT    = os.path.join(STATE_DIR, "KY-facilities.csv")

HEADERS = [
    "License_Holder", "DBA", "County", "State",
    "Approved_To_Operate", "License_Type", "Region"
]

# Section markers -> license type
SECTION_MAP = {
    "Safety Compliance Facility Licensees":  "Safety Compliance",
    "Cultivator Tier I Licensees":           "Cultivator Tier I",
    "Cultivator Tier II Licensees":          "Cultivator Tier II",
    "Cultivator Tier III Licensees":         "Cultivator Tier III",
    "Processor Licensees":                   "Processor",
    "Dispensary Licensees":                  "Dispensary",
}

# Region markers (dispensary sub-regions)
REGION_RE = re.compile(r'^Region \d+ .+$')

# Entry pattern: Name (DBA: Brand)*** (County Co.) ...
# The *** may or may not be present
# County is always "(Xxx Co.)" or "(Xxx County)"
COUNTY_RE = re.compile(r'\(([A-Za-z\s]+(?:Co\.|County))\)')
DBA_RE    = re.compile(r'\(DBA:\s*([^)]+)\)')
APPROVED  = '***'


def parse_entry(line):
    """Parse a single licensee line into structured fields."""
    approved = APPROVED in line

    # Remove *** marker
    line = line.replace(APPROVED, '').strip()

    # Extract DBA
    dba = ""
    dba_m = DBA_RE.search(line)
    if dba_m:
        dba = dba_m.group(1).strip()
        line = line[:dba_m.start()].strip() + line[dba_m.end():].strip()

    # Extract county — first occurrence of "(Xxx Co.)"
    county = ""
    county_m = COUNTY_RE.search(line)
    if county_m:
        county = county_m.group(1).strip()
        # Remove everything from first parenthesis onward (history notes)
        line = line[:county_m.start()].strip()

    # What's left is the license holder name
    license_holder = line.strip().rstrip(',').strip()

    return {
        "License_Holder":    license_holder,
        "DBA":               dba,
        "County":            county,
        "State":             "KY",
        "Approved_To_Operate": "Yes" if approved else "No",
    }


def main():
    if not os.path.exists(INPUT):
        print(f"Input file not found: {INPUT}")
        print("Please save the KY OMC licensee page text as ky_licensees.txt")
        return

    rows = []
    current_type   = ""
    current_region = ""

    with open(INPUT, encoding="utf-8") as f:
        for raw_line in f:
            line = raw_line.strip()
            if not line:
                continue

            # Check for section header
            matched_section = False
            for marker, lic_type in SECTION_MAP.items():
                if marker.lower() in line.lower():
                    current_type   = lic_type
                    current_region = ""
                    matched_section = True
                    break
            if matched_section:
                continue

            # Check for region header
            if REGION_RE.match(line):
                current_region = line.strip()
                continue

            # Skip page headers, notes, blank-ish lines
            skip_patterns = [
                "Medical Cannabis Businesses",
                "Forms and Resources",
                "Licensees may find",
                "Please note:",
                "the information on this page",
            ]
            if any(p.lower() in line.lower() for p in skip_patterns):
                continue

            # Must have a county marker to be a valid entry
            if not COUNTY_RE.search(line):
                continue

            # Parse the entry
            entry = parse_entry(line)
            if entry["License_Holder"]:
                entry["License_Type"] = current_type
                entry["Region"]       = current_region
                rows.append(entry)

    with open(OUTPUT, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=HEADERS)
        w.writeheader()
        w.writerows(rows)

    print(f"{len(rows)} records -> KY-facilities.csv")

    # Summary
    types = {}
    approved = sum(1 for r in rows if r["Approved_To_Operate"] == "Yes")
    for r in rows:
        t = r["License_Type"]
        types[t] = types.get(t, 0) + 1
    for t, n in sorted(types.items()):
        print(f"  {n:>4}  {t}")
    print(f"\n  {approved} approved to operate (***)")
    print(f"  {len(rows)-approved} licensed but not yet operational")


if __name__ == "__main__":
    main()
