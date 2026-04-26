"""
MD Dispensary HTML Parser
Written by Amazon Q for Loyal9 / poweredby.ci

Parses the Maryland Cannabis Administration dispensary directory HTML table
into MD-facilities.csv

The source is a 2-column HTML table where each cell contains:
  - Dispensary name (in <strong> or alt text)
  - Street address
  - City, State ZIP
  - Phone (optional)
  - Email (optional)
  - Website (optional)

Save the raw HTML table from the MCA page as md_dispensaries.html
then run this script.
"""

import csv
import html as html_module
import os
import re
from html.parser import HTMLParser

BASE_DIR  = os.path.dirname(os.path.abspath(__file__))
STATE_DIR = os.path.abspath(os.path.join(BASE_DIR, ".."))
INPUT     = os.path.join(STATE_DIR, "md_dispensaries.html")
OUTPUT    = os.path.join(STATE_DIR, "MD-facilities.csv")

HEADERS = [
    "Business_Name", "Street", "City", "State", "ZIP",
    "Phone", "Email", "Website"
]

# Patterns
PHONE_RE   = re.compile(r'\(?\d{3}\)?[\s\-\.]\d{3}[\s\-\.]\d{4}')
EMAIL_RE   = re.compile(r'[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}')
CITY_RE    = re.compile(r'^(.+?),?\s+(MD|Maryland)\s+(\d{5})', re.IGNORECASE)
ZIP_RE     = re.compile(r'\d{5}')


class CellParser(HTMLParser):
    """Extracts visible text lines and links from a single table cell."""
    def __init__(self):
        super().__init__()
        self.lines   = []
        self.links   = []
        self._cur    = []
        self._in_a   = False
        self._href   = ""

    def handle_starttag(self, tag, attrs):
        if tag == "br":
            text = " ".join(self._cur).strip()
            if text:
                self.lines.append(text)
            self._cur = []
        elif tag == "a":
            self._in_a = True
            for k, v in attrs:
                if k == "href" and v:
                    self._href = v

    def handle_endtag(self, tag):
        if tag == "a":
            self._in_a = False
            href = self._href.strip()
            if href and not href.startswith("/") and not href.startswith("#"):
                self.links.append(href)
            self._href = ""
        elif tag in ("div", "p", "span", "strong", "b", "font"):
            text = " ".join(self._cur).strip()
            if text:
                self.lines.append(text)
            self._cur = []

    def handle_data(self, data):
        text = data.strip()
        if text and text != "\xa0":
            self._cur.append(text)

    def get_lines(self):
        # Flush any remaining
        text = " ".join(self._cur).strip()
        if text:
            self.lines.append(text)
        # Clean and deduplicate while preserving order
        seen = set()
        result = []
        for l in self.lines:
            l = l.strip()
            if l and l not in seen and l != "\xa0":
                seen.add(l)
                result.append(l)
        return result


# Detect street-like lines (start with a number or common street words)
STREET_RE = re.compile(r'^\d+\s|^\d{3,}[A-Z-]', re.IGNORECASE)


def parse_cell(html):
    """Parse a single <td> cell into a dispensary record."""
    # Extract <strong>/<b> text as candidate name — strip inner tags first
    strong_m = re.search(r'<(?:strong|b)[^>]*>(.*?)</(?:strong|b)>', html, re.DOTALL | re.IGNORECASE)
    strong_name = ""
    if strong_m:
        inner = re.sub(r'<[^>]+>', ' ', strong_m.group(1))
        strong_name = html_module.unescape(' '.join(inner.split())).strip().strip('\u200b').strip()

    # Extract img alt as candidate name (skip empty alts)
    alt_m = re.search(r'<img[^>]+alt="([^"]+)"', html, re.IGNORECASE)
    img_alt = alt_m.group(1).strip() if alt_m else ""

    parser = CellParser()
    parser.feed(html)
    lines = parser.get_lines()
    links = parser.links

    if not lines and not strong_name and not img_alt:
        return None

    name = street = city = state = zip_code = phone = email = website = ""

    # Find city/state/zip line index
    city_idx = -1
    for i, line in enumerate(lines):
        m = CITY_RE.search(line)
        if m:
            city     = m.group(1).strip().rstrip(",").strip()
            state    = "MD"
            zip_code = m.group(3).strip()
            city_idx = i
            break

    # Determine name: prefer <strong>, then img alt, then first text line
    if strong_name:
        name = strong_name
    elif img_alt:
        name = img_alt
    elif city_idx > 0:
        name = lines[0]
    elif lines:
        name = lines[0]

    # Street = lines before city, excluding name/phone/email duplicates
    name_clean = name.strip()
    name_norm = name_clean.lower()
    if city_idx >= 0:
        street_parts = []
        for line in lines[:city_idx]:
            clean = line.strip(", ").strip().strip('\u200b').strip()
            if not clean:
                continue
            if clean.lower() == name_norm or name_norm in clean.lower():
                continue
            if PHONE_RE.search(clean) or EMAIL_RE.search(clean):
                continue
            street_parts.append(clean)
        street = ", ".join(p for p in street_parts if p).lstrip(", ").strip()

    # Phone
    for line in lines:
        m = PHONE_RE.search(line)
        if m:
            phone = m.group(0).strip()
            break

    # Email — check lines and mailto links
    for line in lines:
        m = EMAIL_RE.search(line)
        if m:
            email = m.group(0).strip()
            break
    if not email:
        for link in links:
            if link.startswith("mailto:"):
                email = link[7:].strip()
                break

    # Website — first http link that isn't mailto
    for link in links:
        if link.startswith("http") and "@" not in link:
            website = link.strip()
            break

    name = html_module.unescape(name.strip().strip(".,").strip())
    name_norm = name.lower()
    street = street.strip(", ").strip()

    if not name and not street:
        return None

    return {
        "Business_Name": name,
        "Street":        street,
        "City":          city,
        "State":         state,
        "ZIP":           zip_code,
        "Phone":         phone,
        "Email":         email,
        "Website":       website,
    }


def extract_cells(html):
    """Extract all <td> cell HTML from the table."""
    cells = re.findall(r'<td[^>]*>(.*?)</td>', html, re.DOTALL | re.IGNORECASE)
    return cells


def main():
    if not os.path.exists(INPUT):
        print(f"Input file not found: {INPUT}")
        print("Please save the MD dispensary table HTML as md_dispensaries.html")
        return

    with open(INPUT, encoding="utf-8") as f:
        html = f.read()

    cells = extract_cells(html)
    print(f"Found {len(cells)} table cells")

    rows = []
    for cell in cells:
        record = parse_cell(cell)
        if record and record["Business_Name"]:
            rows.append(record)

    with open(OUTPUT, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=HEADERS)
        w.writeheader()
        w.writerows(rows)

    print(f"{len(rows)} dispensaries -> MD-facilities.csv")
    for r in rows:
        print(f"  {r['Business_Name']:<40} {r['City']}, {r['State']} {r['ZIP']}".encode('ascii', 'replace').decode())


if __name__ == "__main__":
    main()
