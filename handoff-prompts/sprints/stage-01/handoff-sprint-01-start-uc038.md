# Handoff Prompt: Execute Ticket UC-038 — Bulk Accept Maintenance Schedule

We are working on the **Veltrics Fleet & Vehicle Management Platform** (Python FastAPI Backend + Flutter Frontend).
Sprint 01 is active in Stage 01.

---

## 1. Project Context & Current State
- **Branch Strategy:** Work on active sprint branch (`sprint/sprint-01` or feature branch).
- **Backend Stack:** Python FastAPI + SQLAlchemy + SQLite (`sqlite:///./dev.db`) local-first.
- **Frontend Stack:** Flutter Client App (`src/frontend`).
- **Governance Rules:** Follow `.agents/AGENTS.md`.
- **Completed Tickets (11 / 27 in Sprint 01):**
  - `UC-001` (Auth Google One-Tap), `UC-024` (Add Vehicle), `UC-025` (View Vehicles), `UC-026` (Vehicle Detail), `UC-027` (Edit Vehicle), `UC-034` (View Maintenance Schedule), `UC-035` (Customize Maintenance Schedule Items), `UC-036` (Log Service Record), `UC-037` (View Service History), `UC-064` (Overview Fleet Dashboard KPI Metrics), `UC-118` (DB Seeding).
- **Available Database Entities:** `organizations`, `users`, `vehicles`, `vehicle_types`, `drivers`, `maintenance_schedules`, `service_records`.

---

## 2. Target Ticket Specification: UC-038
- **Ticket ID:** `UC-038: Bulk Accept Maintenance Schedule`
- **Linked Story:** `FS-MAINT-004`
- **Actor:** User (Consumer / Fleet Manager)
- **Trigger:** User bulk-acknowledges or confirms pre-populated default maintenance schedules for a vehicle.
- **Endpoints to Implement / Verify:**
  1. `POST /api/v1/maintenance/schedules/bulk-accept`: Bulk accept/activate default schedules for a vehicle.
     - Payload: `{ "vehicle_id": "string", "schedule_ids": ["string"] }`
     - Header: `X-Organization-ID` (required).
- **Frontend Requirements (`src/frontend`):**
  - Wire repository `bulkAcceptSchedules()` call.
  - Provide batch selection/acceptance UI component.
- **Testing Requirements (`src/tests/unit/test_maintenance_uc038.py`):**
  - Test bulk acceptance success and database state updates.
  - Test tenant isolation boundaries.

---

## 3. Mandatory Next Action
Please start by entering **Planning Mode**, inspecting the codebase as needed, and generating the `implementation_plan.md` artifact for **UC-038** for review and approval.
