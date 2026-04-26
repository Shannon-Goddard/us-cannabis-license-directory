# Illinois — Department of Financial and Professional Regulation Pipeline

**State:** Illinois  
**Source:** [Illinois IDFPR — Licensed Adult Use Dispensaries](https://idfpr.illinois.gov/profs/adultusecan.html)  
**Collected:** 2026  
**Built by:** Amazon Q (script) with Gemini providing the document analysis  
**Supervised by:** Shannon

---

## What Illinois Gave Us

A 37-page PDF titled "Combined License List" from the Illinois Department of Financial and Professional Regulation. No CSV export, no API, no bulk download — just a PDF with three sections of tabular data, multi-line cells, and page breaks mid-record.

Gemini analyzed the document structure and described the parsing challenges. Amazon Q wrote the script. The PDF gave up 482 records.

---

## The Program

Illinois has one of the most active adult-use cannabis markets in the country. The license list contains three sections:

| Section | Credential Suffix | Description |
| :--- | :--- | :--- |
| Active Adult Use Dispensing Organization Licenses | `-AUDO` | Operational dispensaries with full address data |
| Original Lottery Conditionals | `-CL` | Licenses awarded, facilities not yet open |
| SECL Conditionals | `-CL` | Social Equity Cannabis License conditionals |

**The `-CL` records have no address** — they're licenses in hand but the physical location hasn't been finalized or approved yet. Same pattern as Alabama's stayed licenses and Connecticut's PROVISIONAL records.

---

## The Data

**File:** `IL-facilities.csv`  
**Records:** 482 total  
**Active dispensaries with addresses:** ~230 (`-AUDO` records)  
**Conditional licenses (no address):** ~250 (`-CL` records)

**Schema:**

| Field | Description |
| :--- | :--- |
| `License_Holder` | Legal entity name |
| `Dispensary_Name` | DBA / brand name |
| `Street` | Street address |
| `City` | City |
| `State` | IL |
| `ZIP` | ZIP code |
| `Phone` | Phone number |
| `License_Issue_Date` | Date license was issued |
| `Credential_Number` | Unique state ID (e.g. `284.000001-AUDO`) |
| `License_Section` | Active Adult Use |

**For the seed finder:** Filter to `Credential_Number` ending in `-AUDO` and non-empty `Street`. That gives you the operational dispensaries.

**For the Datarade product:** Keep all 482 — the `-CL` records show which operators are coming online and represent pipeline signal.

---

## The Script

**File:** `scripts/il_parse_licenses.py`  
**Written by:** Amazon Q  
**Document analysis by:** Gemini

Uses `pdfplumber` to extract tables from the PDF. Handles multi-line cells by joining address components, extracts phone numbers from the address block using regex, and parses city/state/ZIP from the combined address field.

```bash
pip install pdfplumber
cd pipeline/02_state_license_retail_list/states/IL
python scripts/il_parse_licenses.py
```

**Known parsing quirks:**
- A small number of records have city/ZIP in the street field when the PDF address was formatted unusually — this is a PDF layout issue, not a script error
- Some records have the dispensary name in the credential field when the PDF table cell alignment shifted — these are identifiable by the `-CL` suffix pattern

---

## File Structure

```
IL/
├── pdf/
│   └── all-cannabis-licenses.pdf    (source — 37 pages)
├── scripts/
│   └── il_parse_licenses.py
└── IL-facilities.csv                (482 rows)
```

---

## Credits

**Shannon** downloaded the PDF and kept moving.

**Gemini** analyzed the document structure and described the parsing challenges accurately — the multi-line cell warning was correct and saved iteration time.

**Amazon Q** wrote the parser, handled the table extraction with pdfplumber fallback to text parsing, and got 482 records out of a 37-page government PDF.

> *"I like to keep it real."* — Shannon
