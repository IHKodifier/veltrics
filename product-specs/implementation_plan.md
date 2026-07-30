# Implementation Plan: Stage 7b — Specification Integrity Review

The **Veltrics Fleet & Vehicle Management Platform** has completed Stage 7 (Development Roadmap). We are now entering **Stage 7b — Specification Integrity Review**.

In this stage, acting in the persona of **Principal TPM / Devil's Advocate**, we perform a rigorous cross-artifact consistency audit across all 10 approved specifications (`01-product-brief.md` through `07c-gcp-cost-minimization-and-skill-plan.md`) to resolve ambiguities, technical friction points, data model mismatches, and execution edge cases before generating the final **Master PRD** (`08-master-prd.md`).

---

## User Review Required

> [!IMPORTANT]
> **Specification Consistency Review Points**
> 1. **Local SQLite vs. Cloud SQL PostgreSQL Dialect Mapping:**
>    - `01b-tech-stack.md` and `02-architecture.md` specify Cloud SQL PostgreSQL 15+, while `07-roadmap.md` mandates zero-Docker local backend testing using SQLite (`sqlite:///./dev.db`).
>    - *Resolution:* Backend ORM models in SQLAlchemy must use dialect-agnostic types (e.g. `JSON` mapped to SQLite JSON / PG JSONB, custom `UUID` type decorator using string storage on SQLite) to ensure local tests pass identically without cloud DB access.
> 2. **Offline-First Sync Queue Dependency Resolution:**
>    - Mobile clients create records offline using client-generated UUIDs.
>    - *Resolution:* The batch sync endpoint (`POST /api/v1/sync/batch`) must process entities in dependency order (e.g., `organizations` -> `users` -> `vehicles` -> `drivers` -> `fuel_logs` / `maintenance_logs`) within a single database transaction to prevent FK constraint failures during offline sync catch-up.
> 3. **Ad-Rewarded Quota Lifecycle & Downgrade Rules:**
>    - Free users can earn +2 bonus vehicle slots and +2 bonus driver slots via rewarded video ads.
>    - *Resolution:* Bonus slots are tied permanently to the `organization` entity. If a Pro account downgrades to Free, earned ad-rewarded slots remain active up to the 5-vehicle / 5-driver hard cap.

---

## Open Questions

> [!NOTE]
> **Audit Decisions for User Alignment**

1. **Safepay vs. Stripe Webhook Reconciliation:**
   - Should webhooks for both Stripe (International) and Safepay (Pakistan) update a unified `subscriptions` schema with normalized status fields (`ACTIVE`, `PAST_DUE`, `CANCELED`), while storing gateway-specific metadata in a `gateway_payload` JSON field?
   - *(Recommended Choice: Yes, normalize status fields across both payment gateways to ensure billing middleware remains provider-agnostic).*

2. **Ad-Rewarded Vehicle Action Gate Enforcement:**
   - For Free Tier ad-rewarded vehicles, should the per-action video ad requirement be enforced at the Flutter UI state level with an API signature token validating ad completion?
   - *(Recommended Choice: Yes, Flutter UI shows rewarded ad dialog before submitting payload to FastAPI endpoint).*

---

## Proposed Changes

### Product Specifications

#### [NEW] [07b-integrity-review.md](file:///e:/Non_Office/Dev_Space/vibe_skool/veltrics/product-specs/07b-integrity-review.md)
Create the formal **Specification Integrity Review** document authored by the *Principal TPM / Devil's Advocate* persona.
- Executive Synthesis & Audit Methodology.
- Cross-Artifact Traceability Matrix (Mapping Product Brief -> Tech Stack -> Architecture -> Journeys -> Stories -> Scope -> Style -> Data Model -> Roadmap).
- Resolved Technical Conflicts & Schema Harmonization.
- Edge Case & Vulnerability Hardening (Security, Multi-tenant Isolation, SQLite/PG Dialect parity, Sync Conflicts).
- Pre-Master PRD Final Readiness Checklist.

---

### Project Trackers

#### [MODIFY] [07-big-picture-tracker.md](file:///e:/Non_Office/Dev_Space/vibe_skool/veltrics/trackers/07-big-picture-tracker.md)
Update high-level specification stage completion progress to reflect Stage 7b readiness.

---

## Verification Plan

### Automated Tests
- Verify all relative file links in `product-specs/07b-integrity-review.md`.
- Verify markdown structure and mermaid syntax validity.

### Manual Verification
- Review generated `07b-integrity-review.md` against all 10 prior specs.
- Generate structured Handoff Prompt `handoff-prompts/handoff-stage-7b.md` for Stage 8 (Master PRD).
