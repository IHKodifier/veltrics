# Handoff Prompt: Execute Ticket UC-011 — Account Deletion (GDPR Right to be Forgotten)

We are working on the **Veltrics Fleet & Vehicle Management Platform** (Python FastAPI Backend + Flutter Frontend).
Sprint 01 is active in Stage 01.

---

## 1. Project Context & Current State
- **Branch Strategy:** Active sprint branch (`sprint/sprint-01` or feature branch).
- **Backend Stack:** Python FastAPI + SQLAlchemy + SQLite (`sqlite:///./dev.db`) local-first.
- **Frontend Stack:** Flutter Client App (`src/frontend`).
- **Governance Rules:** Follow `.agents/AGENTS.md`.
- **Completed Tickets (24 / 27 in Sprint 01 — 88.9% Complete):**
  - `UC-001`, `UC-002`, `UC-003`, `UC-004`, `UC-005`, `UC-006`, `UC-007`, `UC-008`, `UC-009`, `UC-010` (User Sign Out & Token Revocation), `UC-014`, `UC-015`, `UC-016`, `UC-024`, `UC-025`, `UC-026`, `UC-027`, `UC-034`, `UC-035`, `UC-036`, `UC-037`, `UC-038`, `UC-064`, `UC-118`.

---

## 2. Target Ticket Specification: UC-011
- **Ticket ID:** `UC-011: Account Deletion (GDPR Right to be Forgotten)`
- **Linked Story:** `FS-AUTH-010`
- **Actor:** Authenticated User
- **Trigger:** User requests account deletion in Privacy / Account Settings.
- **Key Requirements:**
  1. Implement backend endpoint `DELETE /api/v1/users/me` requiring user authentication.
  2. Verify user is not sole owner of an active non-personal organization with active members (or require transfer).
  3. Soft-delete user record (`deleted_at = utc_now()`) and anonymize PII (`email = "deleted_<uuid>@anonymized.local"`, `full_name = "Deleted User"`, `phone_number = None`).
  4. Revoke active refresh tokens server-side and log an `AuditLog` event (`USER_ACCOUNT_DELETED`).
  5. Add client UI account deletion action in Flutter `ProfileScreen` with confirmation modal.
- **Testing Requirements (`src/tests/unit/test_auth_uc011.py`):**
  - Test successful account deletion, soft-delete timestamp, and PII anonymization.
  - Test blocking deletion for sole owners with active members/orgs.
  - Test that deleted users cannot authenticate or refresh tokens post-deletion.

---

## 3. Mandatory Next Action
Please start by entering **Planning Mode**, inspecting the codebase as needed, and generating the `implementation_plan.md` artifact for **UC-011** for review and approval.
