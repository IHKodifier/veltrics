# Handoff Prompt: Execute Ticket UC-002 — Sign Up with Facebook Login

We are working on the **Veltrics Fleet & Vehicle Management Platform** (Python FastAPI Backend + Flutter Frontend).
Sprint 01 is active in Stage 01.

---

## 1. Project Context & Current State
- **Branch Strategy:** Active sprint branch (`sprint/sprint-01` or feature branch).
- **Backend Stack:** Python FastAPI + SQLAlchemy + SQLite (`sqlite:///./dev.db`) local-first.
- **Frontend Stack:** Flutter Client App (`src/frontend`).
- **Governance Rules:** Follow `.agents/AGENTS.md`.
- **Completed Tickets (15 / 27 in Sprint 01 — 55.6% Complete):**
  - `UC-001` (Auth Google One-Tap), `UC-014` (Auto-Create Personal Org), `UC-015` (View & Switch Active Organization), `UC-016` (Invite Team Member to Organization), `UC-024` (Add Vehicle), `UC-025` (View Vehicles), `UC-026` (Vehicle Detail), `UC-027` (Edit Vehicle), `UC-034` (View Maintenance Schedule), `UC-035` (Customize Maintenance Schedule Items), `UC-036` (Log Service Record), `UC-037` (View Service History), `UC-038` (Bulk Accept Maintenance Schedule), `UC-064` (Overview Fleet Dashboard KPI Metrics), `UC-118` (DB Seeding).

---

## 2. Target Ticket Specification: UC-002
- **Ticket ID:** `UC-002: Sign Up with Facebook Login`
- **Linked Story:** `FS-AUTH-001b`
- **Actor:** Unauthenticated User
- **Trigger:** User taps "Continue with Facebook" button on auth screen.
- **Endpoints to Implement / Verify:**
  1. `POST /api/v1/auth/register`: Extend auth registration endpoint to support `auth_provider = "facebook"` and append `"facebook"` to `linked_providers` JSON array in `users` entity.
- **Frontend Requirements (`src/frontend`):**
  - Support Facebook auth provider integration in auth repository / domain models.
  - Wire "Continue with Facebook" button action in login/registration screen.
- **Testing Requirements (`src/tests/unit/test_auth_uc002.py`):**
  - Test registration with `auth_provider = "facebook"`.
  - Assert `"facebook"` is added to `linked_providers` array in `users` entity.
  - Test account linking behavior when email matches existing account with a different provider.

---

## 3. Mandatory Next Action
Please start by entering **Planning Mode**, inspecting the codebase as needed, and generating the `implementation_plan.md` artifact for **UC-002** for review and approval.
