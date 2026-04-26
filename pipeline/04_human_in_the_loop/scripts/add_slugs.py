import csv, re

def slugify(name):
    if not name: return ''
    s = name.lower().strip()
    if s.startswith('the '): s = s[4:]
    s = re.sub(r'[^a-z0-9\s-]', '', s)
    s = re.sub(r'[\s_]+', '-', s).strip('-')
    return re.sub(r'-+', '-', s)

STATE = r'c:\Users\uthin\Desktop\NEW-SEEDS-LAW\pipeline\04_human_in_the_loop\output\state-verified.csv'

with open(STATE, encoding='utf-8') as f:
    reader = csv.DictReader(f)
    headers = list(reader.fieldnames)
    rows = list(reader)

# Insert slug and dba_slug after name/dba if not present
for col in ['dba_slug', 'slug']:
    if col not in headers:
        # Insert after 'name' for slug, after 'dba' for dba_slug
        after = 'name' if col == 'slug' else 'dba'
        idx = headers.index(after) + 1 if after in headers else len(headers)
        headers.insert(idx, col)

for row in rows:
    # For pipe-separated names, slug the first one
    name = row.get('name', '').split('|')[0].strip()
    dba = row.get('dba', '').split('|')[0].strip()
    row['slug'] = slugify(name)
    row['dba_slug'] = slugify(dba)

with open(STATE, 'w', newline='', encoding='utf-8') as f:
    w = csv.DictWriter(f, fieldnames=headers)
    w.writeheader()
    w.writerows(rows)

print(f"Rows: {len(rows)}")
print(f"Headers: {headers}")
