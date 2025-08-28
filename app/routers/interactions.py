from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models import Interaction
from models import Candidate
from schemas.domain import InteractionCreate, InteractionOut


router = APIRouter()


@router.post("/", response_model=InteractionOut)
def create_interaction(payload: InteractionCreate, db: Session = Depends(get_db)):
    candidate = db.get(Candidate, payload.candidate_id)
    if not candidate:
        raise HTTPException(400, "Invalid candidate")
    data = payload.dict()
    if "metadata" in data:
        data["metadata_"] = data.pop("metadata")
    record = Interaction(**data)
    db.add(record)
    db.commit()
    db.refresh(record)
    return record


@router.get("/candidate/{candidate_id}", response_model=List[InteractionOut])
def list_interactions(candidate_id: int, db: Session = Depends(get_db)):
    return (
        db.query(Interaction)
        .filter(Interaction.candidate_id == candidate_id)
        .order_by(Interaction.created_at.desc())
        .all()
    )

