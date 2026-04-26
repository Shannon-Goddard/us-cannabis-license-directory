"""
Master Facilities Builder — Stage 02
Written by Amazon Q for Loyal9 / poweredby.ci

Merges all state facilities CSVs into a single master dataset.

Master schema (19 fields):
  Source_State, License_Number, Business_Name, Legal_Name,
  License_Type, License_Status,
  Street, City, State_Code, ZIP, County,
  Phone, Email, Website,
  Latitude, Longitude,
  Expiration_Date, Home_Delivery,
  Source_File, Data_Collected

Data_Collected: 04/18/2026 (date Shannon collected each state's data)
"""

import csv
import os
import re

BASE_DIR   = os.path.dirname(os.path.abspath(__file__))
STATES_DIR = os.path.abspath(os.path.join(BASE_DIR, "..", "states"))
OUTPUT_ALL    = os.path.abspath(os.path.join(BASE_DIR, "..", "master-facilities.csv"))
OUTPUT_ACTIVE = os.path.abspath(os.path.join(BASE_DIR, "..", "master-facilities-active.csv"))

HEADERS = [
    "Source_State", "License_Number", "Business_Name", "Legal_Name",
    "License_Type", "License_Status",
    "Street", "City", "State_Code", "ZIP", "County",
    "Phone", "Email", "Website",
    "Latitude", "Longitude",
    "Expiration_Date", "Home_Delivery",
    "Source_File", "Data_Collected",
]

ACTIVE_STATUSES = {
    "active", "active (issued)", "active title certificate",
    "operational with product", "current", "licact",
    "license issued", "open",
    "",  # blank = state doesn't publish status (CO, GA, IL, MD, MO)
}

ADDR_RE = re.compile(r'^(.+),\s+([A-Za-z\s]+),?\s+[A-Z]{2}\s+(\d{5})', re.IGNORECASE)


def is_active(status):
    return status.lower().strip() in ACTIVE_STATUSES


def parse_az_address(raw):
    """Parse AZ single-field address: 'Street, City, AZ ZIP'"""
    m = re.match(r'^(.+),\s+(.+),\s+AZ\s+(\d{5})', raw.strip(), re.IGNORECASE)
    if m:
        return m.group(1).strip(), m.group(2).strip(), m.group(3).strip()
    return raw.strip(), "", ""


def row_template(source_state, collected="04/18/2026"):
    return {
        "Source_State": source_state, "License_Number": "", "Business_Name": "",
        "Legal_Name": "", "License_Type": "", "License_Status": "",
        "Street": "", "City": "", "State_Code": source_state, "ZIP": "", "County": "",
        "Phone": "", "Email": "", "Website": "",
        "Latitude": "", "Longitude": "",
        "Expiration_Date": "", "Home_Delivery": "",
        "Source_File": "", "Data_Collected": collected,
    }


def load_al():
    rows = []
    path = os.path.join(STATES_DIR, "AL", "AL-facilities.csv")
    with open(path, encoding="utf-8") as f:
        for r in csv.DictReader(f):
            row = row_template("AL")
            row.update({
                "License_Number": r["License #"],
                "Business_Name":  r["Legal Name"],
                "License_Type":   r["License Category"],
                "License_Status": r["Status"],
                "Street":         r["Facility Street"],
                "City":           r["Facility City"],
                "State_Code":     r["Facility State"],
                "ZIP":            r["Facility Zip"],
                "County":         r["Facility County"],
                "Phone":          r["Phone"],
                "Website":        r["Website"],
                "Expiration_Date": r["Expires"],
                "Source_File":    "AL-facilities.csv",
            })
            rows.append(row)
    return rows


