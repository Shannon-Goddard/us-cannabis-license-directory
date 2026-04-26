import csv
import re
from bs4 import BeautifulSoup

NOTES = r"c:\Users\uthin\Desktop\NEW-SEEDS-LAW\notes.txt"
OUTPUT = r"c:\Users\uthin\Desktop\NEW-SEEDS-LAW\pipeline\04_human_in_the_loop\output\aeterna-locations.csv"

with open(NOTES, encoding="utf-8") as f:
    html = f.read()

soup = BeautifulSoup(html, "html.parser")

HEADERS = [
    "name", "dba", "slug", "type", "url", "is_bad_url",
    "street_address", "city", "state", "zip_code", "country",
    "lat", "lng", "phone", "email", "license_state", "multiple_locations",
]

rows = []
for li in soup.find_all("li", {"data-store-id": True}):
    store_name_tag = li.find("strong")
    if not store_name_tag:
        continue
    a_tag = store_name_tag.find("a")
    dba = a_tag.get_text(strip=True) if a_tag else store_name_tag.get_text(strip=True)

    street_tag = li.find("span", class_="wpsl-street")
    street = street_tag.get_text(strip=True) if street_tag else ""

    # City, state, zip are in the next <span> after street
    city_span = None
    for span in li.find_all("span"):
        if "wpsl-street" not in span.get("class", []) and "wpsl-country" not in span.get("class", []):
            text = span.get_text(strip=True)
            if text and text != street:
                city_span = text
                break

    city = ""
    state = ""
    zip_code = ""
    if city_span:
        # Format: "City ST ZIPCODE"
        m = re.match(r"^(.+?)\s+([A-Z]{2})\s+(\d{5})", city_span)
        if m:
            city = m.group(1)
            state = m.group(2)
            zip_code = m.group(3)

    def slugify(name):
        name = name.lower().strip()
        if name.startswith("the "):
            name = name[4:]
        name = re.sub(r"[^\w\s-]", "", name)
        name = re.sub(r"[\s_]+", "-", name)
        return name.strip("-")

    rows.append({
        "name": "Aeterna",
        "dba": dba,
        "slug": slugify("Aeterna"),
        "type": "other",
        "url": "https://aeternacannabis.com/",
        "is_bad_url": "",
        "street_address": street,
        "city": city,
        "state": state,
        "zip_code": zip_code,
        "country": "US",
        "lat": "",
        "lng": "",
        "phone": "",
        "email": "",
        "license_state": "OCM-MICR-24-000139",
        "multiple_locations": "true",
    })

with open(OUTPUT, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=HEADERS)
    writer.writeheader()
    writer.writerows(rows)

print(f"Parsed {len(rows)} Aeterna locations -> {OUTPUT}")

# Show first 5
for r in rows[:5]:
    print(f"  {r['dba']} | {r['street_address']}, {r['city']}, {r['state']} {r['zip_code']}")
