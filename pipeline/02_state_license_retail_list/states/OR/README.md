# Oregon — State License & Retail List

**Source:** Oregon Liquor and Cannabis Commission (OLCC) — Cannabis Business Licenses & Endorsements  
**Collected:** 2026 — downloaded by Shannon  
**Records:** 569 total retailers / 462 active  
**Output:** `OR-facilities.csv`, `OR-facilities-active.csv`

---

## Source File

`Cannabis Business Licenses & Endorsements.csv` — OLCC full license export. UTF-16 encoded, tab-delimited inside a `.csv` wrapper. 3,526 records across all license types including producers, processors, wholesalers, and labs.

---

## Data Notes

- **No email or phone** — OLCC public export does not include contact info
- **Address in one field** — format `STREET CITY OR ZIP`; parsed by script
- **`Endorsement` field** — includes `Marijuana Home Delivery`; 309 of 462 active retailers (67%) carry this endorsement
- **`SOS Registration Number`** — Secretary of State registration number where present; useful for Level 3 SOS enrichment
- **1,149 blank rows** — Excel/export padding; filtered out by script
- **Status breakdown:** 462 Active, 107 Inactive/Expired/Cancelled/Revoked/Suspended

---

## Script

**`scripts/or_build_facilities.py`** — written by Amazon Q

- Reads UTF-16 tab-delimited file, pads ragged rows to header length
- Filters to `RECREATIONAL RETAILER` license type
- Parses single-field address into Street / City / State / ZIP
- Outputs `OR-facilities.csv` and `OR-facilities-active.csv`

---

## Output Schema

| Field | Notes |
| :--- | :--- |
| `License_Number` | OLCC license number (e.g. 050-3054) |
| `Business_Name` | DBA name |
| `Legal_Name` | Legal entity name from `Business Licenses` column |
| `License_Type` | Always RECREATIONAL RETAILER |
| `Status` | ACTIVE / INACTIVE / EXPIRED / CANCELLED / REVOKED / SUSPENDED |
| `Expiration_Date` | License expiration |
| `Street` | Parsed from address |
| `City` | Parsed from address |
| `State` | Always OR |
| `ZIP` | Parsed from address |
| `County` | Included |
| `Endorsement` | e.g. Marijuana Home Delivery |
| `SOS_Registration_Number` | Where present |

---

> *"I like to keep it real."* — Shannon
