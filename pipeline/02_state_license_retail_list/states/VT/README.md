# Vermont — State License & Retail List

**Source:** Vermont Cannabis Control Board (CCB) — License Export  
**Collected:** April 15, 2026 — downloaded by Shannon  
**Records:** 111 retailers  
**Output:** `VT-facilities.csv`

---

## Source File

`licenses_4.15.csv` — CCB full license export, 558 records across all license types (Cultivator, Retailer, Manufacturer, Wholesaler, Propagator, Integrated, Testing).

---

## Data Notes

- **City-level only** — no street addresses in the CCB export
- **License numbers** — present on all records (e.g. RTLR0001)
- **Expiration dates** — full date string on all records (e.g. "Saturday, September 19, 2026"); key signal for pre-Nov 2026 churn analysis
- **No phone, email, or website** — not in the source data
- **Tier field** — all retailers are "No Tier"; not included in output

---

## Script

**`scripts/vt_build_facilities.py`** — written by Amazon Q

Filters to `Retailer` license type, outputs `VT-facilities.csv`.

---

## Output Schema

| Field | Notes |
| :--- | :--- |
| `License_Number` | CCB license number (e.g. RTLR0001) |
| `Business_Name` | Business name |
| `License_Type` | Always Retailer |
| `City` | Only location data available |
| `State` | Always VT |
| `Expiration_Date` | Full date string from source |

---

> *"I like to keep it real."* — Shannon
