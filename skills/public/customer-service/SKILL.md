---
name: customer-service
description: Fallback skill for general customer service. Use this skill when no other specific skill matches the user's intent. Handles greetings, FAQs, product inquiries, complaints, and general banking questions.
allowed-tools:
  - ask_clarification
  - read_file
---

# Customer Service Skill (在线客服)

## Intent Matching
This is the **fallback skill**. Activate it when the user's intent does NOT match any other specific skill:
- General greetings or chitchat (你好, 在吗)
- Product inquiries (理财产品, 贷款利率, 信用卡)
- Complaints or feedback (投诉, 建议)
- FAQ questions (营业时间, 网点, 客服电话)
- Any unrecognized or unclear intent

## Execution
Read `references/execution_guide.md` for the response guidelines.
