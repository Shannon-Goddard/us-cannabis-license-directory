# Michigan — State License & Retail List

**Source:** Michigan Cannabis Regulatory Agency (CRA) — Public License Search  
**Collected:** April 18, 2026 — downloaded by Shannon  
**Records:** 1,905 total retail / 935 active  
**Output:** `MI-facilities.csv`, `MI-facilities-active.csv`

---

## Source Files

| File | Records | Contents |
| :--- | :--- | :--- |
| `RecordList20260418-adult-use.csv` | 5,416 | All adult-use license types |
| `RecordList20260418-medical.csv` | 4,267 | All medical license types |

---

## License Types Included

| Type | Source | Active |
| :--- | :--- | :--- |
| Marihuana Retailer | Adult-use | ~847 |
| Marihuana Microbusiness | Adult-use | included |
| Class A Marihuana Microbusiness | Adult-use | included |
| Provisioning Center | Medical | ~88 |

Adult-use total active: **847** — Medical total active: **88**

---

## Data Notes

- **No email or phone** — the CRA public download does not include contact info
- **Address in one field** — format is `Street, City MI ZIP`; parsed by script into separate columns
- **`Home_Delivery` flag** — present on medical records only
- **`Disciplinary_Action`** — populated where applicable; useful for Datarade compliance tier
- **`Notes`** — sparse but preserved
- **Statuses in full dataset:** Active, License Void, Closed - Suspended

---

## Script

**`scripts/mi_build_facilities.py`** — written by Amazon Q

- Filters adult-use file for Retailer + Microbusiness types
- Filters medical file for Provisioning Center
- Parses single-field address into Street / City / State / ZIP
- Tags each record with `Source` = adult-use or medical
- Outputs `MI-facilities.csv` and `MI-facilities-active.csv`

---

## Output Schema

| Field | Notes |
| :--- | :--- |
| `License_Number` | CRA record number (e.g. AU-R-001544) |
| `Business_Name` | License name |
| `License_Type` | Full record type string |
| `License_Status` | Active / License Void / Closed - Suspended |
| `Street` | Parsed from address field |
| `City` | Parsed from address field |
| `State` | Always MI |
| `ZIP` | Parsed from address field |
| `Expiration_Date` | License expiration |
| `Home_Delivery` | Medical records only |
| `Disciplinary_Action` | Where present |
| `Notes` | Where present |
| `Source` | adult-use or medical |

---

> *"I like to keep it real."* — Shannon
