import csv

STATE = r'c:\Users\uthin\Desktop\NEW-SEEDS-LAW\pipeline\04_human_in_the_loop\output\state-verified.csv'

with open(STATE, encoding='utf-8') as f:
    reader = csv.DictReader(f)
    headers = reader.fieldnames
    rows = list(reader)

for col in ['delivery', 'sells_seeds']:
    if col not in headers:
        headers.append(col)

delivery_count = 0
for row in rows:
    hit = False
    for field in ['name', 'dba']:
        if 'delivery' in row.get(field, '').lower():
            hit = True
            break
    row['delivery'] = 'TRUE' if hit else 'FALSE'
    row['sells_seeds'] = ''
    if hit:
        delivery_count += 1

with open(STATE, 'w', newline='', encoding='utf-8') as f:
    w = csv.DictWriter(f, fieldnames=headers)
    w.writeheader()
    w.writerows(rows)

print(f"Rows: {len(rows)}")
print(f"Delivery=TRUE: {delivery_count}")
