# Handoff Prompt — Sprint 01 (Starting UC-027: Update Vehicle Metadata & Specifications)

> **Context:** This prompt is for starting implementation of **`UC-027: Update Vehicle Metadata & Specifications`** on **Sprint 01** in a new chat session.

---

## 1. Executive Summary & Repository State

- **Active Git Branch:** `sprint/sprint-01` (checked out from `dev`). Remote `origin` linked to `https://github.com/IHKodifier/veltrics.git`.
- **Completed Tickets (5 / 27 — 18.5%):**
  1. `UC-001`: Sign Up with Google One-Tap & Registration API (Passes `test_auth_uc001.py`)
  2. `UC-118`: Database Migration & Schema Seeding Infrastructure (Passes `test_db_seeding_uc118.py`)
  3. `UC-024`: Register New Vehicle with Typeahead Lookup & Pakistani License Plates (Passes `test_vehicles_uc024.py`)
  4. `UC-025`: View Fleet Vehicle Directory & Filter (Passes `test_vehicles_uc025.py`)
  5. `UC-026`: View Vehicle Detailed Overview (Passes `test_vehicles_uc026.py` & static analysis `0 errors`)
- **Active Backend Server:** Running locally via `.\scripts\start_backend.ps1` on `http://127.0.0.1:8000`.
- **Active Flutter Client:** Scaffolding in `src/frontend`.

---

## 2. Goal & Backlog Focus for New Chat: `UC-027`

**Ticket Title:** `UC-027: Update Vehicle Metadata & Specifications`  
**Spec Document:** [06a-use-case-tickets.md](file:///e:/Non_Office/Dev_Space/vibe_skool/veltrics/product-specs/06a-use-case-tickets.md) (Lines 1006–1040)

### Key Tasks for UC-027:
1. **Backend Implementation (`src/backend`):**
   - Implement `PATCH /api/v1/vehicles/{vehicle_id}` accepting `VehicleUpdateRequest` payload (license_plate, registration_province, current_odometer_km, custom_specs dictionary).
   - Validate tenant ownership (`HTTP 403 Forbidden` if wrong organization).
   - Enforce audit log entry if manual odometer adjustment discrepancy > 500 km.
2. **Automated Unit Tests (`src/tests/unit/test_vehicles_uc027.py`):**
   - Test successful metadata update.
   - Test tenant isolation (`HTTP 403`).
   - Test custom_specs update & validation.
3. **Flutter Client Implementation (`src/frontend`):**
   - Add `updateVehicle` in `VehicleRepository` (`src/frontend/lib/features/vehicle/data/vehicle_repository.dart`).
   - Create `EditVehicleScreen` (`src/frontend/lib/features/vehicle/presentation/screens/edit_vehicle_screen.dart`) or modal dialog with pre-populated form fields.
   - Add "Edit Vehicle" button in `VehicleDetailScreen` header.
4. **Verification & Tracker Updates:**
   - Execute backend test runner (`python src/tests/run_and_report.py`).
   - Run Dart static analysis (`dart-mcp-server/analyze_files`).
   - Update `07.01.01-tracker.md`, `07.01-tracker.md`, and `07-big-picture-tracker.md`.

---

## 3. Copy-Paste Prompt for New Chat

```text
Hi! I am resuming work on Veltrics Sprint 01 on branch `sprint/sprint-01`.

We are starting implementation of ticket **`UC-027: Update Vehicle Metadata & Specifications`**.
Please read:
- Governance rules: `.agents/AGENTS.md`
- Master Tracker: `trackers/stage-01/sprints/07.01.01-tracker.md`
- Use Case Specs: `product-specs/06a-use-case-tickets.md` (UC-027)
- Handoff file: `handoff-prompts/sprints/stage-01/handoff-sprint-01-start-uc027.md`

Please draft an implementation plan for UC-027 and present it for approval before building the backend endpoint, unit tests, and Flutter edit screen!
```
