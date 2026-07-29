# Handoff Prompt: Stage 4b (MVP Scoping Gate) Completed

> **Reads from:** [01-product-brief.md](file:///e:/Non_Office/Dev_Space/vibe_skool/veltrics/product-specs/01-product-brief.md), [01b-tech-stack.md](file:///e:/Non_Office/Dev_Space/vibe_skool/veltrics/product-specs/01b-tech-stack.md), [02-architecture.md](file:///e:/Non_Office/Dev_Space/vibe_skool/veltrics/product-specs/02-architecture.md), [03-user-journeys.md](file:///e:/Non_Office/Dev_Space/vibe_skool/veltrics/product-specs/03-user-journeys.md), [04-feature-stories.md](file:///e:/Non_Office/Dev_Space/vibe_skool/veltrics/product-specs/04-feature-stories.md), [04b-mvp-scope.md](file:///e:/Non_Office/Dev_Space/vibe_skool/veltrics/product-specs/04b-mvp-scope.md)  
> **Target Stage:** `★ STYLE GUIDE` (resulting in `05-style-guide.md`)  
> **Status:** Approved & Ready for Handoff

---

## 1. Project State & Key Decisions Summary

The **Veltrics Fleet & Vehicle Management** platform has completed the Product Brief, Tech Stack, Architecture, User Journeys, Feature Stories, and MVP Scoping Gate. All 6 artifacts are approved.

- **Core Strategy:** Dual-wedge SaaS — free consumer tier (Android, ad-supported) → paid Pro/Enterprise tiers (Chrome Web + Android) for fleet operators. Consumer-first acquisition funnel.
- **Architecture:** Modular Monolith (FastAPI on Cloud Run, 12 domain modules, PostgreSQL + Redis, Firebase Auth RBAC).
- **Frontend:** Flutter (Dart) single codebase — Android + Web. Offline-first on Android with Hive sync queue.
- **MVP Scope:** 117 granular user stories across 16 epics, all tagged `IN`. Ships in 90 days across 6 two-week sprints.
- **Build Sequence:** Foundation → Data Entry → Offline+Fleet → Monetization → Fleet Intelligence → Polish.
- **Ad Strategy:** Banners + native ad cards on dashboards/lists (never on data entry forms). Rewarded video ads (3 consecutive to earn) for **permanent** bonus slots with per-action ad gate. Pro/Enterprise are ad-free.
- **Driver Scoring:** Logging consistency score (% of days with ≥1 entry) — Consistent (🟢 ≥80%), Moderate (🟡 50–79%), Needs Attention (🔴 <50%).
- **Dark Mode:** Ships in MVP. Light/Dark/System toggle.
- **Data Export:** PDF maintenance history + CSV fuel/expenses + Fleet summary report. Pro-gated.

### Resolved Tier Limits (from 04b-mvp-scope.md)

| Resource | Free Tier | Pro Tier | Enterprise Tier |
|:---|:---|:---|:---|
| **Base vehicles** | 3 | 25 | Up to 1000 |
| **Ad-rewarded bonus vehicles** | +2 (max total: **5**) | — | — |
| **Base drivers** | 3 | 15 | Up to 1000 |
| **Ad-rewarded bonus drivers** | +2 (max total: **5**) | — | — |
| **Ads** | Banners + native cards + rewarded video | Ad-free | Ad-free |
| **Data export (PDF/CSV)** | 🔒 Locked | ✅ Included | ✅ Included |
| **Driver scoring** | 🔒 Locked | ✅ Included | ✅ Included |

### Ad-Rewarded Slot Mechanic (Resolved)

- **Earn a slot:** Watch **3 consecutive full video ads** (no skip). Unlocks 1 permanent bonus slot for vehicles or drivers.
- **Max bonus:** 2 per resource type. Vehicle bonus wall triggers at vehicle 4 (or 6 if both slots used). Driver bonus wall triggers at driver 4 (or 6 if both slots used).
- **Per-action gate:** Every action on an ad-rewarded resource requires watching 1 video ad first.
- **Upgrade path:** Pro upgrade converts all ad-rewarded resources to standard. All per-action gates removed.

### MVP Build Sequence (6 Sprints × 15 Days = 90 Days)

| Sprint | Days | Focus | Stories |
|:---|:---|:---|:---|
| **Sprint 1** | 1–15 | Auth + Vehicle + Maintenance Core | 20 |
| **Sprint 2** | 16–30 | Fuel + Trip + Expense + Notifications | 22 |
| **Sprint 3** | 31–45 | Offline Sync + Organizations + Drivers | 20 |
| **Sprint 4** | 46–60 | Payments + Ads + Upgrade Flow | 16 |
| **Sprint 5** | 61–75 | Fleet Dashboard + Driver Scoring + Export | 17 |
| **Sprint 6** | 76–90 | Dark Mode + Settings + Recovery + Hardening | 22 |

### Minimum Value Loop (MVL)

**Auth → Add Vehicle → Pre-Populated Maintenance Schedule (✨ aha moment) → Push Reminder → Log Service → Schedule Auto-Advances**

MVL = 18 stories. Functional by end of Sprint 1.

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
| EP-AD | 5 | Banners + native + rewarded video (permanent slots), ad-free data entry |
| EP-DRV | 4 | Consistency scoring, inactive alerts |
| EP-THEME | 3 | Light/Dark/System |
| EP-EXPORT | 3 | PDF + CSV exports (Pro-gated) |
| EP-SET | 6 | Units, account deletion, data download |

### Cumulative Constraints

All constraints from Stages 1–4 remain in effect, plus:

1. **Ad-free data entry forms.** No ads on SCR-FUEL-001, SCR-MNT-002, SCR-TRIP-001, SCR-EXP-001.
2. **Rewarded video ads** provide **permanent** bonus slots (not time-limited). 3 consecutive ads unlock 1 slot. Per-action ad gate applies on every subsequent action involving that resource.
3. **Free tier quota:** 3 base + 2 ad-rewarded = **5 max** (vehicles and drivers, symmetrical).
4. **Driver scoring** is Pro-gated. Based on logging consistency — (days with ≥1 entry / total active days) × 100.
5. **Dark mode** is a Day 1 feature with a proper dark palette (not inverted colors).
6. **PDF/CSV export** is Pro-gated. Free tier sees a lock icon on export buttons.
7. **90-day build target:** 117 stories, 6 sprints, ~1.3 stories/day velocity.
8. **Sprint 4 fallback:** Launch Stripe-only if Safepay integration blocks. Safepay added post-launch.

### Post-MVP Roadmap (Formally Deferred)

| Priority | Feature |
|:---|:---|
| **Immediate** | AI-Powered Predictive Maintenance |
| **Immediate** | iOS App (Flutter native) |
| **Immediate** | Transactional Email (SendGrid/Mailgun) |
| **High** | GPS Trip Tracking (auto-logging) |
| **Medium** | Feature Flags (Firebase Remote Config) |
| **Low** | QuickBooks/Xero Integration |

### Out-of-Scope

OCR receipt scanning, Multi-language/i18n, OBD-II telematics integration, full-text search (PostgreSQL tsvector, post-MVP), Cloud CDN for API (post-MVP).

---

## 2. Approved Artifacts

- [01-product-brief.md](file:///e:/Non_Office/Dev_Space/vibe_skool/veltrics/product-specs/01-product-brief.md) — ✅ Approved
- [01b-tech-stack.md](file:///e:/Non_Office/Dev_Space/vibe_skool/veltrics/product-specs/01b-tech-stack.md) — ✅ Approved
- [02-architecture.md](file:///e:/Non_Office/Dev_Space/vibe_skool/veltrics/product-specs/02-architecture.md) — ✅ Approved
- [03-user-journeys.md](file:///e:/Non_Office/Dev_Space/vibe_skool/veltrics/product-specs/03-user-journeys.md) — ✅ Approved
- [04-feature-stories.md](file:///e:/Non_Office/Dev_Space/vibe_skool/veltrics/product-specs/04-feature-stories.md) — ✅ Approved
- [04b-mvp-scope.md](file:///e:/Non_Office/Dev_Space/vibe_skool/veltrics/product-specs/04b-mvp-scope.md) — ✅ Approved

---

## 3. Next Stage: ★ STYLE GUIDE

- **Next Persona:** Brand & Design Systems Lead
- **Output:** `product-specs/05-style-guide.md`
- **Focus:** Visual identity, color system (light + dark mode palettes), typography, iconography, spacing/grid, component design tokens, motion/animation principles, and platform-specific adaptations (Android mobile vs. Chrome web desktop). The style guide must cover both the free-tier ad-supported experience and the clean Pro/Enterprise experience.

### Key Style Inputs for Stage 5

The style guide persona should be aware of:

- **Two surfaces:** Android mobile app (consumer + driver) and Chrome desktop web app (fleet manager + admin).
- **Two modes:** Light and Dark (system-following toggle, ships in MVP).
- **Two user states:** Free tier (banners/native ad cards visible, quota wall prompts, ad-rewarded badges) and Pro/Enterprise (ad-free, full-feature UI).
- **Emotional arc:** Consumer onboarding should feel clean and trustworthy. Fleet manager dashboard should feel data-dense but calm. Quota wall / upgrade prompts should feel motivating, not punishing.
- **Ad placement constraints:** Banners at bottom of dashboard screens; native ad cards in vehicle/activity lists. Never on data entry forms.
- **Badge system:** Ad-rewarded resources show a "🎬 Ad" badge. Pro-gated features show a lock icon (🔒).

### Kickstart Prompt for Stage 5 (Copy and Paste to Start)

```markdown
Hello! I have completed Stages 1–4b for Veltrics (Product Brief, Tech Stack, Architecture, User Journeys, Feature Stories, MVP Scoping Gate). All six artifacts are approved. I would like to proceed to the Style Guide stage.

Here are the details:
- **Next Stage:** ★ STYLE GUIDE (resulting in `05-style-guide.md`)
- **Active Persona:** Brand & Design Systems Lead
- **Project:** Veltrics Fleet & Vehicle Management SaaS — Flutter (Android + Chrome Web), FastAPI backend, Firebase Auth.

**Product context:**
- Consumer-first: Individual vehicle owners on Android (free, ad-supported) → SMB fleet managers on Chrome desktop (Pro, paid).
- 117 MVP stories across 16 epics. Ships in 90 days.
- Dark mode ships in MVP (Light/Dark/System toggle).
- Two surfaces: Android mobile (bottom nav, thumb-friendly) and Chrome desktop web (sidebar nav, data-dense tables).
- Free tier shows banner + native ads. Pro/Enterprise is ad-free.
- Ad-rewarded resources carry a "🎬 Ad" badge. Pro-gated features show a lock icon (🔒).

**Resolved tier limits:**
- Free: 3 base vehicles + 2 ad-rewarded = 5 max; 3 base drivers + 2 ad-rewarded = 5 max.
- Pro: 25 vehicles, 15 drivers, ad-free.
- Enterprise: up to 1000 vehicles/drivers.

**Approved artifacts:**
- `product-specs/01-product-brief.md`
- `product-specs/01b-tech-stack.md`
- `product-specs/02-architecture.md`
- `product-specs/03-user-journeys.md`
- `product-specs/04-feature-stories.md`
- `product-specs/04b-mvp-scope.md`

Please activate the Brand & Design Systems Lead persona and ask the initial questions to help us define the Veltrics visual identity and design system.
```

---

## 4. Full Decision Record (All Stages)

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
| FD-002 | Rewarded video ads for **permanent** bonus slots (3 ads to earn + per-action gate) | High |
| FD-003 | Driver scoring by logging consistency | High |
| FD-004 | Dark mode ships in MVP (Light/Dark/System toggle) | High |
| FD-005 | PDF/CSV export is Pro-gated | High |
| FD-006 | Ad-free data entry forms (no ads on forms, ever) | Medium |
| FD-007 | AI Predictive Maintenance is immediate post-MVP | High |
| FD-008 | Transactional Email is immediate post-MVP, user-toggleable | High |

### MVP Scoping Decisions (MVS — from Stage 4b)

| ID | Decision | Rationale |
|:---|:---|:---|
| MVS-001 | All 117 stories remain IN — zero cuts | Solo + AI-assisted velocity makes full scope achievable in 90 days. |
| MVS-002 | Free: 3 vehicles + 2 ad-rewarded (max 5), 3 drivers + 2 ad-rewarded (max 5) | Balanced pressure: base limits are usable, bonus slots create ad revenue, Pro is the clean exit. |
| MVS-003 | Pro: 25 vehicles, 15 drivers | Covers 90%+ of Pakistan SMB fleets. |
| MVS-004 | Enterprise: up to 1000 vehicles/drivers, contact sales beyond | Practical soft limit with sales escalation. |
| MVS-005 | Ad-rewarded slots: 3 consecutive ads to earn, 1 ad per subsequent action | Creates durable upgrade pressure without destroying UX. |
| MVS-006 | Build sequence: Foundation → Data Entry → Offline+Fleet → Monetization → Intelligence → Polish | Dependencies flow left-to-right. Each sprint produces a deployable increment. |
| MVS-007 | Sprint 4 fallback: launch Stripe-only if Safepay integration blocks | De-risks payment sprint. Safepay added post-launch. |
