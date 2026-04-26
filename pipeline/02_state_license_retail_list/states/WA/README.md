# Washington — State License & Retail List

**Source:** Washington State Liquor and Cannabis Board (LCB) — License Search export  
**Collected:** 2026 — downloaded by Shannon  
**Records:** 1,208 total / 457 active  
**Output:** `WA-facilities.csv`, `WA-facilities-active.csv`

---

## Source Files

| File | Records | Contents |
| :--- | :--- | :--- |
| `retailers.csv` | 1,209 | Primary — all retailer statuses, address, phone |
| `se-retailers.csv` | 1,209 | Social Equity retailers — 9 active with legal name, expiration, mailing address; rest blank rows |

---

## Data Notes

- **Full street addresses** — pre-split into Street, Suite, City, State, ZIP
- **Phone** — present on most active records
- **Historical records included** — 659 CLOSED (PERMANENT) records in the full dataset; useful for Datarade churn analysis
- **SE enrichment** — `se-retailers.csv` has 9 active SE retailers; only 2 matched by license number due to format inconsistency between files
- **`UBI`** — Unified Business Identifier; Washington's SOS cross-reference key — useful for Level 3 enrichment
- **Status breakdown:** 457 Active, 659 Closed Permanent, 87 Former Title Certificate, 3 Closed Temporary, 1 Expired

---

## Script

**`scripts/wa_build_facilities.py`** — written by Amazon Q

- Reads `retailers.csv` as primary, left-joins `se-retailers.csv` on license number
- Outputs `WA-facilities.csv` and `WA-facilities-active.csv`

---

## Output Schema

| Field | Notes |
| :--- | :--- |
| `License_Number` | LCB license number |
| `UBI` | Unified Business Identifier — SOS cross-reference key |
| `Trade_Name` | DBA / trade name |
| `Licensee` | Legal entity name (from SE file where matched) |
| `Privilege_Status` | ACTIVE (ISSUED) / CLOSED (PERMANENT) / etc. |
| `Privilege_Type` | CANNABIS RETAILER / RETAIL CERTIFICATE HOLDER |
| `Street / Suite / City / State / ZIP` | Pre-split address fields |
| `County` | Included |
| `Phone` | Day phone |
| `Expiration_Date` | From SE file where matched (YYYYMMDD format) |
| `Mailing_Address` | From SE file where matched |
| `SE_Retailer` | 1 if matched in SE file |

---

> *"I like to keep it real."* — Shannon
