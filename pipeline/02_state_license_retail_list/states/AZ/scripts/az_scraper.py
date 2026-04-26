"""
AZ Care Check Scraper v2
Written by Amazon Q for Loyal9 / poweredby.ci

Navigates each facility detail page individually, waits for full render,
extracts all visible text then parses it into structured fields.

Outputs:
  - AZ-facilities-v2.csv  (new file so we can compare)
  - csv/inspections/inspections-{license_number}.csv
  - csv/enforcements/enforcements-{license_number}.csv
"""

import csv
import os
import re
import time
from playwright.sync_api import sync_playwright

# ── Paths ─────────────────────────────────────────────────────────────────────
BASE_DIR   = os.path.dirname(os.path.abspath(__file__))
STATE_DIR  = os.path.abspath(os.path.join(BASE_DIR, ".."))
URL_FILE   = os.path.join(BASE_DIR, "az_urls.txt")
FACILITIES = os.path.join(STATE_DIR, "AZ-facilities-v2.csv")
INSP_DIR   = os.path.join(STATE_DIR, "csv", "inspections")
ENF_DIR    = os.path.join(STATE_DIR, "csv", "enforcements")

os.makedirs(INSP_DIR, exist_ok=True)
os.makedirs(ENF_DIR,  exist_ok=True)

FACILITY_HEADERS = [
    "Facility_ID", "Business_Name", "Legal_Name", "Address", "Mailing_Address",
    "Phone", "Facility_Status", "Owner_License",
    "Hours_Mon", "Hours_Tue", "Hours_Wed", "Hours_Thu", "Hours_Fri", "Hours_Sat", "Hours_Sun",
    "Lic1_Type", "Lic1_Services", "Lic1_Number", "Lic1_Originally",
    "Lic1_Effective", "Lic1_Expires", "Lic1_Status", "Lic1_PDF_URL",
    "Lic2_Type", "Lic2_Services", "Lic2_Number", "Lic2_Originally",
    "Lic2_Effective", "Lic2_Expires", "Lic2_Status", "Lic2_PDF_URL",
    "Offsite_Cultivation_Address", "Manufacture_Address", "Source_URL"
]

INSP_HEADERS = ["Facility_ID", "Inspection_Num", "Inspection_Date",
                "Inspection_Type", "Location_Type", "Worksheet_Type",
                "License_Number", "Status"]

ENF_HEADERS  = ["Facility_ID", "Enforcement_Num", "Enforcement_URL",
                "Date_Finalized", "License_Type", "License_Number", "Status"]

# ── Shadow DOM text extractor ─────────────────────────────────────────────────
EXTRACT_JS = """
() => {
    const result = {
        business_name: '', legal_name: '', address: '', mailing_address: '',
        phone: '', facility_status: '', owner_license: '',
        hours: {},
        licenses: [],
        offsite_cultivation: '', manufacture_address: ''
    };

    const getText = (root, label) => {
        const walker = (r) => {
            const els = r.querySelectorAll('*');
            for (const el of els) {
                if (el.shadowRoot) {
                    const v = walker(el.shadowRoot);
                    if (v !== null) return v;
                }
                // Look for label/value pairs in Salesforce form elements
                const lblEl = el.querySelector ? el.querySelector('[class*="label"]') : null;
                if (lblEl && lblEl.innerText && lblEl.innerText.trim() === label) {
                    const valEl = el.querySelector('[class*="value"], [class*="static"], [class*="output"]');
                    if (valEl) return valEl.innerText.trim();
                }
            }
            return null;
        };
        return walker(root) || '';
    };

    // Get all text content from shadow DOM flattened
    const allText = [];
    const flatten = (root) => {
        root.querySelectorAll('*').forEach(el => {
            if (el.shadowRoot) flatten(el.shadowRoot);
            if (el.children.length === 0 && el.innerText && el.innerText.trim()) {
                allText.push(el.innerText.trim());
            }
        });
    };
    flatten(document);

    // Get business name from h4 and legal name from h3 in the facility header
    let business_name = '';
    let header_legal_name = '';
    const findHeader = (root) => {
        const h4 = root.querySelector('h4');
        const h3 = root.querySelector('h3');
        if (h4) business_name = h4.innerText.trim();
        if (h3) header_legal_name = h3.innerText.trim();
        if (business_name) return;
        root.querySelectorAll('*').forEach(el => {
            if (el.shadowRoot) findHeader(el.shadowRoot);
        });
    };
    findHeader(document);

    // Get all anchor hrefs from shadow DOM (for license PDFs)
    const links = [];
    const findLinks = (root) => {
        root.querySelectorAll('a[href*="salesforce.com"]').forEach(a => {
            links.push({ text: a.innerText.trim(), href: a.href });
        });
        root.querySelectorAll('*').forEach(el => {
            if (el.shadowRoot) findLinks(el.shadowRoot);
        });
    };
    findLinks(document);

    return { allText, links, business_name, header_legal_name };
}
"""

