# Handoff Prompt: Execute Ticket UC-036 — Log Service Record

We are working on the **Veltrics Fleet & Vehicle Management Platform** (Python FastAPI Backend + Flutter Frontend).
Sprint 01 is active in Stage 01.

---

## 1. Project Context & Current State
- **Branch Strategy:** Work on active sprint branch (`sprint/sprint-01` or feature branch).
- **Backend Stack:** Python FastAPI + SQLAlchemy + SQLite (`sqlite:///./dev.db`) local-first.
- **Frontend Stack:** Flutter Client App (`src/frontend`).
- **Governance Rules:** Follow `.agents/AGENTS.md`.
- **Completed Tickets (9 / 27 in Sprint 01):**
  - `UC-001` (Auth Google One-Tap), `UC-024` (Add Vehicle), `UC-025` (View Vehicles), `UC-026` (Vehicle Detail), `UC-027` (Edit Vehicle), `UC-034` (View Maintenance Schedule), `UC-035` (Customize Maintenance Schedule Items), `UC-064` (Overview Fleet Dashboard KPI Metrics), `UC-118` (DB Seeding).
- **Available Database Entities:** `organizations`, `users`, `vehicles`, `vehicle_types`, `drivers`, `maintenance_schedules`, `service_records`.

---

## 2. Target Ticket Specification: UC-036
- **Ticket ID:** `UC-036: Log Service Record`
- **Linked Story:** `FS-MAINT-003`
- **Actor:** User (Consumer / Fleet Manager / Driver)
- **Trigger:** User completes a maintenance task or routine service and logs the record via the UI.
- **Endpoints to Implement / Verify:**
  1. `POST /api/v1/maintenance`: Log service record.
     - Payload: `vehicle_id`, `maintenance_schedule_id` (optional), `service_type`, `cost`, `service_date`, `odometer_reading`, `service_provider_name` (optional), `notes` (optional), `photo_url` (optional).
     - Behavior:
       - Creates `service_records` entry in DB.
       - Auto-updates vehicle's `current_odometer_km` if `odometer_reading > vehicle.current_odometer_km`.
       - Resets matching `maintenance_schedules` item (`last_performed_km = odometer_reading`, `last_performed_date = service_date`, `next_due_km = odometer_reading + interval_km`, `next_due_date = service_date + interval_days`).
- **Backend Validation & Constraints:**
  - Header: `X-Organization-ID` (required).
  - Validation: `cost >= 0`, `odometer_reading >= 0`, non-empty `service_type`.
  - Multi-tenant isolation: verify vehicle belongs to caller's active organization.
- **Frontend Requirements (`src/frontend`):**
  - Verify and wire `LogMaintenanceScreen` with full form validation, date picker, dropdown/custom task entry, and cost inputs.
  - Call `_repository.logMaintenance()` with proper error feedback and return back to schedule screen / vehicle detail with automatic refresh.
- **Testing Requirements (`src/tests/unit/test_maintenance_uc036.py`):**
  - Test service record logging success.
  - Test auto-updating vehicle current odometer.
  - Test resetting maintenance schedule due targets.
  - Test validation error handling (negative cost / negative odometer).
  - Test tenant isolation boundary checks.

---

## 3. Mandatory Next Action
Please start by entering **Planning Mode**, inspecting the codebase as needed, and generating the `implementation_plan.md` artifact for **UC-036** for my review and approval.
