# Handoff Prompt: Execute Ticket UC-046 — Log Fuel Fill-Up Entry

We are transitioning to **Sprint 02 (Fuel Logging, Trip Management, Expense Tracking & Push Notifications)** for the **Veltrics Fleet & Vehicle Management Platform**.

---

## 1. Project Context & Current State
- **Branch Strategy:** Active sprint branch (`sprint/sprint-02` checked out from `dev`).
- **Backend Stack:** Python FastAPI + SQLAlchemy + SQLite (`sqlite:///./dev.db`) local-first.
- **Frontend Stack:** Flutter Client App (`src/frontend`).
- **Governance Rules:** Follow `.agents/AGENTS.md`.
- **Sprint 01 Completed:** 27 / 27 Tickets Completed (100.0%).
- **Stage 01 Overall Progress:** 27 / 122 Tickets Completed (22.1%).

---

## 2. Target Ticket Specification: UC-046
- **Ticket ID:** `UC-046: Log Fuel Fill-Up Entry`
- **Linked Story:** `FS-FUEL-001`
- **Actor:** Driver / Consumer / Fleet Manager
- **Trigger:** User submits fuel log entry form on `SCR-FUEL-002`.
- **Key Requirements:**
  1. Implement backend endpoint `POST /api/v1/fuel` accepting fuel fill-up details (`vehicle_id`, `odometer`, `fuel_amount_liters`, `cost_amount`, `fuel_type`, `fill_date`, `is_full_tank`, optional `receipt_image_url`).
  2. Validate that `odometer` is greater than or equal to vehicle's current odometer reading (reject with `HTTP 400 Bad Request` if lower).
  3. Automatically update `vehicles.current_odometer` if the logged odometer reading exceeds current value.
  4. Automatically create a linked expense record under category `FUEL`.
  5. Build Flutter UI screens/forms for fuel logging and `FuelRepository`.
- **Testing Requirements (`src/tests/unit/test_fuel_uc046.py`):**
  - Test successful fuel log creation & vehicle odometer update.
  - Test automatic linked expense record generation under category `FUEL`.
  - Test rejection of odometer readings lower than current vehicle odometer.

---

## 3. Mandatory Next Action
Please start by entering **Planning Mode**, inspecting the codebase as needed, and generating the `implementation_plan.md` artifact for **UC-046** for review and approval.
