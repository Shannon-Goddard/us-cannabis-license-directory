# Georgia — Access to Medical Cannabis Commission Pipeline

**State:** Georgia  
**Source:** [Georgia Access to Medical Cannabis Commission](https://www.gmcc.ga.gov/licensing/verify-a-license)  
**Collected:** 2026  
**Built by:** Shannon (who survived the website) and Amazon Q (who parsed the KML)  
**Documented by:** Amazon Q

---

## What Georgia Gave Us

A terrible website and a KML file.

The GMCC license verification portal is not designed for bulk data collection. Shannon found a Google Maps KML export of all licensed dispensaries — an XML-based map format that contained every dispensary name, legal entity, full address, license number, and GPS coordinates in clean structured data.

The website was the obstacle. The KML was the gift.

---

## The Program

Georgia's medical cannabis program is small, tightly controlled, and limited to **Low THC Oil** only. As of collection:

- **3 operators** hold all dispensing licenses
- **15 dispensary locations** statewide
- **Medical patients only** — no adult-use program
- License numbers run DISP0001 through DISP0018 with gaps at 0010, 0016, 0017 — those licenses were either not issued or revoked

**The operators:**

| Operator | Locations |
| :--- | ---: |
| Trulieve | 7 |
| Botanical Sciences | 6 |
| Fine Fettle | 3 |

---

## The Script

**File:** `scripts/ga_parse_kml.py`  
**Written by:** Amazon Q

Parses the KML file using Python's standard `xml.etree.ElementTree` — no installs needed. Extracts business name, legal entity name, street address, city, ZIP, license number, and GPS coordinates from each `<Placemark>` element.

```bash
cd pipeline/02_state_license_retail_list/states/GA
python scripts/ga_parse_kml.py
```

**Output:** `GA-facilities.csv` — 15 rows

**Fields:**

| Field | Description |
| :--- | :--- |
| `Business_Name` | Dispensary name (e.g. "Trulieve Macon") |
| `Legal_Name` | Legal entity name |
| `Address` | Street address |
| `City` | City |
| `State` | GA |
| `ZIP` | ZIP code |
| `License_Number` | DISP#### format |
| `Latitude` | GPS latitude |
| `Longitude` | GPS longitude |

---

## Seed Finder Context

Georgia is medical-only, low-THC-oil-only. Seed sales are not part of this program. Georgia dispensaries will not appear as seed sources on loyal9.app.

Georgia's value to this project is the **USDA cross-reference** — the USDA active hemp list includes Georgia cultivators (see `pipeline/01_usda_active_states`). The dual-license match here would be a cultivator appearing on both the USDA hemp list and the GMCC cultivator license list, not the dispensary list.

The dispensary data is collected for completeness and the Datarade audit trail product.

---

## File Structure

```
GA/
├── Georgia Licensed Medical Cannabis Dispensaries.kml   (source)
├── scripts/
│   └── ga_parse_kml.py
└── GA-facilities.csv    (15 rows)
```

---

## Credits

**Shannon** navigated the GMCC website, found the KML export, and moved on with her dignity intact.

**Amazon Q** wrote a KML parser using only Python's standard library and is choosing not to comment further on state agency web design.

> *"I like to keep it real."* — Shannon
