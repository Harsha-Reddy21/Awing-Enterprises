from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
from models import Candidate, Requirement


router = APIRouter()


def simple_match_score(candidate: Candidate, requirement: Requirement) -> float:
    score = 0.0
    if candidate.experience_years and requirement.min_experience:
        if candidate.experience_years >= requirement.min_experience:
            score += 0.4
    if requirement.skills_required and candidate.skills:
        req_skills = {s.strip().lower() for s in requirement.skills_required.split(',')}
        cand_skills = {s.strip().lower() for s in candidate.skills.split(',')}
        overlap = len(req_skills & cand_skills)
        score += min(0.5, 0.1 * overlap)
    if requirement.location and candidate.location and requirement.location.lower() == candidate.location.lower():
        score += 0.1
    return round(min(score, 1.0), 2)


@router.get("/requirement/{requirement_id}")
def match_candidates(requirement_id: int=1, limit: int = 20, db: Session = Depends(get_db)):
    requirement = db.get(Requirement, requirement_id)
    if not requirement:
        return []
    candidates = db.query(Candidate).all()
    scored = [
        {
            "candidate_id": c.id,
            "full_name": c.full_name,
            "score": simple_match_score(c, requirement),
        }
        for c in candidates
    ]
    scored.sort(key=lambda x: x["score"], reverse=True)
    return scored[:limit]

