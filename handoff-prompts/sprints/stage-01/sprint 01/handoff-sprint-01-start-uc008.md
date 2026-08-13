# Handoff Prompt: Execute Ticket UC-008 — View and Edit Profile

We are working on the **Veltrics Fleet & Vehicle Management Platform** (Python FastAPI Backend + Flutter Frontend).
Sprint 01 is active in Stage 01.

---

## 1. Project Context & Current State
- **Branch Strategy:** Active sprint branch (`sprint/sprint-01` or feature branch).
- **Backend Stack:** Python FastAPI + SQLAlchemy + SQLite (`sqlite:///./dev.db`) local-first.
- **Frontend Stack:** Flutter Client App (`src/frontend`).
- **Governance Rules:** Follow `.agents/AGENTS.md`.
- **Completed Tickets (21 / 27 in Sprint 01 — 77.8% Complete):**
  - `UC-001` (Auth Google One-Tap), `UC-002` (Auth Facebook Login), `UC-003` (Auth Email & Password Registration), `UC-004` (User Password Authentication), `UC-005` (Sign In - All Methods), `UC-006` (Forgot Password & Reset Flow), `UC-007` (Complete Profile Setup & Multi-Tenant Role-Based Authorization), `UC-014` (Auto-Create Personal Org), `UC-015` (View & Switch Active Organization), `UC-016` (Invite Team Member to Organization), `UC-024` (Add Vehicle), `UC-025` (View Vehicles), `UC-026` (Vehicle Detail), `UC-027` (Edit Vehicle), `UC-034` (View Maintenance Schedule), `UC-035` (Customize Maintenance Schedule Items), `UC-036` (Log Service Record), `UC-037` (View Service History), `UC-038` (Bulk Accept Maintenance Schedule), `UC-064` (Overview Fleet Dashboard KPI Metrics), `UC-118` (DB Seeding).

---

## 2. Target Ticket Specification: UC-008
- **Ticket ID:** `UC-008: View and Edit Profile`
- **Linked Story:** `FS-AUTH-007`
- **Actor:** Registered User
- **Trigger:** User taps "Profile & Settings" from navigation menu or app header.
- **Key Requirements:**
  1. Render Profile View screen showing current user details (Full Name, Email, Phone Number, City, Job Role, Avatar, Auth Provider, Organization Role).
  2. Provide Edit mode allowing profile field updates and avatar URL update.
  3. Wire frontend with `GET /api/v1/users/me` and `PATCH /api/v1/users/me`.
- **Testing Requirements (`src/tests/unit/test_auth_uc008.py`):**
  - Test viewing user profile details.
  - Test editing profile fields and persisting changes.

---

## 3. Mandatory Next Action
Please start by entering **Planning Mode**, inspecting the codebase as needed, and generating the `implementation_plan.md` artifact for **UC-008** for review and approval.
