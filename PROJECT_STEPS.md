# Cloud Compliance Readiness Toolkit – Step Log

Plain-language log of what we did (and why) while building this project.

## 1. Planning the Project

- Wrote `portfolio_project_plan.md` to describe the Fortreum role and
  how this toolkit will demonstrate SOC 2 / ISO 27001 / PCI skills.
- Chose **Option 1 – Cloud Compliance Readiness Toolkit** as the primary
  portfolio project (with PCI and content automation as inspirations).
- Defined problem, outcomes, personas, and a phased delivery plan.

## 2. Mapping Controls to Labs (Control Catalog)

- Created `control_catalog_skeleton.yaml` at the portfolio root.
- This YAML maps **frameworks → controls → labs → AWS services →
  evidence types**.
- Included Labs 1–9 (CloudTrail, EC2 inventory, S3 public check, MFA,
  SG drift, continuous monitoring, IAM role review, audit pack,
  dashboard).
- This catalog is the “source of truth” the app will later read.

## 3. FastAPI Backend Scaffold

- Created the `cloud_compliance_readiness_toolkit` folder.
- Added a **FastAPI** backend under `backend/app/`:
  - `main.py` – FastAPI app, `/health` endpoint, empty routers for
    `/frameworks`, `/controls`, `/labs`, `/projects`, `/evidence`,
    `/tasks`.
  - `db.py` – SQLite database config (`toolkit.db`) using SQLAlchemy.
  - `models.py` – database models for `Framework`, `Control`, `Lab`,
    `Project`, `EvidenceItem`, `RemediationTask`.
  - `routes/*.py` – each file defines an API router with a placeholder
    "list" endpoint.
- Added docs in `docs/`:
  - `ARCHITECTURE.md` – how the pieces fit (FastAPI, DB, routes,
    catalog).
  - `CONTROL_MAPPING.md` – explains how the YAML control catalog is
    used.
- Created `requirements.txt` with FastAPI / Uvicorn / SQLAlchemy /
  PyYAML, and a `README.md` with run instructions.

## 4. Local Environment Setup

- In the `cloud_compliance_readiness_toolkit` folder, created and
  activated a Python virtual environment:
  - `python3 -m venv .venv`
  - `source .venv/bin/activate`
- Installed dependencies from `requirements.txt` using `python3 -m pip
  install -r requirements.txt`.
- Ran the app locally with `uvicorn app.main:app --reload --app-dir
  backend` and confirmed:
  - `GET /health` returns `{ "status": "ok" }`.
  - `/docs` shows the stub endpoints.

## 5. Next up – Load the Control Catalog into the API

- Goal: on app startup, read `control_catalog_skeleton.yaml` and
  populate the SQLite database with frameworks, controls, and labs.
- Then change the `/frameworks`, `/controls`, and `/labs` endpoints to
  return **real data** from the database instead of empty lists.
- This will turn the API into a live reflection of the portfolio labs
  and their compliance mappings.

## 6. Implemented – Catalog Loaded into the API

- Added `backend/app/catalog_loader.py` which:
  - Finds `control_catalog_skeleton.yaml` at the portfolio root.
  - Creates the database tables if they do not exist.
  - Reads the YAML once and seeds the `frameworks`, `controls`, and
    `labs` tables the first time the app starts.
- Updated `backend/app/db.py` with a `get_db()` helper so FastAPI
  routes can safely open/close database connections.
- Updated `backend/app/main.py` to call the catalog loader on startup:
  - When you run `uvicorn`, the app now automatically creates the
    tables and loads the control catalog.
- Updated the `/frameworks`, `/controls`, and `/labs` routes so they:
  - Query the SQLite database instead of returning empty lists.
  - Return real data that matches the YAML catalog (framework IDs,
    control IDs, lab IDs, plus service/evidence lists).
- Result: when you visit these endpoints in `/docs` or via HTTP calls,
  you are now seeing **live catalog data** that directly reflects your
  AWS labs and control mappings.

## 7. Filters and Readiness Engagement Endpoints

- Added **filters** to catalog endpoints so you can slice the data:
  - `/controls?framework_id=iso27001_2022` returns only ISO controls.
  - `/labs?service=Security Hub` returns only labs that use Security
    Hub.
- Replaced placeholder endpoints with real ones for **projects,
  evidence, and tasks**:
  - `/projects` (GET/POST) – list and create readiness projects (for
    example, a SaaS SOC 2 + ISO 27001 engagement).
  - `/evidence` (GET/POST) – attach concrete evidence items (CSV/JSON
    reports, screenshots) to a specific project + control + lab.
  - `/tasks` (GET/POST) – create and track remediation tasks tied to a
    project and control (owner, due date, status).
