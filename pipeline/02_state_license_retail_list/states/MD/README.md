# Maryland — State License & Retail List

**Source:** Maryland Cannabis Administration (MCA) Dispensary Directory  
**URL:** https://mmcc.maryland.gov/Pages/dispensaries.aspx  
**Collected:** 2026 — manual copy/paste by Shannon  
**Records:** 91 dispensaries  
**Output:** `MD-facilities.csv`

---

## Source Format

The MCA publishes its dispensary directory as a static HTML table — no CSV download, no API. The table has 2 dispensaries per row, alternating even/odd row classes. Each cell contains:

- Dispensary logo (`<img>` with alt text, often empty)
- Business name in `<strong>` or `<b>` tags (some cells name-only, no logo)
- Street address in `<div>` or `<br>`-separated lines
- City, State ZIP
- Phone, email, website (where available — many cells have address only)

---

## Data Notes

- **No license numbers** — the MCA directory does not publish license numbers. This dataset is address/contact only.
- **No status field** — all listed dispensaries are assumed active at time of collection.
- **Phone/email/website sparse** — roughly half the records have contact info; the rest are name + address only.
- **8 blank names** — a small number of cells use logo images with empty `alt=""` and no `<strong>` tag. Shannon filled these in manually after the script ran.
- **`Curaleaf Gaithersburg`** — source HTML has a trailing comma in the city field; corrected manually.

---

## Script

**`scripts/md_parse_dispensaries.py`** — written by Amazon Q

- Input: `md_dispensaries.html` (raw HTML table saved by Shannon)
- Parser: Python `HTMLParser` with custom `CellParser` class
- Name extraction: prefers `<strong>`/`<b>` tag text, falls back to `<img alt>`, then first text line
- Handles `\u200b` zero-width space characters embedded in the source HTML
- Street deduplication: skips any line that contains the business name (case-insensitive)
- Output: `MD-facilities.csv`

---

## Output Schema

| Field | Notes |
| :--- | :--- |
| `Business_Name` | From `<strong>`, `<img alt>`, or first text line |
| `Street` | Street address lines between name and city |
| `City` | Parsed from `City, MD ZIP` pattern |
| `State` | Always `MD` |
| `ZIP` | 5-digit ZIP |
| `Phone` | Where present |
| `Email` | Where present |
| `Website` | First `http` link in cell, where present |

---

> *"I like to keep it real."* — Shannon
