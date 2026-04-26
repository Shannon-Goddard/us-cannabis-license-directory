import csv

files = {
    "usda-verified.csv": r"c:\Users\uthin\Desktop\NEW-SEEDS-LAW\pipeline\04_human_in_the_loop\output\usda-verified.csv",
    "seedfinder-verified.csv": r"c:\Users\uthin\Desktop\NEW-SEEDS-LAW\pipeline\04_human_in_the_loop\output\seedfinder-verified.csv",
    "state-verified.csv": r"c:\Users\uthin\Desktop\NEW-SEEDS-LAW\pipeline\04_human_in_the_loop\output\state-verified.csv",
}

for name, path in files.items():
    try:
        with open(path, newline="", encoding="utf-8-sig", errors="replace") as f:
            reader = csv.DictReader(f)
            headers = reader.fieldnames
            rows = list(reader)
        print(f"=== {name} ===")
        print(f"  Rows: {len(rows)}")
        print(f"  Headers: {headers}")
        print()
    except Exception as e:
        print(f"=== {name} === {e}\n")
