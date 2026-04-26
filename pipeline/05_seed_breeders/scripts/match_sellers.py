import csv, re

def slugify(name):
    if not name: return ''
    s = name.lower().strip()
    s = re.sub(r'[^a-z0-9]', '', s)
    if s[:3] == 'the': s = s[3:]
    for suffix in ['genetics', 'genetix', 'seeds', 'seed', 'bank', 'llc', 'co', 'inc', 'corp', 'ltd', 'company', 'farms', 'farm', 'international', 'enterprises', 'supply', 'productions', 'production']:
        if s.endswith(suffix): s = s[:-len(suffix)]
    return s

# Load breeders-master — slugify name and dba fresh
master_by_slug = {}
master_by_dba = {}
with open('../breeders-master.csv', encoding='utf-8') as f:
    for row in csv.DictReader(f):
        s = slugify(row.get('name',''))
        d = slugify(row.get('dba',''))
        if s: master_by_slug[s] = row['name']
        if d: master_by_dba[d] = row['name']

# Load sellers, skip page markers
sellers = []
with open('../csv/Dir_RegisteredSeedSellers.csv', encoding='utf-8') as f:
    for row in csv.DictReader(f):
        firm = row.get('Firm','').strip()
        if not firm or firm.startswith('Page '): continue
        sellers.append(firm)

# Match
name_hits = []
dba_hits = []
for firm in sellers:
    s = slugify(firm)
    if s in master_by_slug:
        name_hits.append((firm, s, master_by_slug[s]))
    if s in master_by_dba:
        dba_hits.append((firm, s, master_by_dba[s]))

print(f"Sellers: {len(sellers)}")
print(f"Breeder master slugs: {len(master_by_slug)}")
print(f"\n--- NAME (slug) matches: {len(name_hits)} ---")
for firm, slug, master_name in name_hits:
    print(f"  {firm}  ->  {master_name}  [{slug}]")

print(f"\n--- DBA (dba_slug) matches: {len(dba_hits)} ---")
for firm, slug, master_name in dba_hits:
    print(f"  {firm}  ->  {master_name}  [{slug}]")
