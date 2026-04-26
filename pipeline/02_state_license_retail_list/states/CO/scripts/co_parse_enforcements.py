"""
CO Enforcement PDF Parser
Written by Amazon Q for Loyal9 / poweredby.ci

Parses Colorado MED Administrative Actions PDFs into structured CSV.

Usage:
    python co_parse_enforcements.py

Reads all PDFs from ../pdf/ and outputs CO-enforcements.csv
"""

import csv
import os
import re
import pdfplumber

BASE_DIR  = os.path.dirname(os.path.abspath(__file__))
STATE_DIR = os.path.abspath(os.path.join(BASE_DIR, ".."))
PDF_DIR   = os.path.join(STATE_DIR, "pdf")
OUTPUT    = os.path.join(STATE_DIR, "CO-enforcements.csv")

HEADERS = ["Source_File", "Action_Date", "Licensee_Name", "License_Number",
           "Action_Type", "Fine_Amount"]

# Date patterns: "January 8, 2025" or "1/8/2025" or "1/8/25"
DATE_RE  = re.compile(
    r'^([A-Za-z]+ \d{1,2},?\s*\d{4}|\d{1,2}/\d{1,2}/\d{2,4})$'
)

# License number pattern — Colorado uses formats like M12345678, R12345678, or plain numbers
LIC_RE   = re.compile(r'\b([MR]\d{6,}|\d{6,})\b')

# Fine amount pattern
FINE_RE  = re.compile(r'\$[\d,]+')

# Action type keywords
SAO_RE   = re.compile(r'stipulation|agreement|SAO', re.IGNORECASE)
FAO_RE   = re.compile(r'final agency order|FAO|hearing', re.IGNORECASE)


def parse_pdf(fpath):
    rows     = []
    fname    = os.path.basename(fpath)
    current_date = None
    current_type = "SAO"  # default — most CO enforcement actions are SAOs

    with pdfplumber.open(fpath) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if not text:
                continue

            for line in text.split("\n"):
                line = line.strip()
                if not line:
                    continue

                # Detect action type headers
                if SAO_RE.search(line):
                    current_type = "SAO"
                elif FAO_RE.search(line):
                    current_type = "FAO"

                # Detect date lines
                if DATE_RE.match(line):
                    current_date = line.strip(",")
                    continue

                # Detect inline dates like "Company Name, 1/28/26"
                inline_date = re.search(r',\s*(\d{1,2}/\d{1,2}/\d{2,4})$', line)
                if inline_date:
                    current_date = inline_date.group(1)
                    line = line[:inline_date.start()].strip()

                # Extract license number if present
                lic_match = LIC_RE.search(line)
                lic_num   = lic_match.group(1) if lic_match else ""

                # Extract fine amount if present
                fine_match = FINE_RE.search(line)
                fine_amt   = fine_match.group(0) if fine_match else ""

                # Clean licensee name — remove license number and fine from line
                name = line
                if lic_num:
                    name = name.replace(lic_num, "").strip()
                if fine_amt:
                    name = name.replace(fine_amt, "").strip()
                name = re.sub(r'[,;]+$', '', name).strip()

                # Skip header/footer lines and short noise
                if len(name) < 4:
                    continue
                skip_words = {"page", "date", "licensee", "license", "med",
                              "marijuana", "enforcement", "division", "colorado",
                              "stipulation", "agreement", "order", "final",
                              "agency", "administrative", "actions", "fao", "sao"}
                if name.lower() in skip_words:
                    continue

                # Only write rows that look like actual enforcement entries
                # Must have a date and a name of reasonable length
                if current_date and len(name) > 5:
                    rows.append({
                        "Source_File":    fname,
                        "Action_Date":    current_date,
                        "Licensee_Name":  name,
                        "License_Number": lic_num,
                        "Action_Type":    current_type,
                        "Fine_Amount":    fine_amt,
                    })

    return rows


def main():
    if not os.path.exists(PDF_DIR):
        print(f"No pdf/ folder found at {PDF_DIR}")
        return

    pdfs = [f for f in os.listdir(PDF_DIR) if f.lower().endswith(".pdf")]
    if not pdfs:
        print("No PDF files found in pdf/ folder")
        return

    all_rows = []
    for fname in sorted(pdfs):
        fpath = os.path.join(PDF_DIR, fname)
        print(f"Parsing: {fname}")
        rows = parse_pdf(fpath)
        print(f"  {len(rows)} rows extracted")
        all_rows.extend(rows)

    with open(OUTPUT, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=HEADERS)
        w.writeheader()
        w.writerows(all_rows)

    print(f"\n{len(all_rows)} total rows -> CO-enforcements.csv")


if __name__ == "__main__":
    main()
