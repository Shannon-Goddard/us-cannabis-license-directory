# CI Seed Registry — US Cannabis & Hemp License Directory

[![DOI](https://img.shields.io/badge/DOI-10.5281/zenodo.19800772-blue.svg)](https://doi.org/10.5281/zenodo.19800772)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

**Owner:** Shannon Goddard — Loyal9 LLC
**Status:** Active · Community Editable

---

## Purpose

This registry provides a unified, structured view of the US cannabis and hemp licensing landscape. By consolidating fragmented state-level portals and USDA data, it supports compliance research and market analysis necessitated by evolving federal agricultural policies.

The dataset is published with a DOI for academic citation. The community edit system allows anyone with a GitHub account to improve the data — every edit is logged in an immutable ledger.

---

## Live Site

🌐 [**Open the Directory**](https://shannon-goddard.github.io/us-cannabis-license-directory/)

| Page | Description |
|---|---|
| [Directory](https://shannon-goddard.github.io/us-cannabis-license-directory/) | Searchable, sortable table — 29,633 records |
| [Edit Ledger](https://shannon-goddard.github.io/us-cannabis-license-directory/ledger.html) | Every community edit, fully transparent |
| [How to Contribute](https://shannon-goddard.github.io/us-cannabis-license-directory/contributing.html) | Step-by-step guide for editors |

---

## Project Structure

```
us-cannabis-license-directory/
├── aws-setup/                         # AWS infrastructure templates & docs
│   ├── aws-setup.md                   # Architecture, deploy steps, cost breakdown
│   ├── trust-policy.json              # IAM trust policy
│   ├── lambda-policy.json             # IAM permissions (sanitized)
│   └── lambda/                        # Lambda function source code
│       ├── submit_edit.py             # POST /edit — write to DynamoDB
│       ├── get_ledger.py              # GET /ledger — read from DynamoDB
│       └── github_oauth.py            # POST /auth/github — OAuth exchange
├── pipeline/
│   ├── 01_usda_active_states/         # USDA hemp licensee data (3,371 active)
│   ├── 02_state_license_retail_list/  # 25 state cannabis license portals
│   ├── 03_seed_suppliers/             # Seedfinder.eu breeder directory
│   ├── 04_human_in_the_loop/         # Manual review, dedup, cross-reference
│   ├── 05_seed_breeders/             # Breeder master + CA registered seed sellers
│   └── pdf-to-csv.html              # In-browser PDF-to-CSV converter
├── assets/img/                        # Badge images
├── index.html                         # Directory UI — search, sort, edit
├── ledger.html                        # Edit ledger UI
├── contributing.html                  # How to contribute guide
├── us-cannabis-license-directory.csv  # Community dataset — 29,633 records, 38 columns
├── raw.csv                            # Published DOI dataset — 13,128 records, 21 columns
├── raw.json                           # Same DOI dataset in JSON format
├── CONTRIBUTING.md                    # Contribution guidelines
├── SOURCE.md                          # Data dictionary, methodology, citation
├── LICENSE                            # MIT License
└── README.md                          # This file
```

---

## Datasets

### Published Dataset (DOI)

📥 [Download raw.csv](raw.csv) · 📥 [Download raw.json](raw.json)

The frozen, citable dataset. 13,128 records across 35 US states. 21 columns.

| Type | Count |
|---|---|
| Dispensary | 5,678 |
| Cultivator | 5,001 |
| Other | 3,049 |
| Breeder | 145 |
| Bank | 18 |

Top states: CA (7,743), CO (1,390), MI (857), NY (801), OR (468)

See `SOURCE.md` for full column reference, methodology, and known limitations.

### Community Dataset

📥 [Download us-cannabis-license-directory.csv](us-cannabis-license-directory.csv)

The living dataset. 29,633 records. 38 columns (20 original + 18 community-editable). This is the file the [live directory](https://shannon-goddard.github.io/us-cannabis-license-directory/) reads from.

Community columns include: `Business_Category`, `Product_Focus`, `Is_Medical`, `Is_Adult_Use`, `Payment_Methods`, `Ownership_Type`, `Hours_of_Operation`, `Instagram_URL`, `Google_Place_ID`, and more.

---

## Community Edit System

Anyone with a GitHub account can edit records directly in the browser.

1. **Login with GitHub** — OAuth, read-only profile access
2. **Click a cell** — one cell at a time
3. **Submit** — edit is logged to AWS DynamoDB with your username, timestamp, and the change
4. **Ledger** — every edit is visible in the [Edit Ledger](https://shannon-goddard.github.io/us-cannabis-license-directory/ledger.html)

See [CONTRIBUTING.md](CONTRIBUTING.md) or the [How to Contribute](https://shannon-goddard.github.io/us-cannabis-license-directory/contributing.html) page for the full guide.

### Architecture

```
Browser → API Gateway (HTTP) → Lambda (Python) → DynamoDB
```

| Service | Purpose | Cost |
|---|---|---|
| API Gateway | 3 routes: /edit, /ledger, /auth/github | $0.00/month |
| Lambda | 3 functions: submit, ledger, OAuth | $0.00/month |
| DynamoDB | Immutable edit ledger | $0.00/month |

Full infrastructure docs: [`aws-setup/aws-setup.md`](aws-setup/aws-setup.md)

---

## Getting Started

Use the data immediately via the CSV/JSON files, or explore the live directory.

```bash
git clone https://github.com/Shannon-Goddard/us-cannabis-license-directory.git
```

Each `pipeline/` subdirectory contains specific scripts for data fetching and cleaning.

---

## Data Maintenance

- **Last Full Sync:** April 2026
- **Update Frequency:** The DOI dataset (`raw.csv`) will not be updated. The community dataset (`us-cannabis-license-directory.csv`) is updated by contributors.
- **Verification:** Verified records are cross-referenced via `04_human_in_the_loop`.

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

**Shannon Goddard** — Research, data collection, legal analysis, manual verification, and the vision that turned a fragmented regulatory landscape into a single open dataset.

**Amazon Q** (AWS AI Assistant) — Pipeline architecture, data processing, AWS infrastructure (DynamoDB, Lambda, API Gateway), frontend development, community edit system, and documentation.

Breeder directory sourced from [seedfinder.eu](https://seedfinder.eu/en/database/breeder).  

This project was inspired by Seedfinder.eu's ambitious attempt to catalog 2,000+ cannabis breeders and seed banks. I originally hoped to use their list as a starting point for mapping licensed operators in the US. Unfortunately, the data quality made that impossible. I manually visited every single link in their breeder directory. 76.3% were broken, spam, malicious, parked domains, 404s, or redirects to low-quality/scam sites. I've compiled a full transparency report: CSV: Download the full audit [here](seedfindereu.csv)
(Columns include: url, name, homepage, url_is_bad)

Dear Seedfinder.eu team,
Thank you for the idea and for maintaining a public directory — it sparked this entire effort. However, the current state of the links significantly undermines its usefulness. I'm releasing this audit in the hope it helps you clean up the data for the community.  Happy to share more details or collaborate. You can [buy me a beer](https://buymeacoffee.com/goddardshannon9) - cheers 🍻

— Shannon

ps: yes, I really did manually click all 2,059 links  

---

[GitHub ❤️ Sponsor](https://github.com/sponsors/Shannon-Goddard)

Built with grit in Riverside, CA. Chaos Preferred. Integrity Required.
