import csv, re

def slugify(name):
    if not name: return ''
    s = name.lower().strip()
    s = re.sub(r'[^a-z0-9]', '', s)
    if s[:3] == 'the': s = s[3:]
    for suffix in ['genetics', 'genetix', 'seeds', 'seed', 'bank', 'llc', 'co', 'inc', 'corp', 'ltd', 'company', 'farms', 'farm', 'international', 'enterprises', 'supply', 'productions', 'production']:
        if s.endswith(suffix): s = s[:-len(suffix)]
    return s

STATE = r'c:\Users\uthin\Desktop\NEW-SEEDS-LAW\pipeline\04_human_in_the_loop\output\state-verified.csv'
MASTER = r'c:\Users\uthin\Desktop\NEW-SEEDS-LAW\pipeline\05_seed_breeders\breeders-master.csv'

# Build breeder slug set from slug and dba_slug (re-slugified with fuzzy logic)
breeder_slugs = set()
with open(MASTER, encoding='utf-8', errors='replace') as f:
    for row in csv.DictReader(f):
        for field in ['name', 'dba']:
            s = slugify(row.get(field, ''))
            if s:
                breeder_slugs.add(s)

print(f"Breeder unique fuzzy slugs: {len(breeder_slugs)}")

# Load state, add column, match
with open(STATE, encoding='utf-8') as f:
    reader = csv.DictReader(f)
    headers = reader.fieldnames
    rows = list(reader)

if 'other_license' not in headers:
    headers.append('other_license')

matches = 0
for row in rows:
    hit = False
    for field in ['name', 'dba']:
        val = row.get(field, '')
        for part in val.split('|'):
            if slugify(part) in breeder_slugs:
                hit = True
                break
        if hit:
            break
    row['other_license'] = 'TRUE' if hit else ''
    if hit:
        matches += 1

with open(STATE, 'w', newline='', encoding='utf-8') as f:
    w = csv.DictWriter(f, fieldnames=headers)
    w.writeheader()
    w.writerows(rows)

print(f"State rows: {len(rows)}")
print(f"Matches: {matches}")

print("\nAll matches:")
for row in rows:
    if row['other_license'] == 'TRUE':
        print(f"  {row.get('name','')}  |  dba={row.get('dba','')}")
