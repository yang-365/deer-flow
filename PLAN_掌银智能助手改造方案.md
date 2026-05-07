# 掌银智能助手改造方案（基于 DeerFlow 2.0）— V2 简化版

## 一、改造目标

将 DeerFlow 改造为**掌上银行智能助手**，核心能力：
- **意图识别**：识别用户意图（转账、缴费、购物、查询、闲聊、客服等）
- **参数提取**：从对话中提取业务参数，缺失参数自动反问
- **Workflow 调用**：通过 `call_workflow` 工具调用外部 Workflow API
- **多任务管理**：沿用现有 TodoMiddleware
- **多用户隔离**：现有架构已支持

## 二、改造原则

1. **全量加载 Skill**：100+ Skill 的 name+description 直接注入 System Prompt，不做分类索引
2. **Skill 不执行 script**：只能调用 `call_workflow` 工具 + `ask_clarification` 反问
3. **参数分离**：认证参数 + header 由总 API 透传，业务参数由模型根据 reference 中的参数定义填写
4. **最小改动**：沙箱、子智能体通过配置关闭，不删代码
5. **多任务沿用现有**：TodoMiddleware 已够用

## 三、改造文件清单

### 新增文件

| 文件路径 | 说明 |
|----------|------|
| `backend/packages/harness/deerflow/tools/builtins/workflow_tool.py` | call_workflow 工具 |
| `backend/packages/harness/deerflow/config/workflow_config.py` | Workflow 配置类 |
| `skills/public/transfer/SKILL.md` | 转账 Skill（示例） |
| `skills/public/transfer/references/params_schema.yaml` | 转账参数定义 |
| `skills/public/transfer/references/workflow_api.yaml` | 转账 Workflow 调用方式 |
| `skills/public/bill-payment/SKILL.md` | 缴费 Skill（示例） |
| `skills/public/bill-payment/references/params_schema.yaml` | 缴费参数定义 |
| `skills/public/bill-payment/references/workflow_api.yaml` | 缴费 Workflow 调用方式 |
| `skills/public/balance-query/SKILL.md` | 余额查询 Skill（示例） |
| `skills/public/balance-query/references/params_schema.yaml` | 查询参数定义 |
| `skills/public/balance-query/references/workflow_api.yaml` | 查询 Workflow 调用方式 |

### 修改文件

| 文件路径 | 改动说明 |
|----------|----------|
| `backend/packages/harness/deerflow/config/app_config.py` | 新增 WorkflowConfig 字段 |
| `backend/packages/harness/deerflow/tools/tools.py` | 注册 call_workflow 工具 |
| `backend/packages/harness/deerflow/agents/lead_agent/prompt.py` | System Prompt 适配掌银助手 |
| `backend/packages/harness/deerflow/agents/middlewares/tool_error_handling_middleware.py` | sandbox disabled 时跳过沙箱中间件 |
| `config.yaml` | 新增 workflow 配置，关闭沙箱 |
| `frontend/src/core/threads/hooks.ts` | context 中新增 passthrough_params |

## 四、详细设计

### 4.1 call_workflow 工具

统一的外部 Workflow 调用入口。

**参数模型**：
```
总 API 请求
├── headers (透传给 workflow API)
│   ├── Authorization: Bearer xxx
│   ├── X-User-Id: user123
│   ├── X-Device-Id: device456
│   └── X-Channel-Code: mobile_bank
├── passthrough_params (透传给 workflow API body)
│   ├── session_token
│   └── client_ip
└── user_message (给模型看的)
    └── "帮我转账500给张三"

模型从对话中提取参数（根据 Skill reference 中的 params_schema）
├── payee_name: "张三"
├── amount: 500
└── ...

call_workflow 合并参数后调用外部 API
├── headers: 透传的 headers
├── body: passthrough_params + 模型提取的参数
└── workflow_name: "transfer"
```

### 4.2 Skill 结构

```
skills/public/transfer/
├── SKILL.md                        # 意图描述 + 业务流程
└── references/
    ├── params_schema.yaml          # 模型需要提取的参数定义
    ├── workflow_api.yaml           # workflow 调用方式
    └── business_rules.md           # 业务知识（限额等）
```

### 4.3 中间件链

sandbox disabled 时自动跳过：SandboxMiddleware、SandboxAuditMiddleware、UploadsMiddleware

保留全部其他中间件不变。
