# Bill Payment Execution Guide

## Step 1: Parameter Extraction
Read `params_schema.yaml` in this folder to understand the full parameter schema. Extract the following from the conversation:

| Parameter | Required | Description |
|-----------|----------|-------------|
| bill_type | Yes | Type of bill: electricity, water, gas, phone, internet, property |
| account_number | Yes | The utility or service account number |
| amount | No | Payment amount. If not specified, the outstanding balance will be paid |
| billing_period | No | Billing period (e.g., "2026-01", "2026-Q1") |

## Step 2: Collect Missing Parameters
If any **required** parameter is missing, use `ask_clarification` with `clarification_type="missing_info"` to ask the user for each missing field.

## Step 3: Execute Payment
Read `workflow_api.yaml` in this folder for the endpoint URL, then call:
```
call_workflow(endpoint="<endpoint from workflow_api.yaml>", params={
  "bill_type": "...",
  "account_number": "...",
  "amount": ...,
  "billing_period": "..."
})
```

## Step 4: Present Result
- On success: Show payment confirmation with receipt number
- On failure: Show error message and suggest alternatives
