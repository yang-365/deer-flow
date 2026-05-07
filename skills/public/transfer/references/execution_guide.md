# Transfer Execution Guide

## Step 1: Parameter Extraction
Read `params_schema.yaml` in this folder to understand the full parameter schema. Extract the following from the conversation:

| Parameter | Required | Description |
|-----------|----------|-------------|
| payee_name | Yes | Name of the recipient |
| payee_account | Yes | Bank account number of the recipient |
| amount | Yes | Transfer amount (must be positive, max 50,000 CNY) |
| currency | No (default: CNY) | Currency code |
| remark | No | Transfer memo/remark |

## Step 2: Collect Missing Parameters
If any **required** parameter is missing, use `ask_clarification` with `clarification_type="missing_info"` to ask the user for each missing field.

## Step 3: Confirmation
Before executing the transfer, summarize the details and ask the user to confirm:
- Recipient: {payee_name}
- Account: {payee_account} (mask to show only last 4 digits)
- Amount: {amount} {currency}
- Remark: {remark} (if provided)

Use `ask_clarification` with `clarification_type="risk_confirmation"` to get explicit confirmation.

## Step 4: Execute Transfer
Read `workflow_api.yaml` in this folder for the endpoint URL, then call:
```
call_workflow(endpoint="<endpoint from workflow_api.yaml>", params={
  "payee_name": "...",
  "payee_account": "...",
  "amount": ...,
  "currency": "...",
  "remark": "..."
})
```

## Step 5: Present Result
- On success: Show transfer confirmation with transaction ID and status
- On failure: Show error message and suggest next steps

## Business Rules
- Single transfer limit: 50,000 CNY (configurable per user level)
- Daily transfer limit: 200,000 CNY
- Cross-bank transfers may take 1-2 business days
- Same-bank transfers are usually instant
