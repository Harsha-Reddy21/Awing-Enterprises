from __future__ import annotations

from typing import List, Optional

from schemas.domain import SourcingQuery, SourcedCandidate


class LinkedInProvider:
    name = "linkedin"

    def __init__(self, access_token: Optional[str]):
        self.access_token = access_token

    def search_candidates(self, query: SourcingQuery) -> List[SourcedCandidate]:
        # TODO: integrate LinkedIn Talent or Sales Navigator API
        # Stub returns demo data shaped for UI/testing
        skills = (
            [s.strip() for s in (query.skills_required or "").split(",") if s.strip()]
            or None
        )
        return [
            SourcedCandidate(
                full_name="Jane Doe",
                headline=f"{query.title or 'Engineer'} at Example",
                location=query.location or "Remote",
                skills=skills,
                source=self.name,
                profile_url="https://www.linkedin.com/in/jane-doe",
                score=0.82,
            )
        ]


