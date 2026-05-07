"""call_workflow tool — unified external workflow API invocation.

Authentication headers and passthrough parameters are injected from the
runtime context (``context.passthrough_params`` / ``context.passthrough_headers``)
so the LLM only sees and fills business parameters defined in each Skill's
``references/params_schema.yaml``.
"""

import json
import logging
from typing import Annotated

import httpx
from langchain_core.tools import tool
from langgraph.prebuilt.tool_node import InjectedToolCallId
from langgraph.runtime import get_runtime

from deerflow.config import get_app_config

logger = logging.getLogger(__name__)


@tool
def call_workflow(
    workflow_name: str,
    params: dict,
    tool_call_id: Annotated[str, InjectedToolCallId],
) -> str:
    """Call an external workflow API to execute a business process.

    Use this tool ONLY after you have collected all required parameters
    as defined in the Skill's ``references/params_schema.yaml``.

    Args:
        workflow_name: The workflow identifier (e.g. "transfer", "bill_payment",
            "balance_query").  Must match the workflow name declared in the
            Skill's ``references/workflow_api.yaml``.
        params: A dictionary of business parameters extracted from the
            conversation.  Only include fields defined in the Skill's
            params_schema — authentication and session parameters are
            injected automatically.
    """
    config = get_app_config()
    workflow_config = getattr(config, "workflow", None)
    if workflow_config is None or not workflow_config.enabled:
        return json.dumps({"success": False, "error": "Workflow integration is not enabled. Please configure workflow settings in config.yaml."})

    base_url = workflow_config.base_url.rstrip("/")
    if not base_url:
        return json.dumps({"success": False, "error": "Workflow base_url is not configured."})

    # Retrieve passthrough headers and params from runtime context.
    # These are injected by the frontend and are invisible to the LLM.
    runtime = get_runtime()
    context = (runtime.context or {}) if runtime else {}
    passthrough_headers: dict = context.get("passthrough_headers", {})
    passthrough_params: dict = context.get("passthrough_params", {})

    # Build the request
    url = f"{base_url}/{workflow_name}"
    headers = {
        "Content-Type": "application/json",
        **passthrough_headers,
    }
    body = {
        **passthrough_params,
        **params,
    }

    timeout = workflow_config.timeout_seconds

    try:
        with httpx.Client(timeout=timeout) as client:
            response = client.post(url, json=body, headers=headers)
            response.raise_for_status()
            result = response.json()
            return json.dumps({"success": True, "data": result})
    except httpx.TimeoutException:
        logger.warning("Workflow API timeout: %s", url)
        return json.dumps({"success": False, "error": f"Workflow API call timed out after {timeout}s. Please try again later."})
    except httpx.HTTPStatusError as exc:
        status_code = exc.response.status_code
        detail = exc.response.text[:500] if exc.response.text else str(exc)
        logger.warning("Workflow API error %d: %s", status_code, detail)
        return json.dumps({"success": False, "error": f"Workflow API returned HTTP {status_code}: {detail}"})
    except Exception as exc:
        logger.exception("Workflow API call failed: %s", url)
        return json.dumps({"success": False, "error": f"Workflow API call failed: {exc}"})


# Convenience alias for registration
call_workflow_tool = call_workflow
