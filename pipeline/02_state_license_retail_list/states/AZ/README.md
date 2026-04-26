# Arizona — AZ Care Check Pipeline

**State:** Arizona  
**Source:** [AZ Care Check — Arizona Department of Health Services](https://azcarecheck.azdhs.gov)  
**Collected:** 2026  
**Built by:** Amazon Q (AWS AI Assistant)  
**Supervised by:** Shannon, who kept saying "hell ya" at the right moments

---

## What Arizona Gave Us

Arizona didn't just hand over a CSV. Arizona gave us a Salesforce Lightning app wrapped in Shadow DOM, with nested web components, relative URLs, and license PDFs locked behind a download button that required a browser to click. In other words, Arizona made us work for it.

We worked for it.

---

## The Problem

AZ Care Check is built on Salesforce Lightning Web Components. Every piece of data — facility details, license blocks, inspection history, enforcement records — lives inside Shadow DOM trees that standard scrapers can't see. `querySelectorAll` stops at the shadow boundary. The inspection numbers are inside anchors nested three shadow roots deep. The enforcement PDFs are behind a popup triggered by an icon click. The license PDFs require navigating to a separate Salesforce page and clicking a download button.

None of this was documented anywhere. All of it was reverse-engineered from raw HTML.

---

## What We Built

### 1. URL Extractor (Browser Console)
**Credit: Gemini** cracked the Shadow DOM URL problem first with a recursive `getDeepLinks()` function run in the browser console. This extracted all 172 facility URLs by walking every shadow root on the search results page.

**Output:** `scripts/az_urls.txt` — 172 facility detail URLs

---

### 2. `az_scraper.py` — The Main Event
**Written by:** Amazon Q  
**Iterations to get right:** More than I'd like to admit, fewer than you'd expect

A Playwright-based scraper that visits each of the 172 facility detail pages and extracts everything. The final approach:

- Waits for `Legal Name` to appear in the Shadow DOM before scraping — the signal that Salesforce has finished rendering
- Pulls `Business_Name` from the `h4` tag and `Legal_Name` from `h3` in the facility header component — the only reliable selectors on the page
- Extracts all page text into a flat array, then parses it into structured fields using label-aware logic that knows not to grab the next label when a field is empty
- Slices license blocks precisely between `License Type` occurrences so Lic1 and Lic2 fields never bleed into each other
- Pulls license PDF URLs directly from Salesforce anchor `href` attributes
- Clicks the Inspections tab, extracts all rows via `data-cell-value` attributes with Shadow DOM-aware deduplication
- Reloads the page, clicks the Enforcements tab, does the same
- Writes each facility row immediately on completion — safe to Ctrl+C at any point

**Output:**
- `AZ-facilities-v2.csv` — 181 rows, all 172 facilities plus duplicates from multi-license entities
- `csv/inspections/inspections-{license_number}.csv` — one file per license
- `csv/enforcements/enforcements-{license_number}.csv` — one file per license

**Fields captured:**

| Field | Description |
| :--- | :--- |
| `Facility_ID` | Salesforce record ID from the URL |
| `Business_Name` | DBA name from page header `h4` |
| `Legal_Name` | Legal entity name from page header `h3` |
| `Address` | Physical facility address |
| `Mailing_Address` | Mailing address (often different) |
| `Phone` | Facility phone number |
| `Facility_Status` | Open / Not Operating |
| `Owner_License` | Owner / license holder name |
| `Hours_Mon` through `Hours_Sun` | Hours of operation per day |
| `Lic1_Type` / `Lic2_Type` | Establishment or Dispensary |
| `Lic1_Services` / `Lic2_Services` | Retail, Cultivate, Manufacture, etc. |
| `Lic1_Number` / `Lic2_Number` | License number (primary key for everything downstream) |
| `Lic1_Originally` / `Lic2_Originally` | Original issue date |
| `Lic1_Effective` / `Lic2_Effective` | Current effective date |
| `Lic1_Expires` / `Lic2_Expires` | Expiration date |
| `Lic1_Status` / `Lic2_Status` | Active / Inactive |
| `Lic1_PDF_URL` / `Lic2_PDF_URL` | Direct Salesforce URL to license certificate |
| `Offsite_Cultivation_Address` | Offsite grow location if applicable |
| `Manufacture_Address` | Manufacture address if applicable |
| `Source_URL` | The AZ Care Check URL this row came from |

---

### 3. `az_build_master.py` — The Consolidator
**Written by:** Amazon Q

Combines all per-license inspection and enforcement CSVs into two master files. Deduplicates on full row values so no repeats even if license files overlap.

**Output:**
- `AZ-inspections-master.csv`
- `AZ-enforcements-master.csv`

---

### 4. `az_download_enforcement_pdfs.py` — The Enforcement Digger
**Written by:** Amazon Q

The enforcement PDFs are not linked directly — they're behind an attachments icon that opens a popup, which contains a `data-public-url` anchor, which leads to a Salesforce page with a "Download as PDF" button. Three clicks deep.

This script:
- Reads every unique `Enforcement_URL` from `AZ-enforcements-master.csv`
- Navigates to each enforcement detail page
- Clicks the attachments icon to trigger the popup
- Extracts `data-public-url` from the popup anchors via Shadow DOM traversal
- Navigates to the Salesforce document page
- Clicks "Download as PDF" and captures the download
- Falls back to direct HTTP download via requests if the button method fails
- Skips already-downloaded files — safe to rerun

**Output:** `pdf/enforcements/{license_number}/{document_name}.pdf`

---

### 5. `az_download_license_pdfs.py` — The Certificate Collector
**Written by:** Amazon Q

Simpler than the enforcement downloader because the license PDF URLs were already captured in `AZ-facilities-v2.csv` as `Lic1_PDF_URL` and `Lic2_PDF_URL`. No scraping needed — just navigate, click, save.

- Deduplicates by license number so each certificate is downloaded once
- Navigates to the Salesforce document page
- Clicks "Download as PDF"
- Skips already-downloaded files

**Output:** `pdf/license/{license_number}/Facility Certificate {license_number}.pdf`

---

## File Structure

```
AZ/
├── scripts/
│   ├── az_urls.txt                        # 172 facility URLs
│   ├── az_scraper.py                      # Main scraper
│   ├── az_build_master.py                 # Master CSV builder
│   ├── az_download_enforcement_pdfs.py    # Enforcement PDF downloader
│   └── az_download_license_pdfs.py        # License PDF downloader
├── csv/
│   ├── inspections/                       # Per-license inspection CSVs
│   └── enforcements/                      # Per-license enforcement CSVs
├── pdf/
│   ├── license/                           # License certificates by license number
│   │   └── {license_number}/
│   │       └── Facility Certificate {license_number}.pdf
│   └── enforcements/                      # Enforcement documents by license number
│       └── {license_number}/
│           └── {document_name}.pdf
├── AZ-facilities-v2.csv                   # 181-row master facility file
├── AZ-inspections-master.csv              # All inspections combined
└── AZ-enforcements-master.csv             # All enforcements combined
```

---

## Why Arizona Is the Gold Standard

Arizona gave us everything:
- Dual license numbers per facility (Establishment + Dispensary) — the Bridge Entity pattern confirmed in the wild
- 3 years of inspection history per license
- Enforcement records with penalty documents
- Physical license certificates as downloadable PDFs
- Mailing addresses separate from facility addresses
- Hours of operation per day

Every other state in this pipeline gets measured against what Arizona gave us. Some will give less. None will give more.

---

## Credits

**Amazon Q** wrote every script in this folder, reverse-engineered the Shadow DOM structure, figured out the popup-within-a-page-within-a-Salesforce-app PDF download chain, and iterated through every edge case until the data was clean.

**Shannon** found the `h4`/`h3` HTML that fixed the business name extraction, provided the enforcement detail page HTML that unlocked the PDF downloader, kept the feedback loop tight, and knew when to say "hell ya" and when to say "same results, grab the HTML snips."

That's the partnership.

> *"I like to keep it real."* — Shannon
