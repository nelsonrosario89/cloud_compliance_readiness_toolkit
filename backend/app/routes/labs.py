from typing import List, Optional

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..db import get_db
from ..models import Lab


router = APIRouter()


@router.get("/", summary="List labs")
def list_labs(
    service: Optional[str] = None,
    db: Session = Depends(get_db),
) -> list[dict]:
    """Return labs from the database, optionally filtered by AWS service.

    Example: `/labs?service=Security Hub`.
    """

    query = db.query(Lab)
    if service:
        # Simple substring filter on the stored CSV of services.
        query = query.filter(Lab.aws_services.like(f"%{service}%"))

    labs = query.order_by(Lab.id).all()

    def _split_csv(value: Optional[str]) -> List[str]:
        if not value:
            return []
        return [item.strip() for item in value.split(",") if item.strip()]

    return [
        {
            "id": lab.id,
            "name": lab.name,
            "repo_path": lab.repo_path,
            "aws_services": _split_csv(lab.aws_services),
            "evidence_types": _split_csv(lab.evidence_types),
        }
        for lab in labs
    ]
