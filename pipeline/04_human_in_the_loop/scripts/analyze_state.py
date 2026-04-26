import csv

PATH = r"c:\Users\uthin\Desktop\NEW-SEEDS-LAW\pipeline\04_human_in_the_loop\output\state-verified.csv"

with open(PATH, newline="", encoding="utf-8-sig", errors="replace") as f:
    reader = csv.DictReader(f)
    headers = reader.fieldnames
    rows = list(reader)

print(f"=== state-verified.csv ===")
print(f"Rows: {len(rows)}")
print(f"Headers: {headers}")

# Coverage
def has(row, field):
    return bool(row.get(field, "").strip())

fields = ["name", "dba", "slug", "dba_slug", "type", "url", "street_address", "city", "state", "zip_code", "lat", "lng", "phone", "email", "license_state"]
print(f"\n=== Data Coverage ===")
for f in fields:
    count = sum(1 for r in rows if has(r, f))
    pct = round(count / len(rows) * 100, 1)
    print(f"  {f:<20} {count:>6}  ({pct}%)")

# State breakdown
states = {}
for r in rows:
    s = r.get("state", "").strip()
    states[s] = states.get(s, 0) + 1
print(f"\n=== States ({len(states)}) ===")
for s, c in sorted(states.items()):
    print(f"  {s}: {c}")

# Type breakdown
types = {}
for r in rows:
    t = r.get("type", "").strip()
    types[t] = types.get(t, 0) + 1
print(f"\n=== Type Breakdown ===")
for t, c in sorted(types.items(), key=lambda x: -x[1]):
    print(f"  {t}: {c}")

# Empty names
empty_names = sum(1 for r in rows if not has(r, "name"))
print(f"\n=== Quality Checks ===")
print(f"  Empty names: {empty_names}")

# Bad slugs
bad_slugs = sum(1 for r in rows if not has(r, "slug"))
print(f"  Empty slugs: {bad_slugs}")

# Zip code check — all should be 5 digits or blank
bad_zips = []
for r in rows:
    z = r.get("zip_code", "").strip()
    if z and (len(z) != 5 or not z.isdigit()):
        bad_zips.append(z)
print(f"  Non-5-digit zips: {len(bad_zips)}")
if bad_zips:
    from collections import Counter
    for z, c in Counter(bad_zips).most_common(10):
        print(f"    '{z}': {c}")

# Rows with no address, phone, email, or coords
bare = sum(1 for r in rows if not has(r, "street_address") and not has(r, "phone") and not has(r, "email") and not has(r, "lat"))
print(f"  Bare rows (no addr/phone/email/coords): {bare}")

# Duplicate slugs
from collections import Counter
slug_counts = Counter(r.get("slug", "") for r in rows if has(r, "slug"))
dupes = {s: c for s, c in slug_counts.items() if c > 1}
print(f"  Duplicate slugs: {len(dupes)} unique slugs appear more than once ({sum(dupes.values())} total rows)")
if dupes:
    print(f"  Top 10 duplicate slugs:")
    for s, c in sorted(dupes.items(), key=lambda x: -x[1])[:10]:
        print(f"    {s}: {c}")
