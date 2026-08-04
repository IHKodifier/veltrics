# Antigravity Agent Rules — Veltrics Project Directives

> Engineering governance for Veltrics Fleet & Vehicle Management Platform. Read this before any code change.  
> Master Spec: `product-specs/08-master-prd.md` | Backlog: `product-specs/06a-use-case-tickets.md` | Master Tracker: `trackers/07-big-picture-tracker.md`

---

## 1. Git Branch Protection & Workflow
- **`main` / `master` (Production):** NEVER commit or push code directly to `main`. This branch is strictly for production releases merged from `dev`.
- **`dev` (Staging):** Protected staging branch. All feature work must take place on dedicated `sprint/sprint-XX` or `feature/` branches checked out from `dev`.
- **Initial Setup Workflow:**
  1. Commit initial project configuration and specs to `main`.
  2. Checkout staging branch `dev`: `git checkout -b dev`.
  3. Checkout sprint branch `sprint/sprint-01` from `dev`: `git checkout -b sprint/sprint-01`.
- **Merging Protocol:** Only propose or execute a PR/merge from `sprint/sprint-XX` into `dev` when **100% of automated tests pass locally**.
- **Commit Format:** `feat(UC-XXX): brief description` or `fix(UC-XXX): brief description`.

---

## 2. Phase 0 Scaffolding & Firebase Multi-Env Baseline
- **Flutter Scaffolding:** Create Flutter project boilerplate inside `/src/frontend` (`cd src; flutter create frontend`) before active ticket implementation. Apply theme tokens from `product-specs/05b-flutter-theme.dart`.
- **Firebase Binding:** Link Firebase projects for Dev, Staging, and Production environments (`flutterfire configure`):
  - **Dev:** Local auth emulator / `veltrics-dev` Firebase bindings.
  - **Staging:** `veltrics-staging` Firebase bindings.
  - **Prod:** `veltrics-prod` Firebase bindings.

---

## 3. Local-First & Zero-Cloud Execution
- **No Docker Required:** Local development MUST use `.\scripts\start_backend.ps1` (FastAPI + Uvicorn + SQLite `sqlite:///./dev.db` + Local Auth Emulator targeting `src/backend`).
- **GCP Cost Protection:** Do NOT spin up GCP Cloud SQL instances during routine feature development. Use `.\scripts\gcp_cloud_control.ps1 -Action start|stop` strictly for staging deployment verification.
- **SQLite/PostgreSQL Dialect Parity:** Use dialect-agnostic SQLAlchemy types (`JSON` → SQLite JSON / PG JSONB; string-backed `UUID` decorator).

---

## 4. TDD & API-First Mandate
- **Test-First Development:** Before writing implementation code or feature logic, create or update automated test files in `./src/tests/unit/` or `./src/tests/integration/`.
- **100% API Decoupling:** The frontend must NEVER interact directly with database models. All data requests must route through FastAPI REST endpoints governed by Pydantic payload models.
- **Every Acceptance Criterion:** Every testable acceptance criterion in `06a-use-case-tickets.md` must have a corresponding test assertion.

---

## 5. Automatic Hierarchical Tracker Maintenance
- Whenever a task, feature, or test suite is completed or updated:
  1. Record test names and Pass/Fail results in the active sprint tracker (`trackers/stage-01/sprints/07.01.XX-tracker.md`).
  2. Update the task status in the stage tracker (`trackers/stage-01/07.01-tracker.md`).
  3. Update the overall sprint completion percentage in the master tracker (`trackers/07-big-picture-tracker.md`).

---

## 6. Sprint Handoff Prompt Generation
- **End-of-Sprint Protocol:** At the end of every sprint (once 100% of DoD criteria and local tests pass), the agent MUST automatically generate a structured Handoff Prompt file indicating both the completed sprint and the upcoming sprint (e.g. `handoff-sprint-01-to-02.md`) and save it in `handoff-prompts/sprints/stage-01/handoff-sprint-01-to-02.md`.
- **Handoff Content:** Summary of completed user stories/tasks, test results, branch merge status, updated tracker links, and initial prompts/goals for the subsequent sprint.

---

## 7. Execution Commands & Boundary Matrix

### Quick Commands
- Start Backend Local: `.\scripts\start_backend.ps1`
- Run Backend Tests: `pytest src/tests/ -v`
- Start Mobile Client: `cd src/mobile_frontend; flutter run`
- Manage GCP Cloud SQL: `.\scripts\gcp_cloud_control.ps1 -Action start|stop`

### Governance Boundaries
| Always | Ask First | Never |
|:---|:---|:---|
| Run local tests before PR | Spinning up GCP Cloud SQL | Commit or push directly to `main` |
| Work one ticket at a time | Adding new core dependencies | Commit `.env` secrets or credentials |
| Use SQLite `dev.db` for local dev | Changing database schema definitions | Delete or weaken failing tests |

---

## 8. Project Structure
```
veltrics/
├── .agents/                       # Custom agent skills & local rules
│   └── AGENTS.md                  # Canonical engineering governance rules
├── .github/                       # GitHub Actions workflows & PR templates
├── handoff-prompts/               # Stage & Sprint handoff prompts
│   ├── specs-planning/
│   └── sprints/
│       └── stage-01/
├── product-specs/                 # All Product Specifications & Master PRD
├── scripts/                       # Development & GCP cloud management scripts
├── trackers/                      # Live hierarchical backlog trackers
└── src/                           # Single container for all application code
    ├── backend/                   # Python FastAPI Backend
    ├── frontend/                      # Flutter Client App (Web / Mobile / Desktop)
    └── tests/                     # Automated Test Suite
```
