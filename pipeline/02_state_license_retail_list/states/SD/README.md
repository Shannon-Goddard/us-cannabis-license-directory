# South Dakota — State License & Retail List

**Source:** South Dakota Department of Health — Certified Establishments directory  
**Collected:** 2026 — manual copy/paste by Shannon from notes.text  
**Records:** 62 dispensaries  
**Output:** `SD-facilities.csv`

---

## Data Notes

- **City-level only** — the SD DOH certified establishments page lists legal name, DBA, and city. No street addresses, no phone, no license numbers, no expiration dates.
- **Inspection reports exist** but are vague on addresses — not useful for this pipeline.
- **No script needed** — written directly to CSV from notes.text.
- **Genesis Farms dominates** — appears 18 times across 10+ cities; largest operator in the state by location count.
- **Puffy's LLC** — 5 locations across Rapid City and Sturgis.
- **Royzzz** — 5 locations across North Sioux City, Sioux Falls, Watertown, Yankton.

---

## Output Schema

| Field | Notes |
| :--- | :--- |
| `Legal_Name` | Registered legal entity name |
| `DBA` | Doing business as |
| `City` | Only location data available |
| `State` | Always SD |

---

> *"I like to keep it real."* — Shannon
