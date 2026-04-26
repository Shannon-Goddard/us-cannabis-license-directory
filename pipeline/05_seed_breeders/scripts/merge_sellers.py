import csv, re

US_STATES = {
    'AL','AK','AZ','AR','CA','CO','CT','DE','FL','GA','HI','ID','IL','IN','IA',
    'KS','KY','LA','ME','MD','MA','MI','MN','MS','MO','MT','NE','NV','NH','NJ',
    'NM','NY','NC','ND','OH','OK','OR','PA','RI','SC','SD','TN','TX','UT','VT',
    'VA','WA','WV','WI','WY','DC','PR','GU','VI','AS','MP','ca'
}

COUNTRY_KEYWORDS = {
    'Canada': 'Canada', 'UK': 'UK', 'Italy': 'Italy', 'Israel': 'Israel',
    'Japan': 'Japan', 'Thailand': 'Thailand', 'The Netherlands': 'Netherlands',
    'South Africa': 'South Africa', 'Jordan': 'Jordan',
}

def slugify(name):
    if not name: return ''
    s = name.lower().strip()
    if s.startswith('the '): s = s[4:]
    s = re.sub(r'[^a-z0-9\s-]', '', s)
    s = re.sub(r'[\s_]+', '-', s).strip('-')
    return re.sub(r'-+', '-', s)

def parse_address(addr):
    result = {'street_address': '', 'city': '', 'state': '', 'zip_code': '', 'country': 'USA'}
    if not addr:
        return result
    for kw, country in COUNTRY_KEYWORDS.items():
        if addr.rstrip().endswith(kw):
            result['country'] = country
            addr = addr[:addr.rfind(kw)].rstrip(' ,')
            break
    m = re.search(r',\s*([A-Za-z]{2})\s+(\d{5}(?:-?\d{0,4})?)\s*$', addr)
    if m:
        result['state'] = m.group(1).upper()
        result['zip_code'] = m.group(2)[:5]
        rest = addr[:m.start()].strip()
        parts = [p.strip() for p in rest.split(',')]
        if len(parts) >= 2:
            result['street_address'] = ', '.join(parts[:-1])
            result['city'] = parts[-1]
        elif len(parts) == 1:
            result['city'] = parts[0]
        return result
    if result['country'] != 'USA':
        result['street_address'] = addr
        result['state'] = ''
        result['zip_code'] = ''
    else:
        result['street_address'] = addr
        result['country'] = ''
    return result

JUNK = {'Inc.', 'Japan', 'MO 63017', '2847', 'area, P.O. Box 245 Ammam Postal Code 11732,',
        'ammam/Jordan,', 'Khanong District, Bankonk 10260 Thailand,',
        'Street, Marj Al-Hammam', '1L5,', '10170,', '63017', '92673', '695'}

MASTER = r'c:\Users\uthin\Desktop\NEW-SEEDS-LAW\pipeline\05_seed_breeders\breeders-master.csv'
SELLERS = r'c:\Users\uthin\Desktop\NEW-SEEDS-LAW\pipeline\05_seed_breeders\csv\Dir_RegisteredSeedSellers.csv'

# Load master
with open(MASTER, encoding='utf-8', errors='replace') as f:
    reader = csv.DictReader(f)
    headers = reader.fieldnames
    master_rows = list(reader)

existing_slugs = {r['slug'] for r in master_rows if r.get('slug')}
print(f"Master: {len(master_rows)} rows, {len(existing_slugs)} slugs")

# Load and parse sellers
new_rows = []
dupes = []
with open(SELLERS, encoding='utf-8', errors='replace') as f:
    for row in csv.DictReader(f):
        name = row.get('name', '').strip()
        if not name or name in JUNK:
            continue
        addr = row.get('address', '').strip()
        p = parse_address(addr)
        slug = slugify(name)

        if slug in existing_slugs:
            dupes.append(name)
            continue

        new = {h: '' for h in headers}
        new['name'] = name
        new['slug'] = slug
        new['type'] = 'other'
        new['is_breeder'] = 'FALSE'
        new['is_bank'] = 'FALSE'
        new['is_cultivator'] = 'FALSE'
        new['is_dispensary'] = 'FALSE'
        new['is_academic'] = 'FALSE'
        new['street_address'] = p['street_address']
        new['city'] = p['city']
        new['state'] = p['state']
        new['zip_code'] = p['zip_code']
        new['country'] = p['country']
        new['is_licensed'] = 'TRUE'
        new['license_other'] = 'CA Registered Seed Seller'

        existing_slugs.add(slug)
        new_rows.append(new)

print(f"New rows to add: {len(new_rows)}")
print(f"Dupes (already in master): {len(dupes)}")
if dupes:
    for d in dupes:
        print(f"  skip: {d}")

# Write
all_rows = master_rows + new_rows
with open(MASTER, 'w', newline='', encoding='utf-8') as f:
    w = csv.DictWriter(f, fieldnames=headers)
    w.writeheader()
    w.writerows(all_rows)

print(f"\nMaster updated: {len(all_rows)} rows ({len(master_rows)} existing + {len(new_rows)} new)")

# Quick stats on new rows
us = sum(1 for r in new_rows if r['country'] == 'USA')
intl = sum(1 for r in new_rows if r['country'] and r['country'] != 'USA')
no_country = sum(1 for r in new_rows if not r['country'])
print(f"New rows: {us} USA, {intl} international, {no_country} no country (needs review)")
