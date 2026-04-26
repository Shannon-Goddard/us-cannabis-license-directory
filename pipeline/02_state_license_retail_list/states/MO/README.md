# Missouri — State License & Retail List

**Source:** Missouri DHSS — Dispensary Map (ArcGIS export)  
**Collected:** 2026 — "Download Map Data" button by Shannon  
**Records:** 223 dispensaries  
**Output:** `MO-facilities.csv`

---

## Source File

`dispensary_map_arcgis_current.csv` — direct ArcGIS map data export. Already clean, no parsing needed.

---

## Data Notes

- **GPS coordinates** — latitude/longitude on every record
- **Phone** — populated on all records
- **Address pre-split** — Street, City, ZIP already in separate columns
- **County** — included
- **`Last_Updated`** — per-record date from the map layer (e.g. "March 11, 2026")
- **No email** — not in the source data
- **No license status field** — map only shows active dispensaries; all 223 assumed active at time of collection

---

## Script

**`scripts/mo_build_facilities.py`** — written by Amazon Q

Passthrough rename from ArcGIS column names to project schema. No parsing required — the state did the work.

---

## Output Schema

| Field | Notes |
| :--- | :--- |
| `Business_Name` | From `Dispensary` column |
| `License_Number` | CRC license number (e.g. DIS000143) |
| `Street` | Pre-split by source |
| `City` | Pre-split by source |
| `State` | Always MO |
| `ZIP` | Pre-split by source |
| `County` | Included |
| `Phone` | Direct from source |
| `Latitude` / `Longitude` | ArcGIS coordinates |
| `Last_Updated` | Map layer update date per record |

---

> *"I like to keep it real."* — Shannon
