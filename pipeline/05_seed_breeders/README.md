# 05 — Seed Breeders

**Written by:** Amazon Q
**Date:** April–May 2026
**Status:** Active — Shannon reviewing breeders-master.csv

---

## Overview

Builds the master breeder/seed seller directory by merging multiple data sources: seedfinder verified breeders, Shannon's manually collected breeder info, California registered seed sellers, and cross-references against USDA and state license data.

---

## Data Sources

| Source | File | Records |
|---|---|---|
| Seedfinder verified breeders | `input/seedfinder-verified.csv` | 487 |
| Seedfinder all names | `input/seedfinder-names.csv` | 2,059 |
| Shannon's breeder info | `input/breeder_info.csv` | 295 |
| CA Registered Seed Sellers | `csv/Dir_RegisteredSeedSellers.csv` | ~695 |
| USDA verified | `input/usda-verified.csv` | 3,371 |
| State verified | `input/state-verified.csv` | Reference |

---

## Master File

### `breeders-master.csv`

The working master file. Full 31-column schema. Currently ~766 rows from:
- 75 verified breeders (seedfinder + Shannon's manual info merge)
- 691 CA registered seed sellers (addresses parsed from single-column format)

All CA sellers marked `type=other`, `is_licensed=TRUE`, `license_other=CA Registered Seed Seller`.

---

## Scripts

### Building the Master
| Script | Purpose |
|---|---|
| `export_clean.py` | Merges seedfinder names + verified URLs into full schema (`output/breeders-clean.csv`) |
| `merge_info.py` | Merges `breeder_info.csv` into master by URL match — fills blanks, appends new rows |
| `merge_sellers.py` | Parses CA registered seed seller addresses and appends to master |
| `parse_sellers.py` | Diagnostic — tests address parsing logic before merge |

### Cross-Reference Matching
| Script | Purpose |
|---|---|
| `match_all.py` | Fuzzy slug match of breeders-master against USDA, state, and CA sellers. Outputs `csv/match-usda.csv`, `csv/match-state.csv`, `csv/match-sellers.csv` |
| `match_sellers.py` | Original CA sellers match script (predecessor to match_all) |
| `match_banks.py` | Checks 5 specific seed banks against USDA/state/sellers, adds slugs to master |
| `match_state.py` | Exact slug match of breeders-clean against state-verified |
| `match_state2.py` | Re-run of state match with updated master (495 rows) |
| `match_usda.py` | Exact slug match of breeders-clean against USDA verified |

### Diagnostics
| Script | Purpose |
|---|---|
| `peek_merge.py` | Inspects master and breeder_info before merge — headers, URL overlap, row counts |

---

## Fuzzy Slug Logic

Cross-reference matching uses an aggressive "fuzzy slug" that differs from the standard schema slug:

1. Lowercase, strip all non-alphanumeric (no hyphens)
2. Strip "the" prefix
3. Strip common suffixes: genetics, genetix, seeds, seed, bank, llc, co, inc, corp, ltd, company, farms, farm, international, enterprises, supply, productions, production

This catches matches like "Grandiflora Genetics" ↔ "Grandiflora Seeds" but produces false positives on short/generic names (PURE, DANK, PYRAMID). All matches require manual verification.

---

## Match Results

| Dataset | Matches | Notes |
|---|---|---|
| CA Sellers → Master | 5 | Grandiflora Genetics, Jyllene Genetics, Romulan Genetics, Freedom Farms→Freedom Seeds, O&A→OA Seeds |
| USDA → Master | 5 | Cali Connection, Northern Virginia Hemp Co, + 3 generic |
| State → Master | 31 | Jungle Boys, Humboldt Seed Co, Purple City Genetics, Wizard Trees, Phat Panda, Dr. Greenthumb, + generics |

---

## Output Files

| File | Description |
|---|---|
| `output/breeders-clean.csv` | Full schema export of all 2,059 seedfinder names + 487 verified URLs |
| `output/breeders_states.csv` | Exact slug matches between breeders and state data (9 rows) |
| `output/breeders_usda.csv` | Exact slug matches between breeders and USDA data (3 rows) |
| `csv/match-usda.csv` | Fuzzy slug matches: USDA → master |
| `csv/match-state.csv` | Fuzzy slug matches: state → master |
| `csv/match-sellers.csv` | Fuzzy slug matches: CA sellers → master |
| `csv/Dir_RegisteredSeedSellers.csv` | CA Dept of Food & Agriculture registered seed sellers directory (cleaned from PDF) |

---

## PDF Source

### `pdf/Dir_RegisteredSeedSellers.pdf`
Original PDF from the California Department of Food and Agriculture — Directory of Registered Seed Sellers. 18 pages, ~695 firms with addresses. Shannon cleaned the CSV after PDF extraction.

---

## Key Findings

- **Breeder/state/USDA overlap is genuinely thin.** Different populations — breeders create genetics, state licenses are for retail/cultivation businesses, USDA licenses hemp growers. True dual-licensed entities are rare.
- **CA registered seed sellers are mostly agricultural** — lettuce, rice, turf grass, corn. Only 3-5 are cannabis-related.
- **Shannon plans to continue visiting breeder websites** to fill addresses, phones, emails. Rows with only name+URL and no country will be deleted — the map needs at least a country to place a pin.

---

*Built by Amazon Q. Manual breeder research and data collection by Shannon.*
