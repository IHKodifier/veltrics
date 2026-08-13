# Handoff Prompt — Sprint 01 (Starting UC-034: Log Completed Maintenance Task & View Schedule)

> **Context:** This prompt is for starting implementation of **`UC-034: Log Completed Maintenance Task & View Schedule`** on **Sprint 01** in a new chat session.

---

## 1. Executive Summary & Repository State

- **Active Git Branch:** `sprint/sprint-01` (checked out from `dev`). Remote `origin` linked to `https://github.com/IHKodifier/veltrics.git`.
- **Completed Tickets (6 / 27 — 22.2%):**
  1. `UC-001`: Sign Up with Google One-Tap & Registration API (Passes `test_auth_uc001.py`)
  2. `UC-118`: Database Migration & Schema Seeding Infrastructure (Passes `test_db_seeding_uc118.py`)
  3. `UC-024`: Register New Vehicle with Typeahead Lookup & Pakistani License Plates (Passes `test_vehicles_uc024.py`)
  4. `UC-025`: View Fleet Vehicle Directory & Filter (Passes `test_vehicles_uc025.py`)
  5. `UC-026`: View Vehicle Detailed Overview (Passes `test_vehicles_uc026.py` & static analysis `0 errors`)
  6. `UC-027`: Update Vehicle Metadata & Specifications (Passes `test_vehicles_uc027.py` & static analysis `0 errors`)
- **Active Backend Server:** Running locally via `.\scripts\start_backend.ps1` on `http://127.0.0.1:8000`.
- **Active Flutter Client:** Scaffolding in `src/frontend`.

---

## 2. Goal & Backlog Focus for New Chat: `UC-034`

**Ticket Title:** `UC-034: Log Completed Maintenance Task`  
**Spec Document:** [06a-use-case-tickets.md](file:///e:/Non_Office/Dev_Space/vibe_skool/veltrics/product-specs/06a-use-case-tickets.md) (Lines 1266–1310)

### Key Tasks for UC-034:
1. **Backend Implementation (`src/backend`):**
   - Implement `GET /api/v1/maintenance/schedules` for retrieving pre-populated maintenance items by `vehicle_id`.
   - Implement `POST /api/v1/maintenance` accepting maintenance log payload (service_type, cost, service_date, odometer_reading, service_provider_name, notes, photo_url).
   - Enforce automatic vehicle odometer update if logged odometer > current odometer.
   - Enforce maintenance schedule timer/odometer reset upon service log submission.
2. **Automated Unit Tests (`src/tests/unit/test_maintenance_uc034.py`):**
   - Test pre-populated maintenance schedule query.
   - Test logging maintenance task, odometer update, and schedule reset logic.
   - Test negative cost validation (`HTTP 422`).
3. **Flutter Client Implementation (`src/frontend`):**
   - Create `MaintenanceRepository` (`src/frontend/lib/features/maintenance/data/maintenance_repository.dart`).
   - Create `LogMaintenanceScreen` or modal dialog (`src/frontend/lib/features/maintenance/presentation/screens/log_maintenance_screen.dart`).
   - Add "Log Service" button in `VehicleDetailScreen`.
4. **Verification & Tracker Updates:**
   - Execute backend test runner (`python src/tests/run_and_report.py`).
   - Run Dart static analysis (`dart-mcp-server/analyze_files`).
   - Update `07.01.01-tracker.md`, `07.01-tracker.md`, and `07-big-picture-tracker.md`.

---

## 3. Copy-Paste Prompt for New Chat

```text
Hi! I am resuming work on Veltrics Sprint 01 on branch `sprint/sprint-01`.

We are starting implementation of ticket **`UC-034: Log Completed Maintenance Task & View Schedule`**.
Please read:
- Governance rules: `.agents/AGENTS.md`
- Master Tracker: `trackers/stage-01/sprints/07.01.01-tracker.md`
- Use Case Specs: `product-specs/06a-use-case-tickets.md` (UC-034)
- Handoff file: `handoff-prompts/sprints/stage-01/handoff-sprint-01-start-uc034.md`

Please draft an implementation plan for UC-034 and present it for approval before building the backend endpoints, unit tests, and Flutter maintenance logging UI!
```
