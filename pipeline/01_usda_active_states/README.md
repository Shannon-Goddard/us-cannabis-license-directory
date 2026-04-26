# 01 — USDA Active States

**Written by:** Amazon Q
**Date:** March 31 – April 19, 2026
**Status:** Complete

---

## Overview

First stage of the Loyal9 Seed Registry data pipeline. Two objectives:

1. Identify every U.S. state and territory with at least one **Active** USDA hemp license — defines the scope for all downstream pipeline work.
2. Produce a clean, geocoded, schema-compliant CSV of all active USDA hemp licensees for the master registry.

---

## Source Data

**File:** `csv/USDA_search_tool.csv`
**Source:** [USDA Hemp Public Search Tool](https://hemp.ams.usda.gov/s/PublicSearchTool)
**Date Collected:** March 31, 2026
**Collection Method:** Manual copy/paste by Shannon
**Total Records:** 17,175

| Field | Description |
|---|---|
| `Business or License Holder Name` | Licensed entity or individual |
| `License Number` | Unique license identifier |
| `Regulatory Body` | Issuing agency (USDA or state department) |
| `City` | City of the license holder |
| `State` | State or territory (full name) |
| `Zip Code` | ZIP code |
| `Status` | License status |

### Status Breakdown (Raw)

| Status | Count |
|---|---|
| Expired | 12,134 |
| Active | 3,290 |
| Inactive | 1,416 |
| Surrendered | 123 |
| Active on CAP | 81 |
| (blank) | 49 |
| Revoked | 34 |
| Archived | 25 |
| Superseded | 19 |
| Suspended | 4 |

---

## Scripts

### `scripts/active_states.py`

Reads the raw CSV, filters to `Status = Active`, prints a deduplicated, sorted list of states/territories.

**Result:** 47 active states/territories identified.

**Dependencies:** Python standard library only.

### `scripts/geocode_usda.py`

Adds `Latitude` and `Longitude` to every record using Google Maps Geocoding API. Caches by `(City, State, Zip Code)` tuple — 17,175 records reduced to 9,889 unique API calls.

**Result:** 17,175 / 17,175 geocoded (100%). All records have coordinates because every record has at least a city and state.

**Dependencies:** `requests`. Requires a Google Maps API key (replace `<YOUR_GOOGLE_API_KEY>` in the script).

### `scripts/export_clean.py`

Filters `USDA_geocoded.csv` to active licenses only (`Active` + `Active on CAP`), maps fields to the plan-a registry schema, converts full state names to 2-letter codes, generates URL-safe slugs.

**Drops:** `Regulatory Body`, `Status` (all rows are active by definition).

**Result:** 3,371 active records across 47 states.

**Dependencies:** Python standard library only.

### `scripts/inspect.py`

Diagnostic — prints headers, row counts, status breakdowns, and sample rows for both the raw and geocoded CSVs.

---

## Output Files

### `csv/USDA_search_tool.csv`
Raw source data. 17,175 rows, 7 columns. Unmodified from USDA.

### `csv/USDA_geocoded.csv`
All 17,175 rows with `Latitude` and `Longitude` appended. Includes all statuses (Active, Expired, Revoked, etc.). Retained in full for the future "Audit Trail" Datarade product — expired/revoked licenses cross-referenced against active state lists can flag compliance red flags.

### `csv/usda-clean.csv`
**The clean output.** 3,371 active records mapped to the plan-a registry schema:

| Column | Source | Notes |
|---|---|---|
| `name` | Business or License Holder Name | |
| `slug` | Auto-generated | Lowercase, stripped, "the" prefix removed |
| `type` | `cultivator` | All USDA hemp licenses are grow/process |
| `url` | (blank) | USDA doesn't publish websites |
| `is_bad_url` | (blank) | |
| `city` | City | |
| `state` | State → 2-letter code | Full name converted via lookup |
| `zip_code` | Zip Code | |
| `country` | `US` | All records |
| `lat` | Latitude | From geocoding |
| `lng` | Longitude | From geocoding |
| `phone` | (blank) | USDA doesn't publish phone |
| `email` | (blank) | USDA doesn't publish email |
| `license_usda` | License Number | |

---

## 47 Active States/Territories

Alabama, Arizona, California, Colorado, Connecticut, Delaware, Georgia, Hawaii, Idaho, Illinois, Indiana, Iowa, Kansas, Kentucky, Louisiana, Maine, Maryland, Massachusetts, Michigan, Minnesota, Mississippi, Missouri, Montana, Nebraska, Nevada, New Hampshire, New Jersey, New Mexico, New York, North Carolina, North Dakota, Ohio, Oklahoma, Oregon, Pennsylvania, Puerto Rico, South Carolina, South Dakota, Tennessee, Texas, Utah, Vermont, Virginia, Washington, West Virginia, Wisconsin, Wyoming.

---

## Pipeline Context

This is **Level 1** verification in the Loyal9 data logic. The 47 active states define the scope for:
- **Pipeline 02** — State license & retail list collection
- **Pipeline 05** — Seed breeder matching

The non-active records (13,804 rows: Expired, Revoked, Surrendered, etc.) are preserved in `USDA_geocoded.csv` for reference.

---

*Built by Amazon Q. Source data collected by Shannon from the USDA Hemp Public Search Tool.*
