from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
from config import get_settings
from schemas.domain import SourcingQuery, SourcedCandidate
from providers.linkedin import LinkedInProvider
from providers.naukri import NaukriProvider


router = APIRouter()


def _select_providers(settings) -> list:
    providers: list = []
    providers.append(LinkedInProvider(settings.linkedin_access_token))
    providers.append(NaukriProvider(settings.naukri_api_key, settings.naukri_api_secret))
    return providers


@router.post("/search", response_model=List[SourcedCandidate])
def search_candidates(payload: SourcingQuery, db: Session = Depends(get_db)):
    settings = get_settings()
    selected_names = set([p.lower() for p in (payload.providers or ["linkedin", "naukri"])])
    providers = _select_providers(settings)

    results: list[SourcedCandidate] = []
    for provider in providers:
        if provider.name not in selected_names:
            continue
        results.extend(provider.search_candidates(payload))

    # Simple cap
    limit = payload.limit or 20
    return results[:limit]


