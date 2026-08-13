# Handoff Prompt: Execute Ticket UC-012 — Audit Log Recording for Authentication Events

We are working on the **Veltrics Fleet & Vehicle Management Platform** (Python FastAPI Backend + Flutter Frontend).
Sprint 01 is active in Stage 01.

---

## 1. Project Context & Current State
- **Branch Strategy:** Active sprint branch (`sprint/sprint-01` or feature branch).
- **Backend Stack:** Python FastAPI + SQLAlchemy + SQLite (`sqlite:///./dev.db`) local-first.
- **Frontend Stack:** Flutter Client App (`src/frontend`).
- **Governance Rules:** Follow `.agents/AGENTS.md`.
- **Completed Tickets (25 / 27 in Sprint 01 — 92.6% Complete):**
  - `UC-001`, `UC-002`, `UC-003`, `UC-004`, `UC-005`, `UC-006`, `UC-007`, `UC-008`, `UC-009`, `UC-010`, `UC-011` (Account Deletion), `UC-014`, `UC-015`, `UC-016`, `UC-024`, `UC-025`, `UC-026`, `UC-027`, `UC-034`, `UC-035`, `UC-036`, `UC-037`, `UC-038`, `UC-064`, `UC-118`.

---

## 2. Target Ticket Specification: UC-012
- **Ticket ID:** `UC-012: Audit Log Recording for Authentication Events`
- **Linked Story:** `FS-AUTH-011`
- **Actor:** System / Middleware
- **Trigger:** Any auth event occurs (login, failed login, registration, password change/reset, logout, account deletion).
- **Key Requirements:**
  1. Capture auth event metadata (IP address, user agent, event action type, actor_id, timestamp).
  2. Insert immutable records into `audit_logs` table (`action`, `actor_id`, `organization_id`, `payload`).
  3. Support unauthenticated event logging (`actor_id = None`).
  4. Ensure log writing operates efficiently without blocking main user request flows.
- **Testing Requirements (`src/tests/unit/test_auth_uc012.py`):**
  - Test audit log creation on successful authentication events (login, register, reset password, logout, account deletion).
  - Test audit log recording on failed login / unauthenticated attempts (with `actor_id = None`).
  - Test payload metadata verification (IP address, action string, user ID linkage).

---

## 3. Mandatory Next Action
Please start by entering **Planning Mode**, inspecting the codebase as needed, and generating the `implementation_plan.md` artifact for **UC-012** for review and approval.