def parse_page_text(texts, links, facility_id, url):
    """Parse the flat text array from the page into structured fields."""
    row = {h: "" for h in FACILITY_HEADERS}
    row["Facility_ID"] = facility_id
    row["Source_URL"]  = url

    def after(label, lines):
        """Return the value on the line immediately after the label.
        Returns empty string if next line is another known label.
        """
        known_labels = {
            "Legal Name", "Address", "Mailing Address", "Phone",
            "Facility Status", "Owner / License", "Hours of Operation",
            "Monday", "Tuesday", "Wednesday", "Thursday", "Friday",
            "Saturday", "Sunday", "License Type", "Services",
            "License", "Licensed Originally", "License Effective",
            "License Expires", "License Status", "Offsite Cultivation Address",
            "Manufacture Address", "Help"
        }
        for i, line in enumerate(lines):
            if line.strip() == label and i + 1 < len(lines):
                val = lines[i + 1].strip()
                if val and val not in known_labels:
                    return val
        return ""

    # ── Business name ─────────────────────────────────────────────────────────
    # It appears in the page header before "Legal Name"
    skip = {
        "Details", "Inspections", "Enforcements", "Back to Search",
        "AZ Care Check", "About", "Contact", "ADHS Home",
        "AZ Care Check Home", "Warning!", "Marijuana Facility",
        "Marijuana Establishment", "Marijuana Dispensary",
        "Marijuana Laboratory", "Not Operating",
        "Information on this site is believed to be accurate, but is not guaranteed.",
        "See key licensing information currently on file with the Arizona Department of Health Services below. If applicable, click on the license # to view the currently effective license."
    }
    try:
        ln_idx = next(i for i, t in enumerate(texts) if t.strip() == "Legal Name")
        for i in range(ln_idx - 1, max(0, ln_idx - 20), -1):
            t = texts[i].strip()
            # Skip multi-line blocks (contain newlines)
            if "\n" in t:
                continue
            if t and t not in skip and len(t) > 2:
                row["Business_Name"] = t
                break
    except StopIteration:
        pass

    # ── Simple fields ─────────────────────────────────────────────────────────
    row["Legal_Name"]      = after("Legal Name", texts)
    row["Address"]         = after("Address", texts)
    row["Mailing_Address"] = after("Mailing Address", texts)
    row["Phone"]           = after("Phone", texts)
    row["Facility_Status"] = after("Facility Status", texts)
    row["Owner_License"]   = after("Owner / License", texts)
    row["Hours_Mon"]       = after("Monday", texts)
    row["Hours_Tue"]       = after("Tuesday", texts)
    row["Hours_Wed"]       = after("Wednesday", texts)
    row["Hours_Thu"]       = after("Thursday", texts)
    row["Hours_Fri"]       = after("Friday", texts)
    row["Hours_Sat"]       = after("Saturday", texts)
    row["Hours_Sun"]       = after("Sunday", texts)

    # Offsite and Manufacture — only grab if the value doesn't look like a license block
    offsite = after("Offsite Cultivation Address", texts)
    if offsite and not offsite.startswith("License") and not offsite.startswith("00000"):
        row["Offsite_Cultivation_Address"] = offsite

    manufacture = after("Manufacture Address", texts)
    if manufacture and not manufacture.startswith("License") and not manufacture.startswith("00000"):
        row["Manufacture_Address"] = manufacture

    # ── License blocks ────────────────────────────────────────────────────────
    # Find all occurrences of "License Type" — each is a license block
    lic_type_indices = [i for i, t in enumerate(texts) if t.strip() == "License Type"]

    for lic_num, idx in enumerate(lic_type_indices[:2]):
        prefix = f"Lic{lic_num+1}_"
        # Slice just this license block (up to next "License Type" or end)
        end = lic_type_indices[lic_num + 1] if lic_num + 1 < len(lic_type_indices) else idx + 30
        block = texts[idx:end]

        row[f"{prefix}Type"]       = block[1].strip() if len(block) > 1 else ""
        row[f"{prefix}Services"]   = after("Services", block)
        row[f"{prefix}Originally"] = after("Licensed Originally", block)
        row[f"{prefix}Effective"]  = after("License Effective", block)
        row[f"{prefix}Expires"]    = after("License Expires", block)
        row[f"{prefix}Status"]     = after("License Status", block)

    # License numbers and PDF URLs from anchor links
    for i, lnk in enumerate(links[:2]):
        prefix = f"Lic{i+1}_"
        row[f"{prefix}Number"]  = lnk["text"]
        row[f"{prefix}PDF_URL"] = lnk["href"]

    return row


