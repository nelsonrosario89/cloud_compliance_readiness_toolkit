from typing import List, Optional
from uuid import uuid4

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from ..db import get_db
from ..models import Project


router = APIRouter()


class ProjectCreate(BaseModel):
    name: str
    description: Optional[str] = None
    status: Optional[str] = "planning"
    target_frameworks: Optional[List[str]] = None


def _split_csv(value: Optional[str]) -> List[str]:
    if not value:
        return []
    return [item.strip() for item in value.split(",") if item.strip()]


def _project_to_dict(project: Project) -> dict:
    return {
        "id": project.id,
        "name": project.name,
        "description": project.description,
        "status": project.status,
        "target_frameworks": _split_csv(project.target_frameworks),
    }


@router.get("/", summary="List projects")
def list_projects(db: Session = Depends(get_db)) -> list[dict]:
    """Return all readiness projects from the database."""

    projects = db.query(Project).order_by(Project.name).all()
    return [_project_to_dict(p) for p in projects]


@router.post("/", summary="Create project")
def create_project(payload: ProjectCreate, db: Session = Depends(get_db)) -> dict:
    """Create a new readiness project.

    This models a Fortreum-style engagement (e.g., "SaaS SOC 2 + ISO 27001
    Readiness").
    """

    project_id = str(uuid4())
    target_frameworks_str = (
        ",".join(payload.target_frameworks) if payload.target_frameworks else None
    )

    project = Project(
        id=project_id,
        name=payload.name,
        description=payload.description,
        status=payload.status or "planning",
        target_frameworks=target_frameworks_str,
    )
    db.add(project)
    db.commit()
    db.refresh(project)
    return _project_to_dict(project)
