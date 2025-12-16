from datetime import datetime
from typing import List, Optional
from uuid import uuid4

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from ..db import get_db
from ..models import EvidenceItem


router = APIRouter()


class EvidenceCreate(BaseModel):
    project_id: str
    control_id: str
    lab_id: Optional[str] = None
    type: str
    location: str
    collected_at: Optional[datetime] = None


def _evidence_to_dict(e: EvidenceItem) -> dict:
    return {
        "id": e.id,
        "project_id": e.project_id,
        "control_id": e.control_id,
        "lab_id": e.lab_id,
        "type": e.type,
        "location": e.location,
        "collected_at": e.collected_at.isoformat() if e.collected_at else None,
    }


@router.get("/", summary="List evidence items")
def list_evidence(
    project_id: Optional[str] = None,
    control_id: Optional[str] = None,
    db: Session = Depends(get_db),
) -> list[dict]:
    """Return evidence items, optionally filtered by project and control."""

    query = db.query(EvidenceItem)
    if project_id:
        query = query.filter(EvidenceItem.project_id == project_id)
    if control_id:
        query = query.filter(EvidenceItem.control_id == control_id)

    items = query.order_by(EvidenceItem.collected_at.desc()).all()
    return [_evidence_to_dict(e) for e in items]


@router.post("/", summary="Create evidence item")
def create_evidence(payload: EvidenceCreate, db: Session = Depends(get_db)) -> dict:
    """Record a new evidence item for a given project/control.

    Example: link a CSV from the EC2 inventory lab or a JSON report from the
    S3 public access check to a specific control in a readiness project.
    """

    evidence_id = str(uuid4())
    evidence = EvidenceItem(
        id=evidence_id,
        project_id=payload.project_id,
        control_id=payload.control_id,
        lab_id=payload.lab_id,
        type=payload.type,
        location=payload.location,
        collected_at=payload.collected_at or datetime.utcnow(),
    )
    db.add(evidence)
    db.commit()
    db.refresh(evidence)
    return _evidence_to_dict(evidence)
