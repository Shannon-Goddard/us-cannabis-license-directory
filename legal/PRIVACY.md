# Privacy Policy

**Effective Date:** April 27, 2026
**Last Updated:** April 27, 2026

**Loyal9 LLC**
Riverside, CA
Contact: legal@loyal9.app

---

This Privacy Policy applies to the US Cannabis License Directory ("the Site") operated at:

- https://shannon-goddard.github.io/us-cannabis-license-directory
- https://poweredby.ci/us-cannabis-license-directory

---

## 1. Information We Collect

### 1.1 GitHub Authentication

When you log in via GitHub OAuth, we receive:

- Your GitHub **username**
- Your GitHub **avatar URL** (public profile image)

We request `read:user` scope only. We do not access your repositories, email, or any private data.

### 1.2 Community Edits

When you submit an edit, we store:

- Your GitHub username
- Timestamp of the edit (UTC)
- The business record identifier (license number)
- The column edited
- The old value and new value
- The business name (for context)

This data is stored in AWS DynamoDB and is publicly visible in the [Edit Ledger](https://shannon-goddard.github.io/us-cannabis-license-directory/ledger.html).

### 1.3 Automatically Collected Information

The Site is hosted on GitHub Pages and uses AWS API Gateway. These services may automatically collect:

- IP addresses
- Browser type and version
- Referring URLs
- Access timestamps

We do not control or access GitHub Pages server logs. AWS API Gateway logs are used solely for debugging and are not shared with third parties.

## 2. Information We Do NOT Collect

- Email addresses (unless publicly displayed on your GitHub profile)
- Passwords or authentication tokens (GitHub OAuth tokens are used transiently and not stored)
- Payment information
- Location data beyond what is publicly available in the directory dataset
- Cookies for tracking or advertising

## 3. How We Use Information

- **GitHub username and avatar:** Displayed in the Edit Ledger to attribute community contributions
- **Edit data:** Stored as an immutable audit trail for data integrity
- **Server logs:** Debugging and abuse prevention only

## 4. Data Storage

| Data | Location | Retention |
|---|---|---|
| Edit ledger | AWS DynamoDB (us-east-1) | Indefinite |
| GitHub OAuth tokens | Browser memory only | Session (cleared on logout or page close) |
| Server logs | GitHub Pages / AWS | Per provider retention policies |

## 5. Third-Party Services

| Service | Purpose | Privacy Policy |
|---|---|---|
| GitHub | Authentication, hosting | [github.com/privacy](https://docs.github.com/en/site-policy/privacy-policies/github-general-privacy-statement) |
| AWS (API Gateway, Lambda, DynamoDB) | API and data storage | [aws.amazon.com/privacy](https://aws.amazon.com/privacy/) |

## 6. Data Sharing

We do not sell, rent, or share personal information with third parties. Edit data (including GitHub usernames) is publicly visible by design — the ledger is a transparency mechanism.

## 7. Your Rights

- **Access:** The Edit Ledger is public. You can see all data associated with your username.
- **Deletion:** To request removal of your edits from the ledger, contact legal@loyal9.app.
- **Opt out:** Don't log in. The directory is fully usable without authentication.

## 8. Children's Privacy

The Site is not directed at individuals under 13. We do not knowingly collect information from children.

## 9. Changes to This Policy

We may update this policy as the Site evolves. Changes will be reflected in the "Last Updated" date above. Continued use of the Site constitutes acceptance of the updated policy.

## 10. Contact

For privacy-related inquiries:

**Loyal9 LLC**
Riverside, CA
legal@loyal9.app
