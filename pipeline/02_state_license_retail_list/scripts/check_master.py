import csv, sys
sys.stdout.reconfigure(encoding='utf-8')
rows = list(csv.DictReader(open('../master-facilities-active.csv', encoding='utf-8')))
by_state = {}
for r in rows:
    by_state[r['Source_State']] = by_state.get(r['Source_State'], 0) + 1
print(f'Active by state ({len(rows)} total):')
for s, c in sorted(by_state.items()):
    print(f'  {s}: {c}')
print(f'\nField coverage:')
for field in ['License_Number','Phone','Email','GPS (Latitude)','Expiration_Date']:
    key = 'Latitude' if 'GPS' in field else field
    n = sum(1 for r in rows if r.get(key,''))
    print(f'  {field:<20} {n:>6} / {len(rows)} ({100*n//len(rows)}%)')
