"""Mock Workflow Server - simulates external banking workflow APIs for testing."""

import json
import uuid
from datetime import datetime, timezone

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

app = FastAPI(title="Mock Workflow Platform")


@app.post("/api/v1/workflows/transfer")
async def transfer(request: Request):
    """Simulate a bank transfer workflow."""
    body = await request.json()

    payee_name = body.get("payee_name", "")
    payee_account = body.get("payee_account", "")
    amount = body.get("amount", 0)
    currency = body.get("currency", "CNY")
    remark = body.get("remark", "")

    # Simulate validation
    if not payee_name:
        return JSONResponse(
            status_code=400,
            content={"success": False, "error": "payee_name is required"},
        )
    if not payee_account:
        return JSONResponse(
            status_code=400,
            content={"success": False, "error": "payee_account is required"},
        )
    if not amount or float(amount) <= 0:
        return JSONResponse(
            status_code=400,
            content={"success": False, "error": "amount must be positive"},
        )
    if float(amount) > 50000:
        return JSONResponse(
            status_code=400,
            content={"success": False, "error": "Single transfer limit exceeded (max 50,000 CNY)"},
        )

    # Simulate successful transfer
    txn_id = f"TXN{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S')}{uuid.uuid4().hex[:6].upper()}"
    return JSONResponse(
        status_code=200,
        content={
            "success": True,
            "data": {
                "transaction_id": txn_id,
                "status": "completed",
                "payee_name": payee_name,
                "payee_account": f"****{payee_account[-4:]}" if len(payee_account) >= 4 else payee_account,
                "amount": float(amount),
                "currency": currency,
                "remark": remark,
                "timestamp": datetime.now(timezone.utc).isoformat(),
            },
        },
    )


@app.post("/api/v1/workflows/balance-query")
async def balance_query(request: Request):
    """Simulate a balance query workflow."""
    return JSONResponse(
        status_code=200,
        content={
            "success": True,
            "data": {
                "balance": 125680.50,
                "currency": "CNY",
                "available_balance": 120000.00,
                "frozen_amount": 5680.50,
                "last_updated": datetime.now(timezone.utc).isoformat(),
            },
        },
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=9100)