def scrape_table_rows(page, tab_data_value):
    """Click a tab by data-tab-value and extract table rows via data-cell-value."""
    try:
        clicked = page.evaluate(f"""() => {{
            const click = (root) => {{
                const tabs = root.querySelectorAll('a[data-tab-value]');
                for (const t of tabs) {{
                    if (t.getAttribute('data-tab-value').toLowerCase() === '{tab_data_value.lower()}') {{
                        t.click(); return true;
                    }}
                }}
                for (const el of root.querySelectorAll('*')) {{
                    if (el.shadowRoot && click(el.shadowRoot)) return true;
                }}
                return false;
            }};
            return click(document);
        }}""")

        if not clicked:
            return []

        time.sleep(2)

        rows = page.evaluate("""() => {
            const seen = new Set();
            const results = [];
            const extract = (root) => {
                root.querySelectorAll('tr[data-row-key-value]').forEach(tr => {
                    if (tr.getAttribute('data-row-key-value') === 'HEADER') return;
                    const row = {};
                    tr.querySelectorAll('[data-label][data-cell-value]').forEach(cell => {
                        const label = cell.getAttribute('data-label').trim();
                        const value = cell.getAttribute('data-cell-value').trim();
                        if (label) row[label] = value;
                    });
                    // Walk into shadow roots to find the anchor with the number/link
                    const findAnchor = (r) => {
                        const anchors = r.querySelectorAll('a');
                        for (const a of anchors) {
                            const txt = a.innerText ? a.innerText.trim() : '';
                            if (txt) return a;
                        }
                        for (const el of r.querySelectorAll('*')) {
                            if (el.shadowRoot) {
                                const found = findAnchor(el.shadowRoot);
                                if (found) return found;
                            }
                        }
                        return null;
                    };
                    const anchor = findAnchor(tr);
                    if (anchor) {
                        row['_link_text'] = anchor.innerText.trim();
                        const href = anchor.getAttribute('href') || '';
                        row['_link_url'] = href.replace('/../', 'https://azcarecheck.azdhs.gov/');
                    }
                    const key = row['_link_url'] || row['_link_text'] || JSON.stringify(row);
                    if (!seen.has(key) && Object.keys(row).length > 0) {
                        seen.add(key);
                        results.push(row);
                    }
                });
                root.querySelectorAll('*').forEach(el => {
                    if (el.shadowRoot) extract(el.shadowRoot);
                });
            };
            extract(document);
            return results;
        }""")
        return rows
    except Exception as e:
        print(f"      Tab error ({tab_data_value}): {e}")
        return []


