# Balance Query Execution Guide (余额查询执行指南)

## Step 1: Parameter Extraction
Extract the following parameters from the conversation (all optional):

| Parameter | Required | Description |
|-----------|----------|-------------|
| query_type | No (default: balance) | What to query: balance, transactions, or account_info (查询类型) |
| account_type | No (default: checking) | Which account: checking, savings, credit_card (账户类型) |

These are usually optional since users typically just want their primary account balance.

## Step 2: Collect Parameters (if needed)
If the user's request is ambiguous about which account or query type, use `ask_clarification` with `clarification_type="ambiguous_requirement"` to clarify.

## Step 3: Execute Query
Call the workflow API:
```
call_workflow(endpoint="http://localhost:9100/api/v1/workflows/balance-query", params={
  "query_type": "...",
  "account_type": "..."
})
```

## Step 4: Present Result
- Show balance in a clear, readable format
- If showing transactions, format as a table
- Mask sensitive information (show only last 4 digits of account numbers)
