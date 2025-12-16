from fastapi import FastAPI

from .catalog_loader import init_db_and_seed
from .routes import controls, evidence, frameworks, labs, projects, tasks


app = FastAPI(
    title="Cloud Compliance Readiness Toolkit API",
    version="0.1.0",
    description="FastAPI backend for the Cloud Compliance Readiness Toolkit portfolio project.",
)


@app.get("/health", tags=["meta"])
async def health() -> dict:
    """Simple health check endpoint."""
    return {"status": "ok"}


@app.on_event("startup")
def startup_event() -> None:
    """Initialize database schema and seed from the control catalog."""

    init_db_and_seed()


app.include_router(frameworks.router, prefix="/frameworks", tags=["frameworks"])
app.include_router(controls.router, prefix="/controls", tags=["controls"])
app.include_router(labs.router, prefix="/labs", tags=["labs"])
app.include_router(projects.router, prefix="/projects", tags=["projects"])
app.include_router(evidence.router, prefix="/evidence", tags=["evidence"])
app.include_router(tasks.router, prefix="/tasks", tags=["tasks"])