def load_az():
    rows = []
    path = os.path.join(STATES_DIR, "AZ", "AZ-facilities-v2.csv")
    with open(path, encoding="utf-8") as f:
        for r in csv.DictReader(f):
            street, city, zip_code = parse_az_address(r["Address"])
            row = row_template("AZ")
            row.update({
                "License_Number": r["Lic1_Number"],
                "Business_Name":  r["Business_Name"],
                "Legal_Name":     r["Legal_Name"],
                "License_Type":   r["Lic1_Type"],
                "License_Status": r["Facility_Status"],
                "Street":         street,
                "City":           city,
                "ZIP":            zip_code,
                "Phone":          r["Phone"],
                "Expiration_Date": r["Lic1_Expires"],
                "Source_File":    "AZ-facilities-v2.csv",
            })
            rows.append(row)
    return rows


def load_ca():
    rows = []
    path = os.path.join(STATES_DIR, "CA", "CA-facilities.csv")
    with open(path, encoding="utf-8") as f:
        for r in csv.DictReader(f):
            row = row_template("CA")
            row.update({
                "License_Number": r["licenseNumber"],
                "Business_Name":  r["businessDbaName"] or r["businessLegalName"],
                "Legal_Name":     r["businessLegalName"],
                "License_Type":   r["licenseType"],
                "License_Status": r["licenseStatus"],
                "Street":         r["premiseStreetAddress"],
                "City":           r["premiseCity"],
                "State_Code":     r["premiseState"],
                "ZIP":            r["premiseZipCode"],
                "County":         r["premiseCounty"],
                "Phone":          r["businessPhone"],
                "Email":          r["businessEmail"],
                "Latitude":       r["PremiseLatitude"],
                "Longitude":      r["PremiseLongitude"],
                "Expiration_Date": r["expirationDate"],
                "Source_File":    "CA-facilities.csv",
            })
            rows.append(row)
    return rows


def load_co():
    rows = []
    path = os.path.join(STATES_DIR, "CO", "CO-facilities.csv")
    with open(path, encoding="utf-8") as f:
        for r in csv.DictReader(f):
            row = row_template("CO")
            row.update({
                "License_Number": r["License_Number"],
                "Business_Name":  r["DBA"] or r["Facility_Name"],
                "Legal_Name":     r["Facility_Name"],
                "License_Type":   r["Facility_Type"],
                "Street":         r["Street"],
                "City":           r["City"],
                "ZIP":            r["ZIP_Code"],
                "Expiration_Date": r["Expiration_Date"],
                "Source_File":    "CO-facilities.csv",
            })
            rows.append(row)
    return rows


def load_ct():
    rows = []
    path = os.path.join(STATES_DIR, "CT", "CT-facilities.csv")
    with open(path, encoding="utf-8") as f:
        for r in csv.DictReader(f):
            row = row_template("CT")
            row.update({
                "License_Number": r["License_Number"],
                "Business_Name":  r["DBA"] or r["Business_Name"],
                "Legal_Name":     r["Business_Name"],
                "License_Type":   r["License_Type"],
                "License_Status": r["License_Status"],
                "Street":         r["Street"],
                "City":           r["City"],
                "ZIP":            r["ZIP"],
                "Expiration_Date": r["Expiration_Date"],
                "Source_File":    "CT-facilities.csv",
            })
            rows.append(row)
    return rows


def load_ga():
    rows = []
    path = os.path.join(STATES_DIR, "GA", "GA-facilities.csv")
    with open(path, encoding="utf-8") as f:
        for r in csv.DictReader(f):
            row = row_template("GA")
            row.update({
                "License_Number": r["License_Number"],
                "Business_Name":  r["Business_Name"],
                "Legal_Name":     r["Legal_Name"],
                "Street":         r["Address"],
                "City":           r["City"],
                "ZIP":            r["ZIP"],
                "Latitude":       r["Latitude"],
                "Longitude":      r["Longitude"],
                "Source_File":    "GA-facilities.csv",
            })
            rows.append(row)
    return rows


