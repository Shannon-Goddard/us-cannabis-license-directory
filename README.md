# CI Seed Registry — Data Pipeline

[![DOI](https://zenodo.org/badge/1221929074.svg)](https://doi.org/10.5281/zenodo.19800772)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

**Owner:** Shannon Goddard — Loyal9 LLC
**Status:** Active

---

## Project Structure

```
NEW-SEEDS-LAW/
├── pipeline/
│   ├── 01_usda_active_states/         # USDA hemp licensee data (3,371 active)
│   ├── 02_state_license_retail_list/  # 25 state cannabis license portals (14,507 active)
│   ├── 03_seed_suppliers/             # Seedfinder.eu breeder directory (2,059 names, 487 verified)
│   ├── 04_human_in_the_loop/         # Manual review, dedup, cross-reference matching
│   ├── 05_seed_breeders/             # Breeder master + CA registered seed sellers
│   └── pdf-to-csv.html              # In-browser PDF-to-CSV converter (client-side, no install)
├── raw.csv                            # Published dataset — 13,119 US cannabis/hemp businesses
├── raw.json                           # Same dataset in JSON format
├── SOURCE.md                          # Data dictionary, methodology, citation info for DOI
└── README.md                          # This file
```

Each pipeline folder has its own README with source details, scripts, and output descriptions.

---

## raw.csv / raw.json

📥 [Download raw.csv](raw.csv) · 📥 [Download raw.json](raw.json)

The published dataset. 13,119 records across 27 US states. 22 columns. Available in CSV and JSON formats.

| Type | Count |
|---|---|
| Dispensary | 5,678 |
| Cultivator | 5,001 |
| Other | 3,049 |
| Breeder | 136 |
| Bank | 18 |

Top states: CA (7,743), CO (1,390), MI (857), NY (801), OR (468)

See `SOURCE.md` for full column reference, methodology, known limitations, and citation format.

---

## DOI

`DOI: 10.5281/zenodo.19800772`

### How to Cite

> Goddard, S., & Amazon Q. (2026). *CI Seed Registry: US Cannabis & Hemp License Directory* (Version 1.0) [Data set]. Loyal9 LLC. https://doi.org/10.5281/zenodo.19800772

---

## License

This project is licensed under the [MIT License](LICENSE).

© 2026 Shannon Goddard | Loyal9 LLC

---

## Credits

**Shannon Goddard** — Research, data collection, legal analysis, manual verification.
**Amazon Q** (AWS AI Assistant) — Scripts, pipeline architecture, data processing, documentation.

Breeder directory sourced from [seedfinder.eu](https://seedfinder.eu/en/database/breeder).
