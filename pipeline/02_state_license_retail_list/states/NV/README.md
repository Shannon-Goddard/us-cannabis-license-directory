# Nevada — State License & Retail List

**Source:** Nevada Cannabis Compliance Board (CCB) — License List Excel workbook  
**Collected:** 2026 — downloaded by Shannon, saved as 3 CSVs  
**Records:** 132 total dispensaries / 106 active  
**Output:** `NV-facilities.csv`, `NV-facilities-active.csv`

---

## Source Files

| File | Contents |
| :--- | :--- |
| `active-license-list.csv` | Active licenses — all types |
| `conditional-licenses.csv` | Conditional licenses — all types |
| `surrendered-revoked-licenses.csv` | Surrendered / revoked — all types |

Original source was a 3-tab Excel workbook. Shannon saved each tab as a separate CSV.

---

## License Types Included

`Retail Dispensary` + `Medical Dispensary` only.

Other types in the source (Retail Cultivation, Retail Production, Retail Distributor, Retail Lounge, labs, transporters) excluded.

---

## Data Notes

- **No address, phone, or email** — the CCB public license list only provides county-level location
- **`CE_ID`** — establishment ID (e.g. `RD374`, `C126`); useful as a secondary cross-reference key
- **424 empty rows** in the source — Excel padding from the 3-tab workbook; filtered out by script
- **Status breakdown:** 106 Active, 22 Conditional, 3 Surrendered, 1 Non-Operational

---

## Script

**`scripts/nv_build_facilities.py`** — written by Amazon Q

- Reads all three CSVs, skips empty rows, filters to dispensary types
- Combines into single output with `Source_File` tag
- Outputs `NV-facilities.csv` and `NV-facilities-active.csv`

---

## Output Schema

| Field | Notes |
| :--- | :--- |
| `License_Number` | CCB license number |
| `CE_ID` | Establishment ID |
| `Business_Name` | License name |
| `License_Type` | Retail Dispensary / Medical Dispensary |
| `License_Status` | Active / Conditional / Surrendered / Non-Operational |
| `County` | Only location data available |
| `State` | Always NV |
| `Source_File` | Which of the 3 CSVs the record came from |

---

> *"I like to keep it real."* — Shannon
