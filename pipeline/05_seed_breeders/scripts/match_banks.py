import csv, re

def slugify(name):
    if not name: return ''
    s = name.lower().strip()
    s = re.sub(r'[^a-z0-9\s-]', '', s)
    s = re.sub(r'[\s_]+', '-', s).strip('-')
    return re.sub(r'-+', '-', s)

def fuzzy(name):
    if not name: return ''
    s = name.lower().strip()
    s = re.sub(r'[^a-z0-9]', '', s)
    if s[:3] == 'the': s = s[3:]
    for suffix in ['genetics', 'genetix', 'seeds', 'seed', 'bank', 'llc', 'co', 'inc', 'corp', 'ltd', 'company', 'farms', 'farm', 'international', 'enterprises', 'supply', 'productions', 'production']:
        if s.endswith(suffix): s = s[:-len(suffix)]
    return s

BANKS = [
    'Deeply Rooted Seed Bank',
    'Attitude Seed Bank USA',
    'Darkstar Genetics Seed Bank',
    'US Seed Hub',
    'DC Seed Exchange',
]

# 1) Check master and add slugs
master_path = r'c:\Users\uthin\Desktop\NEW-SEEDS-LAW\pipeline\05_seed_breeders\breeders-master.csv'
with open(master_path, encoding='utf-8') as f:
    reader = csv.DictReader(f)
    headers = reader.fieldnames
    rows = list(reader)

found = set()
for row in rows:
    if row['name'] in BANKS:
        found.add(row['name'])
        if not row.get('slug'):
            row['slug'] = slugify(row['name'])
            print(f"  Added slug: {row['name']} -> {row['slug']}")
        else:
            print(f"  Already has slug: {row['name']} -> {row['slug']}")

missing = [b for b in BANKS if b not in found]
if missing:
    print(f"\n  NOT in master (need to add): {missing}")

with open(master_path, 'w', newline='', encoding='utf-8') as f:
    w = csv.DictWriter(f, fieldnames=headers)
    w.writeheader()
    w.writerows(rows)
print(f"\nMaster updated ({len(rows)} rows)")

# 2) Match against USDA/state/sellers
bank_fuzzy = {fuzzy(b): b for b in BANKS}
print(f"\nBank fuzzy slugs: {bank_fuzzy}")

def match_dataset(path, label, name_col='name', dba_col='dba', firm_col=None):
    hits = []
    with open(path, encoding='utf-8') as f:
        for row in csv.DictReader(f):
            if firm_col:
                n = row.get(firm_col, '').strip()
                if not n or n.startswith('Page '): continue
                s = fuzzy(n)
                if s in bank_fuzzy:
                    hits.append((n, 'firm', s, bank_fuzzy[s]))
            else:
                n = row.get(name_col, '').strip()
                d = row.get(dba_col, '').strip()
                if n:
                    s = fuzzy(n)
                    if s in bank_fuzzy:
                        hits.append((n, 'name', s, bank_fuzzy[s]))
                if d:
                    s = fuzzy(d)
                    if s in bank_fuzzy:
                        hits.append((d, 'dba', s, bank_fuzzy[s]))

    print(f"\n{label}: {len(hits)} matches")
    for src, mtype, slug, bank in hits:
        print(f"  {src} ({mtype}) [{slug}] -> {bank}")

base = r'c:\Users\uthin\Desktop\NEW-SEEDS-LAW\pipeline\04_human_in_the_loop\output'
match_dataset(f'{base}\\usda-verified.csv', 'USDA')
match_dataset(f'{base}\\state-verified.csv', 'STATE')
match_dataset(r'c:\Users\uthin\Desktop\NEW-SEEDS-LAW\pipeline\05_seed_breeders\csv\Dir_RegisteredSeedSellers.csv', 'CA_SELLERS', firm_col='Firm')
