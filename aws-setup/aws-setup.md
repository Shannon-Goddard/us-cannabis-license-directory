# AWS Infrastructure Setup

This document describes the AWS backend that powers the community edit system for the US Cannabis License Directory.

---

## Architecture

```
┌─────────────┐     ┌──────────────────┐     ┌──────────────┐
│  index.html │────▶│  API Gateway     │────▶│  Lambda (x3) │
│  (static)   │     │  (HTTP API)      │     │              │
└─────────────┘     └──────────────────┘     └──────┬───────┘
                                                     │
                                              ┌──────▼───────┐
                                              │  DynamoDB     │
                                              │  (ledger)     │
                                              └──────────────┘
```

### Components

| Resource | Name | Purpose |
|---|---|---|
| DynamoDB Table | `cannabis-directory-ledger` | Stores all community edits |
| IAM Role | `cannabis-directory-lambda-role` | Execution role for all Lambdas |
| Lambda | `cannabis-directory-submit-edit` | Validates GitHub token, writes edit to DynamoDB |
| Lambda | `cannabis-directory-get-ledger` | Returns recent edits from DynamoDB |
| Lambda | `cannabis-directory-github-oauth` | Exchanges GitHub OAuth code for access token |
| API Gateway | `cannabis-directory-api` | HTTP API with CORS, routes to Lambdas |

### API Routes

| Method | Path | Lambda | Description |
|---|---|---|---|
| `POST` | `/edit` | submit_edit | Submit a cell edit |
| `GET` | `/ledger` | get_ledger | Fetch recent edits |
| `POST` | `/auth/github` | github_oauth | GitHub OAuth code exchange |

---

## DynamoDB Schema

**Table:** `cannabis-directory-ledger`
**Billing:** PAY_PER_REQUEST (on-demand)

| Key | Type | Description |
|---|---|---|
| `edit_id` (PK) | String | UUID for each edit |
| `timestamp` (SK) | String | ISO 8601 UTC timestamp |

**Additional attributes per item:**

| Attribute | Description |
|---|---|
| `github_user` | GitHub username of the editor |
| `row_index` | License number or row identifier |
| `column` | Column name that was edited |
| `old_value` | Value before the edit |
| `new_value` | Value after the edit |
| `business_name` | Business name for context |
| `status` | `pending` / `approved` / `rejected` |

---

## Deploy Steps

Replace `<AWS_ACCOUNT_ID>` with your AWS account ID and `<API_ID>` with the API Gateway ID after creation.

### 1. DynamoDB Table

```bash
aws dynamodb create-table \
  --table-name cannabis-directory-ledger \
  --attribute-definitions \
    AttributeName=edit_id,AttributeType=S \
    AttributeName=timestamp,AttributeType=S \
  --key-schema \
    AttributeName=edit_id,KeyType=HASH \
    AttributeName=timestamp,KeyType=RANGE \
  --billing-mode PAY_PER_REQUEST \
  --region us-east-1
```

### 2. IAM Role

```bash
aws iam create-role \
  --role-name cannabis-directory-lambda-role \
  --assume-role-policy-document file://aws-setup/trust-policy.json

aws iam put-role-policy \
  --role-name cannabis-directory-lambda-role \
  --policy-name cannabis-directory-lambda-policy \
  --policy-document file://aws-setup/lambda-policy.json
```

### 3. Lambda Functions

Package each function (rename to `lambda_function.py` inside the zip):

```bash
# Submit Edit
cp aws-setup/lambda/submit_edit.py lambda_function.py
zip submit_edit.zip lambda_function.py
aws lambda create-function \
  --function-name cannabis-directory-submit-edit \
  --runtime python3.12 \
  --role arn:aws:iam::<AWS_ACCOUNT_ID>:role/cannabis-directory-lambda-role \
  --handler lambda_function.lambda_handler \
  --zip-file fileb://submit_edit.zip \
  --timeout 10 --memory-size 128 --region us-east-1

# Get Ledger
cp aws-setup/lambda/get_ledger.py lambda_function.py
zip get_ledger.zip lambda_function.py
aws lambda create-function \
  --function-name cannabis-directory-get-ledger \
  --runtime python3.12 \
  --role arn:aws:iam::<AWS_ACCOUNT_ID>:role/cannabis-directory-lambda-role \
  --handler lambda_function.lambda_handler \
  --zip-file fileb://get_ledger.zip \
  --timeout 10 --memory-size 128 --region us-east-1

# GitHub OAuth
cp aws-setup/lambda/github_oauth.py lambda_function.py
zip github_oauth.zip lambda_function.py
aws lambda create-function \
  --function-name cannabis-directory-github-oauth \
  --runtime python3.12 \
  --role arn:aws:iam::<AWS_ACCOUNT_ID>:role/cannabis-directory-lambda-role \
  --handler lambda_function.lambda_handler \
  --zip-file fileb://github_oauth.zip \
  --timeout 10 --memory-size 128 --region us-east-1 \
  --environment "Variables={GITHUB_CLIENT_ID=<YOUR_CLIENT_ID>,GITHUB_CLIENT_SECRET=<YOUR_CLIENT_SECRET>}"
```

### 4. API Gateway

```bash
aws apigatewayv2 create-api \
  --name cannabis-directory-api \
  --protocol-type HTTP \
  --cors-configuration AllowOrigins=*,AllowMethods=GET,POST,OPTIONS,AllowHeaders=Content-Type,Authorization \
  --region us-east-1
```

