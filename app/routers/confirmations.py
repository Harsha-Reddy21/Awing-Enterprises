from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime

from app.database import get_db
from app import models
from app.schemas.domain import ConfirmationCreate, ConfirmationOut


router = APIRouter()


@router.post("/", response_model=ConfirmationOut)
def create_confirmation(payload: ConfirmationCreate, db: Session = Depends(get_db)):
    app_rec = db.get(models.Application, payload.application_id)
    if not app_rec:
        raise HTTPException(400, "Invalid application")
    if app_rec.confirmation:
        raise HTTPException(400, "Confirmation already exists")
    record = models.Confirmation(
        application_id=payload.application_id,
        rate_or_salary=payload.rate_or_salary,
        contract_duration=payload.contract_duration,
        email_confirmed=payload.email_confirmed or False,
        notes=payload.notes,
        confirmed_at=datetime.utcnow() if payload.email_confirmed else None,
    )
    db.add(record)
    db.commit()
    db.refresh(record)
    return record


@router.get("/{application_id}", response_model=ConfirmationOut)
def get_confirmation(application_id: int, db: Session = Depends(get_db)):
    record = (
        db.query(models.Confirmation)
        .filter(models.Confirmation.application_id == application_id)
        .first()
    )
    if not record:
        raise HTTPException(404, "Confirmation not found")
    return record

