from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app import models
from app.schemas.domain import FeedbackCreate, FeedbackOut


router = APIRouter()


@router.post("/", response_model=FeedbackOut)
def create_feedback(payload: FeedbackCreate, db: Session = Depends(get_db)):
    if not db.get(models.Candidate, payload.candidate_id):
        raise HTTPException(400, "Invalid candidate")
    record = models.Feedback(**payload.dict())
    db.add(record)
    db.commit()
    db.refresh(record)
    return record


@router.get("/candidate/{candidate_id}", response_model=List[FeedbackOut])
def list_feedback(candidate_id: int, db: Session = Depends(get_db)):
    return (
        db.query(models.Feedback)
        .filter(models.Feedback.candidate_id == candidate_id)
        .order_by(models.Feedback.created_at.desc())
        .all()
    )

