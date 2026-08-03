# Master Product Requirements Document
# Veltrics — Fleet & Vehicle Management Platform [Version 1.0]

> **Document Type:** Master Product Requirements Document (PRD)  
> **Stage:** Stage 8 — Master PRD (Final Specification Synthesis)  
> **Persona:** Chief of Product  
> **Status:** ✅ Approved  
> **Last Updated:** 2026-08-02  
> **Reads from:** `01` · `01b` · `02` · `03` · `04` · `04b` · `05` · `06` · `06a` · `07` · `07a` · `07b`  
>
> **Intended Audience:** Founders, engineering leads, AI coding agents, QA engineers, designers, investors.  
> **Canonical Engineering Rules:** Repo root [`/AGENTS.md`](file:///e:/Non_Office/Dev_Space/vibe_skool/veltrics/AGENTS.md)  
> **Master Backlog & Trackers:** [`trackers/07-big-picture-tracker.md`](file:///e:/Non_Office/Dev_Space/vibe_skool/veltrics/trackers/07-big-picture-tracker.md)  

---

## 1. Executive Summary

### 1.1 Product Vision
Veltrics is a multi-tenant Fleet & Vehicle Management Platform serving single-vehicle consumers, small-to-medium commercial fleets (3–25 vehicles), and enterprise logistics networks across Pakistan and international markets. It replaces paper logbooks and bloated enterprise software with automated maintenance schedules, offline-first mobile transaction logging, driver safety scoring, and dual payment gateway subscription billing.

### 1.2 Core Hypothesis
If vehicle owners and fleet managers are provided with pre-populated maintenance schedules and an offline-first mobile logger, they will consistently log maintenance and operational data—unlocking higher vehicle resale values, lower downtime, and sustainable subscription/ad revenue.

### 1.3 Success Definition

| Time Horizon | Success Target | Key Metric |
|:---|:---|:---|
| **MVP Launch (Day 90)** | 100 active vehicle logs; zero critical sync data losses. | 100% test pass rate across all 122 UC tickets. |
| **3 Months Post-Launch** | 500 active vehicles; 50 Pro tier organizations onboarded. | Day-30 user retention > 45%; Monthly Recurring Revenue (MRR) growth. |
| **12 Months** | 5,000+ managed vehicles across Pakistan & South Asia. | > 60% conversion on rewarded video ad bonus quota triggers. |

### 1.4 Scale Profile
- **Target Market:** Pakistan (local payment via Safepay, Urdu RTL locale) and International (Stripe USD billing, English locale).
- **Scale Profile:** Regional MVP scaling to 100k+ concurrent connected devices. Architecture enforces dialect-agnostic SQLAlchemy models (SQLite local, PostgreSQL staging/prod on Cloud Run + Cloud SQL).

---

## 2. Problem & Market

### 2.1 Problem Statement
Vehicle owners and fleet managers lack an intuitive, localized platform to track routine servicing, fuel usage, trip logs, and driver accountability. Existing solutions are either generic expense trackers or overpriced enterprise telematics systems requiring expensive OBD-II hardware.

### 2.2 The Insight
80% of vehicle maintenance is predictable by odometer interval. Pre-populating manufacturer service schedules upon vehicle selection removes 90% of data entry friction, driving immediate user adoption.

### 2.3 Target Users

| Segment | Who They Are | Primary Pain Point | Value Driver / Trigger |
|:---|:---|:---|:---|
| **Consumer Owner** | Individual car/bike owners. | Forgets oil changes; loses service paper receipts. | Automatic service push reminders & PDF maintenance record export. |
| **SMB Fleet Manager** | Operates 3–25 commercial vehicles / delivery vans. | Unclear fuel theft, high downtime, driver misuse. | Fleet cost ranking heatmap, driver safety score, PDF/CSV export. |
| **Commercial Driver** | Appointed driver operating assigned fleet vehicle. | Complex logging forms; spotty cell connectivity. | 1-tap offline logging with client-side UUID generation. |

### 2.4 Competitive Differentiation
1. **Ad-Rewarded Quota Expansion:** Free users can earn +2 vehicle and +2 driver slots via rewarded video ads, unlocking up to 5 free vehicles/drivers without paying subscription fees.
2. **Dual Gateway Localization:** Native integration with Safepay (PKR) alongside Stripe (International USD).
3. **Offline-First Transaction Sync:** Full mobile functionality without internet connection, syncing seamlessly upon reconnect via `POST /api/v1/sync/batch`.

---

## 3. Business Model & Tier Limits

### 3.1 Monetization Tier Limits

| Feature / Resource | Free Tier | Pro Tier ($19/mo or Local PKR Equivalent) | Enterprise Tier |
|:---|:---|:---|:---|
| **Base Vehicles** | 3 Base | 25 Base | Up to 1,000 |
| **Bonus Ad Vehicles** | +2 via Rewarded Ads (Max: 5) | — (Ad-free) | — (Ad-free) |
| **Base Drivers** | 3 Base | 15 Base | Up to 1,000 |
| **Bonus Ad Drivers** | +2 via Rewarded Ads (Max: 5) | — (Ad-free) | — (Ad-free) |
| **Ad Experience** | Banners + Rewarded Videos | 100% Ad-Free | 100% Ad-Free |
| **Data Export (PDF/CSV)** | 🔒 Locked | ✅ Included | ✅ Included |
| **Driver Safety Scoring** | 🔒 Locked | ✅ Included | ✅ Included |

---

## 4. Architecture & Technology Stack

### 4.1 Tech Stack Summary
- **Mobile Frontend:** Flutter (Dart) targeting Android, iOS, and Web.
- **Backend API:** Python FastAPI + Pydantic v2 validation.
- **Local Dev Database:** SQLite (`sqlite:///./dev.db`). Zero Docker required.
- **Staging / Prod Database:** Managed PostgreSQL on GCP Cloud SQL (dialect-agnostic SQLAlchemy models).
- **Authentication:** Firebase Auth SDK on mobile with FastAPI JWT mock middleware for local dev.
- **Payment Gateways:** Stripe Webhooks + Safepay Webhooks writing to unified `subscriptions` table.

### 4.2 Local-First Execution & Git Branch Protocol
- **Git Branch Hierarchy:** `main` (Production) → `dev` (Staging) → `sprint/sprint-XX` (Feature/Ticket Work).
- **Phase 0 Setup:** Initial repo commit to `main` → checkout `dev` → checkout `sprint/sprint-01`. Flutter project creation (`flutter create mobile_frontend`) linked to Firebase Dev/Staging/Prod options (`flutterfire configure`).
- **Local Backend Runner:** `.\scripts\start_backend.ps1` (FastAPI + SQLite + Local Auth Emulator).
- **GCP Cost Control:** `.\scripts\gcp_cloud_control.ps1 -Action start|stop` strictly for staging verification.

---

## 5. Feature Requirements & Implementation Ticket Backlog

The complete backlog consists of **122 implementation-ready tickets** (`UC-001` through `UC-122`) detailed in `06a-use-case-tickets.md`:

- **EP-AUTH (UC-001..013):** Google One-Tap, Facebook Login, Email/Pass, Phone OTP, Silent JWT Refresh, Role Navigation, Session Expiry.
- **EP-ORG (UC-014..023):** Multi-Tenancy, Organization Profiles, Invites, Member Removal, Soft Delete.
- **EP-VEH (UC-024..033):** Vehicle Registry with Typeahead, Detail Screens, Driver Assignment, Document Uploads, Recovery.
- **EP-MNT (UC-034..045):** Pre-Populated Schedules, Custom Items, Log Service, Vendors, Inspection Checklists, Alert Snoozing.
- **EP-FUEL (UC-046..051):** Fuel Logs, Efficiency Calculation, Receipt Photos, Quick-Log Widgets.
- **EP-TRIP (UC-052..057):** Manual & GPS Trips, Distance Summaries, Quick-Log Widgets.
- **EP-EXP (UC-058..063):** Expense Records, Receipt Attachments, Categorization.
- **EP-DASH (UC-064..071):** Consumer & Fleet Manager Web Dashboards, Cost Rankings, Availability Widgets, Leaderboards.
- **EP-NOTIF (UC-072..079):** Push Notification Registration, Overdue Service Alerts, Preference Toggles, Token Cleanup.
- **EP-PAY (UC-080..089):** Stripe & Safepay Checkout Flows, Quota Wall Enforcement, Downgrade Processing, Enterprise Form.
- **EP-SYNC (UC-090..097):** Offline SQLite Queueing, Client UUID v4 Keys, Delta Payload Construction, Conflict Resolution.
- **EP-AD (UC-098..102):** AdMob Banners, Rewarded Video Ad Playback, Bonus Slot Lifecycle, Ad-Free Pro Enforcement.
- **EP-DRV (UC-103..106):** Driver Consistency Safety Scoring, Anomaly Alerts, Certificate Badges.
- **EP-THEME (UC-107..109):** Light / Slate Teal Dark Mode Theme Engine.
- **EP-EXPORT (UC-110..112):** PDF Maintenance History, CSV Data Export, Scheduled Monthly Email Reports.
- **EP-SET (UC-113..118):** Settings, Unit Conversions (Metric/Imperial), English/Urdu RTL Locale, Support Ticket, DB Seeding (`UC-118`).
- **CORE INFRA (UC-119..122):** Sync Batch Transaction Engine (`UC-119`), Ad-Rewarded Quota Lifecycle Engine (`UC-120`), Dual Webhook Reconciliation Engine (`UC-121`), Ad-Gate Signature Enforcement Protocol (`UC-122`).

---

## 6. 90-Day Build Roadmap & Phase 0 Setup Sequence

- **Phase 0 (Weeks 1–2):** Git setup (`main` → `dev` → `sprint/sprint-01`), Flutter boilerplate (`flutter create mobile_frontend`), Firebase Dev/Staging/Prod bindings (`flutterfire configure`), Theme application (`05b-flutter-theme.dart`), FastAPI & SQLite DB Seeding (`UC-118`).
- **Sprint 1 (Days 1–15):** Auth, Org Baseline, Vehicle CRUD, Maintenance Core (`UC-001`..`UC-016`, `UC-024`..`UC-027`, `UC-034`..`UC-038`, `UC-064`, `UC-118` — 27 Tickets).
- **Sprint 2 (Days 16–30):** Fuel, Trip, Expense Logging, Push Notifications (`UC-046`..`UC-063`, `UC-065`..`UC-066`, `UC-072`..`UC-075` — 24 Tickets).
- **Sprint 3 (Days 31–45):** Offline Sync Batch Engine & Multi-Tenant Core (`UC-017`..`UC-023`, `UC-028`..`UC-033`, `UC-090`..`UC-097`, `UC-119` — 22 Tickets).
- **Sprint 4 (Days 46–60):** Stripe/Safepay Payments, Ad Engine & Ad-Gate Middleware (`UC-080`..`UC-089`, `UC-098`..`UC-102`, `UC-120`..`UC-122` — 18 Tickets).
- **Sprint 5 (Days 61–75):** Fleet Intelligence Dashboard, Driver Safety Scoring & PDF/CSV Export (`UC-039`..`UC-045`, `UC-067`..`UC-071`, `UC-076`..`UC-079`, `UC-103`..`UC-106`, `UC-110`..`UC-112` — 23 Tickets).
- **Sprint 6 (Days 76–90):** Dark Mode, Unit Conversion, Urdu Locale, Account Deletion & Hardening (`UC-107`..`UC-109`, `UC-113`..`UC-117` — 8 Tickets).

---

## 7. Engineering Governance Summary

Project governance directives live at repo root [`/AGENTS.md`](file:///e:/Non_Office/Dev_Space/vibe_skool/veltrics/AGENTS.md):
- **Branch Strategy:** `main` (Production) ← `dev` (Staging) ← `sprint/sprint-XX` or `feature/` branches.
- **Merge Criteria:** 100% local test suite pass required prior to merging into `dev`.
- **TDD Mandate:** Tests created in `./tests/unit/` or `./tests/integration/` before implementation logic.
- **Tracker Rollup:** Live execution status maintained in `trackers/07-big-picture-tracker.md` and sprint trackers.

---

## Appendix — Master Specification Artifact Index

| Order | Artifact Path | Stage Name | Description |
|:---|:---|:---|:---|
| 0 | `product-specs/00-carry-forward-flags.md` | 📋 Flag Register | Open/Resolved architectural decisions and deferred flags. |
| 1 | `product-specs/01-product-brief.md` | Stage 1 | Vision, market insight, target user segments, problem statement. |
| 2 | `product-specs/01b-tech-stack.md` | ★ Tech Stack | Technical stack selections, libraries, testing frameworks. |
| 3 | `product-specs/02-architecture.md` | Stage 2 | System architecture diagrams, service boundaries, scale profile. |
| 4 | `product-specs/03-user-journeys.md` | Stage 3 | User journeys, emotional maps, full screen inventory. |
| 5 | `product-specs/04-feature-stories.md` | Stage 4 | Epics E1–E16, feature stories, acceptance criteria. |
| 6 | `product-specs/04b-mvp-scope.md` | ★ Scope Gate | Tier limit definitions, minimum value loop. |
| 7 | `product-specs/05-style-guide.md` | Stage 5 | Design tokens, typography, Slate Teal palette, motion rules. |
| 8 | `product-specs/05b-flutter-theme.dart` | Stage 5 Output | Theme code implementation. |
| 9 | `product-specs/06-data-model.md` | Stage 6 | Relational ERD, 18 entity schemas, state machines, API map. |
| 10 | `product-specs/06a-use-case-tickets.md` | ★ Tickets | 122 implementation-ready tickets (`UC-001` .. `UC-122`). |
| 11 | `product-specs/07-roadmap.md` | Stage 7 | 6-sprint development roadmap, phase gates, risk register. |
| 12 | `product-specs/07a-engineering-charter.md` | ★ Charter | Governance spec trail record (mirrored in root `/AGENTS.md`). |
| 13 | `product-specs/07b-integrity-review.md` | ★ Integrity | Specification integrity findings & audit report. |
| 14 | `product-specs/08-master-prd.md` | Stage 8 | **Master PRD (this document) — Master Synthesis** |
| 15 | `AGENTS.md` | Project Root | Canonical engineering governance directives. |
| 16 | `trackers/07-big-picture-tracker.md` | Trackers | Hierarchical master tracker tracking all 122 UC tickets. |
