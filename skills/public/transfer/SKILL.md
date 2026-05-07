---
name: transfer
description: Use this skill when the user wants to transfer money to another person or account. Handles bank transfers, interbank transfers, and mobile payments.
allowed-tools:
  - call_workflow
  - ask_clarification
  - read_file
---

# Transfer Skill (转账)

## Intent Matching
Match this skill when the user expresses any of these intents:
- Transfer money to someone
- Send payment to a bank account
- Wire funds / remittance
- Keywords: 转账, 汇款, 打款, 转钱

## Execution
Read `references/execution_guide.md` for the complete execution workflow including parameter extraction, confirmation, and API calling.
