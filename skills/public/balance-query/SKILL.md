---
name: balance-query
description: Use this skill when the user wants to check their bank account balance, view recent transactions, or query account information.
allowed-tools:
  - call_workflow
  - ask_clarification
  - read_file
---

# Balance Query Skill (余额查询)

## Overview
This skill handles account balance inquiries and basic account information queries.

## Workflow

### Step 1: Parameter Extraction
Read `references/params_schema.yaml` to understand required parameters.

### Step 2: Collect Parameters
Check the conversation for:
- **query_type** (optional, default: balance): What to query — balance, transactions, or account_info
- **account_type** (optional, default: checking): Which account — checking, savings, credit_card

These are usually optional since users typically just want their primary account balance.

### Step 3: Execute Query
Read `references/workflow_api.yaml` for the endpoint URL and call:
```
call_workflow(endpoint="<endpoint from workflow_api.yaml>", params={...extracted parameters...})
```

### Step 4: Present Result
- Show balance in a clear, readable format
- If showing transactions, format as a table
- Mask sensitive information (show only last 4 digits of account numbers)
