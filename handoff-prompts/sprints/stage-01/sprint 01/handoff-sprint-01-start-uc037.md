# Handoff Prompt: Execute Ticket UC-037 — View Service History

We are working on the **Veltrics Fleet & Vehicle Management Platform** (Python FastAPI Backend + Flutter Frontend).
Sprint 01 is active in Stage 01.

---

## 1. Project Context & Current State
- **Branch Strategy:** Work on active sprint branch (`sprint/sprint-01` or feature branch).
- **Backend Stack:** Python FastAPI + SQLAlchemy + SQLite (`sqlite:///./dev.db`) local-first.
- **Frontend Stack:** Flutter Client App (`src/frontend`).
- **Governance Rules:** Follow `.agents/AGENTS.md`.
- **Completed Tickets (10 / 27 in Sprint 01):**
  - `UC-001` (Auth Google One-Tap), `UC-024` (Add Vehicle), `UC-025` (View Vehicles), `UC-026` (Vehicle Detail), `UC-027` (Edit Vehicle), `UC-034` (View Maintenance Schedule), `UC-035` (Customize Maintenance Schedule Items), `UC-036` (Log Service Record), `UC-064` (Overview Fleet Dashboard KPI Metrics), `UC-118` (DB Seeding).
- **Available Database Entities:** `organizations`, `users`, `vehicles`, `vehicle_types`, `drivers`, `maintenance_schedules`, `service_records`.

---

## 2. Target Ticket Specification: UC-037
- **Ticket ID:** `UC-037: View Service History`
- **Linked Story:** `FS-MAINT-003`
- **Actor:** User (Consumer / Fleet Manager / Driver)
- **Trigger:** User opens maintenance service history tab or views historical maintenance records for a vehicle.
- **Endpoints to Implement / Verify:**
  1. `GET /api/v1/maintenance/records`: Retrieve list of service records for a vehicle.
     - Query Parameters: `vehicle_id` (required), optional `limit`, optional `offset`.
     - Behavior: Returns list of `ServiceRecordResponse` sorted by `service_date` descending.
- **Backend Validation & Constraints:**
  - Header: `X-Organization-ID` (required).
  - Multi-tenant isolation: verify vehicle belongs to caller's active organization.
- **Frontend Requirements (`src/frontend`):**
  - Implement/verify `ServiceHistoryScreen` displaying chronological service records, cost summary, provider names, and notes.
  - Wire repository `getServiceHistory()` call.
- **Testing Requirements (`src/tests/unit/test_maintenance_uc037.py`):**
  - Test service history retrieval success and sorting order.
  - Test filtering by vehicle ID.
  - Test tenant isolation boundary checks.

---

## 3. Mandatory Next Action
Please start by entering **Planning Mode**, inspecting the codebase as needed, and generating the `implementation_plan.md` artifact for **UC-037** for my review and approval.
