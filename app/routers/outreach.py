from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db


router = APIRouter()


@router.post("/mass-mail")
def mass_mail(requirement_id: int, query: str, db: Session = Depends(get_db)):
    return {"status": "queued", "requirement_id": requirement_id, "query": query}


@router.post("/linkedin/message")
def linkedin_message(candidate_id: int, message: str, db: Session = Depends(get_db)):
    return {"status": "sent", "candidate_id": candidate_id}


@router.post("/whatsapp/send")
def whatsapp_send(candidate_id: int, message: str, db: Session = Depends(get_db)):
    return {"status": "sent", "candidate_id": candidate_id}

