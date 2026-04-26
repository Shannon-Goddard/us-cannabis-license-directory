# CI Seed Registry — US Cannabis & Hemp License Directory

**Version:** 1.0
**File:** `raw.csv`
**Records:** 13,119
**Country:** United States
**License:** CC BY 4.0

---

## Authors

**Shannon Goddard** — Loyal9 LLC
Research, legal analysis, data collection, manual verification, and business strategy.

**Amazon Q** — AWS AI Assistant
Pipeline architecture, data processing scripts, address parsing, cross-reference matching, and documentation.

---

## What This Is

A consolidated directory of cannabis and hemp businesses operating in the United States, compiled from federal and state regulatory sources and verified breeder directories. Built in response to the FY 2026 Agriculture Appropriations Act (P.L. 119-37, Section 781), which adopts a Total THC standard effective November 12, 2026.

This dataset is intended as a free, open, community-maintained data utility for researchers, policymakers, and industry participants.

---

## Summary Statistics

| Metric | Count |
|---|---|
| Total records | 13,119 |
| States represented | 27 |
| Has street address | 6,237 (47.5%) |
| Has geocoordinates | 6,495 (49.5%) |
| Has phone | 9,234 (70.4%) |
| Has email | 8,097 (61.7%) |
| Has website URL | 483 (3.7%) |

### By Entity Type

| Type | Count |
|---|---|
| Dispensary | 5,678 |
| Cultivator | 5,001 |
| Other (distributor, manufacturer, processor, etc.) | 3,049 |
| Breeder | 136 |
| Bank (seed bank) | 18 |

Some records have multiple types (e.g., `cultivator|dispensary` for vertically integrated businesses). Counts above reflect each type individually.

### Top 10 States

| State | Records |
|---|---|
| CA | 7,743 |
| CO | 1,390 |
| MI | 857 |
| NY | 801 |
| OR | 468 |
| WA | 461 |
| MA | 398 |
| IL | 288 |
| MO | 224 |
| AZ | 181 |

### License Coverage

| License Type | Records |
|---|---|
| State license | 13,029 |
| CA Registered Seed Seller | 23 |
| USDA hemp license (cross-referenced) | 11 |

### Flags

| Flag | TRUE |
|---|---|
| `duplicate` — possible duplicate based on slug matching | 6,669 |
| `sells_seeds` — name matches known seed breeder/bank directory | 166 |
| `delivery` — name or DBA contains "delivery" (delivery-only, no storefront) | 76 |

---

## Column Reference

| Column | Description |
|---|---|
| `index` | Unique record identifier. Format: `US-0000001`. Sequential, stable across versions. |
| `name` | Display name or legal business name. Pipe-separated (`\|`) when multiple names exist at the same address. |
| `name_slug` | URL-safe slug derived from `name`. Lowercase, "the" prefix stripped, non-alphanumeric replaced with hyphens. |
| `dba` | Doing Business As — alternate or legal name. Used for fuzzy matching and deduplication. If no DBA exists, populated from `name`. |
| `dba_slug` | URL-safe slug derived from `dba`. Same rules as `name_slug`. |
| `type` | Entity classification. Values: `breeder`, `bank`, `cultivator`, `dispensary`, `other`. Pipe-separated when multiple types apply. |
| `url` | Business website URL. |
| `street_address` | Street address. Blank for California confidential records and delivery-only businesses. |
| `city` | City. |
| `state` | US state, 2-letter code. |
| `zip_code` | 5-digit US ZIP code. See note on leading zeros below. |
| `country` | `US` for all records in this version. |
| `lat` | Latitude (WGS 84). Geocoded from address via Google Maps API and US Census Geocoder. |
| `lng` | Longitude (WGS 84). |
| `phone` | Phone number. |
| `email` | Email address. |
| `license_usda` | `TRUE` if the business name fuzzy-matches a USDA hemp licensee. Cross-reference flag, not a license number. |
| `license_state` | State-issued cannabis license number(s). Pipe-separated when a business holds multiple licenses at one address. |
| `license_other` | Other license information. Values: `CA Registered Seed Seller`, `TRUE` (matched against breeder directory), or `FALSE`. |
| `delivery` | `TRUE` if "delivery" appears in the business name or DBA. Indicates delivery-only operations with no physical storefront. |
| `sells_seeds` | `TRUE` if the business name fuzzy-matches a known cannabis seed breeder or bank from the seedfinder.eu directory. Includes false positives — manual verification recommended. |
| `duplicate` | `TRUE` if the `name_slug` or `dba_slug` appears more than once in the dataset. Expected for multi-location chains. Does not necessarily indicate a data error. |

