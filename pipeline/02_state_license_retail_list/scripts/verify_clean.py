import csv

path = r"c:\Users\uthin\Desktop\NEW-SEEDS-LAW\pipeline\02_state_license_retail_list\state-clean.csv"

with open(path, newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    headers = reader.fieldnames
    rows = list(reader)

print(f"Headers: {headers}")
print(f"Total: {len(rows)}")

# Verify no empty names
empty_names = [r for r in rows if not r["name"].strip()]
print(f"\nEmpty names: {len(empty_names)}")

# Verify slugs look right
bad_slugs = [r for r in rows if not r["slug"].strip() or " " in r["slug"]]
print(f"Bad slugs (empty or has spaces): {len(bad_slugs)}")
if bad_slugs:
    for r in bad_slugs[:3]:
        print(f"  name='{r['name']}' slug='{r['slug']}'")

# Verify all country = US
non_us = [r for r in rows if r["country"] != "US"]
print(f"Non-US country: {len(non_us)}")

# Verify state codes are 2 letters
bad_states = [r for r in rows if len(r["state"]) != 2]
print(f"Bad state codes: {len(bad_states)}")
if bad_states:
    for r in bad_states[:3]:
        print(f"  state='{r['state']}' name='{r['name']}'")

# DBA check — should be blank when same as name
same_dba = [r for r in rows if r["dba"] and r["dba"].lower() == r["name"].lower()]
print(f"DBA same as name (should be 0): {len(same_dba)}")

# Sample: dispensary type
print(f"\n=== Sample dispensary rows ===")
for r in [r for r in rows if r["type"] == "dispensary"][:3]:
    print(f"  {r['name']} | {r['dba'][:30]} | {r['state']} | {r['license_state']}")

# Sample: cultivator type
print(f"\n=== Sample cultivator rows ===")
for r in [r for r in rows if r["type"] == "cultivator"][:3]:
    print(f"  {r['name']} | {r['dba'][:30]} | {r['state']} | {r['license_state']}")

# Sample: other type
print(f"\n=== Sample other rows ===")
for r in [r for r in rows if r["type"] == "other"][:3]:
    print(f"  {r['name']} | {r['dba'][:30]} | {r['state']} | {r['license_state']}")

# Sample: cultivator|dispensary (vertically integrated)
print(f"\n=== Sample cultivator|dispensary rows ===")
for r in [r for r in rows if r["type"] == "cultivator|dispensary"][:3]:
    print(f"  {r['name']} | {r['state']} | {r['license_state']}")

# Sample: rows with DBA different from name
print(f"\n=== Sample DBA != name ===")
for r in [r for r in rows if r["dba"] and r["dba"].lower() != r["name"].lower()][:5]:
    print(f"  name='{r['name']}' dba='{r['dba'][:40]}'")

# Check for junk in address field
junk_addrs = [r for r in rows if r["street_address"].lower().strip() in ("not published", "not available", "n/a", "none", "data not available")]
print(f"\nJunk addresses: {len(junk_addrs)}")

# Check for rows missing everything (name only)
bare = [r for r in rows if not r["street_address"] and not r["phone"] and not r["email"] and not r["lat"]]
print(f"Bare rows (no address, phone, email, or coords): {len(bare)}")