def main():
    with open(URL_FILE) as f:
        urls = [u.strip() for u in f if u.strip()]

    facilities_rows = []

    # Write header immediately so file exists from the start
    with open(FACILITIES, "w", newline="", encoding="utf-8") as f:
        csv.DictWriter(f, fieldnames=FACILITY_HEADERS, extrasaction="ignore").writeheader()

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page    = browser.new_page()

        for i, url in enumerate(urls):
            fid_match  = re.search(r'facilityId=([^&]+)', url)
            facility_id = fid_match.group(1) if fid_match else f"unknown_{i}"
            print(f"[{i+1}/{len(urls)}] {facility_id}")

            try:
                # ── Load detail page ──────────────────────────────────────────
                page.goto(url, wait_until="networkidle", timeout=30000)

                # Wait for the Legal Name label to appear — signals detail loaded
                try:
                    page.wait_for_function("""() => {
                        const find = (root) => {
                            for (const el of root.querySelectorAll('*')) {
                                if (el.shadowRoot && find(el.shadowRoot)) return true;
                                if (el.children.length === 0 &&
                                    el.innerText && el.innerText.trim() === 'Legal Name') return true;
                            }
                            return false;
                        };
                        return find(document);
                    }""", timeout=15000)
                except:
                    print(f"      Timeout waiting for detail — skipping license data")

                time.sleep(1)

                # ── Extract all text + links ──────────────────────────────────
                result = page.evaluate(EXTRACT_JS)
                texts  = result.get("allText", [])
                links  = result.get("links", [])
                # Use h4/h3 directly from header component — most reliable
                row = parse_page_text(texts, links, facility_id, url)
                if result.get("business_name"):
                    row["Business_Name"] = result["business_name"]
                if result.get("header_legal_name"):
                    row["Legal_Name"] = result["header_legal_name"]
                facilities_rows.append(row)

                # Write row immediately — safe even if Ctrl+C
                with open(FACILITIES, "a", newline="", encoding="utf-8") as f:
                    w = csv.DictWriter(f, fieldnames=FACILITY_HEADERS, extrasaction="ignore")
                    w.writerow(row)

                lic_numbers = [row["Lic1_Number"], row["Lic2_Number"]]
                lic_numbers = [l for l in lic_numbers if l]

                print(f"      {row['Business_Name']} | {row['Legal_Name']} | "
                      f"Lic1: {row['Lic1_Number']} | Lic2: {row['Lic2_Number']}")

                # ── Inspections tab ───────────────────────────────────────────
                insp_rows = scrape_table_rows(page, "Inspections")
                if insp_rows:
                    targets = lic_numbers if lic_numbers else [facility_id]
                    for lic in targets:
                        fpath = os.path.join(INSP_DIR, f"inspections-{lic}.csv")
                        if not os.path.exists(fpath):
                            with open(fpath, "w", newline="", encoding="utf-8") as f:
                                w = csv.writer(f)
                                w.writerow(INSP_HEADERS)
                                for r in insp_rows:
                                    insp_num = r.get("_link_text", "")
                                    w.writerow([
                                        facility_id,
                                        insp_num,
                                        r.get("Inspection Date(s)", ""),
                                        r.get(" Inspection Type", r.get("Inspection Type", "")),
                                        r.get(" Location Type", r.get("Location Type", "")),
                                        r.get(" Worksheet Type", r.get("Worksheet Type", "")),
                                        r.get(" License Number", r.get("License Number", "")),
                                        r.get("Status", ""),
                                    ])
                    print(f"      Inspections: {len(insp_rows)} rows")

                # ── Enforcements tab ──────────────────────────────────────────
                # Reload page to reset tab state cleanly
                page.goto(url, wait_until="networkidle", timeout=30000)
                time.sleep(2)

                enf_rows = scrape_table_rows(page, "enforcements")
                if enf_rows:
                    targets = lic_numbers if lic_numbers else [facility_id]
                    for lic in targets:
                        fpath = os.path.join(ENF_DIR, f"enforcements-{lic}.csv")
                        if not os.path.exists(fpath):
                            with open(fpath, "w", newline="", encoding="utf-8") as f:
                                w = csv.writer(f)
                                w.writerow(ENF_HEADERS)
                                for r in enf_rows:
                                    w.writerow([
                                        facility_id,
                                        r.get("_link_text", ""),
                                        r.get("_link_url", ""),
                                        r.get("Date Finalized", ""),
                                        r.get("License Type", ""),
                                        r.get("License Number", ""),
                                        r.get("Status", ""),
                                    ])
                    print(f"      Enforcements: {len(enf_rows)} rows")

            except Exception as e:
                print(f"      ERROR: {e}")
                row = {h: "" for h in FACILITY_HEADERS}
                row["Facility_ID"]    = facility_id
                row["Source_URL"]     = url
                row["Business_Name"]  = f"ERROR: {e}"
                facilities_rows.append(row)
                with open(FACILITIES, "a", newline="", encoding="utf-8") as f:
                    w = csv.DictWriter(f, fieldnames=FACILITY_HEADERS, extrasaction="ignore")
                    w.writerow(row)

            time.sleep(1)

        browser.close()

    print(f"\nDone. {len(facilities_rows)} rows → {FACILITIES}")


if __name__ == "__main__":
    main()
