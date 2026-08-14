# Handoff Prompt: Execute Ticket UC-004 — User Password Authentication & Session Initiation

We are working on the **Veltrics Fleet & Vehicle Management Platform** (Python FastAPI Backend + Flutter Frontend).
Sprint 01 is active in Stage 01.

---

## 1. Project Context & Current State
- **Branch Strategy:** Active sprint branch (`sprint/sprint-01` or feature branch).
- **Backend Stack:** Python FastAPI + SQLAlchemy + SQLite (`sqlite:///./dev.db`) local-first.
- **Frontend Stack:** Flutter Client App (`src/frontend`).
- **Governance Rules:** Follow `.agents/AGENTS.md`.
- **Completed Tickets (17 / 27 in Sprint 01 — 63.0% Complete):**
  - `UC-001` (Auth Google One-Tap), `UC-002` (Auth Facebook Login), `UC-003` (Auth Email & Password), `UC-014` (Auto-Create Personal Org), `UC-015` (View & Switch Active Organization), `UC-016` (Invite Team Member to Organization), `UC-024` (Add Vehicle), `UC-025` (View Vehicles), `UC-026` (Vehicle Detail), `UC-027` (Edit Vehicle), `UC-034` (View Maintenance Schedule), `UC-035` (Customize Maintenance Schedule Items), `UC-036` (Log Service Record), `UC-037` (View Service History), `UC-038` (Bulk Accept Maintenance Schedule), `UC-064` (Overview Fleet Dashboard KPI Metrics), `UC-118` (DB Seeding).

---

## 2. Target Ticket Specification: UC-004
- **Ticket ID:** `UC-004: User Password Authentication & Session Initiation`
- **Linked Story:** `FS-AUTH-003`
- **Actor:** Registered User
- **Trigger:** User submits email & password credentials on login form.
- **Endpoints to Implement / Verify:**
  1. `POST /api/v1/auth/login`: Authenticates registered email & password credentials, verifies active user status (`is_active` / `deleted_at IS NULL`), and returns `AuthSessionDTO`.
- **Frontend Requirements (`src/frontend`):**
  - Add login handler to `AuthRepository` (`loginWithEmail`) and update `LoginScreen` to handle both Sign In and Sign Up actions.
- **Testing Requirements (`src/tests/unit/test_auth_uc004.py`):**
  - Test login with valid email and password credentials returns `HTTP 200 OK` containing Access JWT and Refresh Token.
  - Assert incorrect password or unregistered email returns `HTTP 401 Unauthorized`.
  - Assert disabled or soft-deleted user returns `HTTP 403 Forbidden`.

---

## 3. Mandatory Next Action
Please start by entering **Planning Mode**, inspecting the codebase as needed, and generating the `implementation_plan.md` artifact for **UC-004** for review and approval.
