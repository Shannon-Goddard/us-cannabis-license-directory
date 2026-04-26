# 03 — Seed Suppliers (Breeder Directory)

**Written by:** Amazon Q
**Date:** April 19, 2026
**Status:** Complete

---

## Overview

Builds a directory of cannabis seed banks and breeders worldwide with verified website URLs. The source is [seedfinder.eu](https://seedfinder.eu/en/database/breeder) — the most comprehensive breeder directory in the cannabis space, maintained by a volunteer community.

---

## How the Names Were Collected

**Source:** [seedfinder.eu/en/database/breeder](https://seedfinder.eu/en/database/breeder)

**Method:** Manual extraction by Shannon via browser dev tools.

The seedfinder breeder index uses a filtered view — clicking a letter filter (0-9, A, B, C... Z) shows only breeders starting with that character, but the full list within each filter is collapsed. Shannon:

1. Clicked each filter (0-9 through Z)
2. Clicked the first breeder in each filtered list to expand all names
3. Copied the outer HTML element (`<ul class="list-disc list-inside">`) from the Elements tab in dev tools
4. Pasted the raw HTML into `notes.text`

Amazon Q then wrote `parse_notes_urls.py` (since deleted) to extract all `href` + link text pairs from the HTML into a CSV. The HTML contained entries like:

```html
<a class="link" href="https://seedfinder.eu/en/database/breeder/barneys-farm">Barneys Farm (72)</a>
```

The number in parentheses is the strain count on seedfinder — not extracted, just the URL and name.

**Result:** 2,059 breeder names with seedfinder profile URLs.

---

## Scripts

### `scripts/scrape_seedfinder.py`

Visits each seedfinder breeder profile URL, finds the `<h3>Links</h3>` section, and extracts the `Homepage` anchor — the breeder's actual website.

**Method:** For each URL in `seedfinder-urls.csv`:
1. Fetch the seedfinder profile page
2. Find `<h3>Links</h3>`
3. Walk sibling elements for an `<a>` tag with text "Homepage"
4. Extract the `href` — that's the breeder's real website

Resume-capable — writes back to the CSV after each row. If interrupted, re-run and it picks up where it left off.

**Result:** 1,891 / 2,059 breeders have a homepage URL (91.8% hit rate). The remaining 168 have no website listed on seedfinder.

**Dependencies:** `requests`, `beautifulsoup4`

---

## Output Files

### `csv/seedfinder-names.csv`
The original name list. Two columns: `url`, `name`. 2,059 rows.

### `csv/seedfinder-urls.csv`
Names + seedfinder profile URLs + scraped homepage URLs. Three columns: `url`, `name`, `homepage`. 2,059 rows, 1,891 with a homepage.

### `csv/seedfinder-clean.csv`
Shannon's manually reviewed version — dead URLs removed, junk stripped. This is the verified breeder list that feeds into the master registry.

### `csv/seedfinder_slugs.csv`
Fuzzy slugs generated from all 2,059 breeder names. Two columns: `name`, `slug`. Used by pipeline 04 to mark `sells_seeds` in state-verified data.

---

## What Happened Next (and Why Most Scripts Were Deleted)

After collecting the homepage URLs, two additional scraping passes were attempted:

1. **Google Places API** (`enrich_suppliers.py`) — searched Google Maps for each breeder name. Cost ~$400 and returned mostly wrong dispensaries in Moreno Valley, CA. Deleted.

2. **Direct homepage + Instagram scraping** (pipeline 06) — visited each homepage and Instagram profile to extract contact info. After Shannon's 8-hour manual review, 75%+ of the scraped data was dead links, abandoned domains, GoDaddy placeholders, and spam redirects. Contact info from state and USDA filings is more reliable. Scripts deleted.

The surviving value from this pipeline is the **verified breeder directory with working website URLs** — `seedfinder-clean.csv`.

---

*Built by Amazon Q. Breeder names sourced from seedfinder.eu's volunteer-maintained database. Manual HTML extraction and data review by Shannon.*
