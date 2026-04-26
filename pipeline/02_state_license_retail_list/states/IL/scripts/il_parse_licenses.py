"""
IL Cannabis License PDF Parser
Written by Amazon Q for Loyal9 / poweredby.ci

Parses the Illinois IDFPR Combined License List PDF into IL-facilities.csv

The PDF contains three sections:
  1. Active Adult Use Dispensing Organization Licenses
  2. Original Lottery Conditionals
  3. SECL Conditionals

Columns: License Holder, Dispensary Name, Address & Phone Number,
         License Issue Date, Adult Use Credential Number

Challenges handled:
  - Multi-line cells (address spans multiple lines)
  - Page breaks mid-record
  - Phone number embedded in address block
  - Section headers and page headers to skip
"""

import csv
import os
import re
import pdfplumber

BASE_DIR  = os.path.dirname(os.path.abspath(__file__))
STATE_DIR = os.path.abspath(os.path.join(BASE_DIR, ".."))
PDF_FILE  = os.path.join(STATE_DIR, "pdf", "all-cannabis-licenses.pdf")
OUTPUT    = os.path.join(STATE_DIR, "IL-facilities.csv")

HEADERS = [
    "License_Holder", "Dispensary_Name", "Street", "City", "State", "ZIP",
    "Phone", "License_Issue_Date", "Credential_Number", "License_Section"
]

# Section markers
SECTION_MARKERS = {
    "Active Adult Use Dispensing Organization Licenses": "Active Adult Use",
    "Original Lottery Conditionals": "Original Lottery Conditional",
    "SECL Conditionals": "SECL Conditional",
}

# Credential number pattern
CRED_RE = re.compile(r'\d{3}\.\d{6}-[A-Z]+')

# Date pattern
DATE_RE = re.compile(r'\d{2}/\d{2}/\d{4}')

# Phone pattern
PHONE_RE = re.compile(r'\(?\d{3}\)?[\s\-\.]\d{3}[\s\-\.]\d{4}')

# Lines to skip
SKIP_RE = re.compile(
    r'^(License Holder|Dispensary Name|Address|Phone|License Issue Date|'
    r'Adult Use Credential|Page \d+|Combined License List|Illinois Department|'
    r'IDFPR|Revised|Updated|\s*)$',
    re.IGNORECASE
)


def parse_address_block(lines):
    """Extract street, city, state, zip, phone from address lines."""
    street_parts = []
    city = state = zip_code = phone = ""

    for line in lines:
        # Phone
        ph = PHONE_RE.search(line)
        if ph:
            phone = ph.group(0).strip()
            line = line[:ph.start()].strip()

        # City State ZIP — "Chicago, IL 60601" or "Chicago IL 60601"
        m = re.search(r'([A-Za-z\s]+),?\s+(IL|Illinois)\s+(\d{5})', line)
        if m:
            city     = m.group(1).strip()
            state    = "IL"
            zip_code = m.group(3).strip()
            # Anything before city is more street
            before = line[:m.start()].strip()
            if before:
                street_parts.append(before)
            continue

        if line:
            street_parts.append(line)

    return {
        "Street": ", ".join(street_parts),
        "City":   city,
        "State":  state,
        "ZIP":    zip_code,
        "Phone":  phone,
    }


