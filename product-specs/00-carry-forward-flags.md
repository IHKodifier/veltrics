# Carry Forward Flags: Veltrics Fleet & Vehicle Management Platform

> **Purpose:** Single consolidated reference for every decision, data model requirement, deferred item, assumption, risk, and architectural note flagged for resolution in a later stage or session.
>
> **How to use:** Reference this file before beginning any new stage and before generating tickets or charter instructions.
>
> **Last updated:** Stage 08 (Master PRD) — Session 2 — 2026-08-02

---

## Open Flags

| ID | Type | Flag Summary | Flagged In | Resolve By | Notes |
|----|------|-------------|-----------|-----------|-------|
| — | — | *(none — all flags resolved)* | — | — | — |

---

## Resolved Flags

| ID | Type | Flag Summary | Flagged In | Resolved In | Resolution Summary |
|----|------|-------------|-----------|------------|-------------------|
| `CF-ARC-001` | Architectural | Dual payment gateway reconciliation (Stripe & Safepay) writing to normalized `subscriptions` schema with `gateway_payload` JSON. | Stage 06 | Stage 06a | Fully specified in `UC-121` (Core Webhook Reconciliation Engine), `UC-081` (Stripe Webhook), and `UC-082` (Safepay Webhook). |
| `CF-ARC-002` | Architectural | Offline-first mobile sync batch protocol (`POST /api/v1/sync/batch`) with entity dependency ordering in single DB transaction. | Stage 06 | Stage 06a | Fully specified in `UC-119` (Sync Batch Transaction Engine) and `UC-090`..`UC-097` (Offline Sync Module). |
| `CF-DAT-001` | Data Model | Ad-rewarded quota lifecycle (+2 vehicle, +2 driver slots per organization) maintained across Pro -> Free downgrades. | Stage 06 | Stage 06a | Fully specified in `UC-120` (Ad-Rewarded Quota Lifecycle Engine), `UC-085` (Downgrade Execution), and `UC-099` (Rewarded Ad Playback). |
| `CF-ARC-003` | Architectural | Ad-gate signature enforcement between Flutter client and FastAPI backend. | Stage 06 | Stage 06a | Fully specified in `UC-122` (Ad-Gate Signature Enforcement Protocol) and `UC-100` (Ad-Gate Action Verification). |
| `CF-ARC-004` | Architectural | Local-first & zero-cloud dev rules (SQLite `sqlite:///./dev.db`, local auth emulator, dialect-agnostic SQLAlchemy models). | Stage 06 | Stage 07a | Codified in canonical root `/AGENTS.md` and `07a-engineering-charter.md`. |
| `CF-ARC-005` | Governance | Governance file discovery: write canonical `/AGENTS.md` at root. | Stage 06a | Stage 07a | Canonical `/AGENTS.md` written to repository root. |
