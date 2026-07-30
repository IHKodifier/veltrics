# Handoff Prompt: Stage 3 (User Journeys) Completed

> **Reads from:** [01-product-brief.md](file:///e:/Non_Office/Dev_Space/vibe_skool/veltrics/product-specs/01-product-brief.md), [01b-tech-stack.md](file:///e:/Non_Office/Dev_Space/vibe_skool/veltrics/product-specs/01b-tech-stack.md), [02-architecture.md](file:///e:/Non_Office/Dev_Space/vibe_skool/veltrics/product-specs/02-architecture.md), [03-user-journeys.md](file:///e:/Non_Office/Dev_Space/vibe_skool/veltrics/product-specs/03-user-journeys.md)  
> **Target Stage:** `STAGE 4: Feature Stories` (resulting in `04-feature-stories.md`)  
> **Status:** Approved & Ready for Handoff

---

## 1. Project State & Key Decisions Summary

The **Veltrics Fleet & Vehicle Management** platform has completed the Product Brief, Tech Stack Interlude, High-Level Architecture, and User Journeys:

- **Core Strategy:** Dual-wedge SaaS — free consumer tier (Android mobile, ad-supported) funnels into paid Pro/Enterprise tiers (Chrome Desktop Web + Android) for fleet operators.
- **Architecture Pattern:** Modular Monolith — single Cloud Run service with 12 well-defined domain modules (`auth`, `organizations`, `vehicles`, `maintenance`, `fuel`, `trips`, `expenses`, `dashboard`, `notifications`, `payments`, `ads`, `common`). Clean boundaries enable future microservice extraction.
- **Frontend:** Flutter (Dart) — single codebase targeting Android and Flutter Web. Offline-first on Android with Hive-based sync queue.
- **Backend:** FastAPI (Python) Modular Monolith on Cloud Run with SQLAlchemy 2.0 ORM and Alembic migrations. Async via `asyncpg`.
- **Database:** PostgreSQL 15+ on Cloud SQL (shared schema multi-tenancy with `organization_id` + PostgreSQL RLS as safety net).
- **Authentication:** Firebase Auth with custom claims for RBAC (`consumer`, `fleet_manager`, `driver`, `admin`). JWTs verified server-side via `firebase-admin` Python SDK.
- **Acquisition Funnel:** Consumer-first on Android. Fleet managers are graduated from satisfied consumers, not acquired via separate web sign-up funnel.
- **Aha Moment:** Pre-populated maintenance schedule appears immediately after adding first vehicle (Make/Model/Year + Odometer → intelligent schedule). Target: under 90 seconds to value.
- **Upgrade Path:** Consumer-to-Pro upgrade is seamless — personal pseudo-organization converts to full organization automatically, existing vehicles migrate, Firebase claims update via FCM push.
- **Offline Strategy:** Hive-based offline queue on Flutter Android. Background sync with idempotent batch endpoint (`POST /api/v1/sync/batch`). Client-generated UUIDs for deduplication. Conflict resolution shows side-by-side comparison with user choice (keep mine / accept server / merge).

### Key UX Decisions (from Stage 3)

1. **No email verification gate at onboarding.** Users land on the dashboard immediately. Verification is prompted via a subtle banner later.
2. **Vehicle typeahead from bundled local database.** Eliminates typos and enables pre-populated maintenance schedules.
3. **FCM permission prompt comes AFTER value delivery** — after the user sees their maintenance schedule, not during sign-up.
4. **Driver invitation is phone-first** (Pakistan context). 6-character invite codes (e.g., `VLT-A3K`) for drivers without the app.
5. **Offline is normal, not an error.** Pending sync entries show a yellow informational badge, not a red error indicator.
6. **Sync conflicts are user-resolved.** Side-by-side comparison with three options: keep mine, accept server, merge manually. Non-conflicting items sync immediately.
7. **Upgrade prompts trigger at 5 points:** vehicle quota wall, driver quota wall, Pro-only feature lock, proactive nudge (30 days consistent usage), persistent subtle navigation badge.

### Cumulative Architectural Constraints (Tech Stack + Architecture + UX)

1. **API-first boundary:** Flutter clients talk exclusively to FastAPI REST endpoints (`/api/v1/*`). No direct client-to-PostgreSQL connections.
2. **Firebase Auth is the sole identity layer.** FastAPI verifies Firebase JWTs on every request via 7-step middleware pipeline.
3. **Role enforcement at API layer** via Firebase custom claims + FastAPI `RBACMiddleware`. Four roles: `consumer`, `driver`, `fleet_manager`, `admin`.
4. **Payment gateway abstraction:** Stripe and Safepay wrapped behind a unified `PaymentService` interface with `StripeAdapter` and `SafepayAdapter`. Flutter client calls `/api/v1/payments/*` — never interacts with provider SDKs directly.
5. **PostgreSQL is the single source of truth.** Firestore is NOT used as a database.
6. **All tenant-scoped queries filter by `organization_id`.** PostgreSQL RLS policies provide a database-level safety net.
7. **Event-driven side effects via Pub/Sub.** Core request-response stays synchronous; notifications, cache invalidation, and audit logging are asynchronous.
8. **Offline entries use client-generated UUIDs** as idempotent deduplication keys on the server.
9. **Pre-populated maintenance schedules** require a vehicle Make/Model/Year → default interval template mapping in the backend (data model dependency).
10. **Driver invitation flow** requires an `invitations` table with phone/email, invite code, expiry (7 days), and status tracking.

### Open Items (Carried Forward)

| Item | Owner Stage | Description |
|:---|:---|:---|
| Free tier vehicle limit (X) | Stage 4b — MVP Scoping Gate | Define the exact number of vehicles allowed on the free tier. |
| Free tier driver limit (Y) | Stage 4b — MVP Scoping Gate | Define the exact number of drivers allowed on the free/pro tier. |
| Vehicle Make/Model database | Stage 6 — Data Model | Define the source and schema for the vehicle typeahead database used in onboarding. |
| Default maintenance schedule templates | Stage 6 — Data Model | Define per-vehicle-category default maintenance intervals. |
| Invite code format & generation | Stage 6 — Data Model | Define the invite code format, generation algorithm, and expiry rules. |
| Ad placement policy | Stage 4 — Feature Stories | Define exactly which screens show ads and which are ad-free zones. |
| Offline-capable screen list | Stage 4 — Feature Stories | Formally enumerate which screens function fully offline vs. require connectivity. |

---

## 2. Approved Artifacts

- [01-product-brief.md](file:///e:/Non_Office/Dev_Space/vibe_skool/veltrics/product-specs/01-product-brief.md) — ✅ Approved
- [01b-tech-stack.md](file:///e:/Non_Office/Dev_Space/vibe_skool/veltrics/product-specs/01b-tech-stack.md) — ✅ Approved
- [02-architecture.md](file:///e:/Non_Office/Dev_Space/vibe_skool/veltrics/product-specs/02-architecture.md) — ✅ Approved
- [03-user-journeys.md](file:///e:/Non_Office/Dev_Space/vibe_skool/veltrics/product-specs/03-user-journeys.md) — ✅ Approved

---

## 3. Next Stage: STAGE 4 — Feature Stories

- **Next Persona:** SaaS Founder × Product Designer
- **Output:** `product-specs/04-feature-stories.md`
- **Focus:** Epic overview, detailed user stories with testable acceptance criteria, priority tagging (P0/P1/P2), out-of-scope v1 feature list. Each story should cross-reference Journey IDs (UJ-XXX) and Screen IDs (SCR-XXX-XXX) from Stage 3.

### Screen Inventory Reference (47 screens from Stage 3)

| Category | Count | IDs |
|:---|:---|:---|
| Authentication | 7 | SCR-AUTH-001 → 007 |
| Vehicle | 5 | SCR-VEH-001 → 005 |
| Maintenance | 5 | SCR-MNT-001 → 005 |
| Fuel & Trip | 4 | SCR-FUEL-001/002, SCR-TRIP-001/002 |
| Expense | 2 | SCR-EXP-001/002 |
| Dashboard | 3 | SCR-DASH-001 → 003 |
| Organization & Drivers | 6 | SCR-ORG-001 → 006 |
| Payment & Upgrade | 5 | SCR-PAY-001 → 005 |
| Notifications & Settings | 4 | SCR-NOTIF-001/002, SCR-SET-001/002 |
| Offline & Sync | 3 | SCR-SYNC-001 → 003 |
| Ads | 3 | SCR-AD-001 → 003 |

### Kickstart Prompt for Stage 4 (Copy and Paste to Start)

```markdown
Hello! I have completed Stages 1–3 (Product Brief, Tech Stack, Architecture, User Journeys) for Veltrics. All four artifacts are approved. I would like to proceed to Stage 4: Feature Stories.

Here are the details:
- **Next Stage:** STAGE 4 — Feature Stories (resulting in `04-feature-stories.md`)
- **Active Persona:** SaaS Founder × Product Designer
- **Project Context:** Fleet & vehicle management SaaS. Modular Monolith (FastAPI on Cloud Run). Flutter (Dart) single codebase for Android + Web. Consumer-first Android acquisition funnel. 47 screens inventoried across 12 user journeys. Offline-first on Android. Firebase Auth RBAC. Pre-populated maintenance schedules as onboarding hook.
- **Approved Artifacts:**
  - `product-specs/01-product-brief.md`
  - `product-specs/01b-tech-stack.md`
  - `product-specs/02-architecture.md`
  - `product-specs/03-user-journeys.md`

Please activate the SaaS Founder × Product Designer persona and ask the initial questions to help us design the feature stories.
```

---

## 4. Architecture Decision Record Summary (13 Decisions + 7 UX Decisions Logged)

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

### UX Decisions (UXD — from Stage 3)

| ID | Decision | Reversibility |
| :--- | :--- | :--- |
| UXD-001 | Pre-populated maintenance schedule as onboarding aha moment | Medium |
| UXD-002 | No email verification gate at onboarding (async verification) | High |
| UXD-003 | Vehicle typeahead from bundled local database | Medium |
| UXD-004 | Phone-first driver invitation with 6-char invite codes | High |
| UXD-005 | Offline badge is informational (yellow), not error (red) | High |
| UXD-006 | Sync conflicts show side-by-side comparison with user choice | Medium |
| UXD-007 | Consumer-to-Pro upgrade: 5 trigger points, auto-org creation | Low |