Note the `ApiId` and `ApiEndpoint` from the output, then create integrations and routes:

```bash
# Create integrations (note the IntegrationId from each output)
aws apigatewayv2 create-integration --api-id <API_ID> \
  --integration-type AWS_PROXY \
  --integration-uri arn:aws:lambda:us-east-1:<AWS_ACCOUNT_ID>:function:cannabis-directory-submit-edit \
  --payload-format-version 2.0 --region us-east-1

aws apigatewayv2 create-integration --api-id <API_ID> \
  --integration-type AWS_PROXY \
  --integration-uri arn:aws:lambda:us-east-1:<AWS_ACCOUNT_ID>:function:cannabis-directory-get-ledger \
  --payload-format-version 2.0 --region us-east-1

aws apigatewayv2 create-integration --api-id <API_ID> \
  --integration-type AWS_PROXY \
  --integration-uri arn:aws:lambda:us-east-1:<AWS_ACCOUNT_ID>:function:cannabis-directory-github-oauth \
  --payload-format-version 2.0 --region us-east-1

# Create routes (replace <INTEGRATION_ID> with each integration's ID)
aws apigatewayv2 create-route --api-id <API_ID> --route-key "POST /edit" --target integrations/<SUBMIT_INTEGRATION_ID>
aws apigatewayv2 create-route --api-id <API_ID> --route-key "GET /ledger" --target integrations/<LEDGER_INTEGRATION_ID>
aws apigatewayv2 create-route --api-id <API_ID> --route-key "POST /auth/github" --target integrations/<OAUTH_INTEGRATION_ID>

# Create auto-deploy stage
aws apigatewayv2 create-stage --api-id <API_ID> --stage-name "\$default" --auto-deploy --region us-east-1

# Grant API Gateway permission to invoke Lambdas
aws lambda add-permission --function-name cannabis-directory-submit-edit \
  --statement-id apigateway-invoke --action lambda:InvokeFunction \
  --principal apigateway.amazonaws.com \
  --source-arn "arn:aws:execute-api:us-east-1:<AWS_ACCOUNT_ID>:<API_ID>/*/*"

aws lambda add-permission --function-name cannabis-directory-get-ledger \
  --statement-id apigateway-invoke --action lambda:InvokeFunction \
  --principal apigateway.amazonaws.com \
  --source-arn "arn:aws:execute-api:us-east-1:<AWS_ACCOUNT_ID>:<API_ID>/*/*"

aws lambda add-permission --function-name cannabis-directory-github-oauth \
  --statement-id apigateway-invoke --action lambda:InvokeFunction \
  --principal apigateway.amazonaws.com \
  --source-arn "arn:aws:execute-api:us-east-1:<AWS_ACCOUNT_ID>:<API_ID>/*/*"
```

### 5. GitHub OAuth App

1. Go to [github.com/settings/developers](https://github.com/settings/developers)
2. Click **New OAuth App**
3. Set:
   - **Application name:** `US Cannabis License Directory`
   - **Homepage URL:** Your GitHub Pages URL
   - **Authorization callback URL:** Your GitHub Pages URL (same as homepage)
4. Copy the **Client ID** and **Client Secret**
5. Update the Lambda environment variables:

```bash
aws lambda update-function-configuration \
  --function-name cannabis-directory-github-oauth \
  --environment "Variables={GITHUB_CLIENT_ID=<YOUR_CLIENT_ID>,GITHUB_CLIENT_SECRET=<YOUR_CLIENT_SECRET>}" \
  --region us-east-1
```

6. Update `GITHUB_CLIENT_ID` in `index.html`

---

## Tear Down

To remove all resources:

```bash
aws apigatewayv2 delete-api --api-id <API_ID> --region us-east-1
aws lambda delete-function --function-name cannabis-directory-submit-edit --region us-east-1
aws lambda delete-function --function-name cannabis-directory-get-ledger --region us-east-1
aws lambda delete-function --function-name cannabis-directory-github-oauth --region us-east-1
aws dynamodb delete-table --table-name cannabis-directory-ledger --region us-east-1
aws iam delete-role-policy --role-name cannabis-directory-lambda-role --policy-name cannabis-directory-lambda-policy
aws iam delete-role --role-name cannabis-directory-lambda-role
```

---

## Cost Estimate

All resources run within AWS Free Tier for typical community usage.

| Service | Free Tier | Expected Cost |
|---|---|---|
| DynamoDB (on-demand) | 25 WCU/RCU, 25GB storage | $0.00/month |
| API Gateway (HTTP) | 1M requests/month | $0.00/month |
| Lambda | 1M requests, 400K GB-sec | $0.00/month |
| **Total** | | **$0.00/month** |

At scale (>1M edits/month), expect ~$1–3/month.

---

## File Reference

```
aws-setup/
├── aws-setup.md           # This file
├── trust-policy.json      # IAM trust policy for Lambda execution role
├── lambda-policy.json     # IAM policy — DynamoDB + CloudWatch permissions
└── lambda/
    ├── submit_edit.py     # POST /edit — validate GitHub token, write to DynamoDB
    ├── get_ledger.py      # GET /ledger — return recent edits
    └── github_oauth.py    # POST /auth/github — exchange OAuth code for token
```