---

## Data Sources

| Source | Records | Description |
|---|---|---|
| [USDA Hemp Public Search Tool](https://hemp.ams.usda.gov/s/PublicSearchTool) | Cross-reference | 3,371 active federal hemp licensees used for `license_usda` matching |
| 25 state regulatory portals | ~13,000 | Active cannabis dispensary, cultivator, and processor licenses |
| [seedfinder.eu](https://seedfinder.eu/en/database/breeder) | Cross-reference | 2,059 breeder names used for `sells_seeds` matching |
| CA Dept. of Food & Agriculture | 23 | Directory of Registered Seed Sellers |
| Shannon Goddard (manual collection) | 90 | Verified breeder/seed bank directory with websites |

State license data was collected from official regulatory portals in: AL, AZ, CA, CO, CT, GA, IL, KY, MA, MD, MI, MO, MS, ND, NJ, NM, NV, NY, OK, OR, SD, UT, VT, WA, WV.

---

## Known Limitations

- **California confidential records** (~6,400 rows) have no street address, city, or ZIP code. The California Department of Cannabis Control does not publish this information. These records have a state license number and type but cannot be geocoded.
- **Geocoding coverage is 49.5%.** Records without street addresses cannot be geocoded. City/state-level geocoding was not applied to avoid false precision.
- **`sells_seeds` and `license_usda` are fuzzy matches**, not confirmed facts. The matching algorithm strips common business suffixes (LLC, Inc, Seeds, Genetics, etc.) before comparing. Short or generic names produce false positives. These flags are starting points for research, not definitive classifications.
- **`duplicate` flags are expected for chains.** Multi-location businesses (e.g., dispensary chains) will have multiple rows with the same slug. The flag helps identify them but does not indicate which row to keep.
- **ZIP codes with leading zeros.** US ZIP codes in MA (01xxx), CT (06xxx), NJ (07xxx), and PR (00xxx) begin with zero. Some software (notably Microsoft Excel) strips leading zeros when opening CSV files. The data is correct as published — if zeros appear missing, the file was modified by the software used to open it.

---

## Methodology

Full pipeline documentation, processing scripts, and raw source files are available in the project repository. See `README.md` for the complete project structure.

1. **Pipeline 01** — USDA hemp licensee data collected, geocoded, filtered to active records
2. **Pipeline 02** — 25 state cannabis license portals collected, merged, geocoded, classified by type
3. **Pipeline 03** — 2,059 breeder names scraped from seedfinder.eu, homepage URLs harvested, 487 verified by manual review
4. **Pipeline 04** — Human review of all datasets. Address deduplication (same-address rows condensed with pipe-separated fields). Cross-reference matching against USDA, seedfinder, and breeder directories.
5. **Pipeline 05** — Breeder master directory built from verified seedfinder data, Shannon's manual research, and CA registered seed sellers

---

## Citation

If you use this dataset, please cite:

> Goddard, S., & Amazon Q. (2026). *CI Seed Registry: US Cannabis & Hemp License Directory* (Version 1.0) [Data set]. Loyal9 LLC. https://doi.org/[DOI]

---

## Contact

Shannon Goddard — Loyal9 LLC
Project: [poweredby.ci](https://poweredby.ci)

---

## License

This dataset is released under [Creative Commons Attribution 4.0 International (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/). You are free to share and adapt this data for any purpose, provided you give appropriate credit.
