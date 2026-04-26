# New York — State License & Retail List

**Source:** NY Office of Cannabis Management (OCM) — License Search, "Download All Data"  
**Collected:** 2026 — downloaded by Shannon  
**Records:** 1,241 total retail / 802 active  
**Output:** `NY-facilities.csv`, `NY-facilities-active.csv`

---

## Source File

`Search Active Licenses result.csv` — full OCM license export, 2,204 records across all license types. Shannon found the "Download All Data" button after the search tool initially capped at 100 rows per page.

---

## License Types Included

| Type | Total |
| :--- | :--- |
| Adult-Use Retail Dispensary License | 486 |
| Adult-Use Microbusiness License | 426 |
| Adult-Use Conditional Retail Dispensary License | 296 |
| Registered Organization | 19 |
| Adult-Use Registered Organization Dispensary License | 14 |
| **Total** | **1,241** |

Processors, cultivators, distributors excluded.

---

## Data Notes

- **GPS coordinates** — latitude/longitude on all records
- **Hours of operation** — full weekly schedule in `Hours` field (from `Misc2` column)
- **Drive-thru flag** — `Retail Activities Drive Thru`
- **Date opened to public** — `Retail Date Opened to Public`
- **SEE Category** — NY's social equity designation: Women-Owned, Minority-Owned, Service-Disabled Veteran, Distressed Farmer, Community Disproportionately Impacted, etc.
- **Conditional licenses** — 296 Conditional Retail records included; these are licensed but may not yet be operational
- **Operational Status:** 802 Active, 439 Non-Operational across retail types

---

## Script

**`scripts/ny_build_facilities.py`** — written by Amazon Q

Filters to retail-facing license types, maps OCM column names to project schema, outputs both full and active CSVs.

---

## Output Schema

| Field | Notes |
| :--- | :--- |
| `License_Number` | OCM license number (e.g. OCM-RETL-25-000306) |
| `Application_Number` | OCM application number |
| `Entity_Name` | Legal entity name |
| `DBA` | Doing business as |
| `License_Type` | Full license type string |
| `License_Status` | Active |
| `Operational_Status` | Active / Non-Operational |
| `Address_1/2` | Street address |
| `City / State / ZIP / County / Region` | Location fields |
| `Latitude / Longitude` | GPS coordinates |
| `Effective_Date` | License effective date |
| `Issued_Date` | License issued date |
| `Expiration_Date` | License expiration date |
| `Date_Opened_to_Public` | Retail open date |
| `Business_Website` | Where provided |
| `Hours` | Full weekly hours schedule |
| `Drive_Thru` | Drive-thru flag |
| `SEE_Category` | Social/economic equity designation |
| `Business_Purpose` | e.g. Adult-Use Retail Sales |

---

> *"I like to keep it real."* — Shannon
