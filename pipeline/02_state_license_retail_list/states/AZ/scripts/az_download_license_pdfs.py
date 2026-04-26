"""
AZ License PDF Downloader
Written by Amazon Q for Loyal9 / poweredby.ci

Reads Lic1_PDF_URL and Lic2_PDF_URL from AZ-facilities-v2.csv,
navigates to each Salesforce page, clicks "Download as PDF",
and saves to pdf/license/{license_number}/Facility Certificate.pdf
"""

import csv
import os
import time
from playwright.sync_api import sync_playwright

BASE_DIR    = os.path.dirname(os.path.abspath(__file__))
STATE_DIR   = os.path.abspath(os.path.join(BASE_DIR, ".."))
FACILITIES  = os.path.join(STATE_DIR, "AZ-facilities-v2.csv")
PDF_BASE    = os.path.join(STATE_DIR, "pdf", "license")

os.makedirs(PDF_BASE, exist_ok=True)


def main():
    # Build list of (license_number, pdf_url) pairs from both license columns
    targets = []
    with open(FACILITIES, newline="", encoding="utf-8-sig") as f:
        for row in csv.DictReader(f):
            for n in ("1", "2"):
                lic_num = row.get(f"Lic{n}_Number", "").strip()
                pdf_url = row.get(f"Lic{n}_PDF_URL", "").strip()
                if lic_num and pdf_url:
                    targets.append((lic_num, pdf_url))

    # Deduplicate by license number
    seen = set()
    unique = []
    for lic_num, pdf_url in targets:
        if lic_num not in seen:
            seen.add(lic_num)
            unique.append((lic_num, pdf_url))

    print(f"Found {len(unique)} unique licenses to download")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(accept_downloads=True)
        page    = context.new_page()

        for i, (lic_num, pdf_url) in enumerate(unique):
            save_dir = os.path.join(PDF_BASE, lic_num)
            os.makedirs(save_dir, exist_ok=True)
            dest = os.path.join(save_dir, f"Facility Certificate {lic_num}.pdf")

            if os.path.exists(dest):
                print(f"[{i+1}/{len(unique)}] Already exists — skipping {lic_num}")
                continue

            print(f"[{i+1}/{len(unique)}] {lic_num}")

            try:
                page.goto(pdf_url, wait_until="networkidle", timeout=30000)
                time.sleep(2)

                # Click Download as PDF button
                with page.expect_download(timeout=15000) as dl_info:
                    clicked = page.evaluate("""() => {
                        const btns = document.querySelectorAll('button[title="Download as PDF"]');
                        if (btns.length > 0) { btns[0].click(); return true; }
                        return false;
                    }""")
                    if not clicked:
                        print(f"      Button not found — skipping")
                        continue
                    time.sleep(1)

                download = dl_info.value
                download.save_as(dest)
                print(f"      Saved: Facility Certificate {lic_num}.pdf")

            except Exception as e:
                print(f"      ERROR: {e}")

            time.sleep(1)

        browser.close()

    print("\nDone.")


if __name__ == "__main__":
    main()
