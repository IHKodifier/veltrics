# Handoff Prompt: Stage 4 (Feature Stories) Completed

> **Reads from:** [01-product-brief.md](file:///e:/Non_Office/Dev_Space/vibe_skool/veltrics/product-specs/01-product-brief.md), [01b-tech-stack.md](file:///e:/Non_Office/Dev_Space/vibe_skool/veltrics/product-specs/01b-tech-stack.md), [02-architecture.md](file:///e:/Non_Office/Dev_Space/vibe_skool/veltrics/product-specs/02-architecture.md), [03-user-journeys.md](file:///e:/Non_Office/Dev_Space/vibe_skool/veltrics/product-specs/03-user-journeys.md), [04-feature-stories.md](file:///e:/Non_Office/Dev_Space/vibe_skool/veltrics/product-specs/04-feature-stories.md)  
> **Target Stage:** `★ MVP SCOPING GATE` (resulting in `04b-mvp-scope.md`)  
> **Status:** Approved & Ready for Handoff

---

## 1. Project State & Key Decisions Summary

The **Veltrics Fleet & Vehicle Management** platform has completed the Product Brief, Tech Stack, Architecture, User Journeys, and Feature Stories:

- **Core Strategy:** Dual-wedge SaaS — free consumer tier (Android, ad-supported) → paid Pro/Enterprise tiers (Chrome Web + Android) for fleet operators. Consumer-first acquisition funnel.
- **Architecture:** Modular Monolith (FastAPI on Cloud Run, 12 domain modules, PostgreSQL + Redis, Firebase Auth RBAC).
- **Frontend:** Flutter (Dart) single codebase — Android + Web. Offline-first on Android with Hive sync queue.
- **MVP Scope:** 117 granular user stories across 16 epics, all tagged `IN` (ships in MVP).
- **Priority System:** `IN` (ships in MVP), `POST` (post-MVP), `OUT` (not part of product).
- **Story Format:** Granular (one story per atomic action) with Given/When/Then BDD acceptance criteria.
- **Ad Strategy:** Banners + native ad cards on dashboards/lists (never on data entry forms). Rewarded video ads for temporary tier limit increase (7 days). Pro/Enterprise are ad-free.
- **Driver Scoring:** Logging consistency score (% of days with entries) — Consistent (🟢 ≥80%), Moderate (🟡 50-79%), Needs Attention (🔴 <50%).
- **Dark Mode:** Ships in MVP. Light/Dark/System toggle.
- **Data Export:** PDF maintenance history + CSV fuel/expenses + Fleet summary report. Pro-gated.

### Feature Epic Summary (117 Stories)

| Epic | Stories | Key Capabilities |
|:---|:---|:---|
| EP-AUTH | 12 | Google One-Tap, Email, Phone OTP, silent token refresh, role-based nav |
| EP-ORG | 10 | Auto personal org, org conversion on upgrade, invite by phone/email |
| EP-VEH | 10 | Typeahead add, status badges, driver assignment, soft delete + recovery |
| EP-MNT | 12 | Pre-populated schedule (aha moment), service logging, auto-advance |
| EP-FUEL | 6 | Quick-log <15s, fuel efficiency trend |
| EP-TRIP | 6 | Auto-distance, monthly summaries |
| EP-EXP | 6 | Category-based, receipt photo |
| EP-DASH | 8 | Consumer/Fleet/Driver dashboards, FCM auto-refresh |
| EP-NOTIF | 8 | Overdue/upcoming push, silent refresh, quiet hours |
| EP-PAY | 10 | Stripe + Safepay, webhook processing, quota wall prompts |
| EP-SYNC | 8 | Hive offline, background sync, conflict resolution |
| EP-AD | 5 | Banners + native + rewarded video, ad-free data entry |
| EP-DRV | 4 | Consistency scoring, inactive alerts |
| EP-THEME | 3 | Light/Dark/System |
| EP-EXPORT | 3 | PDF + CSV exports (Pro-gated) |
| EP-SET | 6 | Units, account deletion, data download |

### Cumulative Constraints

All constraints from Stages 1-3 remain in effect, plus:

1. **Ad-free data entry forms.** No ads on SCR-FUEL-001, SCR-MNT-002, SCR-TRIP-001, SCR-EXP-001.
2. **Rewarded video ads** provide a 7-day temporary tier limit increase. After expiry, extra vehicles become inactive unless the user upgrades.
3. **Driver scoring** is based on logging consistency — calculated as (days with ≥1 entry / total active days) × 100.
4. **Dark mode** is a Day 1 feature with proper dark palette (not inverted colors).
5. **PDF/CSV export** is Pro-gated. Free tier sees a lock icon on export buttons.
6. **Tier limits (X vehicles, Y drivers)** remain undefined — to be resolved in Stage 4b.

### Post-MVP Priorities (Immediate After MVP)

| Feature | Notes |
|:---|:---|
| AI-Powered Predictive Maintenance | Leverages MVP-accumulated service history |
| iOS App | Flutter native compilation |
| Transactional Email | User-toggleable in notification preferences |

### Out-of-Scope

OCR receipt scanning, Multi-language/i18n, OBD-II telematics integration.

---

## 2. Approved Artifacts

- [01-product-brief.md](file:///e:/Non_Office/Dev_Space/vibe_skool/veltrics/product-specs/01-product-brief.md) — ✅ Approved
- [01b-tech-stack.md](file:///e:/Non_Office/Dev_Space/vibe_skool/veltrics/product-specs/01b-tech-stack.md) — ✅ Approved
- [02-architecture.md](file:///e:/Non_Office/Dev_Space/vibe_skool/veltrics/product-specs/02-architecture.md) — ✅ Approved
- [03-user-journeys.md](file:///e:/Non_Office/Dev_Space/vibe_skool/veltrics/product-specs/03-user-journeys.md) — ✅ Approved
- [04-feature-stories.md](file:///e:/Non_Office/Dev_Space/vibe_skool/veltrics/product-specs/04-feature-stories.md) — ✅ Approved

---

## 3. Next Stage: ★ MVP SCOPING GATE

- **Next Persona:** Technical Product Strategist
- **Output:** `product-specs/04b-mvp-scope.md`
- **Focus:** Minimum value loop definition, ruthless MVP feature filtering (validate all 117 stories truly belong in MVP), tier limit definitions (Free X vehicles/Y drivers, Pro limits, Enterprise limits), deferral rationale for anything cut, MVP build sequence, explicitly descoped list.

### Critical Open Item for Stage 4b

**Tier limits must be defined in this stage:**
- Free tier: max `X` vehicles, max `Y` drivers
- Pro tier: max vehicles, max drivers
- Enterprise tier: limits or "unlimited"

### Kickstart Prompt for Stage 4b (Copy and Paste to Start)

```markdown
Hello! I have completed Stages 1–4 (Product Brief, Tech Stack, Architecture, User Journeys, Feature Stories) for Veltrics. All five artifacts are approved. I would like to proceed to the MVP Scoping Gate.

Here are the details:
- **Next Stage:** ★ MVP SCOPING GATE (resulting in `04b-mvp-scope.md`)
- **Active Persona:** Technical Product Strategist
- **Project Context:** Fleet & vehicle management SaaS. 117 granular feature stories across 16 epics, all currently tagged IN (ships in MVP). Consumer-first Android acquisition. Tier limits (Free: X vehicles/Y drivers) are undefined and must be resolved. Rewarded video ads as quota escape valve.
- **Approved Artifacts:**
  - `product-specs/01-product-brief.md`
  - `product-specs/01b-tech-stack.md`
  - `product-specs/02-architecture.md`
  - `product-specs/03-user-journeys.md`
  - `product-specs/04-feature-stories.md`

Please activate the Technical Product Strategist persona and ask the initial questions to help us scope the MVP.
```

---

## 4. Decision Record Summary (13 TDL/ADR + 7 UXD + Feature Decisions)

### Tech Stack Decisions (TDL — from Stage 1b)

| ID | Decision | Reversibility |
|:---|:---|:---|
| TDL-001 | Flutter over React Native | Low |
| TDL-002 | FastAPI over Django/Flask | Medium |
| TDL-003 | Cloud SQL PostgreSQL over Firestore/AlloyDB | High |
| TDL-004 | Firebase Auth over Custom JWT / Auth0 | Medium |
| TDL-005 | Cloud Run over GKE / App Engine | High |
| TDL-006 | Safepay for Pakistan domestic payments | High |
| TDL-007 | Stripe for international payments | Medium |

### Architecture Decisions (ADR — from Stage 2)

| ID | Decision | Reversibility |
|:---|:---|:---|
| ADR-001 | Modular Monolith (12 domain modules) | Medium |
| ADR-002 | URL-path API versioning (`/api/v1/*`) | High |
| ADR-003 | Shared schema multi-tenancy + PostgreSQL RLS | Medium |
| ADR-004 | Offline-first with Hive + sync queue (Android) | Low |
| ADR-005 | Polling + FCM push for near-real-time | High |
| ADR-006 | Redis for rate limiting + caching | High |

### UX Decisions (UXD — from Stage 3)

| ID | Decision | Reversibility |
|:---|:---|:---|
| UXD-001 | Pre-populated maintenance schedule as aha moment | Medium |
| UXD-002 | No email verification gate at onboarding | High |
| UXD-003 | Vehicle typeahead from bundled local database | Medium |
| UXD-004 | Phone-first driver invitation with invite codes | High |
| UXD-005 | Offline badge is informational (yellow), not error (red) | High |
| UXD-006 | Sync conflicts: side-by-side with user choice | Medium |
| UXD-007 | Consumer-to-Pro: 5 trigger points, auto-org creation | Low |

### Feature Decisions (FD — from Stage 4)

| ID | Decision | Reversibility |
|:---|:---|:---|
| FD-001 | Granular stories (1 per atomic action) with BDD criteria | High |
| FD-002 | Rewarded video ads for temporary tier increase (7 days) | High |
| FD-003 | Driver scoring by logging consistency | High |
| FD-004 | Dark mode ships in MVP (Light/Dark/System toggle) | High |
| FD-005 | PDF/CSV export is Pro-gated | High |
| FD-006 | Ad-free data entry forms (no ads on forms, ever) | Medium |
| FD-007 | AI Predictive Maintenance is immediate post-MVP | High |
| FD-008 | Transactional Email is immediate post-MVP, user-toggleable | High |
