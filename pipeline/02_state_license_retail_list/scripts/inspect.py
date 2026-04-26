import csv
import os
import re

BASE = r"c:\Users\uthin\Desktop\NEW-SEEDS-LAW\pipeline\02_state_license_retail_list"

# Check master files
for fname in ["master-facilities.csv", "master-facilities-active.csv", "official_state_license_portals.csv"]:
    path = os.path.join(BASE, fname)
    if os.path.exists(path):
        with open(path, newline="", encoding="utf-8-sig", errors="replace") as f:
            reader = csv.DictReader(f)
            headers = reader.fieldnames
            rows = list(reader)
        print(f"=== {fname} ===")
        print(f"  Rows: {len(rows)}")
        print(f"  Headers: {headers}")
        print()

# Check scripts for API keys
print("=== Checking scripts for API keys ===")
scripts_dir = os.path.join(BASE, "scripts")
for fname in os.listdir(scripts_dir):
    if fname.endswith(".py"):
        path = os.path.join(scripts_dir, fname)
        with open(path, encoding="utf-8") as f:
            content = f.read()
        keys = re.findall(r"AIza[A-Za-z0-9_-]{35}", content)
        tokens = re.findall(r"[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}", content)
        if keys or tokens:
            print(f"  WARNING {fname}: FOUND API KEY(S)")
        else:
            print(f"  OK {fname}: clean")

# Status breakdown in active file
path = os.path.join(BASE, "master-facilities-active.csv")
with open(path, newline="", encoding="utf-8-sig", errors="replace") as f:
    rows = list(csv.DictReader(f))

statuses = {}
for r in rows:
    s = r.get("License_Status", "").strip()
    statuses[s] = statuses.get(s, 0) + 1
print(f"\n=== Active file — License_Status breakdown ===")
for s, c in sorted(statuses.items(), key=lambda x: -x[1]):
    print(f"  '{s}': {c}")

# State breakdown
states = {}
for r in rows:
    s = r.get("Source_State", r.get("State_Code", "")).strip()
    states[s] = states.get(s, 0) + 1
print(f"\n=== Active file — States ({len(states)}) ===")
for s, c in sorted(states.items()):
    print(f"  {s}: {c}")

# License type breakdown
types = {}
for r in rows:
    t = r.get("License_Type", "").strip()
    types[t] = types.get(t, 0) + 1
print(f"\n=== Active file — License_Type (top 20) ===")
for t, c in sorted(types.items(), key=lambda x: -x[1])[:20]:
    print(f"  {t}: {c}")
