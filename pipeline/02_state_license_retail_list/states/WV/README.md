# West Virginia — State License & Retail List

**Source:** WV DHHR — Medical Cannabis Dispensary Locator (HTML card list)  
**Collected:** 2026 — manual copy/paste by Shannon from notes.text  
**Records:** 65 dispensaries (all operational with product)  
**Output:** `WV-facilities.csv`

---

## Source Format

The WV DHHR dispensary locator renders as Bootstrap accordion cards. Each card contains:
- `data-county` attribute — county name
- `<h3>` — DBA / trade name
- `<h4>` — full address (STREET, CITY, WV ZIP)
- Dispensary Name label + `<span>` — legal entity name
- Phone Number label + `<span>` — phone
- Operational status span

Shannon copied the full HTML (2,719 rows) into notes.text. Script parses it directly.

---

## Data Notes

- **All 65 are "Operational with product"** — no inactive records in the source
- **Phone missing on ~10 records** — some cards have no phone or "N/A"
- **2 cards have blank `<h3>`** — legal name used as DBA fallback (HCWV Sub LLC, Harvest Care Medical LLC)
- **No license numbers or expiration dates** — not published in the locator

## Key Operators

| Operator | Locations |
| :--- | :--- |
| Harvest Care Medical / Country Grown Cannabis | 10 |
| Trulieve / Trulieve WV | 8 |
| Mountaineer Releaf / The Landing | 7 |
| Greenlight / Logan Investment Partners | 7 |
| Verano WV / Zen Leaf | 4 |
| Columbia Care / Cannabist | 4 |
| New Leaf WV / Newleaf | 5 |
| Curative Growth | 3 |

---

## Script

**`scripts/wv_parse_dispensaries.py`** — written by Amazon Q

Parses Bootstrap card HTML from notes.text using regex. Extracts DBA, legal name, address, phone, county, and operational status. Splits address into Street/City/State/ZIP.

---

## Output Schema

| Field | Notes |
| :--- | :--- |
| `ID` | Card data-id from source HTML |
| `DBA` | Trade name from `<h3>` |
| `Legal_Name` | Legal entity from Dispensary Name span |
| `Full_Address` | Raw address string from `<h4>` |
| `Street` | Parsed |
| `City` | Parsed |
| `State` | Always WV |
| `ZIP` | Parsed |
| `Phone` | Where present |
| `County` | From card data-county attribute |
| `Operational_Status` | Always "Operational with product" |

---

> *"I like to keep it real."* — Shannon
