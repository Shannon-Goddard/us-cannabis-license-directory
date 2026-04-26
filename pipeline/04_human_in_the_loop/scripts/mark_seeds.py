import csv, re

def slugify(name):
    if not name: return ''
    s = name.lower().strip()
    s = re.sub(r'[^a-z0-9]', '', s)
    if s[:3] == 'the': s = s[3:]
    for suffix in ['genetics', 'genetix', 'seeds', 'seed', 'bank', 'llc', 'co', 'inc', 'corp', 'ltd', 'company', 'farms', 'farm', 'international', 'enterprises', 'supply', 'productions', 'production']:
        if s.endswith(suffix): s = s[:-len(suffix)]
    return s

NAMES = r'c:\Users\uthin\Desktop\NEW-SEEDS-LAW\pipeline\03_seed_suppliers\csv\seedfinder-names.csv'
SLUGS_OUT = r'c:\Users\uthin\Desktop\NEW-SEEDS-LAW\pipeline\03_seed_suppliers\csv\seedfinder_slugs.csv'
STATE = r'c:\Users\uthin\Desktop\NEW-SEEDS-LAW\pipeline\04_human_in_the_loop\output\state-verified.csv'

# 1) Build seedfinder_slugs.csv
sf_slugs = set()
with open(NAMES, encoding='utf-8') as f:
    reader = csv.DictReader(f)
    rows = list(reader)

with open(SLUGS_OUT, 'w', newline='', encoding='utf-8') as f:
    w = csv.writer(f)
    w.writerow(['name', 'slug'])
    for row in rows:
        name = row['name'].strip()
        s = slugify(name)
        w.writerow([name, s])
        if s:
            sf_slugs.add(s)

print(f"Seedfinder names: {len(rows)}")
print(f"Unique fuzzy slugs: {len(sf_slugs)}")
print(f"Written: {SLUGS_OUT}")

# 2) Match against state-verified and mark sells_seeds
with open(STATE, encoding='utf-8') as f:
    reader = csv.DictReader(f)
    headers = reader.fieldnames
    state_rows = list(reader)

matches = 0
for row in state_rows:
    hit = False
    for field in ['name', 'dba']:
        val = row.get(field, '')
        for part in val.split('|'):
            if slugify(part) in sf_slugs:
                hit = True
                break
        if hit:
            break
    if hit:
        row['sells_seeds'] = 'TRUE'
        matches += 1

with open(STATE, 'w', newline='', encoding='utf-8') as f:
    w = csv.DictWriter(f, fieldnames=headers)
    w.writeheader()
    w.writerows(state_rows)

print(f"\nState rows: {len(state_rows)}")
print(f"sells_seeds=TRUE: {matches}")

print("\nAll matches:")
for row in state_rows:
    if row.get('sells_seeds') == 'TRUE':
        print(f"  {row.get('name','')}  |  dba={row.get('dba','')}")
