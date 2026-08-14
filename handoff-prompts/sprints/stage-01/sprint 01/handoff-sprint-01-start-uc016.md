# Handoff Prompt: Execute Ticket UC-016 — Invite Team Member to Organization

We are working on the **Veltrics Fleet & Vehicle Management Platform** (Python FastAPI Backend + Flutter Frontend).
Sprint 01 is active in Stage 01.

---

## 1. Project Context & Current State
- **Branch Strategy:** Work on active sprint branch (`sprint/sprint-01` or feature branch).
- **Backend Stack:** Python FastAPI + SQLAlchemy + SQLite (`sqlite:///./dev.db`) local-first.
- **Frontend Stack:** Flutter Client App (`src/frontend`).
- **Governance Rules:** Follow `.agents/AGENTS.md`.
- **Completed Tickets (14 / 27 in Sprint 01 — 51.9% Complete):**
  - `UC-001` (Auth Google One-Tap), `UC-014` (Auto-Create Personal Org), `UC-015` (View & Switch Active Organization), `UC-024` (Add Vehicle), `UC-025` (View Vehicles), `UC-026` (Vehicle Detail), `UC-027` (Edit Vehicle), `UC-034` (View Maintenance Schedule), `UC-035` (Customize Maintenance Schedule Items), `UC-036` (Log Service Record), `UC-037` (View Service History), `UC-038` (Bulk Accept Maintenance Schedule), `UC-064` (Overview Fleet Dashboard KPI Metrics), `UC-118` (DB Seeding).
- **Available Database Entities:** `organizations`, `users`, `vehicles`, `vehicle_types`, `drivers`, `maintenance_schedules`, `service_records`.

---

## 2. Target Ticket Specification: UC-016
- **Ticket ID:** `UC-016: Invite Team Member to Organization`
- **Linked Story:** `FS-ORG-003`
- **Actor:** Owner / Admin
- **Trigger:** User submits invite form with recipient email and assigned role (`admin`, `manager`, `driver`, `viewer`).
- **Endpoints to Implement / Verify:**
  1. `POST /api/v1/organizations/{org_id}/invitations`: Create and record new invitation token.
     - Payload: `{ "email": "string", "role": "admin"|"manager"|"driver"|"viewer" }`
     - Header: `X-User-ID` (required).
  2. `GET /api/v1/organizations/{org_id}/invitations`: List pending organization invitations.
- **Frontend Requirements (`src/frontend`):**
  - Wire repository `inviteTeamMember()` and `getPendingInvitations()` calls in `OrganizationRepository`.
  - Provide invitation form UI widget / dialog in organization settings.
- **Testing Requirements (`src/tests/unit/test_organizations_uc016.py`):**
  - Test token generation (64-character token with 7-day TTL).
  - Test validation errors (invalid email, blank email).
  - Test duplicate invitation behavior (updating expiration).
  - Test tenant isolation boundaries (`HTTP 403 Forbidden` for non-owner/admin callers).

---

## 3. Mandatory Next Action
Please start by entering **Planning Mode**, inspecting the codebase as needed, and generating the `implementation_plan.md` artifact for **UC-016** for review and approval.
