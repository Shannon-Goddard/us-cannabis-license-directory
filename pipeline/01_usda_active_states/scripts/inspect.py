import csv

raw = r"c:\Users\uthin\Desktop\NEW-SEEDS-LAW\pipeline\01_usda_active_states\csv\USDA_search_tool.csv"
geo = r"c:\Users\uthin\Desktop\NEW-SEEDS-LAW\pipeline\01_usda_active_states\csv\USDA_geocoded.csv"

for label, path in [("RAW", raw), ("GEOCODED", geo)]:
    with open(path, newline="", encoding="utf-8-sig", errors="replace") as f:
        reader = csv.DictReader(f)
        headers = reader.fieldnames
        rows = list(reader)

    print(f"=== {label}: {path.split(chr(92))[-1]} ===")
    print(f"  Rows: {len(rows)}")
    print(f"  Headers: {headers}")

    # Status breakdown
    statuses = {}
    for r in rows:
        s = r.get("Status", "").strip()
        statuses[s] = statuses.get(s, 0) + 1
    print(f"  Status values:")
    for s, c in sorted(statuses.items(), key=lambda x: -x[1]):
        print(f"    {s}: {c}")

    # Sample first 3
    print(f"  First 3 rows:")
    for r in rows[:3]:
        print(f"    {dict(r)}")
    print()
