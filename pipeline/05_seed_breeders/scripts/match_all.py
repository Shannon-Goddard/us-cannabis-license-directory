import csv, re

def slugify(name):
    if not name: return ''
    s = name.lower().strip()
    s = re.sub(r'[^a-z0-9]', '', s)
    if s[:3] == 'the': s = s[3:]
    for suffix in ['genetics', 'genetix', 'seeds', 'seed', 'bank', 'llc', 'co', 'inc', 'corp', 'ltd', 'company', 'farms', 'farm', 'international', 'enterprises', 'supply', 'productions', 'production']:
        if s.endswith(suffix): s = s[:-len(suffix)]
    return s

# Load breeders-master
master_by_slug = {}
master_by_dba = {}
with open(r'c:\Users\uthin\Desktop\NEW-SEEDS-LAW\pipeline\05_seed_breeders\breeders-master.csv', encoding='utf-8') as f:
    for row in csv.DictReader(f):
        s = slugify(row.get('name',''))
        d = slugify(row.get('dba',''))
        if s: master_by_slug[s] = row['name']
        if d: master_by_dba[d] = row['name']

# Match a dataset
def match(path, label):
    names = set()
    dbas = set()
    with open(path, encoding='utf-8') as f:
        for row in csv.DictReader(f):
            n = row.get('name','').strip()
            d = row.get('dba','').strip()
            if n: names.add(n)
            if d: dbas.add(d)

    name_hits = []
    dba_hits = []
    for n in names:
        s = slugify(n)
        if s in master_by_slug:
            name_hits.append((n, s, master_by_slug[s]))
        if s in master_by_dba:
            dba_hits.append((n, s, master_by_dba[s]))
    for d in dbas:
        s = slugify(d)
        if s in master_by_slug:
            dba_hits.append((d, s, master_by_slug[s]))
        if s in master_by_dba:
            dba_hits.append((d, s, master_by_dba[s]))

    print(f"\n{'='*60}")
    print(f"{label}: {len(names)} unique names, {len(dbas)} unique dbas")
    print(f"\n  NAME matches: {len(name_hits)}")
    for src, slug, master in name_hits:
        print(f"    {src}  ->  {master}  [{slug}]")
    print(f"\n  DBA matches: {len(dba_hits)}")
    for src, slug, master in dba_hits:
        print(f"    {src}  ->  {master}  [{slug}]")

# Match a dataset and return hits
def match_collect(path):
    names = set()
    dbas = set()
    with open(path, encoding='utf-8') as f:
        for row in csv.DictReader(f):
            n = row.get('name','').strip()
            d = row.get('dba','').strip()
            if n: names.add(n)
            if d: dbas.add(d)

    hits = []
    for n in names:
        s = slugify(n)
        if s in master_by_slug:
            hits.append((n, 'name', s, master_by_slug[s]))
        if s in master_by_dba:
            hits.append((n, 'name->dba', s, master_by_dba[s]))
    for d in dbas:
        s = slugify(d)
        if s in master_by_slug:
            hits.append((d, 'dba', s, master_by_slug[s]))
        if s in master_by_dba:
            hits.append((d, 'dba->dba', s, master_by_dba[s]))
    return hits, len(names), len(dbas)

base = r'c:\Users\uthin\Desktop\NEW-SEEDS-LAW\pipeline\04_human_in_the_loop\output'
out = r'c:\Users\uthin\Desktop\NEW-SEEDS-LAW\pipeline\05_seed_breeders\csv'

datasets = [
    (f'{base}\\usda-verified.csv', 'USDA', f'{out}\\match-usda.csv'),
    (f'{base}\\state-verified.csv', 'STATE', f'{out}\\match-state.csv'),
    (r'c:\Users\uthin\Desktop\NEW-SEEDS-LAW\pipeline\05_seed_breeders\csv\Dir_RegisteredSeedSellers.csv', 'CA_SELLERS', f'{out}\\match-sellers.csv'),
]

for path, label, outpath in datasets:
    if label == 'CA_SELLERS':
        names = set()
        with open(path, encoding='utf-8') as f:
            for row in csv.DictReader(f):
                firm = row.get('Firm','').strip()
                if firm and not firm.startswith('Page '): names.add(firm)
        hits = []
        for n in names:
            s = slugify(n)
            if s in master_by_slug:
                hits.append((n, 'firm', s, master_by_slug[s]))
            if s in master_by_dba:
                hits.append((n, 'firm->dba', s, master_by_dba[s]))
        total_names = len(names)
        total_dbas = 0
    else:
        hits, total_names, total_dbas = match_collect(path)

    with open(outpath, 'w', newline='', encoding='utf-8') as f:
        w = csv.writer(f)
        w.writerow(['source_name', 'match_type', 'fuzzy_slug', 'breeder_master_name'])
        for row in sorted(hits, key=lambda x: x[2]):
            w.writerow(row)

    print(f"{label}: {len(hits)} matches -> {outpath}")
    print(f"  ({total_names} names, {total_dbas} dbas)")