def load_il():
    rows = []
    path = os.path.join(STATES_DIR, "IL", "IL-facilities.csv")
    with open(path, encoding="utf-8") as f:
        for r in csv.DictReader(f):
            row = row_template("IL")
            row.update({
                "License_Number": r["Credential_Number"],
                "Business_Name":  r["Dispensary_Name"] or r["License_Holder"],
                "Legal_Name":     r["License_Holder"],
                "License_Type":   r["License_Section"],
                "Street":         r["Street"],
                "City":           r["City"],
                "ZIP":            r["ZIP"],
                "Phone":          r["Phone"],
                "Expiration_Date": r["License_Issue_Date"],
                "Source_File":    "IL-facilities.csv",
            })
            rows.append(row)
    return rows


def load_ky():
    rows = []
    path = os.path.join(STATES_DIR, "KY", "KY-facilities.csv")
    with open(path, encoding="utf-8") as f:
        for r in csv.DictReader(f):
            row = row_template("KY")
            row.update({
                "Business_Name":  r["DBA"] or r["License_Holder"],
                "Legal_Name":     r["License_Holder"],
                "License_Type":   r["License_Type"],
                "License_Status": "Active" if r["Approved_To_Operate"] == "Yes" else "Conditional",
                "City":           r["County"],  # KY is county-level only
                "Source_File":    "KY-facilities.csv",
            })
            rows.append(row)
    return rows


def load_ma():
    rows = []
    path = os.path.join(STATES_DIR, "MA", "MA-facilities.csv")
    with open(path, encoding="utf-8") as f:
        for r in csv.DictReader(f):
            row = row_template("MA")
            row.update({
                "License_Number": r["License_Number"],
                "Business_Name":  r["Business_Name"],
                "License_Type":   r["License_Type"],
                "License_Status": r["License_Status"],
                "Street":         r["Establishment_Address_1"],
                "City":           r["Establishment_City"],
                "ZIP":            r["Establishment_ZIP"],
                "County":         r["County"],
                "Phone":          r["Business_Phone"],
                "Email":          r["Business_Email"],
                "Latitude":       r["Latitude"],
                "Longitude":      r["Longitude"],
                "Expiration_Date": r["Lic_Expiration_Date"],
                "Source_File":    "MA-facilities.csv",
            })
            rows.append(row)
    return rows


def load_md():
    rows = []
    path = os.path.join(STATES_DIR, "MD", "MD-facilities.csv")
    with open(path, encoding="utf-8") as f:
        for r in csv.DictReader(f):
            row = row_template("MD")
            row.update({
                "Business_Name": r["Business_Name"],
                "Street":        r["Street"],
                "City":          r["City"],
                "ZIP":           r["ZIP"],
                "Phone":         r["Phone"],
                "Email":         r["Email"],
                "Website":       r["Website"],
                "Source_File":   "MD-facilities.csv",
            })
            rows.append(row)
    return rows


def load_mi():
    rows = []
    path = os.path.join(STATES_DIR, "MI", "MI-facilities.csv")
    with open(path, encoding="utf-8") as f:
        for r in csv.DictReader(f):
            row = row_template("MI")
            row.update({
                "License_Number": r["License_Number"],
                "Business_Name":  r["Business_Name"],
                "License_Type":   r["License_Type"],
                "License_Status": r["License_Status"],
                "Street":         r["Street"],
                "City":           r["City"],
                "ZIP":            r["ZIP"],
                "Expiration_Date": r["Expiration_Date"],
                "Home_Delivery":  r["Home_Delivery"],
                "Source_File":    "MI-facilities.csv",
            })
            rows.append(row)
    return rows


def load_mo():
    rows = []
    path = os.path.join(STATES_DIR, "MO", "MO-facilities.csv")
    with open(path, encoding="utf-8") as f:
        for r in csv.DictReader(f):
            row = row_template("MO")
            row.update({
                "License_Number": r["License_Number"],
                "Business_Name":  r["Business_Name"],
                "Street":         r["Street"],
                "City":           r["City"],
                "ZIP":            r["ZIP"],
                "County":         r["County"],
                "Phone":          r["Phone"],
                "Latitude":       r["Latitude"],
                "Longitude":      r["Longitude"],
                "Source_File":    "MO-facilities.csv",
            })
            rows.append(row)
    return rows


