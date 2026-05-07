# Balance Query Execution Guide

## Step 1: Parameter Extraction
Read `params_schema.yaml` in this folder to understand the full parameter schema. Extract the following from the conversation:

| Parameter | Required | Description |
|-----------|----------|-------------|
| query_type | No (default: balance) | What to query: balance, transactions, or account_info |
| account_type | No (default: checking) | Which account: checking, savings, credit_card |

These are usually optional since users typically just want their primary account balance.

## Step 2: Collect Parameters (if needed)
If the user's request is ambiguous about which account or query type, use `ask_clarification` with `clarification_type="ambiguous_requirement"` to clarify.

## Step 3: Execute Query
Read `workflow_api.yaml` in this folder for the endpoint URL, then call:
```
call_workflow(endpoint="<endpoint from workflow_api.yaml>", params={
  "query_type": "...",
  "account_type": "..."
})
```

## Step 4: Present Result
- Show balance in a clear, readable format
- If showing transactions, format as a table
- Mask sensitive information (show only last 4 digits of account numbers)
