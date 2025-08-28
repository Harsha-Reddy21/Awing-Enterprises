from __future__ import annotations

from typing import List, Optional

from schemas.domain import SourcingQuery, SourcedCandidate


class NaukriProvider:
    name = "naukri"

    def __init__(self, api_key: Optional[str], api_secret: Optional[str]):
        self.api_key = api_key
        self.api_secret = api_secret

    def search_candidates(self, query: SourcingQuery) -> List[SourcedCandidate]:
        # TODO: integrate Naukri.com API (Partner/Recruiter APIs)
        skills = (
            [s.strip() for s in (query.skills_required or "").split(",") if s.strip()]
            or None
        )
        return [
            SourcedCandidate(
                full_name="Rahul Kumar",
                headline=f"{query.title or 'Engineer'}",
                location=query.location or "Bengaluru",
                skills=skills,
                source=self.name,
                profile_url="https://www.naukri.com/r/profile/rahul",
                score=0.76,
            )
        ]


