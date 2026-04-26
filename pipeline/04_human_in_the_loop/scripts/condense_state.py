import csv, re

INPUT = r'c:\Users\uthin\Desktop\NEW-SEEDS-LAW\pipeline\04_human_in_the_loop\input\state-clean.csv'
OUTPUT = r'c:\Users\uthin\Desktop\NEW-SEEDS-LAW\pipeline\04_human_in_the_loop\output\state-verified.csv'

# Fields to merge with '|' when different
MERGE_FIELDS = ['name', 'dba', 'type', 'license_state', 'phone', 'email', 'url']
# Fields to keep from first row (address, geo, etc.)
KEEP_FIELDS = ['street_address', 'city', 'state', 'zip_code', 'country', 'lat', 'lng', 'is_bad_url']

def addr_key(r):
    """Build address key. Only group if street_address is non-empty."""
    street = r.get('street_address', '').strip().lower()
    city = r.get('city', '').strip().lower()
    state = r.get('state', '').strip().upper()
    zip_code = r.get('zip_code', '').strip()
    if not street:
        return None  # don't group city-only rows
    # Skip California confidential/placeholder addresses
    if 'not published' in street or 'data not available' in street:
        return None
    return (street, city, state, zip_code)

def merge_values(values):
    """Dedupe and join with '|', preserving order. Splits existing '|' values."""
    seen = []
    for v in values:
        for part in v.split('|'):
            part = part.strip()
            if part and part not in seen:
                seen.append(part)
    return '|'.join(seen)

def condense_group(group, headers):
    """Merge a group of rows sharing the same address into one row."""
    if len(group) == 1:
        return group[0]

    merged = {}
    # Keep address/geo from first row
    for f in KEEP_FIELDS:
        merged[f] = group[0].get(f, '')

    # Merge fields with '|'
    for f in MERGE_FIELDS:
        vals = [r.get(f, '') for r in group]
        merged[f] = merge_values(vals)

    # Any remaining headers — take first non-empty
    for h in headers:
        if h not in merged:
            for r in group:
                if r.get(h, '').strip():
                    merged[h] = r[h]
                    break
            if h not in merged:
                merged[h] = ''

    return merged

# Load
with open(INPUT, encoding='utf-8') as f:
    reader = csv.DictReader(f)
    headers = reader.fieldnames
    rows = list(reader)

print(f"Input: {len(rows)} rows")

# Group by address
from collections import defaultdict, OrderedDict
groups = OrderedDict()
no_street = []

for r in rows:
    key = addr_key(r)
    if key is None:
        no_street.append(r)
    else:
        if key not in groups:
            groups[key] = []
        groups[key].append(r)

# Condense
output_rows = []
condensed_count = 0
for key, group in groups.items():
    merged = condense_group(group, headers)
    output_rows.append(merged)
    if len(group) > 1:
        condensed_count += 1

# Add back no-street rows as-is
for r in no_street:
    output_rows.append(r)

print(f"No street address (kept as-is): {len(no_street)}")
print(f"Address groups: {len(groups)}")
print(f"Groups condensed (2+ rows): {condensed_count}")
print(f"Output: {len(output_rows)} rows")
print(f"Rows saved: {len(rows) - len(output_rows)}")

# Write
with open(OUTPUT, 'w', newline='', encoding='utf-8') as f:
    w = csv.DictWriter(f, fieldnames=headers)
    w.writeheader()
    w.writerows(output_rows)

print(f"\nWritten to: {OUTPUT}")

# Show some examples of condensed rows
print("\nExamples of condensed rows:")
for key, group in list(groups.items()):
    if len(group) >= 3:
        merged = condense_group(group, headers)
        print(f"\n  Address: {key}")
        print(f"  {len(group)} rows -> 1")
        print(f"  name: {merged['name']}")
        print(f"  dba: {merged.get('dba','')}")
        print(f"  type: {merged['type']}")
        print(f"  license: {merged.get('license_state','')}")
        condensed_count -= 1
        if condensed_count < len(groups) - 5:
            break