- Together, these endpoints let you **tell a Fortreum-style story**:
  you can stand up a project, map it to framework controls, link real
  lab evidence, and show remediation tasks – all via the API.

## 8. Demo Runbook for Interviews

Use this as a 5–7 minute walkthrough in an interview.

1. **Start at `/docs`**
   - Say: "This is a small FastAPI backend I built to model SOC 2 / ISO
     27001 / PCI readiness. It loads a control catalog from YAML and
     ties it to AWS labs and evidence."
2. **Show the catalog**
   - Call `GET /frameworks` and `GET /controls?framework_id=iso27001_2022`.
   - Say: "Here are the frameworks and controls. Each control is mapped
     to AWS labs behind the scenes via the catalog."
   - Call `GET /labs?service=Security Hub`.
   - Say: "These labs are the automation side – Security Hub, S3 public
     checks, IAM reviews, etc."
3. **Create a project**
   - Use `POST /projects` with a body like "SaaS SOC 2 + ISO 27001
     Readiness".
   - Say: "I treat each client engagement as a project with in-scope
     frameworks." Copy the returned `project_id`.
4. **Attach evidence**
   - Use `POST /evidence` with that `project_id`, a control (for
     example, `A.12.4.1`), and a lab (for example,
     `lab1_cloudtrail_validation`).
   - Say: "Here I link concrete artifacts from my AWS labs to specific
     controls in the engagement." Show `GET /evidence?project_id=...`.
5. **Create remediation tasks**
   - Use `POST /tasks` for an open item such as enforcing MFA
     (`CC6.1.2`).
   - Say: "Each finding turns into a task with an owner and status,
     similar to how we would track remediation with a client."
6. **Close with the story**
   - Say: "This API is small on purpose – it demonstrates that I can map
     controls to AWS services, automate evidence collection, and express
     it as a repeatable readiness workflow focused on SOC 2 / ISO 27001
     and PCI."

## 9. Interview Checklist (5–7 min)

Use this checklist to stay on track during an interview demo.

| Time | What to show | Key talking point |
|------|--------------|-------------------|
| 0:00–0:30 | Open `/docs` | "I built a FastAPI backend that models GRC readiness engagements." |
| 0:30–1:30 | `GET /frameworks`, `GET /controls?framework_id=iso27001_2022` | "The control catalog maps SOC 2, ISO 27001, and PCI controls to AWS labs." |
| 1:30–2:30 | `GET /labs?service=Security Hub` | "Each lab produces evidence – CloudTrail logs, S3 findings, MFA reports." |
| 2:30–3:30 | `POST /projects` (or show existing) | "I model each client engagement as a project with target frameworks." |
| 3:30–4:30 | `GET /evidence?project_id=...` | "Evidence from AWS labs is linked to specific controls for audit prep." |
| 4:30–5:30 | `GET /tasks?project_id=...` | "Findings become remediation tasks with owners and statuses." |
| 5:30–6:30 | Show a lab screenshot (e.g., Security Hub) | "Here's actual output from Lab 4 – MFA enforcement findings in Security Hub." |
| 6:30–7:00 | Wrap up | "This shows I can connect AWS telemetry to compliance controls and communicate a clear story to clients and auditors." |

### Key points to emphasize

- **Frameworks covered:** SOC 2 Trust Services Criteria, ISO/IEC 27001:2022, PCI DSS v4.0
- **AWS services used:** CloudTrail, S3, Security Hub, IAM, Lambda, GitHub Actions (OIDC)
- **Automation:** Labs run on schedule via GitHub Actions; evidence uploads to S3 automatically
- **Consultant mindset:** Evidence → control mapping → remediation tasks → audit-ready story

### Questions you might get (and answers)

- **"Why FastAPI instead of a full GRC platform?"**
  - "This is a portfolio demo to show I understand the data model and workflow. In practice, I'd use whatever tool the client has – ServiceNow, Vanta, Drata – but the concepts transfer."

- **"How would you scale this?"**
  - "Add a React frontend for non-technical stakeholders, integrate with ticketing systems for task tracking, and deploy to AWS Lambda or ECS for production."

- **"What's the hardest part of a readiness engagement?"**
  - "Getting stakeholders aligned on scope and ownership. The technical controls are straightforward once you have buy-in."

