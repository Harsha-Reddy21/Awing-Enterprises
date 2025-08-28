from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models import Application, Candidate, Requirement
from schemas.domain import ApplicationCreate, ApplicationOut


router = APIRouter()


@router.post("/", response_model=ApplicationOut)
def create_application(payload: ApplicationCreate, db: Session = Depends(get_db)):
    candidate = db.get(Candidate, payload.candidate_id)
    requirement = db.get(Requirement, payload.requirement_id)
    if not candidate or not requirement:
        raise HTTPException(400, "Invalid candidate or requirement")
    record = Application(
        candidate_id=payload.candidate_id,
        requirement_id=payload.requirement_id,
        source=payload.source,
    )
    db.add(record)
    db.commit()
    db.refresh(record)
    return record


@router.get("/", response_model=List[ApplicationOut])
def list_applications(db: Session = Depends(get_db)):
    return db.query(Application).order_by(Application.created_at.desc()).all()


@router.get("/{application_id}", response_model=ApplicationOut)
def get_application(application_id: int, db: Session = Depends(get_db)):
    record = db.get(Application, application_id)
    if not record:
        raise HTTPException(404, "Application not found")
    return record


@router.put("/{application_id}/stage", response_model=ApplicationOut)
def update_stage(application_id: int, stage: str, db: Session = Depends(get_db)):
    record = db.get(Application, application_id)
    if not record:
        raise HTTPException(404, "Application not found")
    record.stage = stage
    db.commit()
    db.refresh(record)
    return record

