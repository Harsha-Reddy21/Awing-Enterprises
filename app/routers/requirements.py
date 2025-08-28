from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models import Requirement
from schemas.domain import RequirementCreate, RequirementOut


router = APIRouter()


@router.post("/", response_model=RequirementOut)
def create_requirement(payload: RequirementCreate, db: Session = Depends(get_db)):
    record = Requirement(**payload.dict())
    db.add(record)
    db.commit()
    db.refresh(record)
    return record


@router.get("/", response_model=List[RequirementOut])
def list_requirements(db: Session = Depends(get_db)):
    return db.query(Requirement).order_by(Requirement.created_at.desc()).all()


@router.get("/{requirement_id}", response_model=RequirementOut)
def get_requirement(requirement_id: int, db: Session = Depends(get_db)):
    record = db.get(Requirement, requirement_id)
    if not record:
        raise HTTPException(404, "Requirement not found")
    return record


@router.put("/{requirement_id}", response_model=RequirementOut)
def update_requirement(requirement_id: int, payload: RequirementCreate, db: Session = Depends(get_db)):
    record = db.get(Requirement, requirement_id)
    if not record:
        raise HTTPException(404, "Requirement not found")
    for k, v in payload.dict().items():
        setattr(record, k, v)
    db.commit()
    db.refresh(record)
    return record


@router.delete("/{requirement_id}")
def delete_requirement(requirement_id: int, db: Session = Depends(get_db)):
    record = db.get(Requirement, requirement_id)
    if not record:
        raise HTTPException(404, "Requirement not found")
    db.delete(record)
    db.commit()
    return {"ok": True}

