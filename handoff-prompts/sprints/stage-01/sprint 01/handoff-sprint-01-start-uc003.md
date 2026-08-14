# Handoff Prompt: Execute Ticket UC-003 — Sign Up with Email and Password

We are working on the **Veltrics Fleet & Vehicle Management Platform** (Python FastAPI Backend + Flutter Frontend).
Sprint 01 is active in Stage 01.

---

## 1. Project Context & Current State
- **Branch Strategy:** Active sprint branch (`sprint/sprint-01` or feature branch).
- **Backend Stack:** Python FastAPI + SQLAlchemy + SQLite (`sqlite:///./dev.db`) local-first.
- **Frontend Stack:** Flutter Client App (`src/frontend`).
- **Governance Rules:** Follow `.agents/AGENTS.md`.
- **Completed Tickets (16 / 27 in Sprint 01 — 59.3% Complete):**
  - `UC-001` (Auth Google One-Tap), `UC-002` (Auth Facebook Login), `UC-014` (Auto-Create Personal Org), `UC-015` (View & Switch Active Organization), `UC-016` (Invite Team Member to Organization), `UC-024` (Add Vehicle), `UC-025` (View Vehicles), `UC-026` (Vehicle Detail), `UC-027` (Edit Vehicle), `UC-034` (View Maintenance Schedule), `UC-035` (Customize Maintenance Schedule Items), `UC-036` (Log Service Record), `UC-037` (View Service History), `UC-038` (Bulk Accept Maintenance Schedule), `UC-064` (Overview Fleet Dashboard KPI Metrics), `UC-118` (DB Seeding).

---

## 2. Target Ticket Specification: UC-003
- **Ticket ID:** `UC-003: Sign Up with Email and Password`
- **Linked Story:** `FS-AUTH-002`
- **Actor:** Unauthenticated User
- **Trigger:** User submits email, password, and confirmation on registration form.
- **Endpoints to Implement / Verify:**
  1. `POST /api/v1/auth/register`: Extend auth registration endpoint to support `auth_provider = "email"`, password validation, and hashing/storing user credentials or token verification.
- **Frontend Requirements (`src/frontend`):**
  - Wire email & password registration form action and client validation (min 8 chars, 1 upper, 1 digit).
- **Testing Requirements (`src/tests/unit/test_auth_uc003.py`):**
  - Test registration with `auth_provider = "email"` and valid password.
  - Assert user entity created with `auth_provider = "facebook" / "email"` and `linked_providers = ["email"]`.
  - Assert weak password or missing fields return `HTTP 400 Bad Request`.

---

## 3. Mandatory Next Action
Please start by entering **Planning Mode**, inspecting the codebase as needed, and generating the `implementation_plan.md` artifact for **UC-003** for review and approval.
