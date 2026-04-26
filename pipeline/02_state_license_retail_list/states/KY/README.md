# Kentucky — Office of Medical Cannabis Pipeline

**State:** Kentucky  
**Source:** [Kentucky Office of Medical Cannabis — Licensees](https://kymedcan.ky.gov/businesses/Pages/licensees.aspx)  
**Collected:** April 1, 2026 (per page update notice)  
**Built by:** Amazon Q  
**Supervised by:** Shannon, who correctly described the source as "just text"

---

## What Kentucky Gave Us

A plain text webpage. No table. No CSV. No map. No API. Just a list of licensees organized by license type and dispensary region, with `***` marking the ones approved to operate, county names in parentheses, and paragraphs of transfer and location change history for each entry.

It was actually very parseable once you know the pattern.

---

## The Program

Kentucky's medical cannabis program launched in 2025 and is one of the youngest in the pipeline. As of April 1, 2026:

- **80 total licenses** issued across all categories
- **22 approved to operate** (`***`)
- **58 licensed but not yet operational**

The program is organized into 11 geographic regions for dispensaries. Most licensees have gone through at least one location change or ownership transfer — Kentucky's OMC has been busy approving relocations since the program launched.

**No street addresses are published.** The state only discloses county-level location. This is a known limitation of Kentucky's program transparency.

---

## The Data

**File:** `KY-facilities.csv`  
**Records:** 80  
**Source text:** `ky_licensees.txt` (copied from the OMC webpage)

**Schema:**

| Field | Description |
| :--- | :--- |
| `License_Holder` | Legal entity name |
| `DBA` | Doing business as name |
| `County` | Kentucky county (no street address available) |
| `State` | KY |
| `Approved_To_Operate` | Yes = `***` on source page / No = licensed but not open |
| `License_Type` | Safety Compliance / Cultivator Tier I-III / Processor / Dispensary |
| `Region` | Dispensary region (e.g. Region 1 Bluegrass) |

**Records by license type:**

| Count | License Type |
| ---: | :--- |
| 48 | Dispensary |
| 10 | Cultivator Tier I |
| 10 | Processor |
| 6 | Safety Compliance |
| 4 | Cultivator Tier II |
| 2 | Cultivator Tier III |

**For the seed finder:** Filter to `License_Type = Dispensary` and `Approved_To_Operate = Yes`. That gives you the 13 operational dispensaries.

**For the Datarade product:** Keep all 80 — the pipeline of licensed-but-not-open operators is signal for what's coming.

---

## The Script

**File:** `scripts/ky_parse_licensees.py`  
**Written by:** Amazon Q

Reads `ky_licensees.txt`, detects section headers and region headers, parses each licensee line using regex to extract the company name, DBA, county, and `***` approval status. Strips all the parenthetical transfer and location change history — that's noise for the CSV.

```bash
cd pipeline/02_state_license_retail_list/states/KY
python scripts/ky_parse_licensees.py
```

---

## File Structure

```
KY/
├── ky_licensees.txt           (source text — copied from OMC webpage)
├── scripts/
│   └── ky_parse_licensees.py
└── KY-facilities.csv          (80 rows)
```

---

## Seed Finder Context

Kentucky is medical-only. No adult-use program exists yet. The 13 operational dispensaries are the seed finder targets — but without street addresses, the seed finder page for Kentucky will show county-level location only until the state publishes more detail or Level 3 SOS verification fills in the gaps.

Kentucky's USDA hemp list is substantial (see `pipeline/01_usda_active_states`) — the dual-license cross-reference here would match cultivators appearing on both the USDA hemp list and the OMC cultivator list.

---

## Credits

**Shannon** copied the text off a webpage that offered nothing else and moved on.

**Amazon Q** wrote a regex parser for plain text government data and got 80 clean records out of it.

> *"I like to keep it real."* — Shannon
