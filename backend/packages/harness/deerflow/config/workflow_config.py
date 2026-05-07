"""Workflow platform configuration for banking assistant integration."""

from pydantic import BaseModel, Field


class WorkflowConfig(BaseModel):
    """Configuration for external workflow API integration.

    The workflow platform handles deterministic business processes (transfer,
    bill payment, etc.).  The agent calls ``call_workflow`` with extracted
    parameters; authentication headers and passthrough parameters are injected
    automatically from the frontend context so the LLM never sees them.
    """

    enabled: bool = Field(default=False, description="Whether workflow integration is enabled")
    base_url: str = Field(default="", description="Base URL of the external workflow platform API")
    timeout_seconds: int = Field(default=30, description="HTTP timeout for workflow API calls")
