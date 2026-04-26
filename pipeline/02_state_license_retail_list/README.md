# 02 — State License & Retail List

**Written by:** Amazon Q
**Date:** April 2026
**Status:** Complete — `state-clean.csv` pending Shannon's manual review

---

## Overview

Second stage of the pipeline. Shannon visited 25 state regulatory portals, downloaded their licensed cannabis facility lists (CSV or PDF), and dropped them into per-state folders. Amazon Q wrote `build_master.py` to merge all 25 states into a single master file with a unified schema.

---

## Source Data

**File:** `official_state_license_portals.csv`
**Contents:** 25 state regulatory portal URLs with agency names and download dates.

### Per-State Raw Data (`states/` folder)

Each state has its own subfolder containing the raw CSV or PDF downloaded from the state's regulatory portal. 25 states collected:

AL, AZ, CA, CO, CT, GA, IL, KY, MA, MD, MI, MO, MS, ND, NJ, NM, NV, NY, OK, OR, SD, UT, VT, WA, WV

These raw files are preserved as-is — they are the audit trail back to the original government source.

---

## Scripts

### `scripts/build_master.py`

Merges all per-state CSVs into two master files with a unified 20-column schema:

- `master-facilities.csv` — all records, all statuses (29,633 rows)
- `master-facilities-active.csv` — active licenses only (14,507 rows)

Active status detection handles state-specific values: `Active`, `ACTIVE`, `Open` (AZ), `License Issued` (AL), blank status (states without status fields).

**Dependencies:** Python standard library only.

### `scripts/check_master.py`

Diagnostic — validates the master files after build.

### `scripts/geocode.py`

Adds `Latitude` and `Longitude` to records in the master files. Originally pipeline 03 — moved here to keep everything self-contained.

- **Primary:** US Census Geocoder batch API (free, no key, up to 10k rows/batch)
- **Fallback:** Google Maps Geocoding API (requires API key)
- Caches by city/ZIP — 17,175 USDA records reduced to 9,889 unique API calls
- Writes coordinates back into both `master-facilities.csv` and `master-facilities-active.csv`

**Dependencies:** `requests`. Requires a Google Maps API key for fallback (replace `<YOUR_GOOGLE_API_KEY>` in the script).

**Results (already applied):**
- State master: 7,121 geocoded. 6,542 permanently ungeocodable (CA confidential addresses, NV/IL/MD/OR missing data).
- USDA: 17,175 / 17,175 geocoded (100%).

### `scripts/export_clean.py`

Maps `master-facilities-active.csv` to the plan-a registry schema (`schema.csv`). Classifies each record's `License_Type` into entity types:

| License_Type contains | Assigned type |
|---|---|
| retail, store, dispensary, retailer | `dispensary` |
| cultiv, grow, nursery, outdoor, indoor, mixed-light | `cultivator` |
| university, research, academic, college | `academic` |
| distributor, manufacturer, processor, microbusiness, or none of the above | `other` |

Records with both cultivator and dispensary keywords get `cultivator|dispensary` (vertically integrated).

Keeps both `Business_Name` (as `name`) and `Legal_Name` (as `dba`) for downstream fuzzy matching and deduplication.

Falls back to `Source_State` when `State_Code` is missing or invalid.

**Output:** `state-clean.csv`

### `scripts/inspect.py`

Diagnostic — prints headers, row counts, status breakdowns, state counts, license type distribution, and checks all scripts for exposed API keys.

### `scripts/verify_clean.py`

Diagnostic — spot-checks `state-clean.csv` for data quality: empty names, bad slugs, bad state codes, DBA logic, junk addresses, bare rows.

---

## Output Files

### `master-facilities.csv`
All 29,633 records across all statuses. 20 columns. Preserved for reference — includes inactive, expired, and revoked licenses.

### `master-facilities-active.csv`
14,507 active records. Same 20 columns. The input for `export_clean.py`.

### `state-clean.csv`
**The clean output.** 14,507 active records mapped to the plan-a registry schema:

| Column | Source | Notes |
|---|---|---|
| `name` | `Business_Name` | Display name |
| `dba` | `Legal_Name` | Blank if same as name |
| `slug` | Auto-generated | From name |
| `type` | From `License_Type` | dispensary, cultivator, academic, other, or combined |
| `url` | `Website` | |
| `is_bad_url` | (blank) | |
| `street_address` | `Street` | |
| `city` | `City` | |
| `state` | `State_Code` | 2-letter, fallback to `Source_State` |
| `zip_code` | `ZIP` | |
| `country` | `US` | All records |
| `lat` | `Latitude` | |
| `lng` | `Longitude` | |
| `phone` | `Phone` | |
| `email` | `Email` | |
| `license_state` | `License_Number` | |

### Data Coverage

| Field | Count | % of 14,507 |
|---|---|---|
| Has address | 13,947 | 96.1% |
| Has phone | 9,275 | 63.9% |
| Has email | 8,147 | 56.2% |
| Has website | 333 | 2.3% |
| Has lat/lng | 7,965 | 54.9% |
| Has DBA | 9,497 | 65.5% |

### Type Breakdown

| Type | Count |
|---|---|
| dispensary | 5,563 |
| cultivator | 4,662 |
| other | 3,823 |
| cultivator\|dispensary | 459 |

### States (22)

AL (9), AZ (181), CA (7,710), CO (1,997), CT (55), GA (15), IL (482), KY (22), MA (397), MD (91), MI (935), MO (223), ND (8), NJ (301), NV (106), NY (802), OR (462), SD (62), UT (15), VT (111), WA (458), WV (65)

---

## Pipeline Context

This is **Level 2** in the Loyal9 data logic — state-licensed cannabis businesses. These records are the primary dataset for the seed finder map (dispensaries, cultivators, and institutions).

The `states/` folder and raw master files are preserved for audit purposes. The per-state PDFs and CSVs are the original government source documents.

---

*Built by Amazon Q. Source data collected by Shannon from 25 state regulatory portals.*
