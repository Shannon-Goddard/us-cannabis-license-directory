# New Jersey — State License & Retail List

**Source:** NJ Cannabis Regulatory Commission — Dispensary Map (hardcoded JS data)  
**Collected:** 2026 — extracted by Shannon from map page source  
**Records:** 301 dispensaries  
**Output:** `NJ-facilities.csv`

---

## Source File

`nj-dispensaries.csv` — extracted from the CRC dispensary map page JavaScript data object. Contains name, full address, and type tags for all 301 mapped locations.

---

## What NJ Sucks At

The official permitted businesses page (nj.gov/cannabis/businesses/permitted/) shows a 100-row-limited table. Each row links to an individual PDF license (e.g. `Funk Recreational License.pdf`) which contains the actual license number, facility address, and expiration date — but there are 4,000+ of them and they require clicking one at a time. No bulk download.

The map page was the practical alternative — 301 records in one shot.

---

## Data Notes

- **No license numbers** — only available in individual PDFs
- **No expiration dates** — same issue
- **No status field** — map only shows active/permitted locations; all 301 assumed active
- **Type flags parsed from pipe-delimited tag string:**

| Flag | Count |
| :--- | :--- |
| Recreational | 295 |
| Medical | 58 |
| Delivery | 82 |
| Microbusiness | 65 |

---

## Script

**`scripts/nj_build_facilities.py`** — written by Amazon Q

- Strips JS artifact single-quote wrapping from all values
- Parses `Street, City, NJ ZIP, USA` address format
- Splits pipe-delimited type tags into boolean flag columns
- Outputs `NJ-facilities.csv`

---

## Output Schema

| Field | Notes |
| :--- | :--- |
| `Business_Name` | Dispensary name |
| `Street` | Parsed from address |
| `City` | Parsed from address |
| `State` | Always NJ |
| `ZIP` | Parsed from address |
| `Recreational` | 1 if tagged |
| `Medical` | 1 if tagged |
| `Delivery` | 1 if offers delivery |
| `Microbusiness` | 1 if microbusiness |
| `Consumption_Area` | 1 if cannabis consumption area |
| `Raw_Type` | Original type string |

---

> *"I like to keep it real."* — Shannon
