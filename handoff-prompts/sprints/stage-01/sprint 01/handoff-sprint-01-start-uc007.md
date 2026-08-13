Created At: 2026-08-09T06:51:00Z
Completed At: 2026-08-09T06:51:00Z
File Path: `file:///e:/Non_Office/Dev_Space/vibe_skool/veltrics/handoff-prompts/sprints/stage-01/handoff-sprint-01-start-uc007.md`

# Handoff Prompt: Execute Ticket UC-007 — Complete Profile Setup / Role-Based Authorization

We are working on the **Veltrics Fleet & Vehicle Management Platform** (Python FastAPI Backend + Flutter Frontend).
Sprint 01 is active in Stage 01.

---

## 1. Project Context & Current State
- **Branch Strategy:** Active sprint branch (`sprint/sprint-01` or feature branch).
- **Backend Stack:** Python FastAPI + SQLAlchemy + SQLite (`sqlite:///./dev.db`) local-first.
- **Frontend Stack:** Flutter Client App (`src/frontend`).
- **Governance Rules:** Follow `.agents/AGENTS.md`.
- **Completed Tickets (20 / 27 in Sprint 01 — 74.1% Complete):**
  - `UC-001` (Auth Google One-Tap), `UC-002` (Auth Facebook Login), `UC-003` (Auth Email & Password Registration), `UC-004` (User Password Authentication & Session Initiation), `UC-005` (Sign In - All Methods), `UC-006` (Forgot Password & Reset Flow), `UC-014` (Auto-Create Personal Org), `UC-015` (View & Switch Active Organization), `UC-016` (Invite Team Member to Organization), `UC-024` (Add Vehicle), `UC-025` (View Vehicles), `UC-026` (Vehicle Detail), `UC-027` (Edit Vehicle), `UC-034` (View Maintenance Schedule), `UC-035` (Customize Maintenance Schedule Items), `UC-036` (Log Service Record), `UC-037` (View Service History), `UC-038` (Bulk Accept Maintenance Schedule), `UC-064` (Overview Fleet Dashboard KPI Metrics), `UC-118` (DB Seeding).

---

## 2. Target Ticket Specification: UC-007
- **Ticket ID:** `UC-007: Complete Profile Setup & Multi-Tenant Role-Based Authorization`
- **Linked Story:** `FS-AUTH-006`
- **Actor:** Authenticated User
- **Trigger:** User completes profile details or performs tenant-scoped requests.
- **Key Requirements:**
  1. Complete User Profile setup (full name, phone, job role/avatar).
  2. Implement multi-tenant role-based authorization dependency (`get_current_user` / role verifier) in FastAPI.
- **Testing Requirements (`src/tests/unit/test_auth_uc007.py`):**
  - Test profile completion / updates.
  - Test tenant boundary authorization & role checks (Owner/Admin/Manager/Driver/Viewer).

---

## 3. Mandatory Next Action
Please start by entering **Planning Mode**, inspecting the codebase as needed, and generating the `implementation_plan.md` artifact for **UC-007** for review and approval.
