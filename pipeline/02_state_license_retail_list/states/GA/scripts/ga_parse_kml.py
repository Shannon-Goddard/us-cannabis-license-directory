"""
GA KML Parser
Written by Amazon Q for Loyal9 / poweredby.ci

Parses Georgia Licensed Medical Cannabis Dispensaries.kml into GA-facilities.csv

KML is a Google Maps/Earth XML format. Each dispensary is a <Placemark>
with a name, description (HTML with address + license number), and GPS coordinates.
"""

import csv
import os
import re
import xml.etree.ElementTree as ET
from html.parser import HTMLParser

BASE_DIR  = os.path.dirname(os.path.abspath(__file__))
STATE_DIR = os.path.abspath(os.path.join(BASE_DIR, ".."))
KML_FILE  = os.path.join(STATE_DIR, "Georgia Licensed Medical Cannabis Dispensaries.kml")
OUTPUT    = os.path.join(STATE_DIR, "GA-facilities.csv")

HEADERS = [
    "Business_Name", "Legal_Name", "Address", "City", "State", "ZIP",
    "License_Number", "Latitude", "Longitude"
]

# Strip HTML tags from description text
class HTMLStripper(HTMLParser):
    def __init__(self):
        super().__init__()
        self.parts = []
    def handle_data(self, data):
        self.parts.append(data.strip())
    def get_text(self):
        return [p for p in self.parts if p]

def strip_html(html):
    s = HTMLStripper()
    s.feed(html)
    return s.get_text()


def parse_description(lines, placemark_name):
    """
    Description lines follow patterns like:
      Line 0: Legal name or DBA intro (e.g. "Trulieve Medical Cannabis Dispensary of Macon")
      Line 1: Street address
      Line 2: Suite (optional)
      Line 3: City, State ZIP
      Line 4: "Dispensing License DISP####"
    """
    # Extract license number
    lic_num = ""
    for line in lines:
        m = re.search(r'(DISP\d+)', line)
        if m:
            lic_num = m.group(1)
            break

    # Remove license line and empty lines
    content = [l for l in lines if l and not re.search(r'Dispensing License', l)]

    # Last line that looks like "City, State ZIP" or "City State ZIP"
    city = state = zip_code = ""
    address_lines = []

    for i, line in enumerate(content):
        # Match "City, GA 12345" or "City GA 12345"
        m = re.match(r'^(.+?),?\s+(GA|Georgia)\s+(\d{5})', line, re.IGNORECASE)
        if m:
            city      = m.group(1).strip()
            state     = "GA"
            zip_code  = m.group(3).strip()
            address_lines = content[:i]
            break

    # Legal name is first line, street address is everything between
    legal_name = content[0] if content else placemark_name

    # Handle "dba" lines — legal name may span 2 lines
    street_parts = []
    collecting = False
    for line in address_lines[1:]:
        if line.lower().startswith("d/b/a") or line.lower().startswith("dba"):
            # This is still part of the legal name block — skip for address
            continue
        street_parts.append(line)

    address = ", ".join(street_parts) if street_parts else ""

    return {
        "Legal_Name":     legal_name,
        "Address":        address,
        "City":           city,
        "State":          state,
        "ZIP":            zip_code,
        "License_Number": lic_num,
    }


def main():
    # KML uses a namespace
    ns = {"kml": "http://www.opengis.net/kml/2.2"}
    tree = ET.parse(KML_FILE)
    root = tree.getroot()

    rows = []

    for placemark in root.findall(".//kml:Placemark", ns):
        name_el = placemark.find("kml:name", ns)
        desc_el = placemark.find("kml:description", ns)
        coord_el = placemark.find(".//kml:coordinates", ns)

        business_name = name_el.text.strip() if name_el is not None else ""
        description   = desc_el.text.strip() if desc_el is not None else ""
        coordinates   = coord_el.text.strip() if coord_el is not None else ""

        # Parse GPS
        lat = lon = ""
        if coordinates:
            parts = coordinates.split(",")
            if len(parts) >= 2:
                lon = parts[0].strip()
                lat = parts[1].strip()

        # Parse description HTML
        lines = strip_html(description)
        parsed = parse_description(lines, business_name)

        rows.append({
            "Business_Name":  business_name,
            "Legal_Name":     parsed["Legal_Name"],
            "Address":        parsed["Address"],
            "City":           parsed["City"],
            "State":          parsed["State"],
            "ZIP":            parsed["ZIP"],
            "License_Number": parsed["License_Number"],
            "Latitude":       lat,
            "Longitude":      lon,
        })

    with open(OUTPUT, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=HEADERS)
        w.writeheader()
        w.writerows(rows)

    print(f"{len(rows)} dispensaries -> GA-facilities.csv")
    for r in rows:
        print(f"  {r['License_Number']}  {r['Business_Name']}  {r['City']}  {r['ZIP']}")


if __name__ == "__main__":
    main()
