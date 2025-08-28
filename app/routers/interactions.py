from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app import models
from app.schemas.domain import InteractionCreate, InteractionOut


router = APIRouter()


@router.post("/", response_model=InteractionOut)
def create_interaction(payload: InteractionCreate, db: Session = Depends(get_db)):
    candidate = db.get(models.Candidate, payload.candidate_id)
    if not candidate:
        raise HTTPException(400, "Invalid candidate")
    record = models.Interaction(**payload.dict())
    db.add(record)
    db.commit()
    db.refresh(record)
    return record


@router.get("/candidate/{candidate_id}", response_model=List[InteractionOut])
def list_interactions(candidate_id: int, db: Session = Depends(get_db)):
    return (
        db.query(models.Interaction)
        .filter(models.Interaction.candidate_id == candidate_id)
        .order_by(models.Interaction.created_at.desc())
        .all()
    )

