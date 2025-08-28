from typing import List
import random

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from database import get_db
from models import Candidate
from schemas.domain import CandidateCreate, CandidateOut


router = APIRouter()


@router.post("/", response_model=CandidateOut)
def create_candidate(payload: CandidateCreate, db: Session = Depends(get_db)):
    record = Candidate(**payload.dict())
    db.add(record)
    db.commit()
    db.refresh(record)
    return record


@router.get("/", response_model=List[CandidateOut])
def list_candidates(q: str | None = Query(None), db: Session = Depends(get_db)):
    query = db.query(Candidate)
    if q:
        like = f"%{q.lower()}%"
        query = query.filter(Candidate.skills.ilike(like) | Candidate.full_name.ilike(like))
    return query.order_by(Candidate.created_at.desc()).all()


@router.get("/{candidate_id}", response_model=CandidateOut)
def get_candidate(candidate_id: int, db: Session = Depends(get_db)):
    record = db.get(Candidate, candidate_id)
    if not record:
        raise HTTPException(404, "Candidate not found")
    return record


@router.put("/{candidate_id}", response_model=CandidateOut)
def update_candidate(candidate_id: int, payload: CandidateCreate, db: Session = Depends(get_db)):
    record = db.get(Candidate, candidate_id)
    if not record:
        raise HTTPException(404, "Candidate not found")
    for k, v in payload.dict().items():
        setattr(record, k, v)
    db.commit()
    db.refresh(record)
    return record


@router.delete("/{candidate_id}")
def delete_candidate(candidate_id: int, db: Session = Depends(get_db)):
    record = db.get(Candidate, candidate_id)
    if not record:
        raise HTTPException(404, "Candidate not found")
    db.delete(record)
    db.commit()
    return {"ok": True}


@router.post("/seed", response_model=List[CandidateOut])
def seed_candidates(count: int = 50, db: Session = Depends(get_db)):
    skills_pool = [
        "python",
        "java",
        "sql",
        "aws",
        "docker",
        "react",
        "node",
        "fastapi",
        "django",
        "kubernetes",
        "golang",
        "typescript",
        "terraform",
    ]
    locations = [
        "Bengaluru",
        "Mumbai",
        "Delhi",
        "Hyderabad",
        "Pune",
        "Chennai",
        "Remote",
    ]

    created: list[Candidate] = []
    for i in range(count):
        chosen_skills = ", ".join(random.sample(skills_pool, k=random.randint(3, 7)))
        record = Candidate(
            full_name=f"Candidate {random.randint(1000, 9999)}",
            email=None,  # keep nullable to avoid unique collisions across runs
            phone=None,  # keep nullable to avoid unique collisions across runs
            location=random.choice(locations),
            experience_years=round(random.uniform(0, 15), 1),
            skills=chosen_skills,
            notice_period_days=random.choice([0, 15, 30, 60, 90]),
            expected_salary=round(random.uniform(3, 50), 1),
            current_salary=round(random.uniform(2, 45), 1),
            resume_url=None,
            linkedin_url=None,
        )
        db.add(record)
        created.append(record)

    db.commit()
    for r in created:
        db.refresh(r)
    return created

