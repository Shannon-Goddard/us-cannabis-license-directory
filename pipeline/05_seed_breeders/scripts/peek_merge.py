import csv

master_path = r"c:\Users\uthin\Desktop\NEW-SEEDS-LAW\pipeline\05_seed_breeders\breeders-master.csv"
info_path = r"c:\Users\uthin\Desktop\NEW-SEEDS-LAW\pipeline\05_seed_breeders\breeder_info.csv"

for label, path in [("MASTER", master_path), ("INFO", info_path)]:
    with open(path, newline="", encoding="utf-8-sig", errors="replace") as f:
        reader = csv.DictReader(f)
        headers = reader.fieldnames
        rows = list(reader)
    print(f"=== {label} ===")
    print(f"  Rows: {len(rows)}")
    print(f"  Headers: {headers}")
    
    # Count URLs
    has_url = sum(1 for r in rows if r.get("url", "").strip())
    print(f"  Has URL: {has_url}")
    
    # Sample
    for r in rows[:3]:
        print(f"  {r.get('name','')[:40]} | {r.get('url','')[:50]}")
    print()

# Check overlap by URL
with open(master_path, newline="", encoding="utf-8-sig", errors="replace") as f:
    master_rows = list(csv.DictReader(f))
with open(info_path, newline="", encoding="utf-8-sig", errors="replace") as f:
    info_rows = list(csv.DictReader(f))

def clean_url(u):
    u = u.strip().lower().rstrip("/")
    for prefix in ["https://www.", "http://www.", "https://", "http://"]:
        if u.startswith(prefix):
            u = u[len(prefix):]
    return u

master_urls = {clean_url(r.get("url", "")) for r in master_rows if r.get("url", "").strip()}
info_urls = {clean_url(r.get("url", "")) for r in info_rows if r.get("url", "").strip()}

overlap = master_urls & info_urls
info_only = info_urls - master_urls

print(f"=== URL Overlap ===")
print(f"  Master URLs: {len(master_urls)}")
print(f"  Info URLs: {len(info_urls)}")
print(f"  Overlap: {len(overlap)}")
print(f"  Info only (new): {len(info_only)}")

# Check shared headers
master_h = set(csv.DictReader(open(master_path, encoding="utf-8-sig")).fieldnames)
info_h = set(csv.DictReader(open(info_path, encoding="utf-8-sig")).fieldnames)
shared = master_h & info_h
info_extra = info_h - master_h
print(f"\n=== Shared Headers ===")
print(f"  Shared: {sorted(shared)}")
print(f"  In info but not master: {sorted(info_extra)}")
