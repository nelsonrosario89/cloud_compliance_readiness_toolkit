from typing import Optional

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..db import get_db
from ..models import Control


router = APIRouter()


@router.get("/", summary="List controls")
def list_controls(
    framework_id: Optional[str] = None,
    db: Session = Depends(get_db),
) -> list[dict]:
    """Return controls from the database, optionally filtered by framework.

    Example: `/controls?framework_id=iso27001_2022`.
    """

    query = db.query(Control)
    if framework_id:
        query = query.filter(Control.framework_id == framework_id)

    controls = query.order_by(Control.id).all()
    return [
        {
            "id": ctrl.id,
            "framework_id": ctrl.framework_id,
            "title": ctrl.title,
            "description": ctrl.description,
            "category": ctrl.category,
        }
        for ctrl in controls
    ]
