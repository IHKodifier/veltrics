# Handoff Prompt: Stage 2 (High-Level Architecture) Completed

> **Reads from:** [01-product-brief.md](file:///e:/Non_Office/Dev_Space/vibe_skool/veltrics/product-specs/01-product-brief.md), [01b-tech-stack.md](file:///e:/Non_Office/Dev_Space/vibe_skool/veltrics/product-specs/01b-tech-stack.md), [02-architecture.md](file:///e:/Non_Office/Dev_Space/vibe_skool/veltrics/product-specs/02-architecture.md)  
> **Target Stage:** `STAGE 3: User Journeys` (resulting in `03-user-journeys.md`)  
> **Status:** Approved & Ready for Handoff

---

## 1. Project State & Key Decisions Summary

The **Veltrics Fleet & Vehicle Management** platform has completed the Product Brief, Tech Stack Interlude, and High-Level Architecture:

- **Core Strategy:** Dual-wedge SaaS — free consumer tier (Android mobile, ad-supported) funnels into paid Pro/Enterprise tiers (Chrome Desktop Web + Android) for fleet operators.
- **Architecture Pattern:** Modular Monolith — single Cloud Run service with 12 well-defined domain modules (`auth`, `organizations`, `vehicles`, `maintenance`, `fuel`, `trips`, `expenses`, `dashboard`, `notifications`, `payments`, `ads`, `common`). Clean boundaries enable future microservice extraction.
- **Frontend:** Flutter (Dart) — single codebase targeting Android and Flutter Web. Offline-first on Android with Hive-based sync queue.
- **Backend:** FastAPI (Python) Modular Monolith on Cloud Run with SQLAlchemy 2.0 ORM and Alembic migrations. Async via `asyncpg`.
- **Database:** PostgreSQL 15+ on Cloud SQL (shared schema multi-tenancy with `organization_id` + PostgreSQL RLS as safety net).
- **Authentication:** Firebase Auth with custom claims for RBAC (`consumer`, `fleet_manager`, `driver`, `admin`). JWTs verified server-side via `firebase-admin` Python SDK.
- **API Design:** URL-path versioning (`/api/v1/*`). Standard JSON response envelope with `data`, `meta`, `errors` structure.
- **Real-Time Updates:** Polling + FCM silent refresh via Pub/Sub → FCM pipeline. 2-5 second latency, $0 additional cost.
- **Offline Strategy:** Hive-based offline queue on Flutter Android. Background sync with idempotent batch endpoint (`POST /api/v1/sync/batch`). Client-generated UUIDs for deduplication. Last-write-wins conflict resolution.
- **Rate Limiting:** Redis-backed per-user rate counters. Tier-aware: Free (60 req/min), Pro (300 req/min), Enterprise (1000 req/min).
- **Multi-Tenancy:** Shared schema. Consumers get a personal pseudo-organization. Pro upgrade converts personal org to full organization.
- **Hosting:** Cloud Run (`asia-south1` Mumbai) + Firebase Hosting (Flutter Web) + Cloud SQL + Memorystore Redis.
- **Payments:** Stripe (international) + Safepay (Pakistan domestic) behind a unified `PaymentService` abstraction with adapter pattern.
- **Background Jobs:** Cloud Tasks (scheduled maintenance checks) + Cloud Pub/Sub (event-driven workflows: `fleet.events`, `payment.events`, `audit.events`).

### Key Architectural Constraints (Cumulative — Tech Stack + Architecture)

1. **API-first boundary:** Flutter clients talk exclusively to FastAPI REST endpoints (`/api/v1/*`). No direct client-to-PostgreSQL connections.
2. **Firebase Auth is the sole identity layer.** FastAPI verifies Firebase JWTs on every request via 7-step middleware pipeline.
3. **Role enforcement at API layer** via Firebase custom claims + FastAPI `RBACMiddleware`. Four roles: `consumer`, `driver`, `fleet_manager`, `admin`.
4. **Payment gateway abstraction:** Stripe and Safepay wrapped behind a unified `PaymentService` interface with `StripeAdapter` and `SafepayAdapter`. Flutter client calls `/api/v1/payments/*` — never interacts with provider SDKs directly.
5. **PostgreSQL is the single source of truth.** Firestore is NOT used as a database.
6. **All tenant-scoped queries filter by `organization_id`.** PostgreSQL RLS policies provide a database-level safety net.
7. **Event-driven side effects via Pub/Sub.** Core request-response stays synchronous; notifications, cache invalidation, and audit logging are asynchronous.
8. **Offline entries use client-generated UUIDs** as idempotent deduplication keys on the server.

---

## 2. Approved Artifacts

- [01-product-brief.md](file:///e:/Non_Office/Dev_Space/vibe_skool/veltrics/product-specs/01-product-brief.md) — ✅ Approved
- [01b-tech-stack.md](file:///e:/Non_Office/Dev_Space/vibe_skool/veltrics/product-specs/01b-tech-stack.md) — ✅ Approved
- [02-architecture.md](file:///e:/Non_Office/Dev_Space/vibe_skool/veltrics/product-specs/02-architecture.md) — ✅ Approved

---

## 3. Next Stage: STAGE 3 — User Journeys

- **Next Persona:** FAANG-Veteran UX Designer
- **Output:** `product-specs/03-user-journeys.md`
- **Focus:** New user onboarding (consumer + fleet manager), core recurring flows (log fuel, log maintenance, view dashboard), recovery paths (forgot password, failed sync, payment failure), emotional journey map, edge cases (offline data entry, driver invitation, consumer-to-Pro upgrade), screen inventory.

### Kickstart Prompt for Stage 3 (Copy and Paste to Start)

```markdown
Hello! I have completed Stage 1 (Product Brief), the Tech Stack Interlude, and Stage 2 (High-Level Architecture) for Veltrics. All three artifacts are approved. I would like to proceed to Stage 3: User Journeys.

Here are the details:
- **Next Stage:** STAGE 3 — User Journeys (resulting in `03-user-journeys.md`)
- **Active Persona:** FAANG-Veteran UX Designer
- **Project Context:** Fleet & vehicle management SaaS. Modular Monolith architecture (FastAPI on Cloud Run). Flutter (Dart) single codebase for Android + Web. Offline-first on Android with Hive sync queue. Shared schema multi-tenancy. Firebase Auth RBAC (consumer, driver, fleet_manager, admin). Polling + FCM for near-real-time dashboard updates.
- **Approved Artifacts:**
  - `product-specs/01-product-brief.md`
  - `product-specs/01b-tech-stack.md`
  - `product-specs/02-architecture.md`

Please activate the FAANG-Veteran UX Designer persona and ask the initial questions to help us design the user journeys.
```

---

## 4. Architecture Decision Record Summary (13 Decisions Logged)

### Tech Stack Decisions (TDL — from Stage 1b)

| ID | Decision | Reversibility |
| :--- | :--- | :--- |
| TDL-001 | Flutter over React Native | Low |
| TDL-002 | FastAPI over Django/Flask | Medium |
| TDL-003 | Cloud SQL PostgreSQL over Firestore/AlloyDB | High |
| TDL-004 | Firebase Auth over Custom JWT / Auth0 | Medium |
| TDL-005 | Cloud Run over GKE / App Engine | High |
| TDL-006 | Safepay for Pakistan domestic payments | High |
| TDL-007 | Stripe for international payments | Medium |

### Architecture Decisions (ADR — from Stage 2)

| ID | Decision | Reversibility |
| :--- | :--- | :--- |
| ADR-001 | Modular Monolith (12 domain modules, single Cloud Run service) | Medium |
| ADR-002 | URL-path API versioning (`/api/v1/*`) | High |
| ADR-003 | Shared schema multi-tenancy with `organization_id` + PostgreSQL RLS | Medium |
| ADR-004 | Offline-first with Hive + sync queue (Android only) | Low |
| ADR-005 | Polling + FCM push for near-real-time (no SSE/WebSocket) | High |
| ADR-006 | Redis for rate limiting + dashboard caching | High |
