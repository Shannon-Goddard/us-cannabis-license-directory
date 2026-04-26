# Alabama — Medical Cannabis Commission Pipeline

**State:** Alabama  
**Source:** [Alabama Medical Cannabis Commission](https://amcc.alabama.gov)  
**Collected:** 2026  
**Built by:** Shannon, who copy/pasted what they had  
**Documented by:** Amazon Q, who was made to write this

---

## What Alabama Gave Us

A PDF.

Not a searchable database. Not a CSV export. Not an API. A PDF of applicant and licensee information published by the Alabama Medical Cannabis Commission, which Shannon ran through `pdf-to-csv.html`, manually corrected, and turned into `AL-facilities.csv`.

That's the whole story.

---

## The Legal Situation (It's A Lot)

Alabama's medical cannabis program has been in court-ordered limbo since the licenses were awarded. Here's the current state of play:

**What's real and operational:**
- **8 Cultivator licenses** with actual issued license numbers — these are active, verified, and in the CSV
- These are your Level 2 cross-reference targets against the USDA list

**What's legal theater:**
- Every **Integrated Facility license** (Trulieve, Wagon Trail, Sustainable Alabama, Flowerwood, Specialty Medical Products) has status `License Awarded / Issuance Stayed by Commission`
- No license numbers. No operational dispensaries. Dead websites.
- These entities have been in injunction hell since the commission awarded licenses in 2023
- They're in the CSV because they exist on paper and may eventually matter — but for the seed finder, they're filtered out

**The practical implication:**
Alabama has active licensed cultivators but zero operational dispensaries. There is currently nowhere in Alabama to legally buy cannabis seeds at retail. The seed finder page for Alabama tells that story honestly and positions Loyal9 as the source of truth when the injunctions finally lift.

---

## The Data

**File:** `AL-facilities.csv`  
**Method:** PDF → `pdf-to-csv.html` → manual correction by Shannon  
**Source PDFs:** `Alabama-Applicant-Licensee-Info-CULTIVATOR.pdf` and `Alabama-Applicant-Licensee-Info-INTEGRATED-FACILITY.pdf`

**What's in it:**

| Field | Notes |
| :--- | :--- |
| `Legal Name` | Entity name |
| `License Category` | Cultivator or Integrated Facility |
| `Status` | License Issued / License Awarded / Issuance Stayed |
| `License #` | Populated for Cultivators only — N/A for everything else |
| `Issued` / `Expires` | Dates where available |
| `Facility Address` | Full address broken into components |
| `Facility Type` | Cultivation, Processing, Dispensing Site |
| `Facility County` | Alabama county |
| `Phone` | Where available |
| `Primary Contact` | Name, title, address, phone, email — manually extracted |
| `Website` | Where available — several are N/A or dead |
| `Ownership / Officers` | Summarized ownership percentages |

**Active Cultivators (the only ones that matter right now):**

| License # | Entity | County |
| :--- | :--- | :--- |
| CULV000636 | Native Black Cultivation | Jefferson |
| CULV000302 | Gulf Shore Remedies, LLC | Baldwin |
| CULV000154 | CRC of Alabama, LLC | Pike |
| CULV000210 | Greenway Botanicals, LLC | Cherokee |
| CULV000407 | Twisted Herb Cultivation | Butler |
| CULV000533 | I Am Farms | Greene |
| CULV000737 | Creek Leaf Wellness, Inc. | Jefferson |
| CULV000902 | Pure by Sirmon Farms, LLC | Baldwin |
| CULV000835 | Blackberry Farms, LLC | Tuscaloosa |

---

## No Scripts

There are no scripts in this folder. The data was small enough to handle manually and the source was a PDF that didn't warrant automation. When Alabama's program comes out of litigation and starts issuing dispensary licenses, this folder gets a scraper. Until then, `AL-facilities.csv` is what it is.

---

## File Structure

```
AL/
├── csv/                                   # Empty — no per-license CSVs
├── pdf/
│   ├── Alabama-Applicant-Licensee-Info-CULTIVATOR.pdf
│   └── Alabama-Applicant-Licensee-Info-INTEGRATED-FACILITY.pdf
└── AL-facilities.csv                      # The whole pipeline, one file
```

---

## Drop 1 Priority

Alabama is Drop 1 on the loyal9.app release schedule — not because the data is rich, but because of the USDA list. Alabama A&M, Auburn University, Troy University, Tuskegee University, and Talladega College all appear on the USDA active hemp list. That university researcher density makes Alabama a high-value SEO target for the academic and compliance audience.

The dispensary side is thin. The cultivator and researcher side is not.

---

## Credits

**Shannon** collected the data, ran the PDFs, manually corrected the output, and provided the ownership depth from the source documents.

**Amazon Q** wrote this README and is choosing not to make further comments about the Alabama Medical Cannabis Commission's relationship with the court system.

> *"I like to keep it real."* — Shannon
