# Development Roadmap: Veltrics Fleet & Vehicle Management Platform

> **Stage:** Stage 7 — Development Roadmap  
> **Persona:** Engineering Programme Manager  
> **Status:** ✅ Approved  
> **Reads from:** [01-product-brief.md](file:///e:/Non_Office/Dev_Space/vibe_skool/veltrics/product-specs/01-product-brief.md) · [01b-tech-stack.md](file:///e:/Non_Office/Dev_Space/vibe_skool/veltrics/product-specs/01b-tech-stack.md) · [02-architecture.md](file:///e:/Non_Office/Dev_Space/vibe_skool/veltrics/product-specs/02-architecture.md) · [04b-mvp-scope.md](file:///e:/Non_Office/Dev_Space/vibe_skool/veltrics/product-specs/04b-mvp-scope.md) · [06-data-model.md](file:///e:/Non_Office/Dev_Space/vibe_skool/veltrics/product-specs/06-data-model.md) · [06a-use-case-tickets.md](file:///e:/Non_Office/Dev_Space/vibe_skool/veltrics/product-specs/06a-use-case-tickets.md)  

---

## Programme Summary

This Development Roadmap translates the 122 implementation-ready use case tickets (`UC-001` through `UC-122`) defined in `06a-use-case-tickets.md` into a structured 6-sprint build sequence. The timeline assumes a 90-day (6 × 2-week sprint) schedule executed by a solo developer operating with AI assistance. Every ticket is assigned to exactly one sprint, respecting topological foreign-key dependencies and prerequisite use cases.

| Phase | Name | Duration | Gate Condition | Owner |
|:---|:---|:---|:---|:---|
| **Phase 0** | Foundation & Project Setup | Weeks 1–2 | Git branch hierarchy initialized (`main` → `dev` → `sprint/sprint-01`), Flutter boilerplate & Firebase (Dev/Staging/Prod) linked, local backend runner (`start_backend.ps1`) verified. | Lead Architect |
| **Phase 1** | MVP Build | Weeks 3–15 | All 122 UC tickets pass test suites; core user loops validated end-to-end. | Engineering Lead |
| **Phase 2** | Beta | Weeks 16–19 | 10–50 SMB fleet managers & individual vehicle owners onboarded; error monitoring active. | Product Lead |
| **Phase 3** | Launch | Weeks 20–23 | Staging verification pass; GCP Cloud SQL start script verified; public app store & web deployment. | Operations |
| **Phase 4** | Post-Launch | Months 6+ | Post-MVP feature backlog (GPS tracking, predictive maintenance) prioritized by analytics. | Product Lead |

**Critical Path Item:** Phase 0 Repo/Firebase Setup, Offline-first Sync Batch Engine (`UC-119`) & Ad-Gate Middleware Signature Enforcement (`UC-122`).  
**Hard Deadline:** Day 90 MVP Feature-Complete Lock (October 2026). Driven by commercial pilot commitments with regional logistics partners in Pakistan.

---

## Phase 0: Foundation & Setup Sequence (Weeks 1–2)

**Goal:** Establish the complete project layout, Firebase project bindings across environments (Dev / Staging / Prod), git branch hierarchy (`main` → `dev` → `sprint/sprint-01`), and zero-cloud local development baseline before feature coding begins.

### Step 0.1 — Git Branch Hierarchy Initialization
- [ ] Initialize Git repository (if not already done).
- [ ] Commit initial project specifications (`product-specs/`, `/AGENTS.md`, `trackers/`) to `main`.
- [ ] Checkout protected staging branch `dev` from `main`: `git checkout -b dev`.
- [ ] Checkout first active sprint branch from `dev`: `git checkout -b sprint/sprint-01`.

### Step 0.2 — Flutter Project Scaffolding & Firebase Multi-Env Setup
- [ ] Create Flutter mobile client boilerplate: `flutter create mobile_frontend`.
- [ ] Configure Flutter package dependencies (`firebase_core`, `firebase_auth`, `provider`/`flutter_bloc`, `sqflite`, `http`).
- [ ] Link Firebase projects for Dev, Staging, and Production environments (`flutterfire configure`):
  - **Dev:** Local emulator / `veltrics-dev` Firebase project bindings.
  - **Staging:** `veltrics-staging` Firebase project bindings.
  - **Prod:** `veltrics-prod` Firebase project bindings.
- [ ] Apply design tokens and theme code from `product-specs/05b-flutter-theme.dart` into `/mobile_frontend/lib/theme/`.
- [ ] Verify "Hello World" app compilation on Android emulator, iOS simulator, and Chrome Web.

### Step 0.3 — Local Backend Runner & Database Seeding Baseline
- [ ] Create `/backend` directory structure (FastAPI routers, Pydantic schemas, SQLAlchemy models).
- [ ] Configure local script `.\scripts\start_backend.ps1` to spin up Uvicorn, SQLite database (`sqlite:///./dev.db`), and Local Auth emulator.
- [ ] CI pipeline configured for linting, format checking, and automated test execution (`pytest tests/ -v`).
- [ ] DB Migration engine (`UC-118`) configured with initial Alembic migrations for all 18 data model entities.

**Phase 0 Gate:** `.\scripts\start_backend.ps1` executes cleanly, Flutter "Hello World" compiles against Firebase Dev environment/emulator, and `sprint/sprint-01` branch is active for ticket implementation.

---

## Phase 1: MVP Build (Weeks 3–15)

The 122 implementation-ready tickets are distributed across 6 two-week sprints. Every ticket from `06a-use-case-tickets.md` is assigned to exactly one sprint.

---

### Sprint 1: Foundation — Auth, Org Baseline, Vehicle CRUD & Maintenance Core (Days 1–15)

**Goal:** User can sign up, create an organization, add a vehicle, view pre-populated maintenance schedules, and log a service record.

| Ticket | Use Case | Owner | Estimate | Depends on | Status |
|:---|:---|:---|:---|:---|:---|
| **UC-001** | Sign Up with Google One-Tap | FE/BE | S | none | Not Started |
| **UC-002** | Sign Up with Facebook Login | FE/BE | S | UC-001 | Not Started |
| **UC-003** | Sign Up with Email and Password | FE/BE | S | UC-001 | Not Started |
| **UC-004** | Sign Up with Phone OTP | FE/BE | M | UC-001 | Not Started |
| **UC-005** | Sign In (All Methods) | FE/BE | S | UC-001, UC-003, UC-004 | Not Started |
| **UC-006** | Forgot Password & Reset Flow | FE/BE | S | UC-003 | Not Started |
| **UC-007** | Complete Profile Setup | FE/BE | S | UC-001 | Not Started |
| **UC-008** | View and Edit Profile | FE/BE | S | UC-007 | Not Started |
| **UC-009** | Silent Token Refresh | FE/BE | M | UC-005 | Not Started |
| **UC-010** | Role-Based Navigation Rendering | FE | S | UC-005 | Not Started |
| **UC-011** | Session-Expired Forced Re-Authentication | FE/BE | S | UC-009 | Not Started |
| **UC-012** | Splash Screen with Auto-Navigation | FE | S | UC-009 | Not Started |
| **UC-013** | Welcome & Onboarding Carousel | FE | S | none | Not Started |
| **UC-014** | Auto-Create Personal Organization | BE | S | UC-001 | Not Started |
| **UC-015** | View & Switch Active Organization | FE/BE | S | UC-014 | Not Started |
| **UC-016** | View Organization Member List & Roles | FE/BE | S | UC-014 | Not Started |
| **UC-024** | Add Vehicle with Typeahead Lookup | FE/BE | M | UC-014 | Not Started |
| **UC-025** | View Vehicle List | FE/BE | S | UC-024 | Not Started |
| **UC-026** | View Vehicle Detail Screen | FE/BE | S | UC-025 | Not Started |
| **UC-027** | Edit Vehicle Information | FE/BE | S | UC-026 | Not Started |
| **UC-034** | View Pre-Populated Maintenance Schedule | FE/BE | M | UC-024 | Not Started |
| **UC-035** | Customize Maintenance Schedule Items | FE/BE | S | UC-034 | Not Started |
| **UC-036** | Log Service Record | FE/BE | M | UC-034 | Not Started |
| **UC-037** | View Service History | FE/BE | S | UC-036 | Not Started |
| **UC-038** | Bulk Accept Maintenance Schedule | FE/BE | S | UC-034 | Not Started |
| **UC-064** | Consumer Dashboard with Vehicle Summary Cards | FE/BE | M | UC-025, UC-034 | Not Started |
| **UC-118** | Database Migration & Schema Seeding Infrastructure | BE | L | none | Not Started |

**Sprint 1 Goal:** Core minimum value loop functional. Sign up → Add vehicle → Pre-populated maintenance schedule → Log service. (27 Tickets)

---

### Sprint 2: Consumer Data Entry Loop — Fuel, Trip, Expense & Push Notifications (Days 16–30)

**Goal:** Complete data entry logging for fuel, trips, and expenses. FCM push notification pipeline operational for upcoming service alerts.

| Ticket | Use Case | Owner | Estimate | Depends on | Status |
|:---|:---|:---|:---|:---|:---|
| **UC-046** | Log Fuel Entry | FE/BE | M | UC-024 | Not Started |
| **UC-047** | View Fuel Log History | FE/BE | S | UC-046 | Not Started |
| **UC-048** | Edit Fuel Entry | FE/BE | S | UC-047 | Not Started |
| **UC-049** | Delete Fuel Entry | FE/BE | S | UC-047 | Not Started |
| **UC-050** | Calculate Fuel Efficiency (MPG / L/100km) | BE | M | UC-046 | Not Started |
| **UC-051** | Quick-Log Fuel from Dashboard | FE/BE | S | UC-046, UC-064 | Not Started |
| **UC-052** | Log Manual Trip Entry | FE/BE | M | UC-024 | Not Started |
| **UC-053** | View Trip History | FE/BE | S | UC-052 | Not Started |
| **UC-054** | Edit Trip Entry | FE/BE | S | UC-053 | Not Started |
| **UC-055** | Delete Trip Entry | FE/BE | S | UC-053 | Not Started |
| **UC-056** | Quick-Log Trip from Dashboard | FE/BE | S | UC-052, UC-064 | Not Started |
| **UC-057** | View Distance & Mileage Summary | FE/BE | S | UC-053 | Not Started |
| **UC-058** | Log Vehicle Expense | FE/BE | M | UC-024 | Not Started |
| **UC-059** | View Expense History | FE/BE | S | UC-058 | Not Started |
| **UC-060** | Edit Expense Entry | FE/BE | S | UC-059 | Not Started |
| **UC-061** | Delete Expense Entry | FE/BE | S | UC-059 | Not Started |
| **UC-062** | Quick-Log Expense from Dashboard | FE/BE | S | UC-058, UC-064 | Not Started |
| **UC-063** | Attach Receipt Photo to Expense/Fuel Log | FE/BE | M | UC-046, UC-058 | Not Started |
| **UC-065** | Cost Breakdown Charts per Vehicle | FE/BE | M | UC-046, UC-058 | Not Started |
| **UC-066** | Quick Actions Floating Button | FE | S | UC-064 | Not Started |
| **UC-072** | Request FCM Push Notification Permission | FE | S | UC-001 | Not Started |
| **UC-073** | Send Maintenance Overdue Push Notification | BE | M | UC-034, UC-072 | Not Started |
| **UC-074** | Send Maintenance Upcoming Push Notification | BE | M | UC-034, UC-072 | Not Started |
| **UC-075** | Background FCM Push Notification Handler | FE | S | UC-072 | Not Started |

**Sprint 2 Goal:** Complete consumer logging suite operational. Users can record fuel, trips, expenses, attach receipts, and receive service reminder push alerts. (24 Tickets)

---

### Sprint 3: Offline Sync Engine & Multi-Tenant Fleet Core (Days 31–45)

**Goal:** Mobile client can operate entirely offline with transactional batch sync (`POST /api/v1/sync/batch`). Fleet managers can invite drivers and manage org assets.

| Ticket | Use Case | Owner | Estimate | Depends on | Status |
|:---|:---|:---|:---|:---|:---|
| **UC-017** | Edit Organization Profile Details | FE/BE | S | UC-014 | Not Started |
| **UC-018** | Invite Driver / Manager via Email or Phone | FE/BE | M | UC-016 | Not Started |
| **UC-019** | Accept Organization Invitation (Existing User) | FE/BE | S | UC-018 | Not Started |
| **UC-020** | Redeem Org Invitation Code (New User) | FE/BE | M | UC-018 | Not Started |
| **UC-021** | Remove Member from Organization | FE/BE | S | UC-016 | Not Started |
| **UC-022** | Cancel Pending Member Invitation | FE/BE | S | UC-018 | Not Started |
| **UC-023** | Soft Delete Organization | BE | M | UC-014 | Not Started |
| **UC-028** | Delete Vehicle (Soft Delete & Audit Log) | FE/BE | S | UC-026 | Not Started |
| **UC-029** | Log Manual Odometer Update | FE/BE | S | UC-026 | Not Started |
| **UC-030** | Upload Vehicle Documents | FE/BE | M | UC-026 | Not Started |
| **UC-031** | Recover Deleted Vehicle | FE/BE | S | UC-028 | Not Started |
| **UC-032** | Assign Primary Driver to Vehicle | FE/BE | S | UC-018, UC-026 | Not Started |
| **UC-033** | Unassign Driver from Vehicle | FE/BE | S | UC-032 | Not Started |
| **UC-090** | Queue Local Entity Mutations in Offline SQLite DB | FE | L | UC-024, UC-046 | Not Started |
| **UC-091** | Background Network Reconnection Sync Listener | FE | M | UC-090 | Not Started |
| **UC-092** | Display Offline Mode Indicator Banner | FE | S | UC-090 | Not Started |
| **UC-093** | View Pending Sync Queue Status | FE | S | UC-090 | Not Started |
| **UC-094** | Client UUID v4 Primary Key Generation | FE | S | UC-090 | Not Started |
| **UC-095** | Incremental Delta Sync Payload Construction | FE | M | UC-090, UC-094 | Not Started |
| **UC-096** | Client-Side Sync Conflict Visual Resolution | FE | M | UC-095 | Not Started |
| **UC-097** | Idempotent Re-Sync Retry Logic | FE/BE | M | UC-095 | Not Started |
| **UC-119** | Sync Batch Transaction Engine (`POST /api/v1/sync/batch`) | BE | XL | UC-094, UC-095 | Not Started |

**Sprint 3 Goal:** Offline sync batch engine fully verified. Organizations can invite members, assign drivers to vehicles, and process multi-entity offline queues in a single DB transaction. (22 Tickets)

---

### Sprint 4: Monetization — Stripe/Safepay Payments, Ads & Ad-Gate Enforcement (Days 46–60)

**Goal:** Dual payment webhooks (Stripe & Safepay) operational. Free-tier rewarded ad playback unlocks permanent bonus vehicle/driver slots governed by ad-gate middleware.

| Ticket | Use Case | Owner | Estimate | Depends on | Status |
|:---|:---|:---|:---|:---|:---|
| **UC-080** | Initiate Pro Tier Subscription (Stripe Checkout) | FE/BE | M | UC-014 | Not Started |
| **UC-081** | Initiate Pro Tier Subscription (Safepay PK Checkout) | FE/BE | M | UC-014 | Not Started |
| **UC-082** | Handle Payment Checkout Failure & Cancellation | FE | S | UC-080, UC-081 | Not Started |
| **UC-083** | View Subscription Status & Billing History | FE/BE | S | UC-080 | Not Started |
| **UC-084** | Cancel Active Subscription | FE/BE | M | UC-083 | Not Started |
| **UC-085** | Process Subscription Downgrade (Pro → Free) | BE | L | UC-084 | Not Started |
| **UC-086** | Vehicle Quota Wall Enforcement Screen | FE/BE | M | UC-024, UC-080 | Not Started |
| **UC-087** | Driver Quota Wall Enforcement Screen | FE/BE | M | UC-018, UC-080 | Not Started |
| **UC-088** | Pro Upgrade Celebration Modal | FE | S | UC-080 | Not Started |
| **UC-089** | Contact Enterprise Sales Inquiry Form | FE/BE | S | UC-086 | Not Started |
| **UC-098** | Display AdMob Banner Ads (Free Tier Mobile) | FE | S | UC-014 | Not Started |
| **UC-099** | Play Rewarded Video Ad for Bonus Slot | FE | M | UC-086, UC-087 | Not Started |
| **UC-100** | Verify Rewarded Ad Completion Signature Token | BE | M | UC-099 | Not Started |
| **UC-101** | Render Ad-Free Experience for Pro Subscribers | FE | S | UC-080, UC-098 | Not Started |
| **UC-102** | Ad Delivery Fallback Grace Handler | FE | S | UC-099 | Not Started |
| **UC-120** | Ad-Rewarded Quota Lifecycle Engine | BE | L | UC-014, UC-022, UC-085, UC-099 | Not Started |
| **UC-121** | Dual Payment Gateway Webhook Reconciliation Engine | BE | L | UC-080, UC-081, UC-082 | Not Started |
| **UC-122** | Ad-Gate Signature Enforcement Protocol | BE | M | UC-099, UC-100 | Not Started |

**Sprint 4 Goal:** Platform revenue engine live. Users can purchase subscriptions via Stripe/Safepay or earn ad-rewarded bonus slots with middleware signature verification. (18 Tickets)

---

### Sprint 5: Fleet Intelligence, Driver Safety & Data Export (Days 61–75)

**Goal:** Fleet manager web dashboard operational. Driver safety consistency scoring calculated. Data exports available in PDF/CSV format.

| Ticket | Use Case | Owner | Estimate | Depends on | Status |
|:---|:---|:---|:---|:---|:---|
| **UC-039** | Add Custom Maintenance Service Item | FE/BE | S | UC-035 | Not Started |
| **UC-040** | Edit Existing Service Record | FE/BE | S | UC-037 | Not Started |
| **UC-041** | Delete Service Record (Soft Delete) | FE/BE | S | UC-037 | Not Started |
| **UC-042** | Filter & Search Service History | FE/BE | S | UC-037 | Not Started |
| **UC-043** | Maintenance Vendor Management | FE/BE | M | UC-036 | Not Started |
| **UC-044** | Perform Vehicle Inspection Checklist | FE/BE | M | UC-026 | Not Started |
| **UC-045** | Snooze / Defer Maintenance Alert | FE/BE | S | UC-073 | Not Started |
| **UC-067** | Fleet Manager Web Dashboard Layout | FE/BE | L | UC-014, UC-025 | Not Started |
| **UC-068** | Fleet Cost Ranking Table & Heatmap | FE/BE | M | UC-067 | Not Started |
| **UC-069** | Fleet Vehicle Availability Widget | FE/BE | M | UC-067 | Not Started |
| **UC-070** | Driver Safety Score Leaderboard Widget | FE/BE | M | UC-067, UC-103 | Not Started |
| **UC-071** | Customize Fleet Dashboard Widget Layout | FE | S | UC-067 | Not Started |
| **UC-076** | Notification Inbox Screen | FE/BE | S | UC-072 | Not Started |
| **UC-077** | Notification Preferences & Channel Config | FE/BE | S | UC-076 | Not Started |
| **UC-078** | Billing & Payment Alert Notifications | BE | S | UC-080, UC-081 | Not Started |
| **UC-079** | Automatically Purge Stale FCM Tokens | BE | S | UC-072 | Not Started |
| **UC-103** | Calculate Driver Consistency Score | BE | M | UC-032, UC-046, UC-052 | Not Started |
| **UC-104** | View Individual Driver Performance Detail | FE/BE | S | UC-103 | Not Started |
| **UC-105** | Driver Inactivity & Anomaly Alert Trigger | BE | M | UC-103 | Not Started |
| **UC-106** | Driver Safety Certificate Badge Generation | FE/BE | S | UC-103 | Not Started |
| **UC-110** | Export Maintenance History to PDF | FE/BE | M | UC-037 | Not Started |
| **UC-111** | Export Fuel & Expense Logs to CSV | FE/BE | S | UC-047, UC-059 | Not Started |
| **UC-112** | Generate & Email Monthly Fleet Summary PDF | BE | M | UC-067, UC-110 | Not Started |

**Sprint 5 Goal:** Fleet managers gain complete operational visibility, safety analytics, and automated PDF compliance reporting. (23 Tickets)

---

### Sprint 6: App Polish, Dark Mode, Locales & Final Hardening (Days 76–90)

**Goal:** Slate Teal / Charcoal dark mode implemented, metric/imperial conversions, Urdu RTL support, account deletion compliance, and launch regression testing.

| Ticket | Use Case | Owner | Estimate | Depends on | Status |
|:---|:---|:---|:---|:---|:---|
| **UC-107** | Toggle Theme (Light / Slate Teal Dark Mode) | FE | S | none | Not Started |
| **UC-108** | Apply Slate Teal / Charcoal Dark Palette | FE | S | UC-107 | Not Started |
| **UC-109** | System Theme Auto-Detection | FE | S | UC-107 | Not Started |
| **UC-113** | View App Settings Screen | FE | S | none | Not Started |
| **UC-114** | Configure Unit Preferences (Metric / Imperial) | FE/BE | S | UC-113 | Not Started |
| **UC-115** | Configure Locale & Language (English / Urdu RTL) | FE/BE | M | UC-113 | Not Started |
| **UC-116** | Request GDPR Account & Data Deletion | FE/BE | M | UC-001 | Not Started |
| **UC-117** | In-App Support Ticket Submission | FE/BE | S | UC-113 | Not Started |

**Sprint 6 Goal:** Production polish complete. All 122 tickets pass regression testing. App ready for public app store and web release. (8 Tickets)

---

## Phase 1 Gate — MVP Definition of Done

- [ ] All 122 UC tickets are marked **Done** with 100% automated test pass rate.
- [ ] Core journey (Sign Up → Add Vehicle → Pre-Populated Schedule → Log Service → Upgrade/Reward) verified.
- [ ] `POST /api/v1/sync/batch` passes multi-entity transaction ordering tests on SQLite.
- [ ] Dual payment webhooks (Stripe & Safepay) pass signature validation tests.
- [ ] Zero critical (P0) or high (P1) bugs open.

---

## Phase 2: Beta (Weeks 16–19)

**Goal:** Onboard 10–50 real vehicle owners and SMB fleet operators in Pakistan and international markets.

### Beta Checklist
- [ ] Sentry / GlitchTip error logging active for mobile and backend.
- [ ] PostHog event tracking instrumented for onboarding and quota walls.
- [ ] Database daily backup and restore verified.
- [ ] 5 non-technical users complete onboarding without assistance.

---

## Phase 3: Public Launch (Weeks 20–23)

### Pre-Launch Verification
- [ ] Security audit: CORS headers, JWT secret rotation, API rate limiting.
- [ ] `.\scripts\gcp_cloud_control.ps1 -Action start` executed for staging verification.
- [ ] Mobile build signed and submitted to Google Play Store.
- [ ] Production web app deployed to Cloud Run (scale-to-zero configured).

---

## Phase 4: Post-Launch Backlog & Roadmap

| Feature | Description | Target Phase |
|:---|:---|:---|
| **GPS Auto-Tracking** | Background location tracking for automatic trip classification. | Phase 4 (Sprint 7) |
| **AI Maintenance Predictor** | Machine learning predictions based on historical breakdown data. | Phase 4 (Sprint 8) |
| **iOS Native App** | iOS build compilation and Apple App Store release. | Phase 4 (Sprint 8) |

---

## Risk Register

| ID | Risk Description | Likelihood | Impact | Early Warning Sign | Mitigation Strategy |
|:---|:---|:---|:---|:---|:---|
| **RSK-001** | Offline sync batch transaction failure due to client/server ID drift. | Medium | High | `HTTP 409 Conflict` rate > 2% in logs. | Client generates UUID v4 locally; backend executes single DB transaction with topological order (`UC-119`). |
| **RSK-002** | Payment gateway (Safepay) webhook failure or signature mismatch. | Low | High | Webhook error log entries; pending subscriptions. | Webhook reconciliation engine (`UC-121`) logs raw payload to `gateway_payload` JSONB and permits idempotent re-processing. |
| **RSK-003** | Ad-gate signature bypass on ad-rewarded vehicles. | Medium | High | Vehicle mutations occurring without ad completion tokens. | FastAPI middleware (`UC-122`) intercepts and cryptographically validates `X-Ad-Reward-Token` prior to DB handler. |
| **RSK-004** | Solo developer velocity shortfall on 122 tickets. | Medium | Medium | Sprint completion rate < 80% at Sprint 3. | Sprints 5–6 contain lower-complexity UI polish (Theme, Settings); non-critical tickets can shift without breaking critical path. |

---

## Decision Log

| Date | Decision | Made By | Rationale |
|:---|:---|:---|:---|
| 2026-08-01 | All 122 UC tickets assigned across 6 two-week sprints. | Programme Mgr | Maintains 90-day timeline with zero feature cuts. |
| 2026-08-01 | Core Infra tickets (`UC-118`..`UC-122`) placed at critical dependency junctions. | Staff Architect | Ensures infrastructure logic is tested before dependent feature tickets ship. |
