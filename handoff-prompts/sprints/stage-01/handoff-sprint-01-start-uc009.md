# Handoff Prompt: Execute Ticket UC-009 — Silent Token Refresh

We are working on the **Veltrics Fleet & Vehicle Management Platform** (Python FastAPI Backend + Flutter Frontend).
Sprint 01 is active in Stage 01.

---

## 1. Project Context & Current State
- **Branch Strategy:** Active sprint branch (`sprint/sprint-01` or feature branch).
- **Backend Stack:** Python FastAPI + SQLAlchemy + SQLite (`sqlite:///./dev.db`) local-first.
- **Frontend Stack:** Flutter Client App (`src/frontend`).
- **Governance Rules:** Follow `.agents/AGENTS.md`.
- **Completed Tickets (22 / 27 in Sprint 01 — 81.5% Complete):**
  - `UC-001` (Auth Google One-Tap), `UC-002` (Auth Facebook Login), `UC-003` (Auth Email & Password Registration), `UC-004` (User Password Authentication), `UC-005` (Sign In - All Methods), `UC-006` (Forgot Password & Reset Flow), `UC-007` (Complete Profile Setup & Multi-Tenant Role-Based Authorization), `UC-008` (View and Edit Profile), `UC-014` (Auto-Create Personal Org), `UC-015` (View & Switch Active Organization), `UC-016` (Invite Team Member to Organization), `UC-024` (Add Vehicle), `UC-025` (View Vehicles), `UC-026` (Vehicle Detail), `UC-027` (Edit Vehicle), `UC-034` (View Maintenance Schedule), `UC-035` (Customize Maintenance Schedule Items), `UC-036` (Log Service Record), `UC-037` (View Service History), `UC-038` (Bulk Accept Maintenance Schedule), `UC-064` (Overview Fleet Dashboard KPI Metrics), `UC-118` (DB Seeding).

---

## 2. Target Ticket Specification: UC-009
- **Ticket ID:** `UC-009: Silent Token Refresh`
- **Linked Story:** `FS-AUTH-008`
- **Actor:** Registered User / System Background Interceptor
- **Trigger:** Access token expiration or pre-expiry timer threshold hit during active app usage.
- **Key Requirements:**
  1. Implement refresh token endpoint `POST /api/v1/auth/refresh` accepting valid refresh token and returning new access token & refresh token.
  2. Implement silent refresh interceptor/logic in Flutter client `AuthRepository` / HTTP client interceptor to transparently renew expired sessions without user intervention.
  3. Reject invalid or revoked refresh tokens with HTTP 401 Unauthorized.
- **Testing Requirements (`src/tests/unit/test_auth_uc009.py`):**
  - Test valid token refresh flow returning new access token.
  - Test expired or invalid refresh token rejection.

---

## 3. Mandatory Next Action
Please start by entering **Planning Mode**, inspecting the codebase as needed, and generating the `implementation_plan.md` artifact for **UC-009** for review and approval.
