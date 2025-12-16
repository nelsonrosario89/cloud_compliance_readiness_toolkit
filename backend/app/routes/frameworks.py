from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..db import get_db
from ..models import Framework


router = APIRouter()


@router.get("/", summary="List frameworks")
def list_frameworks(db: Session = Depends(get_db)) -> list[dict]:
    """Return all frameworks from the database."""

    frameworks = db.query(Framework).order_by(Framework.id).all()
    return [
        {"id": fw.id, "name": fw.name, "description": fw.description}
        for fw in frameworks
    ]
