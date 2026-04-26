import csv

with open(r"csv\USDA_search_tool.csv", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    states = sorted({row["State"] for row in reader if row["Status"].strip().lower() == "active"})

print(f"Active states ({len(states)}):")
for s in states:
    print(f"  {s}")
