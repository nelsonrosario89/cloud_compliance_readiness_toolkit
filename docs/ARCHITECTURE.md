# Cloud Compliance Readiness Toolkit – Architecture

This project is a **FastAPI** backend that exposes a control catalog and
readiness-planning features for SOC 2, ISO 27001, and PCI DSS.

## Components

- **FastAPI app (`backend/app/main.py`)**
  - Provides `/health`, `/frameworks`, `/controls`, `/labs`, `/projects`, `/evidence`, `/tasks`.
- **Database layer (`backend/app/db.py`, `backend/app/models.py`)**
  - Uses SQLite locally via SQLAlchemy.
  - Models: `Framework`, `Control`, `Lab`, `Project`, `EvidenceItem`, `RemediationTask`.
- **Routes (`backend/app/routes/`)**
  - Each module defines an `APIRouter` with placeholder list endpoints.
- **Control catalog (`control_catalog_skeleton.yaml`)**
  - Lives at the portfolio root and defines mappings:
    - Frameworks → Controls → Labs → AWS services → Evidence types.
  - Future work: seed the database from this YAML at startup.

## Data Flow (Future State)

1. On startup, FastAPI reads `control_catalog_skeleton.yaml`.
2. It creates/updates DB rows for frameworks, controls, and labs.
3. UI or API clients query `/frameworks`, `/controls`, and `/labs` to
   drive readiness workflows and advisory reports.
