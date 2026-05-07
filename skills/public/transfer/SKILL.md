---
name: transfer
description: Use this skill when the user wants to transfer money to another person or account. Handles bank transfers, interbank transfers, and mobile payments.
allowed-tools:
  - call_workflow
  - ask_clarification
  - read_file
---

# Transfer Skill (转账)

## Overview
This skill handles money transfer requests. It extracts transfer parameters from conversation, validates required fields, and calls the transfer workflow.

## Workflow

### Step 1: Parameter Extraction
Read the parameter schema to understand what information is needed:
- `read_file` on `references/params_schema.yaml` to get the required/optional parameters

### Step 2: Collect Missing Parameters
Check the conversation for:
- **payee_name** (required): Name of the recipient
- **payee_account** (required): Bank account number of the recipient
- **amount** (required): Transfer amount (must be positive)
- **currency** (optional, default: CNY): Currency code
- **remark** (optional): Transfer memo/remark

If any **required** parameter is missing, use `ask_clarification` to ask the user.

### Step 3: Confirmation
Before executing the transfer, summarize the details and ask the user to confirm:
- Recipient: {payee_name}
- Account: {payee_account} (show last 4 digits only)
- Amount: {amount} {currency}
- Remark: {remark}

Use `ask_clarification` with `clarification_type="risk_confirmation"` to get confirmation.

### Step 4: Execute Transfer
Read `references/workflow_api.yaml` for the endpoint URL and call:
```
call_workflow(endpoint="<endpoint from workflow_api.yaml>", params={...extracted parameters...})
```

### Step 5: Present Result
- On success: Show transfer confirmation with transaction ID
- On failure: Show error message and suggest next steps

## Business Rules
- Single transfer limit: 50,000 CNY (configurable per user level)
- Daily transfer limit: 200,000 CNY
- Cross-bank transfers may take 1-2 business days
- Same-bank transfers are usually instant
