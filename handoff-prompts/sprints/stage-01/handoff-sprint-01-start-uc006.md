Created At: 2026-08-09T05:41:00Z
Completed At: 2026-08-09T05:41:00Z
File Path: `file:///e:/Non_Office/Dev_Space/vibe_skool/veltrics/handoff-prompts/sprints/stage-01/handoff-sprint-01-start-uc006.md`

# Handoff Prompt: Execute Ticket UC-006 — Forgot Password & Reset Flow

We are working on the **Veltrics Fleet & Vehicle Management Platform** (Python FastAPI Backend + Flutter Frontend).
Sprint 01 is active in Stage 01.

---

## 1. Project Context & Current State
- **Branch Strategy:** Active sprint branch (`sprint/sprint-01` or feature branch).
- **Backend Stack:** Python FastAPI + SQLAlchemy + SQLite (`sqlite:///./dev.db`) local-first.
- **Frontend Stack:** Flutter Client App (`src/frontend`).
- **Governance Rules:** Follow `.agents/AGENTS.md`.
- **Completed Tickets (19 / 27 in Sprint 01 — 70.4% Complete):**
  - `UC-001` (Auth Google One-Tap), `UC-002` (Auth Facebook Login), `UC-003` (Auth Email & Password Registration), `UC-004` (User Password Authentication & Session Initiation), `UC-005` (Sign In - All Methods), `UC-014` (Auto-Create Personal Org), `UC-015` (View & Switch Active Organization), `UC-016` (Invite Team Member to Organization), `UC-024` (Add Vehicle), `UC-025` (View Vehicles), `UC-026` (Vehicle Detail), `UC-027` (Edit Vehicle), `UC-034` (View Maintenance Schedule), `UC-035` (Customize Maintenance Schedule Items), `UC-036` (Log Service Record), `UC-037` (View Service History), `UC-038` (Bulk Accept Maintenance Schedule), `UC-064` (Overview Fleet Dashboard KPI Metrics), `UC-118` (DB Seeding).

---

## 2. Target Ticket Specification: UC-006
- **Ticket ID:** `UC-006: Forgot Password & Reset Flow`
- **Linked Story:** `FS-AUTH-005`
- **Actor:** User who forgot their password
- **Trigger:** User clicks "Forgot Password?" link on sign-in UI.
- **Endpoints to Implement / Verify:**
  1. `POST /api/v1/auth/forgot-password` (Issues reset token / email trigger).
  2. `POST /api/v1/auth/reset-password` (Verifies token & updates password hash).
- **Testing Requirements (`src/tests/unit/test_auth_uc006.py`):**
  - Test requesting password reset email/token.
  - Test resetting password with valid token.
  - Assert invalid or expired tokens return appropriate error responses.

---

## 3. Mandatory Next Action
Please start by entering **Planning Mode**, inspecting the codebase as needed, and generating the `implementation_plan.md` artifact for **UC-006** for review and approval.
