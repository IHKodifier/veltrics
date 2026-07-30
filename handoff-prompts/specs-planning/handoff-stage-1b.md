# Handoff Prompt: Stage 1b (Tech Stack Interlude) Completed

> **Reads from:** [01-product-brief.md](file:///e:/Non_Office/Dev_Space/vibe_skool/veltrics/product-specs/01-product-brief.md), [01b-tech-stack.md](file:///e:/Non_Office/Dev_Space/vibe_skool/veltrics/product-specs/01b-tech-stack.md)  
> **Target Stage:** `STAGE 2: High-Level Architecture` (resulting in `02-architecture.md`)  
> **Status:** Approved & Ready for Handoff

---

## 1. Project State & Key Decisions Summary

The **Veltrics Fleet & Vehicle Management** platform has completed both the Product Brief and Tech Stack Interlude:

- **Core Strategy:** Dual-wedge SaaS — free consumer tier (Android mobile, ad-supported) funnels into paid Pro/Enterprise tiers (Chrome Desktop Web + Android) for fleet operators.
- **Frontend:** Flutter (Dart) — single codebase targeting Android and Flutter Web. Eliminates mobile/desktop code divergence risk.
- **Backend:** FastAPI (Python) with SQLAlchemy 2.0 ORM and Alembic migrations. Async via `asyncpg`.
- **Database:** PostgreSQL 15+ hosted on Cloud SQL for PostgreSQL (GCP managed).
- **Authentication:** Firebase Auth with custom claims for RBAC (`consumer`, `fleet_manager`, `driver`, `admin`). JWTs verified server-side via `firebase-admin` Python SDK.
- **Hosting:** Cloud Run (FastAPI backend, serverless, `asia-south1` Mumbai) + Firebase Hosting (Flutter Web).
- **Caching:** Memorystore for Redis (deferrable for MVP).
- **Background Jobs:** Cloud Tasks (scheduled maintenance checks) + Cloud Pub/Sub (event-driven workflows).
- **Push Notifications:** Firebase Cloud Messaging (FCM).
- **Analytics & Monitoring:** Firebase Analytics, GA4, Crashlytics, Cloud Monitoring, Cloud Logging, Sentry.
- **Payments (International):** Stripe — recurring SaaS billing with Checkout + Customer Portal.
- **Payments (Pakistan Domestic):** Safepay — single integration covering Visa/Mastercard (debit + credit) + Easypaisa + JazzCash mobile wallets.
- **Ads:** Google AdMob (Android Free Tier) + Google AdSense (Web Free Tier).
- **CI/CD:** Cloud Build + GitHub Actions.
- **Estimated MVP Infra Cost:** ~$37–57/month (or ~$7–22/month without Redis).

### Key Architectural Constraints (established by Tech Stack)
1. **API-first boundary:** Flutter clients talk exclusively to FastAPI REST endpoints. No direct client-to-PostgreSQL connections.
2. **Firebase Auth is the sole identity layer.** FastAPI verifies Firebase JWTs on every request.
3. **Role enforcement at API layer** via Firebase custom claims + FastAPI middleware.
4. **Payment gateway abstraction:** Stripe and Safepay wrapped behind a unified `/api/payments/*` interface.
5. **PostgreSQL is the single source of truth.** Firestore is NOT used as a database.

---

## 2. Approved Artifacts

- [01-product-brief.md](file:///e:/Non_Office/Dev_Space/vibe_skool/veltrics/product-specs/01-product-brief.md) — ✅ Approved
- [01b-tech-stack.md](file:///e:/Non_Office/Dev_Space/vibe_skool/veltrics/product-specs/01b-tech-stack.md) — ✅ Approved

---

## 3. Next Stage: STAGE 2 — High-Level Architecture

- **Next Persona:** Senior Software Architect
- **Output:** `product-specs/02-architecture.md`
- **Focus:** Architecture pattern (monolith vs. microservices vs. modular monolith), Mermaid system diagram, service responsibilities, core data flow, authentication strategy (Firebase Auth JWT verification flow), third-party integrations (Stripe, Safepay, AdMob, FCM), infrastructure topology (Cloud Run + Cloud SQL + Redis + Pub/Sub), security & compliance, scale profile.

### Kickstart Prompt for Stage 2 (Copy and Paste to Start)

```markdown
Hello! I have completed Stage 1 (Product Brief) and the Tech Stack Interlude for Veltrics. Both artifacts are approved. I would like to proceed to Stage 2: High-Level Architecture.

Here are the details:
- **Next Stage:** STAGE 2 — High-Level Architecture (resulting in `02-architecture.md`)
- **Active Persona:** Senior Software Architect
- **Project Context:** Fleet & vehicle management SaaS targeting Android Mobile (Flutter) and Chrome Desktop Web (Flutter Web), backed by FastAPI (Python) on Cloud Run, PostgreSQL on Cloud SQL, Firebase Auth, Safepay (Pakistan payments) + Stripe (international payments).
- **Approved Artifacts:**
  - `product-specs/01-product-brief.md`
  - `product-specs/01b-tech-stack.md`

Please activate the Senior Software Architect persona and ask the initial questions to help us design the high-level architecture.
```

---

## 4. Tech Decision Log Summary (7 Decisions Logged)

| ID | Decision | Reversibility |
| :--- | :--- | :--- |
| TDL-001 | Flutter over React Native | Low |
| TDL-002 | FastAPI over Django/Flask | Medium |
| TDL-003 | Cloud SQL PostgreSQL over Firestore/AlloyDB | High |
| TDL-004 | Firebase Auth over Custom JWT / Auth0 | Medium |
| TDL-005 | Cloud Run over GKE / App Engine | High |
| TDL-006 | Safepay for Pakistan domestic payments | High |
| TDL-007 | Stripe for international payments | Medium |
