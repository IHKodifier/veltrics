# Handoff Prompt: Execute Ticket UC-064 — Overview Fleet Dashboard KPI Metrics Render

We are working on the **Veltrics Fleet & Vehicle Management Platform** (Python FastAPI Backend + Flutter Frontend).
Sprint 01 is active in Stage 01.

---

## 1. Project Context & Current State
- **Branch Strategy:** Work on active sprint branch (`sprint/sprint-01` or feature branch).
- **Backend Stack:** Python FastAPI + SQLAlchemy + SQLite (`sqlite:///./dev.db`) local-first.
- **Frontend Stack:** Flutter Client App (`src/frontend`).
- **Governance Rules:** Follow `.agents/AGENTS.md`.
- **Completed Tickets (7 / 27 in Sprint 01):**
  - `UC-001` (Auth), `UC-024` (Add Vehicle), `UC-025` (View Vehicles), `UC-026` (Vehicle Detail), `UC-027` (Edit Vehicle), `UC-034` (Maintenance Schedules & Logging), `UC-118` (DB Seeding).
- **Available Database Entities:** `organizations`, `users`, `vehicles`, `vehicle_types`, `drivers`, `maintenance_schedules`, `service_records`.

---

## 2. Target Ticket Specification: UC-064
- **Ticket ID:** `UC-064: Overview Fleet Dashboard KPI Metrics Render`
- **Linked Story:** `FS-DASH-001`
- **Actor:** User (Consumer / Fleet Manager)
- **Trigger:** User opens app home tab (`SCR-DASH-001`).
- **Endpoint to Implement:** `GET /api/v1/dashboard/summary`
- **Backend KPI Requirements:**
  1. `total_vehicles` (Count of active non-deleted vehicles in organization).
  2. `total_drivers` (Count of drivers assigned/active in organization).
  3. `monthly_total_cost` (Sum of `total_cost` in `service_records` for the current month).
  4. `upcoming_maintenance_count` (Count of `maintenance_schedules` due within 7 days or within 500 km of `current_odometer_km`).
  5. `overdue_maintenance_count` (Count of `maintenance_schedules` where `current_odometer_km > next_due_km` or `next_due_date < today`).
  6. Empty state: Returns 0 stats when 0 vehicles exist so client can render "Add your first vehicle" onboarding card.
- **Frontend Requirements (`src/frontend`):**
  1. Create `dashboard_model.dart` and `dashboard_repository.dart`.
  2. Build `dashboard_screen.dart` with KPI metric summary cards (Total Vehicles, Monthly Expenses, Overdue Alerts, Active Drivers).
  3. Support zero-vehicle empty state with an onboarding card button navigating to `AddVehicleScreen`.
  4. Pull-to-refresh integration.
- **Testing Requirements (`src/tests/unit/test_dashboard_uc064.py`):**
  1. Test `GET /api/v1/dashboard/summary` for accurate metric calculations.
  2. Test tenant isolation (requests with another org ID return only that tenant's summary).
  3. Test empty organization zero-metrics behavior.

---

## 3. Mandatory Next Action
Please start by entering **Planning Mode**, inspecting the codebase as needed, and generating the `implementation_plan.md` artifact for **UC-064** for my review and approval.
