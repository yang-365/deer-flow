# Transfer Execution Guide (转账执行指南)

## Step 1: Parameter Extraction
Extract the following parameters from the conversation:

| Parameter | Required | Description |
|-----------|----------|-------------|
| payee_name | Yes | Name of the recipient (收款人姓名) |
| amount | Yes | Transfer amount (转账金额) |

## Step 2: Collect Missing Parameters
If **payee_name** or **amount** is missing, ask the user to provide the missing information.

## Step 3: Confirmation
Before executing the transfer, summarize and ask the user to confirm:
- Recipient: {payee_name}
- Amount: {amount} CNY

## Step 4: Execute Transfer
Call the workflow API:
```
call_workflow(endpoint="http://localhost:9100/api/v1/workflows/transfer", params={
  "payee_name": "...",
  "amount": ...
})
```

## Step 5: Present Result
- On success: Show transfer confirmation with transaction ID and status
- On failure: Show error message and suggest next steps
