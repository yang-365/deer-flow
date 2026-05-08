"""Mock Workflow Server - simulates external banking workflow APIs for testing."""

import random
import uuid
from datetime import datetime, timezone

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

app = FastAPI(title="Mock Workflow Platform")


@app.post("/api/v1/workflows/transfer")
async def transfer(request: Request):
    """Simulate a bank transfer workflow. Auto-mocks missing fields."""
    body = await request.json()

    payee_name = body.get("payee_name", "未知收款人")
    amount = body.get("amount", 0)
    currency = body.get("currency", "CNY")
    remark = body.get("remark", "")

    # Auto-generate mock account number
    mock_account = f"6222{random.randint(1000000000000000, 9999999999999999)}"

    txn_id = f"TXN{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S')}{uuid.uuid4().hex[:6].upper()}"
    return JSONResponse(
        status_code=200,
        content={
            "success": True,
            "data": {
                "transaction_id": txn_id,
                "status": "completed",
                "payee_name": payee_name,
                "payee_account": f"****{mock_account[-4:]}",
                "amount": float(amount) if amount else 0,
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


@app.post("/api/v1/workflows/bill-payment")
async def bill_payment(request: Request):
    """Simulate a bill payment workflow."""
    body = await request.json()

    bill_type = body.get("bill_type", "phone")
    account_number = body.get("account_number", "unknown")
    amount = body.get("amount", 50)
    billing_period = body.get("billing_period", "2026-05")

    receipt_id = f"RCP{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S')}{uuid.uuid4().hex[:6].upper()}"
    return JSONResponse(
        status_code=200,
        content={
            "success": True,
            "data": {
                "receipt_id": receipt_id,
                "status": "completed",
                "bill_type": bill_type,
                "account_number": f"****{str(account_number)[-4:]}",
                "amount": float(amount) if amount else 0,
                "billing_period": billing_period,
                "timestamp": datetime.now(timezone.utc).isoformat(),
            },
        },
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=9100)
