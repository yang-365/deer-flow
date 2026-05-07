---
name: bill-payment
description: Use this skill when the user wants to pay bills such as utilities (water, electricity, gas), phone bills, internet, property management fees, or other recurring payments.
allowed-tools:
  - call_workflow
  - ask_clarification
  - read_file
---

# Bill Payment Skill (缴费)

## Overview
This skill handles bill payment requests including utilities, phone, internet, and other recurring bills.

## Workflow

### Step 1: Parameter Extraction
Read `references/params_schema.yaml` to understand required parameters.

### Step 2: Collect Missing Parameters
Check the conversation for:
- **bill_type** (required): Type of bill (electricity, water, gas, phone, internet, property)
- **account_number** (required): The utility/service account number
- **amount** (optional): Payment amount. If not provided, query the outstanding balance first.
- **billing_period** (optional): Which billing period to pay for

If any **required** parameter is missing, use `ask_clarification` to ask the user.

### Step 3: Execute Payment
Read `references/workflow_api.yaml` and call:
```
call_workflow(workflow_name="bill_payment", params={...extracted parameters...})
```

### Step 4: Present Result
- On success: Show payment confirmation with receipt number
- On failure: Show error message and suggest alternatives
