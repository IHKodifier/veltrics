# Handoff Prompt — Sprint 01 (Midway UC-026: View Vehicle Detailed Overview)

> **Context:** This prompt is for resuming execution of **Sprint 01** in a new chat session. The user is midway through implementing **`UC-026: View Vehicle Detailed Overview`** following the approved implementation plan:
> [implementation_plan.md](file:///C:/Users/Ihtiram/.gemini/antigravity-ide/brain/b28f8a17-9b07-4b43-b38d-cea7630a56e5/implementation_plan.md)

---

## 1. Executive Summary & Repository State

- **Active Git Branch:** `sprint/sprint-01` (checked out from `dev`). Remote `origin` linked to `https://github.com/IHKodifier/veltrics.git`.
- **Completed Tickets (4 / 27 — 14.8%):**
  1. `UC-001`: Sign Up with Google One-Tap & Registration API (Passes `test_auth_uc001.py`)
  2. `UC-118`: Database Migration & Schema Seeding Infrastructure (Passes `test_db_seeding_uc118.py`)
  3. `UC-024`: Register New Vehicle with Typeahead Lookup & Pakistani License Plates (Passes `test_vehicles_uc024.py`)
  4. `UC-025`: View Fleet Vehicle Directory & Filter (Passes `test_vehicles_uc025.py`)
- **Active Backend Server:** Running locally via `.\scripts\start_backend.ps1` on `http://127.0.0.1:8000` (`http://localhost:8000`).
- **Active Flutter Web App:** Running locally on `http://localhost:58827` (or similar active port).

---

## 2. Work Completed for `UC-026` in Current Chat

1. **Backend Schemas Updated (`src/backend/app/schemas/vehicle.py` & `__init__.py`):**
   - Added `VehicleStatusUpdateRequest` DTO (`status`).
   - Added `VehicleDetailResponse` DTO (extending `VehicleResponse` with `assigned_driver_name`, `assigned_driver_phone`, `active_schedules_count`, `total_service_records_count`, `total_expenses_cost`).

2. **Backend Endpoints Added (`src/backend/app/api/v1/vehicles.py`):**
   - `GET /api/v1/vehicles/{vehicle_id}?organization_id=...`: Verifies vehicle existence and tenant scoping (`HTTP 403 Forbidden` if wrong org, `HTTP 404 Not Found` if missing), returning comprehensive detailed vehicle overview.
   - `PATCH /api/v1/vehicles/{vehicle_id}/status?organization_id=...`: Updates status (`ACTIVE`, `MAINTENANCE`, `INACTIVE`).

3. **Automated Pytest Unit Test Suite Created (`src/tests/unit/test_vehicles_uc026.py`):**
   - 4 test cases verifying detail retrieval, 404 error handling, 403 tenant isolation, and status updates.
   - Updated `src/tests/run_and_report.py` test runner.

---

## 3. Remaining Tasks for `UC-026` to Complete in New Chat

1. **Update `VehicleRepository` (`src/frontend/lib/features/vehicle/data/vehicle_repository.dart`):**
   - Implement `Future<VehicleDetailModel> getVehicleDetail({required String vehicleId, required String organizationId})`.
   - Implement `Future<VehicleModel> updateVehicleStatus({required String vehicleId, required String organizationId, required String status})`.

2. **Create `VehicleDetailScreen` (`src/frontend/lib/features/vehicle/presentation/screens/vehicle_detail_screen.dart`):**
   - Build complete UI containing:
     - Header banner with vehicle make/model, photo/icon, and status pill.
     - Pakistani License Plate badge card (`PUNJAB | AFR-024` / `SINDH | LEA-1234`).
     - Key Metrics Grid: Current Odometer (km), Fuel Type, Initial Odometer, Year, Registration Province.
     - Status Action Bar: Quick buttons to mark `Active`, send to `Maintenance`, or `Deactivate`.
     - Quick Action Shortcut cards: Maintenance Schedule, Log Service Record, Service History.

3. **Update `VehicleListScreen` (`src/frontend/lib/features/vehicle/presentation/screens/vehicle_list_screen.dart`):**
   - Connect vehicle card tap callback to navigate to `VehicleDetailScreen`.

4. **Verify Implementation:**
   - Execute `python src/tests/run_and_report.py` (Pytest backend test suite).
   - Execute `dart-mcp-server/analyze_files` on `src/frontend` (Dart static analysis).

5. **Update Sprint 1 Tracker (`trackers/stage-01/sprints/07.01.01-tracker.md`):**
   - Mark `UC-026` as `Completed` with `PASS (test_vehicles_uc026.py)`.

---

## 4. Immediate Prompt to Copy-Paste into New Chat

```text
Hi! I am resuming work on Veltrics Sprint 01 on branch `sprint/sprint-01`.

We are midway through implementing ticket **`UC-026: View Vehicle Detailed Overview`**.
Please read:
- Governance rules: `.agents/AGENTS.md`
- Master Tracker: `trackers/stage-01/sprints/07.01.01-tracker.md`
- Handoff file: `handoff-prompts/sprints/stage-01/handoff-sprint-01-mid-uc026.md`
- Approved Plan: `C:\Users\Ihtiram\.gemini\antigravity-ide\brain\b28f8a17-9b07-4b43-b38d-cea7630a56e5\implementation_plan.md`

Backend endpoints and Pytest unit tests for UC-026 are already completed. Please complete the frontend steps:
1. Update `VehicleRepository` in `src/frontend/lib/features/vehicle/data/vehicle_repository.dart`.
2. Create `VehicleDetailScreen` in `src/frontend/lib/features/vehicle/presentation/screens/vehicle_detail_screen.dart`.
3. Connect card tap in `VehicleListScreen` to open `VehicleDetailScreen`.
4. Run verification tests and update the Sprint 01 tracker!
```
