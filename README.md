# CI Seed Registry — Data Pipeline

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.19800772.svg)](https://doi.org/10.5281/zenodo.19800772)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

**Owner:** Shannon Goddard — Loyal9 LLC
**Status:** Active

---

## Purpose

This registry provides a unified, structured view of the US cannabis and hemp licensing landscape. By consolidating fragmented state-level portals and USDA data, it supports compliance research and market analysis necessitated by evolving federal agricultural policies.

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

## Getting Started

You can use the data immediately via the `raw.csv` / `raw.json` files, or explore the `pdf-to-csv.html` tool for manual processing of new state records.

To run the Python scripts in the `pipeline/` directory:

```bash
git clone https://github.com/Shannon-Goddard/us-cannabis-license-directory.git
```

Each subdirectory contains specific scripts for data fetching and cleaning.

---

## Data Maintenance

- **Last Full Sync:** April 2026
- **Update Frequency:** Data will not be updated in this repo.
- **Verification:** Verified records are cross-referenced via `04_human_in_the_loop`.

---

## Contributing

Contributions will be welcomed on the map repo where the data will be used. Link will be dropped here when available.

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

---

[GitHub ❤️ Sponsor](https://github.com/sponsors/Shannon-Goddard)

Built with grit in Riverside, CA. Chaos Preferred. Integrity Required.
