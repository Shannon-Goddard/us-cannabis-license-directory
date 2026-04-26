# Utah — State License & Retail List

**Source:** Utah Department of Health & Human Services — Medical Cannabis Pharmacy Locator  
**Collected:** 2026 — manual copy/paste by Shannon from notes.text  
**Records:** 15 pharmacies  
**Output:** `UT-facilities.csv`

---

## Data Notes

- **Medical-only state** — Utah has no adult-use program; all locations are licensed medical cannabis pharmacies
- **15 pharmacies statewide** — small market, tightly regulated
- **Full contact info** — name, address, phone, email, and website on all 15 records
- **Home delivery flagged** — 6 of 15 pharmacies offer home delivery (Curaleaf Lehi, Curaleaf Provo, Dragonfly Wellness SLC, The Flower Shop Logan, The Flower Shop Ogden, WholesomeCo)
- **No license numbers** — not published in the state directory
- **No script needed** — written directly to CSV from notes.text
- **Other CSVs in `/csv`** — downloaded by Shannon but contained no useful dispensary data

---

## Operators

| Operator | Locations |
| :--- | :--- |
| Curaleaf | 4 |
| The Flower Shop | 2 |
| Beehive Farmacy | 2 |
| Bloc Pharmacy | 2 |
| Dragonfly Wellness | 2 |
| The Forest | 1 |
| WholesomeCo Cannabis | 1 |
| Zion Medicinal | 1 |

---

## Output Schema

| Field | Notes |
| :--- | :--- |
| `Business_Name` | Pharmacy name including location suffix |
| `Street` | Street address |
| `City` | City |
| `State` | Always UT |
| `ZIP` | ZIP code |
| `Phone` | Direct from source |
| `Email` | Direct from source |
| `Website` | Direct from source |
| `Home_Delivery` | 1 if offers home delivery |
| `License_Type` | Medical Cannabis Pharmacy |

---

> *"I like to keep it real."* — Shannon
