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
USDA = r'c:\Users\uthin\Desktop\NEW-SEEDS-LAW\pipeline\04_human_in_the_loop\output\usda-verified.csv'

# Build USDA slug set from name and dba
usda_slugs = set()
with open(USDA, encoding='utf-8') as f:
    for row in csv.DictReader(f):
        for field in ['name', 'dba']:
            s = slugify(row.get(field, ''))
            if s:
                usda_slugs.add(s)

print(f"USDA unique fuzzy slugs: {len(usda_slugs)}")

# Load state, add column, match
with open(STATE, encoding='utf-8') as f:
    reader = csv.DictReader(f)
    headers = reader.fieldnames
    rows = list(reader)

if 'license_usda' not in headers:
    headers.append('license_usda')

matches = 0
for row in rows:
    hit = False
    for field in ['name', 'dba']:
        val = row.get(field, '')
        # Handle pipe-separated values
        for part in val.split('|'):
            if slugify(part) in usda_slugs:
                hit = True
                break
        if hit:
            break
    row['license_usda'] = 'TRUE' if hit else ''
    if hit:
        matches += 1

print(f"State rows: {len(rows)}")
print(f"Matches: {matches}")

with open(STATE, 'w', newline='', encoding='utf-8') as f:
    w = csv.DictWriter(f, fieldnames=headers)
    w.writeheader()
    w.writerows(rows)

print(f"Written with license_usda column")

# Show some matches
print("\nSample matches:")
count = 0
for row in rows:
    if row['license_usda'] == 'TRUE':
        print(f"  {row.get('name','')}  |  dba={row.get('dba','')}")
        count += 1
        if count >= 15:
            break
