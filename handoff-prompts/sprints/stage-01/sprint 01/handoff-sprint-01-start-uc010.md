# Handoff Prompt: Execute Ticket UC-010 — User Sign Out & Token Revocation

We are working on the **Veltrics Fleet & Vehicle Management Platform** (Python FastAPI Backend + Flutter Frontend).
Sprint 01 is active in Stage 01.

---

## 1. Project Context & Current State
- **Branch Strategy:** Active sprint branch (`sprint/sprint-01` or feature branch).
- **Backend Stack:** Python FastAPI + SQLAlchemy + SQLite (`sqlite:///./dev.db`) local-first.
- **Frontend Stack:** Flutter Client App (`src/frontend`).
- **Governance Rules:** Follow `.agents/AGENTS.md`.
- **Completed Tickets (23 / 27 in Sprint 01 — 85.2% Complete):**
  - `UC-001` (Auth Google One-Tap), `UC-002` (Auth Facebook Login), `UC-003` (Auth Email & Password Registration), `UC-004` (User Password Authentication), `UC-005` (Sign In - All Methods), `UC-006` (Forgot Password & Reset Flow), `UC-007` (Complete Profile Setup & Multi-Tenant Role-Based Authorization), `UC-008` (View and Edit Profile), `UC-009` (Silent Token Refresh), `UC-014` (Auto-Create Personal Org), `UC-015` (View & Switch Active Organization), `UC-016` (Invite Team Member to Organization), `UC-024` (Add Vehicle), `UC-025` (View Vehicles), `UC-026` (Vehicle Detail), `UC-027` (Edit Vehicle), `UC-034` (View Maintenance Schedule), `UC-035` (Customize Maintenance Schedule Items), `UC-036` (Log Service Record), `UC-037` (View Service History), `UC-038` (Bulk Accept Maintenance Schedule), `UC-064` (Overview Fleet Dashboard KPI Metrics), `UC-118` (DB Seeding).

---

## 2. Target Ticket Specification: UC-010
- **Ticket ID:** `UC-010: User Sign Out & Token Revocation`
- **Linked Story:** `FS-AUTH-009`
- **Actor:** Authenticated User
- **Trigger:** User taps "Sign Out" in Settings / Profile screen.
- **Key Requirements:**
  1. Implement backend endpoint `POST /api/v1/auth/logout` accepting the active refresh token and invalidating/revoking it server-side.
  2. Implement client sign-out method in Flutter `AuthRepository` to clear local tokens, user session cache, and reset navigation to Login screen.
  3. Ensure subsequent token refresh requests using a revoked refresh token are rejected with `HTTP 401 Unauthorized`.
- **Testing Requirements (`src/tests/unit/test_auth_uc010.py`):**
  - Test successful sign-out flow and server-side token revocation.
  - Test rejection of refresh attempts using revoked tokens.
  - Test unauthenticated / bad token logout requests.

---

## 3. Mandatory Next Action
Please start by entering **Planning Mode**, inspecting the codebase as needed, and generating the `implementation_plan.md` artifact for **UC-010** for review and approval.
