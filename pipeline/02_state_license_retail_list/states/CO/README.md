# Colorado — Marijuana Enforcement Division Pipeline

**State:** Colorado  
**Source:** [Colorado Marijuana Enforcement Division — Data and Resources](https://med.colorado.gov/data-and-resources)  
**Collected:** April 2026  
**Built by:** Amazon Q  
**Supervised by:** Shannon, who correctly identified that Colorado had enforcement data worth grabbing

---

## What Colorado Gave Us

Ten Excel files split by license category, a quarterly data dashboard that's just graphs built on the same underlying data, and — unexpectedly — a full year of enforcement actions in PDF format going back to 2014.

Colorado is the most mature cannabis market in the country. They've been at this since 2014. The data reflects that.

---

## The License Data

**Source files:** `csv/` — 10 Excel files, April 2026 snapshot  
**Format:** `.xlsx`, two sheets per file (Medical and Retail split)

| File | Category | Rows |
| :--- | :--- | ---: |
| `Stores 2604 Apr.xlsx` | Retail dispensaries | 949 |
| `Cultivations 2604 Apr.xlsx` | Cultivation facilities | 657 |
| `Product Manufacturers 2604 Apr.xlsx` | Manufacturers | 334 |
| `Delivery 2604 Apr.xlsx` | Delivery services | 18 |
| `Hospitality 2604 Apr.xlsx` | Hospitality licenses | 13 |
| `Transporters 2604 Apr.xlsx` | Transporters | 13 |
| `Operators 2604 Apr.xlsx` | Operators | 12 |
| `Research & Development Cultivations 2604 Apr.xlsx` | R&D | 1 |
| `Counts 2604 Apr.xlsx` | Aggregate counts only — skipped | — |
| `Testing Facilities 2604 Apr.xlsx` | Different schema — skipped | — |

**Schema — standard across all processed files:**

| Field | Description |
| :--- | :--- |
| `License_Number` | License number (primary key) |
| `Facility_Name` | Facility name |
| `DBA` | Doing business as |
| `Facility_Type` | License subtype |
| `Street` | Street address |
| `City` | City |
| `ZIP_Code` | ZIP code |
| `Expiration_Date` | License expiration date |
| `Date_Updated` | Last updated date |
| `Category` | Source file category |
| `Sheet` | Medical or Retail sheet |

**What Colorado didn't give us:** Email, phone, GPS coordinates. Leaner than California but clean.

---

## The Scripts

### `co_peek.py`
Quick inspection script — reads all Excel files and prints headers and row counts. Used during initial analysis.

### `co_build_facilities.py`
**Written by:** Amazon Q

Combines all standard-schema Excel files (both sheets per file) into master and active CSVs. Skips `Counts` and `Testing Facilities` which have different schemas. Deduplicates by license number. Active = not expired as of run date.

```bash
cd pipeline/02_state_license_retail_list/states/CO
python scripts/co_build_facilities.py
```

**Output:**

| File | Contents | Rows |
| :--- | :--- | ---: |
| `CO-facilities.csv` | All records, all categories | 1,997 |
| `CO-facilities-active.csv` | Non-expired records only | 1,956 |

**Active records by seed finder relevance:**

| Count | Category | Why It Matters |
| ---: | :--- | :--- |
| 949 | Stores | Dispensaries — seed finder primary target |
| 657 | Cultivations | USDA cross-reference candidates |
| 1 | R&D Cultivations | University/research — academic batch |

---

## The Enforcement Data

Colorado publishes Final Administrative Actions going back to 2014. Two types:

- **SAO (Stipulation, Agreement, and Order)** — settlement between MED and licensee. Acknowledges non-compliance, may include fines, suspension, or license revocation.
- **FAO (Final Agency Order)** — decision following a formal administrative hearing.

**What's in `pdf/`:**
- `MED Administrative Actions CY2025.pdf` — full year 2025 enforcement log, structured list format
- 5 individual SAO PDFs from January 2026 — actual legal documents (dense formatted text)

### `co_parse_enforcements.py`
**Written by:** Amazon Q

Parses the MED Administrative Actions PDF using `pdfplumber`. Detects date lines, extracts licensee names and license numbers, classifies SAO vs FAO, and captures fine amounts where present.

```bash
pip install pdfplumber
python scripts/co_parse_enforcements.py
```

**Output:** `CO-enforcements.csv` — 1,012 rows

**Fields:**

| Field | Description |
| :--- | :--- |
| `Source_File` | PDF filename |
| `Action_Date` | Date of action |
| `Licensee_Name` | Company or individual name |
| `License_Number` | License number where extractable |
| `Action_Type` | SAO or FAO |
| `Fine_Amount` | Dollar amount where present |

**Known noise in the output:** Digital signature lines from individual SAO PDFs, "Total Fines Assessed" summary rows, and month header rows (`Apr-25`, `May-25`, etc.) are present in the CSV. These are easy to filter by pattern when building the Datarade product — they don't contain license numbers and follow predictable formats.

**Historical enforcement data (2014–2024)** is available on the MED website as separate PDFs per year. Not collected yet — flagged for a future pipeline stage when building the full Datarade audit trail product.

---

## File Structure

```
CO/
├── csv/
│   ├── Stores 2604 Apr.xlsx
│   ├── Cultivations 2604 Apr.xlsx
│   ├── Product Manufacturers 2604 Apr.xlsx
│   ├── Delivery 2604 Apr.xlsx
│   ├── Hospitality 2604 Apr.xlsx
│   ├── Operators 2604 Apr.xlsx
│   ├── Transporters 2604 Apr.xlsx
│   ├── Research & Development Cultivations 2604 Apr.xlsx
│   ├── Counts 2604 Apr.xlsx          (skipped — aggregate only)
│   └── Testing Facilities 2604 Apr.xlsx  (skipped — different schema)
├── pdf/
│   ├── MED Administrative Actions CY2025.pdf
│   ├── 260128 SAO Dutch Botanicals LLC_Redacted.pdf
│   ├── 260128 SAO Galactic Meds LLC_Redacted.pdf
│   ├── 260128 SAO Grateful Grove LLC_Redacted.pdf
│   ├── 260128 SAO I&S LLC_Redacted.pdf
│   └── 260128 SAO P2C3 LLC_Redacted.pdf
├── scripts/
│   ├── co_peek.py
│   ├── co_build_facilities.py
│   └── co_parse_enforcements.py
├── CO-facilities.csv                  (1,997 rows)
├── CO-facilities-active.csv           (1,956 rows)
└── CO-enforcements.csv                (1,012 rows)
```

---

## Drop 3 Priority

Colorado is Drop 3 on the loyal9.app release schedule. Mature market, detailed METRC tracking, and the enforcement history makes it the most compliance-rich state in the pipeline so far. The 949 active stores are all verified operational dispensaries with expiration dates.

The enforcement data is a preview of what the Datarade premium tier looks like — a dispensary with a 2025 SAO and a fine is a compliance signal that B2B buyers will pay for.

---

## Credits

**Shannon** identified the enforcement PDFs, downloaded the individual January 2026 SAOs, and correctly called that Colorado's data was worth the extra work.

**Amazon Q** wrote three scripts, hit a naming conflict with Python's built-in `inspect` module on the first try, renamed the file, and moved on.

> *"I like to keep it real."* — Shannon
