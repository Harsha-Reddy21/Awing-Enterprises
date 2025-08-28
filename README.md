# Awign Dost API (FastAPI + Postgres)

## Run locally (Docker)

```bash
docker compose up --build
```

API: http://localhost:8000
Docs: http://localhost:8000/docs

## Environment
- DATABASE_URL (defaults in compose)

## Endpoints (high level)
- GET /health
- Requirements: CRUD under /requirements
- Candidates: CRUD under /candidates
- Applications: create/list/get, update stage under /applications
- Interactions: create/list per candidate under /interactions
- Screening: questions create/list and responses under /screening
- Submissions: create/get under /submissions
- Feedback: create/list under /feedback
- Outreach: stubs for mass-mail, linkedin, whatsapp under /outreach
- Matching: simple scoring under /matching

