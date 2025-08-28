from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models import Submission, Application
from schemas.domain import SubmissionCreate, SubmissionOut


router = APIRouter()


@router.post("/", response_model=SubmissionOut)
def create_submission(payload: SubmissionCreate, db: Session = Depends(get_db)):
    app_rec = db.get(Application, payload.application_id)
    if not app_rec:
        raise HTTPException(400, "Invalid application")
    if app_rec.submission:
        raise HTTPException(400, "Submission already exists")
    record = Submission(application_id=payload.application_id, notes=payload.notes)
    db.add(record)
    db.commit()
    db.refresh(record)
    return record


@router.get("/{application_id}", response_model=SubmissionOut)
def get_submission(application_id: int, db: Session = Depends(get_db)):
    record = (
        db.query(Submission)
        .filter(Submission.application_id == application_id)
        .first()
    )
    if not record:
        raise HTTPException(404, "Submission not found")
    return record

