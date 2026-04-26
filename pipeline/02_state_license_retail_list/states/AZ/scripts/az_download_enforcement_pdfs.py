"""
AZ Enforcement PDF Downloader
Written by Amazon Q for Loyal9 / poweredby.ci

Reads AZ-enforcements-master.csv, visits each Enforcement_URL,
clicks the attachments icon, grabs the data-public-url, navigates
to the Salesforce page, and downloads the PDF.

Saves to: pdf/enforcements/{license_number}/{filename}.pdf
"""

import csv
import os
import re
import time
import requests
from playwright.sync_api import sync_playwright

BASE_DIR    = os.path.dirname(os.path.abspath(__file__))
STATE_DIR   = os.path.abspath(os.path.join(BASE_DIR, ".."))
MASTER_CSV  = os.path.join(STATE_DIR, "AZ-enforcements-master.csv")
PDF_BASE    = os.path.join(STATE_DIR, "pdf", "enforcements")

os.makedirs(PDF_BASE, exist_ok=True)


def safe_filename(name):
    return re.sub(r'[\\/*?:"<>|]', "_", name).strip()


def download_pdf(url, dest_path):
    """Download a file from a Salesforce URL using requests."""
    try:
        r = requests.get(url, timeout=30)
        r.raise_for_status()
        with open(dest_path, "wb") as f:
            f.write(r.content)
        return True
    except Exception as e:
        print(f"        Download error: {e}")
        return False


def main():
    # Read master CSV — get unique enforcement URLs with their license numbers
    rows = []
    with open(MASTER_CSV, newline="", encoding="utf-8-sig") as f:
        for row in csv.DictReader(f):
            url = row.get("Enforcement_URL", "").strip()
            lic = row.get("License_Number", "").strip()
            enf = row.get("Enforcement_Num", "").strip()
            if url and lic:
                rows.append({"url": url, "license": lic, "enforcement": enf})

    # Deduplicate by URL
    seen = set()
    unique = []
    for r in rows:
        if r["url"] not in seen:
            seen.add(r["url"])
            unique.append(r)

    print(f"Found {len(unique)} unique enforcement URLs to process")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page    = context.new_page()

        for i, item in enumerate(unique):
            url     = item["url"]
            lic_num = item["license"]
            enf_num = item["enforcement"]
            print(f"[{i+1}/{len(unique)}] {enf_num} | {lic_num}")

            save_dir = os.path.join(PDF_BASE, lic_num)
            os.makedirs(save_dir, exist_ok=True)

            try:
                page.goto(url, wait_until="networkidle", timeout=30000)
                time.sleep(2)

                # Find and click the attachments icon (c-attach-files-modal)
                clicked = page.evaluate("""() => {
                    const find = (root) => {
                        const icon = root.querySelector('c-attach-files-modal lightning-icon');
                        if (icon) { icon.click(); return true; }
                        for (const el of root.querySelectorAll('*')) {
                            if (el.shadowRoot && find(el.shadowRoot)) return true;
                        }
                        return false;
                    };
                    return find(document);
                }""")

                if not clicked:
                    print(f"        No attachment icon found — skipping")
                    continue

                time.sleep(1.5)

                # Find all data-public-url links in the popup
                pdf_links = page.evaluate("""() => {
                    const links = [];
                    const find = (root) => {
                        root.querySelectorAll('a[data-public-url]').forEach(a => {
                            links.push({
                                url: a.getAttribute('data-public-url'),
                                name: a.innerText.trim()
                            });
                        });
                        root.querySelectorAll('*').forEach(el => {
                            if (el.shadowRoot) find(el.shadowRoot);
                        });
                    };
                    find(document);
                    return links;
                }""")

                if not pdf_links:
                    print(f"        No PDF links found in popup")
                    continue

                print(f"        {len(pdf_links)} attachment(s) found")

                for lnk in pdf_links:
                    sf_url  = lnk["url"]
                    name    = safe_filename(lnk["name"]) or enf_num
                    # Convert preview URL to download URL (add # → direct download)
                    dl_url  = sf_url.replace(
                        "/sfc/p/", "/sfc/p/#"
                    ) if "/sfc/p/" in sf_url and "#" not in sf_url else sf_url

                    dest = os.path.join(save_dir, f"{name}.pdf")

                    if os.path.exists(dest):
                        print(f"        Already exists — skipping: {name}.pdf")
                        continue

                    # Navigate to the Salesforce page and click Download as PDF
                    page.goto(sf_url, wait_until="networkidle", timeout=30000)
                    time.sleep(2)

                    # Try clicking the Download as PDF button
                    dl_clicked = page.evaluate("""() => {
                        const btns = document.querySelectorAll('button[title="Download as PDF"]');
                        if (btns.length > 0) { btns[0].click(); return true; }
                        return false;
                    }""")

                    if dl_clicked:
                        # Wait for download
                        try:
                            with page.expect_download(timeout=15000) as dl_info:
                                time.sleep(1)
                            download = dl_info.value
                            download.save_as(dest)
                            print(f"        Saved: {name}.pdf")
                        except Exception:
                            # Fallback: use requests with cookies from browser
                            cookies = context.cookies()
                            session = requests.Session()
                            for c in cookies:
                                session.cookies.set(c["name"], c["value"],
                                                    domain=c.get("domain", ""))
                            r = session.get(dl_url, timeout=30)
                            if r.status_code == 200:
                                with open(dest, "wb") as f:
                                    f.write(r.content)
                                print(f"        Saved (fallback): {name}.pdf")
                            else:
                                print(f"        Failed ({r.status_code}): {name}")
                    else:
                        # Direct download via requests
                        if download_pdf(dl_url, dest):
                            print(f"        Saved (direct): {name}.pdf")

            except Exception as e:
                print(f"        ERROR: {e}")

            time.sleep(1)

        browser.close()

    print("\nDone.")


if __name__ == "__main__":
    main()
