"""
Pipeline 05 — Seedfinder Homepage Scraper
Visits each https://seedfinder.eu/en/database/breeder/ URL,
finds <h3>Links</h3> -> <a class="link" href="...">Homepage</a>,
writes the result back into seedfinder-urls.csv as a new `homepage` column.
Resume-capable: skips rows where homepage is already populated.
"""

import csv
import os
import time
import requests
from bs4 import BeautifulSoup

CSV_PATH = r"c:\Users\uthin\Desktop\NEW-SEEDS-LAW\pipeline\05_seed_suppliers\csv\seedfinder-urls.csv"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
}

DELAY = 1.5  # seconds between requests — polite crawl


def get_homepage(url: str) -> str:
    """Fetch a seedfinder breeder page and return the Homepage link or ''."""
    try:
        resp = requests.get(url, headers=HEADERS, timeout=15)
        if resp.status_code != 200:
            return ""
        soup = BeautifulSoup(resp.text, "html.parser")

        # Find <h3>Links</h3> then look for Homepage anchor in following siblings
        for h3 in soup.find_all("h3"):
            if h3.get_text(strip=True).lower() == "links":
                for sibling in h3.find_next_siblings():
                    if sibling.name == "a" and "homepage" in sibling.get_text(strip=True).lower():
                        return sibling["href"].strip()
                    # also check anchors nested inside sibling
                    for a in sibling.find_all("a"):
                        if "homepage" in a.get_text(strip=True).lower():
                            return a["href"].strip()
                break
    except Exception:
        pass
    return ""


def main():
    # Load existing CSV
    with open(CSV_PATH, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    # Add homepage column if missing
    if "homepage" not in rows[0]:
        for r in rows:
            r["homepage"] = ""

    fieldnames = ["url", "name", "homepage"]

    total     = len(rows)
    remaining = [r for r in rows if not r.get("homepage")]
    done      = total - len(remaining)

    print(f"Total: {total} | Already done: {done} | Remaining: {len(remaining)}")

    for i, row in enumerate(remaining, 1):
        name = row["name"]
        url  = row["url"]
        print(f"[{done + i}/{total}] {name}", end=" ... ", flush=True)

        homepage = get_homepage(url)
        row["homepage"] = homepage
        print(homepage if homepage else "none")

        # Write back after every row so resume works
        with open(CSV_PATH, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)

        time.sleep(DELAY)

    found = sum(1 for r in rows if r.get("homepage"))
    print(f"\nDone. {found}/{total} have a homepage URL.")


if __name__ == "__main__":
    main()
