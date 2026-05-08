# Bill Payment Execution Guide (缴费执行指南)

## Step 1: Parameter Extraction
Extract the following parameters from the conversation:

| Parameter | Required | Description |
|-----------|----------|-------------|
| bill_type | Yes | Type of bill: electricity, water, gas, phone, internet, property (缴费类型) |
| account_number | Yes | The utility or service account number (缴费账号) |
| amount | No | Payment amount. If not specified, the outstanding balance will be paid (缴费金额) |
| billing_period | No | Billing period, e.g. "2026-01", "2026-Q1" (账期) |

## Step 2: Collect Missing Parameters
If any **required** parameter is missing, use `ask_clarification` with `clarification_type="missing_info"` to ask the user for each missing field.

## Step 3: Execute Payment
Call the workflow API:
```
call_workflow(endpoint="http://localhost:9100/api/v1/workflows/bill-payment", params={
  "bill_type": "...",
  "account_number": "...",
  "amount": ...,
  "billing_period": "..."
})
```

## Step 4: Present Result
- On success: Show payment confirmation with receipt number
- On failure: Show error message and suggest alternatives