def main():
    rows = []
    current_section = "Active Adult Use"

    with pdfplumber.open(PDF_FILE) as pdf:
        # Collect all text lines across all pages
        all_lines = []
        for page in pdf.pages:
            # Try table extraction first
            tables = page.extract_tables()
            if tables:
                for table in tables:
                    for row in table:
                        if row:
                            all_lines.append(("TABLE_ROW", row))
            else:
                text = page.extract_text()
                if text:
                    for line in text.split("\n"):
                        all_lines.append(("TEXT", line.strip()))

    # Process table rows — most reliable for this PDF
    current_row = {}
    address_buffer = []

    for line_type, content in all_lines:
        if line_type == "TABLE_ROW":
            row = content
            # Filter out header rows and empty rows
            if not any(row):
                continue

            # Check for section marker
            first_cell = str(row[0] or "").strip()
            for marker, section_name in SECTION_MARKERS.items():
                if marker.lower() in first_cell.lower():
                    current_section = section_name
                    break

            # Skip header rows
            if first_cell.lower() in ("license holder", "dispensary name", ""):
                if not any(str(c or "").strip() for c in row[1:]):
                    continue

            # Extract cells
            cells = [str(c or "").strip() for c in row]

            # Find credential number in any cell
            cred = ""
            date = ""
            for cell in cells:
                m = CRED_RE.search(cell)
                if m:
                    cred = m.group(0)
                d = DATE_RE.search(cell)
                if d:
                    date = d.group(0)

            if not cred and not date:
                continue  # Skip non-data rows

            # Cells: [License Holder, Dispensary Name, Address+Phone, Date, Credential]
            license_holder  = cells[0] if len(cells) > 0 else ""
            dispensary_name = cells[1] if len(cells) > 1 else ""
            address_raw     = cells[2] if len(cells) > 2 else ""

            # Parse address block
            addr_lines = [l.strip() for l in address_raw.replace("\n", "\n").split("\n") if l.strip()]
            addr = parse_address_block(addr_lines)

            rows.append({
                "License_Holder":    license_holder.replace("\n", " ").strip(),
                "Dispensary_Name":   dispensary_name.replace("\n", " ").strip(),
                "Street":            addr["Street"],
                "City":              addr["City"],
                "State":             addr["State"],
                "ZIP":               addr["ZIP"],
                "Phone":             addr["Phone"],
                "License_Issue_Date": date,
                "Credential_Number": cred,
                "License_Section":   current_section,
            })

    # If table extraction yielded nothing, fall back to text parsing
    if not rows:
        print("Table extraction yielded no results — falling back to text parsing")
        _parse_text_fallback(PDF_FILE, rows, HEADERS)

    with open(OUTPUT, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=HEADERS)
        w.writeheader()
        w.writerows(rows)

    print(f"{len(rows)} records -> IL-facilities.csv")

    # Summary by section
    sections = {}
    for r in rows:
        s = r["License_Section"]
        sections[s] = sections.get(s, 0) + 1
    for s, n in sorted(sections.items()):
        print(f"  {n:>4}  {s}")


def _parse_text_fallback(pdf_path, rows, headers):
    """Text-based fallback parser for when table extraction fails."""
    current_section = "Active Adult Use"
    buffer = []

    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if not text:
                continue
            for line in text.split("\n"):
                line = line.strip()
                if not line:
                    continue

                # Section detection
                for marker, name in SECTION_MARKERS.items():
                    if marker.lower() in line.lower():
                        current_section = name

                # Skip headers/footers
                if SKIP_RE.match(line):
                    continue

                buffer.append((line, current_section))

    # Group lines into records by credential number
    i = 0
    while i < len(buffer):
        line, section = buffer[i]
        cred_m = CRED_RE.search(line)
        if cred_m:
            # Credential line found — look back for the record
            cred = cred_m.group(0)
            date_m = DATE_RE.search(line)
            date = date_m.group(0) if date_m else ""

            # Collect preceding lines as the record body
            record_lines = []
            j = i - 1
            while j >= 0 and not CRED_RE.search(buffer[j][0]):
                record_lines.insert(0, buffer[j][0])
                j -= 1

            if record_lines:
                license_holder  = record_lines[0] if record_lines else ""
                dispensary_name = record_lines[1] if len(record_lines) > 1 else ""
                addr_lines      = record_lines[2:] if len(record_lines) > 2 else []
                addr = parse_address_block(addr_lines)

                rows.append({
                    "License_Holder":     license_holder,
                    "Dispensary_Name":    dispensary_name,
                    "Street":             addr["Street"],
                    "City":               addr["City"],
                    "State":              addr["State"],
                    "ZIP":                addr["ZIP"],
                    "Phone":              addr["Phone"],
                    "License_Issue_Date": date,
                    "Credential_Number":  cred,
                    "License_Section":    section,
                })
        i += 1


if __name__ == "__main__":
    main()
