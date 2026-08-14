# Handoff Prompt: Execute Ticket UC-047 — View Fuel Log History & Calculate Fuel Efficiency

We are continuing **Sprint 02 (Fuel Logging, Trip Management, Expense Tracking & Push Notifications)** for the **Veltrics Fleet & Vehicle Management Platform**.

---

## 1. Project Context & Current State
- **Branch Strategy:** Active sprint branch (`sprint/sprint-02` checked out from `dev` and pushed upstream).
- **Backend Stack:** Python FastAPI + SQLAlchemy + SQLite (`sqlite:///./dev.db`) local-first.
- **Frontend Stack:** Flutter Client App (`src/frontend`).
- **Governance Rules:** Follow `.agents/AGENTS.md`.
- **Completed Tickets:** UC-001 .. UC-016, UC-024 .. UC-027, UC-034 .. UC-038, UC-046, UC-064, UC-118 (28 / 122 Tickets Completed - 23.0%).
- **Active Sprint Progress:** Sprint 02 (1 / 24 Tickets Completed - 4.2%).

---

## 2. Target Ticket Specification: UC-047
- **Ticket ID:** `UC-047: View Fuel Log History & Calculate Fuel Efficiency`
- **Linked Story:** `FS-FUEL-002`, `FS-FUEL-003`
- **Actor:** Driver / Consumer / Fleet Manager / System
- **Trigger:** User opens Fuel Log History tab/screen (`SCR-FUEL-001`).
- **Key Requirements:**
  1. Backend endpoint `GET /api/v1/fuel` returning fuel log history records sorted by log date descending for a target vehicle or organization.
  2. Compute fuel efficiency (`calculated_efficiency_kpl = distance_km / quantity_liters`) on consecutive full-tank entries (`is_full_tank = True`).
  3. Flag potential fuel leak / theft alerts if fuel efficiency drops by more than 30% below the vehicle's historical baseline average.
  4. Flutter UI screen `SCR-FUEL-001` rendering fuel history list cards, distance deltas, km/L efficiency badges, and potential fuel leak alerts.
- **Testing Requirements (`src/tests/unit/test_fuel_uc047.py`):**
  - Test retrieving fuel log history via `GET /api/v1/fuel`.
  - Test distance delta and `calculated_efficiency_kpl` computation across multiple full-tank fuel logs.
  - Test low-efficiency anomaly detection flag when efficiency drops >30% below vehicle baseline average.

---

## 3. Mandatory Next Action
Please start by entering **Planning Mode**, inspecting the codebase as needed, and generating the `implementation_plan.md` artifact for **UC-047** for review and approval.
