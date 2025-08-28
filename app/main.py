from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database import Base, engine
from routers import requirements, candidates, applications, interactions, screening, submissions, feedback, outreach, matching, confirmations, sourcing


Base.metadata.create_all(bind=engine)

app = FastAPI(title="Awign Dost API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health():
    return {"status": "ok"}


app.include_router(requirements.router, prefix="/requirements", tags=["requirements"])
app.include_router(candidates.router, prefix="/candidates", tags=["candidates"])
app.include_router(applications.router, prefix="/applications", tags=["applications"])
app.include_router(interactions.router, prefix="/interactions", tags=["interactions"])
app.include_router(screening.router, prefix="/screening", tags=["screening"])
app.include_router(submissions.router, prefix="/submissions", tags=["submissions"])
app.include_router(feedback.router, prefix="/feedback", tags=["feedback"])
app.include_router(outreach.router, prefix="/outreach", tags=["outreach"])
app.include_router(matching.router, prefix="/matching", tags=["matching"])
app.include_router(confirmations.router, prefix="/confirmations", tags=["confirmations"])
app.include_router(sourcing.router, prefix="/sourcing", tags=["sourcing"])

#http://host.docker.internal:8000
import uvicorn
if __name__ == "__main__":
    uvicorn.run('main:app', host="0.0.0.0", port=8000)

