from datetime import datetime
from typing import List, Optional
from uuid import uuid4

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from ..db import get_db
from ..models import RemediationTask


router = APIRouter()


class TaskCreate(BaseModel):
    project_id: str
    control_id: str
    title: str
    description: Optional[str] = None
    owner: Optional[str] = None
    status: Optional[str] = "open"
    due_date: Optional[datetime] = None


def _task_to_dict(task: RemediationTask) -> dict:
    return {
        "id": task.id,
        "project_id": task.project_id,
        "control_id": task.control_id,
        "title": task.title,
        "description": task.description,
        "owner": task.owner,
        "status": task.status,
        "due_date": task.due_date.isoformat() if task.due_date else None,
    }


@router.get("/", summary="List remediation tasks")
def list_tasks(
    project_id: Optional[str] = None,
    status: Optional[str] = None,
    db: Session = Depends(get_db),
) -> list[dict]:
    """Return remediation tasks, optionally filtered by project and status."""

    query = db.query(RemediationTask)
    if project_id:
        query = query.filter(RemediationTask.project_id == project_id)
    if status:
        query = query.filter(RemediationTask.status == status)

    tasks = query.order_by(RemediationTask.due_date.is_(None), RemediationTask.due_date).all()
    return [_task_to_dict(t) for t in tasks]


@router.post("/", summary="Create remediation task")
def create_task(payload: TaskCreate, db: Session = Depends(get_db)) -> dict:
    """Create a new remediation task for a project/control pair."""

    task_id = str(uuid4())
    task = RemediationTask(
        id=task_id,
        project_id=payload.project_id,
        control_id=payload.control_id,
        title=payload.title,
        description=payload.description,
        owner=payload.owner,
        status=payload.status or "open",
        due_date=payload.due_date,
    )
    db.add(task)
    db.commit()
    db.refresh(task)
    return _task_to_dict(task)