def load_nd():
    rows = []
    path = os.path.join(STATES_DIR, "ND", "ND-facilities.csv")
    with open(path, encoding="utf-8") as f:
        for r in csv.DictReader(f):
            row = row_template("ND")
            row.update({
                "Business_Name": r["Business_Name"],
                "License_Type":  r["License_Type"],
                "License_Status": "Active",
                "Street":        r["Street"],
                "City":          r["City"],
                "Phone":         r["Phone"],
                "Website":       r["Website"],
                "Source_File":   "ND-facilities.csv",
            })
            rows.append(row)
    return rows


def load_nj():
    rows = []
    path = os.path.join(STATES_DIR, "NJ", "NJ-facilities.csv")
    with open(path, encoding="utf-8") as f:
        for r in csv.DictReader(f):
            row = row_template("NJ")
            row.update({
                "Business_Name":  r["Business_Name"],
                "License_Status": "Active",
                "Street":         r["Street"],
                "City":           r["City"],
                "ZIP":            r["ZIP"],
                "Home_Delivery":  r["Delivery"],
                "Source_File":    "NJ-facilities.csv",
            })
            rows.append(row)
    return rows


def load_nv():
    rows = []
    path = os.path.join(STATES_DIR, "NV", "NV-facilities.csv")
    with open(path, encoding="utf-8") as f:
        for r in csv.DictReader(f):
            row = row_template("NV")
            row.update({
                "License_Number": r["License_Number"],
                "Business_Name":  r["Business_Name"],
                "License_Type":   r["License_Type"],
                "License_Status": r["License_Status"],
                "County":         r["County"],
                "Source_File":    "NV-facilities.csv",
            })
            rows.append(row)
    return rows


def load_ny():
    rows = []
    path = os.path.join(STATES_DIR, "NY", "NY-facilities.csv")
    with open(path, encoding="utf-8") as f:
        for r in csv.DictReader(f):
            row = row_template("NY")
            row.update({
                "License_Number": r["License_Number"],
                "Business_Name":  r["DBA"] or r["Entity_Name"],
                "Legal_Name":     r["Entity_Name"],
                "License_Type":   r["License_Type"],
                "License_Status": r["Operational_Status"],
                "Street":         r["Address_1"],
                "City":           r["City"],
                "ZIP":            r["ZIP"],
                "County":         r["County"],
                "Website":        r["Business_Website"],
                "Latitude":       r["Latitude"],
                "Longitude":      r["Longitude"],
                "Expiration_Date": r["Expiration_Date"],
                "Source_File":    "NY-facilities.csv",
            })
            rows.append(row)
    return rows


def load_or():
    rows = []
    path = os.path.join(STATES_DIR, "OR", "OR-facilities.csv")
    with open(path, encoding="utf-8") as f:
        for r in csv.DictReader(f):
            row = row_template("OR")
            row.update({
                "License_Number": r["License_Number"],
                "Business_Name":  r["Business_Name"],
                "Legal_Name":     r["Legal_Name"],
                "License_Type":   r["License_Type"],
                "License_Status": r["Status"],
                "Street":         r["Street"],
                "City":           r["City"],
                "ZIP":            r["ZIP"],
                "County":         r["County"],
                "Expiration_Date": r["Expiration_Date"],
                "Source_File":    "OR-facilities.csv",
            })
            rows.append(row)
    return rows


def load_sd():
    rows = []
    path = os.path.join(STATES_DIR, "SD", "SD-facilities.csv")
    with open(path, encoding="utf-8") as f:
        for r in csv.DictReader(f):
            row = row_template("SD")
            row.update({
                "Business_Name": r["DBA"] or r["Legal_Name"],
                "Legal_Name":    r["Legal_Name"],
                "License_Status": "Active",
                "City":          r["City"],
                "Source_File":   "SD-facilities.csv",
            })
            rows.append(row)
    return rows


