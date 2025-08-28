from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models import ScreeningQuestion, ScreeningResponse, Candidate, Requirement
from schemas.domain import (
    ScreeningQuestionCreate,
    ScreeningQuestionOut,
    ScreeningResponseCreate,
)


router = APIRouter()


@router.post("/questions", response_model=ScreeningQuestionOut)
def create_question(payload: ScreeningQuestionCreate, db: Session = Depends(get_db)):
    requirement = db.get(Requirement, payload.requirement_id)
    if not requirement:
        raise HTTPException(400, "Invalid requirement")
    record = ScreeningQuestion(**payload.dict())
    db.add(record)
    db.commit()
    db.refresh(record)
    return record


@router.get("/questions/{requirement_id}", response_model=List[ScreeningQuestionOut])
def list_questions(requirement_id: int, db: Session = Depends(get_db)):
    print(requirement_id)
    return (
        db.query(ScreeningQuestion)
        .filter(ScreeningQuestion.requirement_id == requirement_id)
        .order_by(ScreeningQuestion.created_at.desc())
        .all()
    )


@router.post("/responses")
def create_response(payload: ScreeningResponseCreate, db: Session = Depends(get_db)):
    if not db.get(Candidate, payload.candidate_id):
        raise HTTPException(400, "Invalid candidate")
    if not db.get(Requirement, payload.requirement_id):
        raise HTTPException(400, "Invalid requirement")
    if not db.get(ScreeningQuestion, payload.question_id):
        raise HTTPException(400, "Invalid question")
    record = ScreeningResponse(**payload.dict())
    db.add(record)
    db.commit()
    return {"ok": True}

