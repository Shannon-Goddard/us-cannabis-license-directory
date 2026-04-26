# Connecticut — Department of Consumer Protection Pipeline

**State:** Connecticut  
**Source:** [Connecticut eLicense — Cannabis License Search](https://www.elicense.ct.gov/lookup/licenselookup.aspx)  
**Collected:** 2026  
**Built by:** Shannon (manually, 5 pages at a time, with patience)  
**Documented by:** Amazon Q

---

## What Connecticut Gave Us

A license lookup portal that displays 10 records per page, requires clicking into each record's detail tab to get the full address, and has 43 pages of total records. Shannon collected the 5 pages of active licenses and skipped the 38 pages of inactive, expired, and historical records.

That was the right call. Connecticut's program is young. The active data is what matters.

---

## The Data

**File:** `csv/Connecticut.csv`  
**Records:** 57 active licenses  
**Status filter:** Active only — inactive records not collected

**Schema:**

| Field | Description |
| :--- | :--- |
| `Name` | Legal entity name |
| `Credential` | License number (primary key) |
| `Credential Description` | License type + issuing department |
| `Status` | ACTIVE |
| `Status_Reason` | CURRENT or PROVISIONAL |
| `City` | City of license address |
| `DBA` | Doing business as name |
| `License_Type` | Full license type string |
| `Effective_Date` | License effective date |
| `Expiration_Date` | Expiration date (blank for PROVISIONAL) |
| `Application_Type` | How the license was obtained |
| `Endorsements` | Additional endorsements (e.g. Food and Beverage Manufacturing) |
| `Mailing_Address` | Mailing address (multi-line) |
| `License_Address` | Physical license address (multi-line) |

**License types present:**

| Type | Code Prefix | Count |
| :--- | :--- | ---: |
| Adult-Use Cannabis Retailer | ACRE | ~30 |
| Adult-Use Cannabis Cultivator | ACCE | ~16 |
| Adult-Use Cannabis Micro-Cultivator | ACME | ~8 |
| Adult-Use Cannabis Product Manufacturer | ACPM | ~3 |

**Application types — Connecticut's equity program is visible in the data:**

| Application Type | Description |
| :--- | :--- |
| Equity Joint Venture | Social equity applicant partnered with existing operator |
| SEC Lottery | Social Equity Council lottery winner |
| General Lottery | Standard lottery applicant |
| DIA Cultivator | Dispensary-integrated adult-use cultivator |
| Conversion | Medical program converting to adult-use |

---

## The PROVISIONAL Flag

Several cultivators have `Status_Reason = PROVISIONAL` and no license address — the field reads `"Address is not available until the final application is complete"`. These are real, active licenses but the facilities are not yet operational.

For the seed finder: **filter to `Status_Reason = CURRENT` only.** PROVISIONAL licenses should not appear as active seed sources.

For the Datarade product: keep both — PROVISIONAL licenses are pipeline signal, showing which operators are coming online.

---

## No Scripts

57 records. One clean CSV. No script needed.

---

## File Structure

```
CT/
└── csv/
    └── Connecticut.csv    (57 active records)
```

---

## Notes

- Connecticut does not publish inspection history or enforcement records through the eLicense portal
- The 38 pages of inactive/expired/historical records were not collected — the active dataset is sufficient for the seed finder and the USDA cross-reference
- Connecticut's equity joint venture structure means many retailers have a corporate mailing address in another state (Michigan, Illinois, Florida) while the license address is in Connecticut — both fields are preserved in the CSV

---

## Credits

**Shannon** manually navigated 5 pages of a 10-records-at-a-time portal, clicked into each detail tab, and got the data. There is no automation story here. Just endurance.

**Amazon Q** wrote this README and has nothing further to add about Connecticut's portal design choices.

> *"I like to keep it real."* — Shannon
