import csv
from collections import Counter, defaultdict

with open(r'c:\Users\uthin\Desktop\NEW-SEEDS-LAW\pipeline\04_human_in_the_loop\output\state-verified.csv', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    headers = reader.fieldnames
    rows = list(reader)

print(f"Rows: {len(rows)}")
print(f"Headers: {headers}")

# Group by address
groups = defaultdict(list)
no_addr = 0
for r in rows:
    street = r.get('street_address','').strip().lower()
    city = r.get('city','').strip().lower()
    state = r.get('state','').strip().upper()
    zip_code = r.get('zip_code','').strip()
    if not street and not city:
        no_addr += 1
        continue
    key = (street, city, state, zip_code)
    groups[key].append(r)

dupes = {k:v for k,v in groups.items() if len(v) > 1}
singles = {k:v for k,v in groups.items() if len(v) == 1}

print(f"\nNo address: {no_addr}")
print(f"Unique addresses: {len(groups)}")
print(f"Single-row addresses: {len(singles)}")
print(f"Multi-row addresses: {len(dupes)}")
print(f"Total rows in dupe groups: {sum(len(v) for v in dupes.values())}")

# Show examples
print("\nTop 15 dupe addresses:")
for addr, group in sorted(dupes.items(), key=lambda x: -len(x[1]))[:15]:
    print(f"\n  {len(group)}x  {addr}")
    for m in group[:4]:
        print(f"    name={m.get('name','')}  dba={m.get('dba','')}  type={m.get('type','')}  lic={m.get('license_state','')}")
    if len(group) > 4:
        print(f"    ... and {len(group)-4} more")
