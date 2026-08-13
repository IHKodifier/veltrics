# Handoff Prompt: Execute Ticket UC-035 — Customize Maintenance Schedule Items

We are working on the **Veltrics Fleet & Vehicle Management Platform** (Python FastAPI Backend + Flutter Frontend).
Sprint 01 is active in Stage 01.

---

## 1. Project Context & Current State
- **Branch Strategy:** Work on active sprint branch (`sprint/sprint-01` or feature branch).
- **Backend Stack:** Python FastAPI + SQLAlchemy + SQLite (`sqlite:///./dev.db`) local-first.
- **Frontend Stack:** Flutter Client App (`src/frontend`).
- **Governance Rules:** Follow `.agents/AGENTS.md`.
- **Completed Tickets (8 / 27 in Sprint 01):**
  - `UC-001` (Auth Google One-Tap), `UC-024` (Add Vehicle), `UC-025` (View Vehicles), `UC-026` (Vehicle Detail), `UC-027` (Edit Vehicle), `UC-034` (View Pre-Populated Maintenance Schedule), `UC-064` (Overview Fleet Dashboard KPI Metrics), `UC-118` (DB Seeding).
- **Available Database Entities:** `organizations`, `users`, `vehicles`, `vehicle_types`, `drivers`, `maintenance_schedules`, `service_records`.

---

## 2. Target Ticket Specification: UC-035
- **Ticket ID:** `UC-035: Customize Maintenance Schedule Items`
- **Linked Story:** `FS-MAINT-002`
- **Actor:** User (Consumer / Fleet Manager)
- **Trigger:** User views maintenance schedule for a vehicle (`UC-034`) and clicks "Add Custom Task", edits task interval, toggles task active state, or soft-deletes a task.
- **Endpoints to Implement:**
  1. `POST /api/v1/maintenance/schedules`: Create custom maintenance schedule task.
     - Payload: `vehicle_id`, `task_name`, `interval_km`, `interval_days`, `last_performed_km` (optional), `last_performed_date` (optional).
     - Calculates `next_due_km` (`current_odometer_km + interval_km`) and `next_due_date` (`today + interval_days`).
  2. `PATCH /api/v1/maintenance/schedules/{schedule_id}`: Update task interval parameters or `is_active` state.
     - Payload: `task_name` (optional), `interval_km` (optional), `interval_days` (optional), `is_active` (optional).
     - Recalculates `next_due_km` and `next_due_date` when intervals change.
  3. `DELETE /api/v1/maintenance/schedules/{schedule_id}`: Soft-delete schedule item (`deleted_at = utc_now()`).
- **Backend Validation & Constraints:**
  - Header: `X-Organization-ID` (required).
  - Validation: `interval_km > 0`, `interval_days > 0`, non-empty `task_name`.
  - Multi-tenant isolation: verify schedule and vehicle belong to active organization.
- **Frontend Requirements (`src/frontend`):**
  - Update `maintenance_model.dart` & `maintenance_repository.dart` to support schedule mutation methods (`createSchedule`, `updateSchedule`, `deleteSchedule`).
  - Build UI dialog / modal in maintenance schedule screen to:
    - Add a custom maintenance task item.
    - Edit existing interval values.
    - Toggle task enabled/disabled state (`is_active`).
    - Delete task item with confirmation modal.
- **Testing Requirements (`src/tests/unit/test_maintenance_uc035.py`):**
  - Test custom schedule item creation.
  - Test schedule interval update & recalculated due targets.
  - Test soft-deletion of schedule task (`deleted_at IS NOT NULL`).
  - Test tenant isolation & invalid input validation (422 / 400).

---

## 3. Mandatory Next Action
Please start by entering **Planning Mode**, inspecting the codebase as needed, and generating the `implementation_plan.md` artifact for **UC-035** for my review and approval.
