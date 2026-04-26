import csv

files = {
    "seedfinder-names.csv": r"c:\Users\uthin\Desktop\NEW-SEEDS-LAW\pipeline\05_seed_breeders\input\seedfinder-names.csv",
    "seedfinder-verified.csv": r"c:\Users\uthin\Desktop\NEW-SEEDS-LAW\pipeline\05_seed_breeders\input\seedfinder-verified.csv",
}

for name, path in files.items():
    with open(path, newline="", encoding="utf-8-sig", errors="replace") as f:
        reader = csv.DictReader(f)
        headers = reader.fieldnames
        rows = list(reader)
    print(f"=== {name} ===")
    print(f"  Rows: {len(rows)}")
    print(f"  Headers: {headers}")
    for r in rows[:3]:
        print(f"  {dict(r)}")
    print()
