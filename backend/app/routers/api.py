from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from datetime import datetime
from typing import Optional
from backend.app.services.gemini_service import gemini_service
from backend.app.services.db_service import get_db, User, Workspace, TransactionRecord, hash_password

router = APIRouter()

class PromptRequest(BaseModel):
    prompt: str

class InvoicePayload(BaseModel):
    recipient: str
    category: str
    description: str
    currency: str = "USD"
    subtotal: float = 0.0
    tax: float = 0.0
    amount: float
    workspace_id: Optional[int] = None

class AuthRequest(BaseModel):
    email: str
    password: str
    full_name: Optional[str] = None

@router.post("/auth/register")
def register(payload: AuthRequest, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.email == payload.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Account with this email already exists.")
    
    new_user = User(
        email=payload.email,
        password_hash=hash_password(payload.password),
        full_name=payload.full_name or payload.email.split("@")[0]
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    ws_personal = Workspace(name="Personal & Freelance", type="FREELANCE", owner_id=new_user.id, balance=12850.00)
    ws_enterprise = Workspace(name="Global Enterprise Inc.", type="ENTERPRISE", owner_id=new_user.id, balance=142900.00)
    db.add_all([ws_personal, ws_enterprise])
    db.commit()

    return {
        "status": "success",
        "user": {"id": new_user.id, "email": new_user.email, "name": new_user.full_name}
    }

@router.post("/auth/login")
def login(payload: AuthRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(
        User.email == payload.email,
        User.password_hash == hash_password(payload.password)
    ).first()

    if not user:
        raise HTTPException(status_code=401, detail="Invalid email or password.")

    workspaces = db.query(Workspace).filter(Workspace.owner_id == user.id).all()
    return {
        "user": {"id": user.id, "email": user.email, "name": user.full_name},
        "workspaces": [{"id": w.id, "name": w.name, "type": w.type, "balance": w.balance} for w in workspaces]
    }

@router.get("/workspaces/{user_id}")
def get_user_workspaces(user_id: int, db: Session = Depends(get_db)):
    workspaces = db.query(Workspace).filter(Workspace.owner_id == user_id).all()
    return [{"id": w.id, "name": w.name, "type": w.type, "balance": w.balance} for w in workspaces]

@router.post("/parse-invoice")
def parse_invoice(data: PromptRequest):
    try:
        return gemini_service.parse_invoice_prompt(data.prompt)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/capture-order/{order_id}")
def capture_order(order_id: str, payload: InvoicePayload, db: Session = Depends(get_db)):
    try:
        record = TransactionRecord(
            workspace_id=payload.workspace_id,
            order_id=order_id,
            recipient=payload.recipient,
            category=payload.category,
            description=payload.description,
            currency=payload.currency,
            subtotal=payload.subtotal,
            tax=payload.tax,
            amount=payload.amount,
            status="PAID",
            created_at=datetime.utcnow()
        )
        db.add(record)

        # Automatically update workspace balance on settlement
        if payload.workspace_id:
            ws = db.query(Workspace).filter(Workspace.id == payload.workspace_id).first()
            if ws:
                ws.balance += payload.amount

        db.commit()
        db.refresh(record)

        new_balance = ws.balance if payload.workspace_id and ws else None
        return {
            "status": "COMPLETED",
            "order_id": record.order_id,
            "id": record.id,
            "new_balance": new_balance
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/transactions")
def get_transactions(workspace_id: Optional[int] = None, db: Session = Depends(get_db)):
    query = db.query(TransactionRecord)
    if workspace_id is not None:
        query = query.filter(TransactionRecord.workspace_id == workspace_id)
    records = query.order_by(TransactionRecord.id.desc()).all()

    return [
        {
            "id": r.id,
            "order_id": r.order_id,
            "recipient": r.recipient,
            "category": r.category,
            "description": r.description,
            "currency": getattr(r, "currency", "USD") or "USD",
            "subtotal": getattr(r, "subtotal", 0.0) or 0.0,
            "tax": getattr(r, "tax", 0.0) or 0.0,
            "amount": r.amount,
            "status": r.status,
            "created_at": r.created_at.strftime("%Y-%m-%d %H:%M:%S") if r.created_at else ""
        }
        for r in records
    ]
