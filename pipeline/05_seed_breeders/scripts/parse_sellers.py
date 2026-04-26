import csv, re

US_STATES = {
    'AL','AK','AZ','AR','CA','CO','CT','DE','FL','GA','HI','ID','IL','IN','IA',
    'KS','KY','LA','ME','MD','MA','MI','MN','MS','MO','MT','NE','NV','NH','NJ',
    'NM','NY','NC','ND','OH','OK','OR','PA','RI','SC','SD','TN','TX','UT','VT',
    'VA','WA','WV','WI','WY','DC','PR','GU','VI','AS','MP','ca'  # lowercase ca appears
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
    """Parse 'street, city, ST zip' or international formats."""
    result = {'street_address': '', 'city': '', 'state': '', 'zip_code': '', 'country': 'USA'}

    if not addr:
        return result

    # Check for country at end
    for kw, country in COUNTRY_KEYWORDS.items():
        if addr.rstrip().endswith(kw):
            result['country'] = country
            addr = addr[:addr.rfind(kw)].rstrip(' ,')
            break

    # Try to find US state + zip pattern: "ST 12345" or "ST 12345-1234"
    m = re.search(r',\s*([A-Za-z]{2})\s+(\d{5}(?:-?\d{0,4})?)\s*$', addr)
    if m:
        result['state'] = m.group(1).upper()
        result['zip_code'] = m.group(2)[:5]  # trim to 5 digits
        rest = addr[:m.start()].strip()
        parts = [p.strip() for p in rest.split(',')]
        if len(parts) >= 2:
            result['street_address'] = ', '.join(parts[:-1])
            result['city'] = parts[-1]
        elif len(parts) == 1:
            result['city'] = parts[0]
        return result

    # No US pattern found — store whole thing as street_address for manual review
    if result['country'] != 'USA':
        result['street_address'] = addr
        result['state'] = ''
        result['zip_code'] = ''
    else:
        # Might be truncated or malformed US address
        result['street_address'] = addr
        result['country'] = ''  # flag for review

    return result

# Load sellers
sellers = []
JUNK = {'Inc.', 'Japan', 'MO 63017', '2847', 'area, P.O. Box 245 Ammam Postal Code 11732,',
         'ammam/Jordan,', 'Khanong District, Bankonk 10260 Thailand,',
         'Street, Marj Al-Hammam', '1L5,', '10170,', '63017', '92673', '695'}

with open(r'c:\Users\uthin\Desktop\NEW-SEEDS-LAW\pipeline\05_seed_breeders\csv\Dir_RegisteredSeedSellers.csv',
          encoding='utf-8', errors='replace') as f:
    for row in csv.DictReader(f):
        name = row.get('name', '').strip()
        if not name or name in JUNK:
            continue
        sellers.append(row)

print(f"Sellers loaded: {len(sellers)}")

# Parse addresses
parsed = []
problems = []
for row in sellers:
    name = row['name'].strip()
    addr = row.get('address', '').strip()
    p = parse_address(addr)

    rec = {
        'name': name,
        'slug': slugify(name),
        'street_address': p['street_address'],
        'city': p['city'],
        'state': p['state'],
        'zip_code': p['zip_code'],
        'country': p['country'],
    }

    if not p['city'] and p['country'] == 'USA':
        problems.append((name, addr))
    elif p['state'] and p['state'].upper() not in US_STATES and p['country'] == 'USA':
        problems.append((name, addr))

    parsed.append(rec)

print(f"Parsed: {len(parsed)}")
print(f"Problems (no city or bad state): {len(problems)}")
for name, addr in problems[:20]:
    print(f"  {name}: {addr}")

# Stats
has_city = sum(1 for r in parsed if r['city'])
has_state = sum(1 for r in parsed if r['state'])
has_zip = sum(1 for r in parsed if r['zip_code'])
has_street = sum(1 for r in parsed if r['street_address'])
intl = sum(1 for r in parsed if r['country'] != 'USA')
print(f"\nStats: {has_street} street, {has_city} city, {has_state} state, {has_zip} zip, {intl} international")

# Sample output
print("\nSample parsed (first 10):")
for r in parsed[:10]:
    print(f"  {r['name']} | {r['street_address']} | {r['city']} | {r['state']} | {r['zip_code']} | {r['country']}")

print("\nInternational:")
for r in parsed:
    if r['country'] != 'USA' and r['country']:
        print(f"  {r['name']} | {r['street_address']} | {r['country']}")
