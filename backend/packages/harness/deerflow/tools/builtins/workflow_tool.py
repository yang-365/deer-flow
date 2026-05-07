"""call_workflow tool — unified external workflow API invocation.

Authentication headers and passthrough parameters are injected from the
runtime context (``context.passthrough_params`` / ``context.passthrough_headers``)
so the LLM only sees and fills business parameters defined in each Skill's
``references/params_schema.yaml``.

The endpoint URL is read from the Skill's ``references/workflow_api.yaml``
by the LLM and passed as the ``endpoint`` parameter — no global workflow
configuration is needed.
"""

import json
import logging
from typing import Annotated

import httpx
from langchain_core.tools import tool
from langchain.tools import InjectedToolCallId
from langgraph.runtime import get_runtime

logger = logging.getLogger(__name__)

_DEFAULT_TIMEOUT_SECONDS = 30


@tool
def call_workflow(
    endpoint: str,
    params: dict,
    tool_call_id: Annotated[str, InjectedToolCallId],
) -> str:
    """Call an external workflow API to execute a business process.

    Use this tool ONLY after you have collected all required parameters
    as defined in the Skill's ``references/params_schema.yaml`` and read
    the endpoint URL from ``references/workflow_api.yaml``.

    Args:
        endpoint: The full workflow API endpoint URL, read from the Skill's
            ``references/workflow_api.yaml`` (e.g.
            "https://workflow-platform.example.com/api/v1/workflows/transfer").
        params: A dictionary of business parameters extracted from the
            conversation.  Only include fields defined in the Skill's
            params_schema — authentication and session parameters are
            injected automatically.
    """
    if not endpoint:
        return json.dumps({"success": False, "error": "Workflow endpoint URL is required. Read it from the Skill's references/workflow_api.yaml."})

    # Retrieve passthrough headers and params from runtime context.
    # These are injected by the frontend and are invisible to the LLM.
    runtime = get_runtime()
    context = (runtime.context or {}) if runtime else {}
    passthrough_headers: dict = context.get("passthrough_headers", {})
    passthrough_params: dict = context.get("passthrough_params", {})

    # Build the request
    headers = {
        "Content-Type": "application/json",
        **passthrough_headers,
    }
    body = {
        **passthrough_params,
        **params,
    }

    try:
        with httpx.Client(timeout=_DEFAULT_TIMEOUT_SECONDS) as client:
            response = client.post(endpoint, json=body, headers=headers)
            response.raise_for_status()
            result = response.json()
            return json.dumps({"success": True, "data": result})
    except httpx.TimeoutException:
        logger.warning("Workflow API timeout: %s", endpoint)
        return json.dumps({"success": False, "error": f"Workflow API call timed out after {_DEFAULT_TIMEOUT_SECONDS}s. Please try again later."})
    except httpx.HTTPStatusError as exc:
        status_code = exc.response.status_code
        detail = exc.response.text[:500] if exc.response.text else str(exc)
        logger.warning("Workflow API error %d: %s", status_code, detail)
        return json.dumps({"success": False, "error": f"Workflow API returned HTTP {status_code}: {detail}"})
    except Exception as exc:
        logger.exception("Workflow API call failed: %s", endpoint)
        return json.dumps({"success": False, "error": f"Workflow API call failed: {exc}"})


# Convenience alias for registration
call_workflow_tool = call_workflow
