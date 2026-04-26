# Massachusetts — State License & Retail List

**Source:** Massachusetts Cannabis Control Commission (CCC) — Open Data Portal  
**Collected:** 2026 — downloaded by Shannon  
**Records:** 418 total retailers / 397 active  
**Output:** `MA-facilities.csv`, `MA-facilities-active.csv`

---

## Source Files

| File | Records | Contents |
| :--- | :--- | :--- |
| `comm-ops.csv` | 772 | Primary — email, phone, GPS, county, active status, license dates |
| `hmwt-yiqy.csv` | 1,725 | Enrichment — suspension, revocation, surrendered dates, full application timeline |
| `Licensing Tracker - Cannabis Control Commission Massachusetts.csv` | 767 | CCC public tracker — used for initial scoping only |

The CCC publishes multiple open datasets. `comm-ops.csv` is the operational license file with geocoded addresses. `hmwt-yiqy.csv` is the full application/compliance history file.

---

## Data Notes

- **GPS coordinates** — `latitude` and `longitude` present on all active records (geocoded by CCC against establishment address)
- **Email and phone** — populated on the majority of records directly from the CCC dataset
- **County** — pre-populated by CCC geocoder
- **Expiration dates** — all 397 active records have `LIC_EXPIRATION_DATE` (key signal for pre-Nov 2026 churn analysis)
- **Suspension/revocation** — joined from `hmwt-yiqy.csv`; no active records currently suspended
- **License types filtered** — `Marijuana Retailer` + `Medical Marijuana Retailer` only; cultivators, manufacturers, labs, transporters excluded

---

## Script

**`scripts/ma_build_facilities.py`** — written by Amazon Q

- Reads `comm-ops.csv` filtered to retailer license types
- Left-joins `hmwt-yiqy.csv` on `LICENSE_NUMBER` for suspension/revocation enrichment
- Outputs `MA-facilities.csv` (all statuses) and `MA-facilities-active.csv` (Active only)

---

## Output Schema

| Field | Source |
| :--- | :--- |
| `Business_Name` | `comm-ops.csv` |
| `License_Number` | `comm-ops.csv` |
| `License_Type` | `comm-ops.csv` |
| `License_Status` | `comm-ops.csv` — Active / Expired / Surrendered |
| `Establishment_Address_1/2` | `comm-ops.csv` |
| `Establishment_City/State/ZIP` | `comm-ops.csv` |
| `Business_Email` | `comm-ops.csv` |
| `Business_Phone` | `comm-ops.csv` |
| `County` | `comm-ops.csv` — CCC geocoder |
| `Latitude` / `Longitude` | `comm-ops.csv` — CCC geocoder |
| `Lic_Start_Date` | `comm-ops.csv` |
| `Lic_Expiration_Date` | `comm-ops.csv` |
| `Commence_Operations_Date` | `comm-ops.csv` |
| `Suspension_Start_Date` | `hmwt-yiqy.csv` |
| `Suspension_End_Date` | `hmwt-yiqy.csv` |
| `Revocation_Date` | `hmwt-yiqy.csv` |
| `Surrendered_Date` | `hmwt-yiqy.csv` |
| `Priority_Status` | `comm-ops.csv` |
| `EIN_TIN` | `comm-ops.csv` |

---

> *"I like to keep it real."* — Shannon
