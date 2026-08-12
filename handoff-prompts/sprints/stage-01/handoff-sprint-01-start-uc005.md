# Handoff Prompt: Execute Ticket UC-005 — Sign In (All Methods)

We are working on the **Veltrics Fleet & Vehicle Management Platform** (Python FastAPI Backend + Flutter Frontend).
Sprint 01 is active in Stage 01.

---

## 1. Project Context & Current State
- **Branch Strategy:** Active sprint branch (`sprint/sprint-01` or feature branch).
- **Backend Stack:** Python FastAPI + SQLAlchemy + SQLite (`sqlite:///./dev.db`) local-first.
- **Frontend Stack:** Flutter Client App (`src/frontend`).
- **Governance Rules:** Follow `.agents/AGENTS.md`.
- **Completed Tickets (18 / 27 in Sprint 01 — 66.7% Complete):**
  - `UC-001` (Auth Google One-Tap), `UC-002` (Auth Facebook Login), `UC-003` (Auth Email & Password Registration), `UC-004` (User Password Authentication & Session Initiation), `UC-014` (Auto-Create Personal Org), `UC-015` (View & Switch Active Organization), `UC-016` (Invite Team Member to Organization), `UC-024` (Add Vehicle), `UC-025` (View Vehicles), `UC-026` (Vehicle Detail), `UC-027` (Edit Vehicle), `UC-034` (View Maintenance Schedule), `UC-035` (Customize Maintenance Schedule Items), `UC-036` (Log Service Record), `UC-037` (View Service History), `UC-038` (Bulk Accept Maintenance Schedule), `UC-064` (Overview Fleet Dashboard KPI Metrics), `UC-118` (DB Seeding).

---

## 2. Target Ticket Specification: UC-005
- **Ticket ID:** `UC-005: Sign In (All Methods)`
- **Linked Story:** `FS-AUTH-004`
- **Actor:** Existing / Returning User
- **Trigger:** User initiates sign-in using Google, Facebook, or Email/Password on login UI.
- **Endpoints to Implement / Verify:**
  1. Unified sign-in routing across OAuth and Email providers.
  2. Session validation and token issuance for existing user accounts.
- **Frontend Requirements (`src/frontend`):**
  - Integrate unified session restoration and authentication flow in `LoginScreen` and `AuthRepository`.
- **Testing Requirements (`src/tests/unit/test_auth_uc005.py`):**
  - Test sign in with existing OAuth and Email accounts.
  - Assert invalid sessions or non-existent accounts handled appropriately.

---

## 3. Mandatory Next Action
Please start by entering **Planning Mode**, inspecting the codebase as needed, and generating the `implementation_plan.md` artifact for **UC-005** for review and approval.
