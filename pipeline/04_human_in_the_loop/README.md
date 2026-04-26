# 04 — Human in the Loop

**Reviewer:** Shannon
**Date:** April–May 2026
**Status:** USDA verified ✅ | Seedfinder verified ✅ | State verified ✅

---

## Overview

Every dataset in this project passes through Shannon's manual review before it enters the master registry. This pipeline is where the clean exports from pipelines 01–03 get verified by a human — row by row.

The input files are the schema-compliant CSVs produced by the upstream pipelines. The output files are the verified versions that feed into pipeline 05 (seed breeders) and the final master registry.

---

## Input Files

| File | Source Pipeline | Rows |
|---|---|---|
| `input/usda-clean.csv` | Pipeline 01 | 3,371 |
| `input/state-clean.csv` | Pipeline 02 | 14,507 |
| `input/seedfinder-clean.csv` | Pipeline 03 | 487 |
| `input/2026-AMS-00094-F Final Response Records_Redacted.xlsx` | USDA FOIA response | Reference |

---

## Output Files

| File | Rows | Status |
|---|---|---|
| `output/usda-verified.csv` | 3,371 | ✅ Complete |
| `output/seedfinder-verified.csv` | 487 | ✅ Complete |
| `output/state-verified.csv` | ~13,030 | ✅ Complete (condensed from 14,507) |
| `output/aeterna-locations.csv` | 100 | Reference only — not added to state data |

---

## Review Notes

### `usda-verified.csv`

**Source:** `usda-clean.csv` (3,371 active USDA hemp licensees)

Shannon's review found:

- **164 incomplete zip codes** in the original USDA data. These were not caused by our pipeline — the USDA source data itself had partial/truncated zip codes. Shannon deleted the bad values and left the field blank.

- **FOIA zip code fill:** Amazon Q wrote `scripts/fill_zip.py` to match `license_usda` against the USDA FOIA response file. Result: 161 of 164 missing zips recovered.

- **Geo verification:** Amazon Q wrote `scripts/check_geo.py` to verify lat/lng accuracy for all 165 rows with missing/bad zip codes. Result: 163/165 were within 50km, 2 corrected.

### `seedfinder-verified.csv`

**Source:** `seedfinder-clean.csv` (487 breeders with verified websites)

Shannon manually clicked every single URL in the original 2,059 breeder list from seedfinder.eu. Over 8+ hours of review, 487 survived with working, legitimate websites.

### `state-verified.csv`

**Source:** `state-clean.csv` (14,507 active state-licensed cannabis businesses)

**Condensing:** Amazon Q wrote `scripts/condense_state.py` to merge rows sharing the same street address into single rows. This handles states like Colorado where each license type (cultivator, dispensary, retail) is a separate row for the same business at the same location. Names, DBAs, types, and license numbers are pipe-separated when different. California confidential addresses (`not published`) and city-only rows are excluded from condensing.

**Result:** 14,507 → ~13,030 rows (901 rows condensed from 545 address groups).

**Additional columns added by matching scripts:**

| Column | Script | Description |
|---|---|---|
| `slug` | `add_slugs.py` | URL-safe slug from name |
| `dba_slug` | `add_slugs.py` | URL-safe slug from DBA |
| `license_usda` | `mark_usda.py` | TRUE if fuzzy slug matches USDA verified names (47 hits) |
| `delivery` | `mark_delivery.py` | TRUE/FALSE if "delivery" appears in name or DBA (58 hits) |
| `sells_seeds` | `mark_seeds.py` | TRUE if fuzzy slug matches seedfinder breeder names (199 hits, many false positives) |
| `other_license` | `mark_breeder.py` | TRUE if fuzzy slug matches breeders-master names (17 hits) |

**Fixes applied earlier by `scripts/fix_state.py`:**
- All slugs rebuilt from name column
- `dba_slug` column generated for all rows with a DBA
- 737 zip codes padded with leading zeros (MA `0xxxx`, CT `06xxx`, NJ `07xxx`, etc.)

---

## Scripts

### Data Cleaning
| Script | Purpose |
|---|---|
| `fill_zip.py` | Fills missing USDA zip codes from FOIA Excel file |
| `check_geo.py` | Verifies lat/lng for flagged rows via Google Maps API |
| `fix_state.py` | Rebuilds slugs, generates dba_slug, pads zip codes |
| `condense_state.py` | Merges same-address rows into single rows with pipe-separated fields |
| `add_slugs.py` | Regenerates slug and dba_slug columns |

### Cross-Reference Matching
| Script | Purpose |
|---|---|
| `mark_usda.py` | Marks `license_usda=TRUE` where state names match USDA names |
| `mark_delivery.py` | Marks `delivery=TRUE/FALSE` based on name/DBA containing "delivery" |
| `mark_seeds.py` | Marks `sells_seeds=TRUE` where names match seedfinder breeder slugs |
| `mark_breeder.py` | Marks `other_license=TRUE` where names match breeders-master slugs |

### Diagnostics
| Script | Purpose |
|---|---|
| `analyze_state.py` | Full state data analysis — coverage, types, quality checks |
| `parse_aeterna.py` | One-off parser for Aeterna Cannabis store locator (100 NY locations — retail partners, not added) |
| `peek_dupes.py` | Analyzes duplicate address patterns before condensing |
| `peek.py` | Prints row counts and headers for all verified files |

**Note:** `check_geo.py` requires a Google Maps API key (replace `<YOUR_GOOGLE_API_KEY>` in the script).

---

*Manual review by Shannon. Scripts by Amazon Q.*
