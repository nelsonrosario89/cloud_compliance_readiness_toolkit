from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml
from sqlalchemy.orm import Session

from .db import Base, SessionLocal, engine
from .models import Control, Framework, Lab


# Locate the YAML catalog at the portfolio root, even when running from the
# backend/app directory.
CATALOG_PATH = (
    Path(__file__).resolve().parents[2].parent / "control_catalog_skeleton.yaml"
)


def init_db_and_seed() -> None:
    """Create database tables and seed them from the YAML catalog if empty."""

    # Ensure tables exist
    Base.metadata.create_all(bind=engine)

    # Seed only if frameworks table is empty
    _seed_catalog_if_empty()


def _seed_catalog_if_empty() -> None:
    db: Session = SessionLocal()
    try:
        has_framework = db.query(Framework).first()
        if has_framework:
            return

        if not CATALOG_PATH.exists():
            # Catalog file missing – nothing to seed.
            return

        raw = CATALOG_PATH.read_text(encoding="utf-8")
        data: dict[str, Any] = yaml.safe_load(raw) or {}

        # Seed labs first so controls can reference them later if needed.
        for lab in data.get("labs", []):
            db.add(
                Lab(
                    id=lab["id"],
                    name=lab["name"],
                    repo_path=lab.get("repo_path"),
                    aws_services=",".join(lab.get("aws_services", [])),
                    evidence_types=",".join(lab.get("evidence_types", [])),
                )
            )

        # Seed frameworks and controls
        for fw in data.get("frameworks", []):
            framework = Framework(
                id=fw["id"],
                name=fw["name"],
                description=fw.get("description"),
            )
            db.add(framework)

            for ctrl in fw.get("controls", []):
                db.add(
                    Control(
                        id=ctrl["control_id"],
                        framework_id=fw["id"],
                        title=ctrl["title"],
                        description=ctrl.get("description"),
                        category=ctrl.get("category"),
                    )
                )

        db.commit()
    finally:
        db.close()
