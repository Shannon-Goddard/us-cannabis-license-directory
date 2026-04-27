# Contributing to the US Cannabis License Directory

Thanks for helping improve the most comprehensive open cannabis license dataset in the US. Every edit makes this resource more accurate for researchers, policymakers, and the industry.

---

## How It Works

This directory is community-maintained through a simple browser-based editing system. No coding required.

### 1. Sign In with GitHub

Click the **Login with GitHub** button on the [directory page](https://shannon-goddard.github.io/us-cannabis-license-directory/). You'll be redirected to GitHub to authorize read-only access to your public profile. We only use your username and avatar — nothing else.

### 2. Edit a Cell

Once logged in, every cell in the table becomes clickable. Click any cell to edit it. You can only edit **one cell at a time** — this keeps edits clean and reviewable.

Some fields have dropdown menus:

| Field | Options |
|---|---|
| Business_Category | Single Location, Multi-Location, MSO, Vertically Integrated, Boutique, Franchise |
| Is_Medical | TRUE, FALSE |
| Is_Adult_Use | TRUE, FALSE |
| Social_Equity_Status | TRUE, FALSE |
| Home_Delivery | TRUE, FALSE |

For multi-value fields like `Product_Focus`, `Payment_Methods`, and `Ownership_Type`, use pipe-separated values (e.g., `Flower|Edibles|Concentrates`).

### 3. Submit

Click **Submit Edit** or press **Enter**. Your edit is recorded with:

- Your GitHub username
- Timestamp (UTC)
- The business name and license number
- The column edited
- The old and new values

All edits start with a `pending` status.

### 4. View the Ledger

Every edit is logged in the [Edit Ledger](https://shannon-goddard.github.io/us-cannabis-license-directory/ledger.html). You can see who edited what, when, and the before/after values. Full transparency.

---

## What to Contribute

The most valuable contributions right now are filling in the **empty community columns** we added:

- `Hours_of_Operation` — business hours
- `Instagram_URL` — social media presence
- `Neighborhood` — local area name
- `Business_Category` — single location, MSO, etc.
- `Product_Focus` — what they specialize in
- `Is_Medical` / `Is_Adult_Use` — license type
- `Payment_Methods` — cash, debit, etc.
- `Ownership_Type` — social equity, veteran-owned, etc.
- `Google_Place_ID` — for map integration
- `Notes` — anything useful

You can also correct existing data — wrong addresses, outdated phone numbers, closed businesses.

---

## Guidelines

- **One cell at a time.** Keep edits atomic and reviewable.
- **Cite your source** in the Notes field if you're adding data from a specific website or document.
- **Don't delete data.** If something is wrong, replace it with the correct value.
- **Be accurate.** This dataset has a DOI and is used for research.

---

## Architecture

The edit system runs on AWS (free tier):

```
Browser → API Gateway → Lambda → DynamoDB
           (HTTP API)    (Python)   (Ledger)
```

- **GitHub OAuth** authenticates contributors
- **DynamoDB** stores every edit as an immutable ledger entry
- **API Gateway + Lambda** handle the API calls
- **GitHub Pages** serves the static frontend

Full infrastructure documentation is in [`aws-setup/aws-setup.md`](aws-setup/aws-setup.md).

---

## Credits

**Shannon Goddard** — Research, data collection, legal analysis, manual verification, and the vision behind this project.

**Amazon Q** (AWS AI Assistant) — Pipeline architecture, data processing, AWS infrastructure, frontend, edit system, and documentation.

Built with grit in Riverside, CA. Chaos Preferred. Integrity Required.

---

## Questions?

Open an [issue](https://github.com/Shannon-Goddard/us-cannabis-license-directory/issues) or find Shannon at [poweredby.ci](https://poweredby.ci).