def load_ut():
    rows = []
    path = os.path.join(STATES_DIR, "UT", "UT-facilities.csv")
    with open(path, encoding="utf-8") as f:
        for r in csv.DictReader(f):
            row = row_template("UT")
            row.update({
                "Business_Name":  r["Business_Name"],
                "License_Type":   r["License_Type"],
                "License_Status": "Active",
                "Street":         r["Street"],
                "City":           r["City"],
                "ZIP":            r["ZIP"],
                "Phone":          r["Phone"],
                "Email":          r["Email"],
                "Website":        r["Website"],
                "Home_Delivery":  r["Home_Delivery"],
                "Source_File":    "UT-facilities.csv",
            })
            rows.append(row)
    return rows


def load_vt():
    rows = []
    path = os.path.join(STATES_DIR, "VT", "VT-facilities.csv")
    with open(path, encoding="utf-8") as f:
        for r in csv.DictReader(f):
            row = row_template("VT")
            row.update({
                "License_Number": r["License_Number"],
                "Business_Name":  r["Business_Name"],
                "License_Type":   r["License_Type"],
                "License_Status": "Active",
                "City":           r["City"],
                "Expiration_Date": r["Expiration_Date"],
                "Source_File":    "VT-facilities.csv",
            })
            rows.append(row)
    return rows


def load_wa():
    rows = []
    path = os.path.join(STATES_DIR, "WA", "WA-facilities.csv")
    with open(path, encoding="utf-8") as f:
        for r in csv.DictReader(f):
            row = row_template("WA")
            row.update({
                "License_Number": r["License_Number"],
                "Business_Name":  r["Trade_Name"],
                "Legal_Name":     r["Licensee"],
                "License_Type":   r["Privilege_Type"],
                "License_Status": r["Privilege_Status"],
                "Street":         r["Street"],
                "City":           r["City"],
                "ZIP":            r["ZIP"],
                "County":         r["County"],
                "Phone":          r["Phone"],
                "Expiration_Date": r["Expiration_Date"],
                "Source_File":    "WA-facilities.csv",
            })
            rows.append(row)
    return rows


def load_wv():
    rows = []
    path = os.path.join(STATES_DIR, "WV", "WV-facilities.csv")
    with open(path, encoding="utf-8") as f:
        for r in csv.DictReader(f):
            row = row_template("WV")
            row.update({
                "Business_Name":  r["DBA"],
                "Legal_Name":     r["Legal_Name"],
                "License_Status": r["Operational_Status"],
                "Street":         r["Street"],
                "City":           r["City"],
                "ZIP":            r["ZIP"],
                "County":         r["County"],
                "Phone":          r["Phone"],
                "Source_File":    "WV-facilities.csv",
            })
            rows.append(row)
    return rows


LOADERS = [
    load_al, load_az, load_ca, load_co, load_ct,
    load_ga, load_il, load_ky, load_ma, load_md,
    load_mi, load_mo, load_nd, load_nj, load_nv,
    load_ny, load_or, load_sd, load_ut, load_vt,
    load_wa, load_wv,
]


def main():
    all_rows = []
    for loader in LOADERS:
        rows = loader()
        state = rows[0]["Source_State"] if rows else "?"
        print(f"  {state}: {len(rows)} rows")
        all_rows.extend(rows)

    active_rows = [r for r in all_rows if is_active(r["License_Status"])]

    for path, data in [(OUTPUT_ALL, all_rows), (OUTPUT_ACTIVE, active_rows)]:
        with open(path, "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=HEADERS)
            w.writeheader()
            w.writerows(data)

    print(f"\n{len(all_rows)} total records    -> master-facilities.csv")
    print(f"{len(active_rows)} active records   -> master-facilities-active.csv")


if __name__ == "__main__":
    main()
