"""
WV Facilities Builder
Written by Amazon Q for Loyal9 / poweredby.ci

Source: notes.text — HTML card list from WV DHHR dispensary locator
  Each card contains: DBA (h3), full address (h4), legal name, phone, county

Output: WV-facilities.csv
"""

import csv
import os
import re

BASE_DIR  = os.path.dirname(os.path.abspath(__file__))
STATE_DIR = os.path.abspath(os.path.join(BASE_DIR, ".."))
NOTES     = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(STATE_DIR)))), "notes.text")
OUTPUT    = os.path.join(STATE_DIR, "WV-facilities.csv")

HEADERS = [
    "ID", "DBA", "Legal_Name", "Full_Address", "Street", "City", "State", "ZIP",
    "Phone", "County", "Operational_Status",
]

# Address format in h4: "STREET, CITY, WV ZIP"
ADDR_RE = re.compile(r'^(.+),\s+(.+),\s+WV\s+(\d{5})', re.IGNORECASE)


def parse_address(raw):
    raw = raw.strip()
    m = ADDR_RE.match(raw)
    if m:
        return raw, m.group(1).strip(), m.group(2).strip(), "WV", m.group(3).strip()
    return raw, raw, "", "WV", ""


def main():
    with open(NOTES, encoding="utf-8") as f:
        html = f.read()

    # Extract each card block
    cards = re.findall(
        r'<div class="card" data-county="([^"]+)" data-id="(\d+)">(.*?)</div>\s*<!-- End Locations -->',
        html, re.DOTALL
    )

    rows = []
    for county, card_id, body in cards:
        # DBA from h3
        h3 = re.search(r'<h3>(.*?)</h3>', body, re.DOTALL)
        dba = h3.group(1).strip() if h3 else ""

        # Full address from h4
        h4 = re.search(r'<h4>(.*?)</h4>', body, re.DOTALL)
        full_addr = h4.group(1).strip() if h4 else ""
        full_addr, street, city, state, zip_code = parse_address(full_addr)

        # Legal name — first span after "Dispensary Name:" label
        legal_m = re.search(r'Dispensary Name:.*?<span>(.*?)</span>', body, re.DOTALL)
        legal_name = legal_m.group(1).strip() if legal_m else ""

        # Phone — span after "Phone Number:" label
        phone_m = re.search(r'Phone Number:.*?<span>(.*?)</span>', body, re.DOTALL)
        phone = phone_m.group(1).strip() if phone_m else ""
        if phone == "N/A":
            phone = ""

        # Operational status
        op_m = re.search(r'<span>(Operational[^<]*)</span>', body)
        op_status = op_m.group(1).strip() if op_m else ""

        # Use legal name as DBA fallback if h3 is empty
        if not dba and legal_name:
            dba = legal_name

        rows.append({
            "ID":                card_id,
            "DBA":               dba,
            "Legal_Name":        legal_name,
            "Full_Address":      full_addr,
            "Street":            street,
            "City":              city.title(),
            "State":             state,
            "ZIP":               zip_code,
            "Phone":             phone,
            "County":            county,
            "Operational_Status": op_status,
        })

    with open(OUTPUT, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=HEADERS)
        w.writeheader()
        w.writerows(rows)

    print(f"{len(rows)} dispensaries -> WV-facilities.csv")
    for r in rows:
        print(f"  {r['DBA']:<40} {r['City']}, {r['State']} {r['ZIP']}  {r['Phone']}")


if __name__ == "__main__":
    main()
