import type { Message, Thread } from "@langchain/langgraph-sdk";

import type { Todo } from "../todos";

export interface AgentThreadState extends Record<string, unknown> {
  title: string;
  messages: Message[];
  artifacts: string[];
  todos?: Todo[];
}

export interface AgentThreadContext extends Record<string, unknown> {
  thread_id: string;
  model_name: string | undefined;
  thinking_enabled: boolean;
  is_plan_mode: boolean;
  subagent_enabled: boolean;
  reasoning_effort?: "minimal" | "low" | "medium" | "high";
  agent_name?: string;
  /** Headers to pass through to external workflow API calls (e.g. Authorization, X-User-Id). */
  passthrough_headers?: Record<string, string>;
  /** Parameters to pass through to external workflow API body (e.g. session_token, client_ip). */
  passthrough_params?: Record<string, unknown>;
}

export interface AgentThread extends Thread<AgentThreadState> {
  context?: AgentThreadContext;
}

export interface RunMessage {
  run_id: string;
  content: Message;
  metadata: {
    caller: string;
  };
  created_at: string;
}
