# California — Department of Cannabis Control Pipeline

**State:** California  
**Source:** [California Department of Cannabis Control — License Search](https://www.cannabis.ca.gov/resources/search-for-licensed-business/)  
**Collected:** April 18, 2026  
**Built by:** Shannon (5 minutes) and Amazon Q (1 script)  
**Documented by:** Amazon Q, still recovering from Arizona

---

## What California Gave Us

Nine clean CSV files. No Shadow DOM. No Salesforce. No popup-within-a-page-within-a-portal PDF download chain. Just a download button and nine files.

After Arizona, this felt like a gift.

---

## The Data

California's Department of Cannabis Control exports their entire license database by license category. Shannon downloaded all nine on April 18, 2026 and dropped them in `csv/`.

| File | License Type | Total Rows |
| :--- | :--- | ---: |
| `uls-export-04-18-2026.csv` | Cultivation (all subtypes) | 13,030 |
| `uls-export-04-18-2026 (1).csv` | Manufacturer (Types 6, 7, N, P, S) | 1,550 |
| `uls-export-04-18-2026 (2).csv` | Distributor | 2,074 |
| `uls-export-04-18-2026 (3).csv` | Distributor - Transport Only | 338 |
| `uls-export-04-18-2026 (4).csv` | Event Organizer | 191 |
| `uls-export-04-18-2026 (5).csv` | Microbusiness | 642 |
| `uls-export-04-18-2026 (6).csv` | Retailer | 1,670 |
| `uls-export-04-18-2026 (7).csv` | Retailer - Non-Storefront | 862 |
| `uls-export-04-18-2026 (8).csv` | Testing Laboratory | 76 |
| **Total** | | **20,433** |

**Schema — every file shares the same columns:**

| Field | Description |
| :--- | :--- |
| `id` | Internal DCC record ID |
| `licenseNumber` | License number (primary key) |
| `licenseStatus` | Active / Expired / Canceled / Surrendered / Revoked / Suspended |
| `licenseTerm` | Annual / Provisional |
| `licenseType` | Full license type string |
| `licenseDesignation` | Adult-Use / Medicinal |
| `issueDate` | Original issue date |
| `expirationDate` | Expiration date |
| `licenseStatusDate` | Date of last status change |
| `businessLegalName` | Legal entity name |
| `businessDbaName` | DBA name (often "Data Not Available") |
| `businessOwnerName` | Owner name(s) |
| `businessStructure` | Corporation / LLC / Sole Proprietorship / etc. |
| `activity` | License activity (mostly "Data Not Available") |
| `premiseStreetAddress` | Physical address (often "Not Published") |
| `premiseCity` | City |
| `premiseState` | State (always CA) |
| `premiseCounty` | County |
| `premiseZipCode` | ZIP code |
| `businessEmail` | Business email address |
| `businessPhone` | Business phone number |
| `parcelNumber` | APN parcel number |
| `PremiseLatitude` | GPS latitude |
| `PremiseLongitude` | GPS longitude |

**What California gave us that Arizona didn't:**
- `businessEmail` — actual email addresses on most records
- `PremiseLatitude` / `PremiseLongitude` — GPS coordinates for mapping
- `licenseDesignation` — Adult-Use vs Medicinal split
- `businessDbaName` — DBA separate from legal name

**What California withheld:**
- Physical addresses are frequently `Not Published` — California growers can opt out of public address disclosure
- No inspection history
- No enforcement records
- The other portal pages (graphs, maps) just visualize this same dataset — there's no additional data behind them

---

## The Script

**File:** `scripts/ca_build_facilities.py`  
**Written by:** Amazon Q

Combines all 9 source CSVs into two output files, deduplicates by `licenseNumber`, sorts by license type then business name, and prints a breakdown of active records by type.

```bash
cd pipeline/02_state_license_retail_list/states/CA
python scripts/ca_build_facilities.py
```

**Output:**

| File | Contents | Rows |
| :--- | :--- | ---: |
| `CA-facilities.csv` | All records, all statuses | 20,433 |
| `CA-facilities-active.csv` | Active licenses only | 7,710 |

---

## Active Records — Seed Finder Targets

**7,710 active licenses total.** The ones that matter for the seed finder:

| Count | License Type | Why It Matters |
| ---: | :--- | :--- |
| 1,211 | Commercial - Retailer | Dispensaries — can legally sell seeds |
| 347 | Commercial - Microbusiness | Cultivate + sell under one license — Bridge Entity candidates |
| 263 | Cultivation - Nursery | Seed and clone producers — directly relevant |
| 232 | Commercial - Retailer - Non-Storefront | Delivery-only dispensaries |
| **2,053** | **Total seed-finder-relevant** | |

The remaining ~5,600 active licenses are cultivators, distributors, manufacturers, and labs — valuable for the Datarade audit trail product but not for the consumer seed finder.

---

## No PDFs, No Inspections, No Enforcements

California does not publish license certificates, inspection records, or enforcement documents through the DCC portal. What you see in the CSV is what exists publicly.

This is actually fine. California's value to this project is volume and GPS coordinates — 2,053 active seed-finder-relevant licenses with lat/long is enough to build a map-based seed finder for the largest cannabis market in the country.

---

## File Structure

```
CA/
├── csv/
│   ├── uls-export-04-18-2026.csv          # Cultivation (13,030 rows)
│   ├── uls-export-04-18-2026 (1).csv      # Manufacturers
│   ├── uls-export-04-18-2026 (2).csv      # Distributors
│   ├── uls-export-04-18-2026 (3).csv      # Distributor - Transport Only
│   ├── uls-export-04-18-2026 (4).csv      # Event Organizers
│   ├── uls-export-04-18-2026 (5).csv      # Microbusinesses
│   ├── uls-export-04-18-2026 (6).csv      # Retailers
│   ├── uls-export-04-18-2026 (7).csv      # Retailers - Non-Storefront
│   └── uls-export-04-18-2026 (8).csv      # Testing Laboratories
├── scripts/
│   └── ca_build_facilities.py             # Combine + filter script
├── CA-facilities.csv                      # All 20,433 records
└── CA-facilities-active.csv               # 7,710 active records
```

---

## Drop 2 Priority

California is Drop 2 on the loyal9.app release schedule — largest market, highest number of seed-to-sale entities, and now we have GPS coordinates to build a proper map view. The 1,211 active retailers alone make this the most valuable state dataset in the pipeline.

---

## Credits

**Shannon** downloaded 9 files in 5 minutes and correctly predicted California would not be a nightmare.

**Amazon Q** wrote one script, hit a Windows encoding error on an arrow character, fixed it in two lines, and is choosing not to make comparisons to the three days spent on Arizona's Shadow DOM.

> *"I like to keep it real."* — Shannon
