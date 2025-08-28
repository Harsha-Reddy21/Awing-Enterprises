from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app import models
from app.schemas.domain import (
    ScreeningQuestionCreate,
    ScreeningQuestionOut,
    ScreeningResponseCreate,
)


router = APIRouter()


@router.post("/questions", response_model=ScreeningQuestionOut)
def create_question(payload: ScreeningQuestionCreate, db: Session = Depends(get_db)):
    requirement = db.get(models.Requirement, payload.requirement_id)
    if not requirement:
        raise HTTPException(400, "Invalid requirement")
    record = models.ScreeningQuestion(**payload.dict())
    db.add(record)
    db.commit()
    db.refresh(record)
    return record


@router.get("/questions/{requirement_id}", response_model=List[ScreeningQuestionOut])
def list_questions(requirement_id: int, db: Session = Depends(get_db)):
    return (
        db.query(models.ScreeningQuestion)
        .filter(models.ScreeningQuestion.requirement_id == requirement_id)
        .order_by(models.ScreeningQuestion.created_at.desc())
        .all()
    )


@router.post("/responses")
def create_response(payload: ScreeningResponseCreate, db: Session = Depends(get_db)):
    if not db.get(models.Candidate, payload.candidate_id):
        raise HTTPException(400, "Invalid candidate")
    if not db.get(models.Requirement, payload.requirement_id):
        raise HTTPException(400, "Invalid requirement")
    if not db.get(models.ScreeningQuestion, payload.question_id):
        raise HTTPException(400, "Invalid question")
    record = models.ScreeningResponse(**payload.dict())
    db.add(record)
    db.commit()
    return {"ok": True}

