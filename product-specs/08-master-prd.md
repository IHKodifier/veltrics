# Veltrics Fleet & Vehicle Management — Master Product Requirement Document (Master PRD)

> **Reads from:** [01-product-brief.md](file:///e:/Non_Office/Dev_Space/vibe_skool/veltrics/product-specs/01-product-brief.md), [01b-tech-stack.md](file:///e:/Non_Office/Dev_Space/vibe_skool/veltrics/product-specs/01b-tech-stack.md), [02-architecture.md](file:///e:/Non_Office/Dev_Space/vibe_skool/veltrics/product-specs/02-architecture.md), [03-user-journeys.md](file:///e:/Non_Office/Dev_Space/vibe_skool/veltrics/product-specs/03-user-journeys.md), [04-feature-stories.md](file:///e:/Non_Office/Dev_Space/vibe_skool/veltrics/product-specs/04-feature-stories.md), [04b-mvp-scope.md](file:///e:/Non_Office/Dev_Space/vibe_skool/veltrics/product-specs/04b-mvp-scope.md), [05-style-guide.md](file:///e:/Non_Office/Dev_Space/vibe_skool/veltrics/product-specs/05-style-guide.md), [05b-flutter-theme.dart](file:///e:/Non_Office/Dev_Space/vibe_skool/veltrics/product-specs/05b-flutter-theme.dart), [06-data-model.md](file:///e:/Non_Office/Dev_Space/vibe_skool/veltrics/product-specs/06-data-model.md), [07-roadmap.md](file:///e:/Non_Office/Dev_Space/vibe_skool/veltrics/product-specs/07-roadmap.md), [07b-integrity-review.md](file:///e:/Non_Office/Dev_Space/vibe_skool/veltrics/product-specs/07b-integrity-review.md), [07c-gcp-cost-minimization-and-skill-plan.md](file:///e:/Non_Office/Dev_Space/vibe_skool/veltrics/product-specs/07c-gcp-cost-minimization-and-skill-plan.md)  
> **Status:** ✅ Approved & Definitive Master Specification  
> **Author:** Chief of Product Persona (App Architect)  
> **Target Release Date:** January 1, 2027 (10 Sprints across 3 Isolated Environment Tiers)

---

## 1. Executive Vision & Strategic Positioning

**Veltrics Fleet & Vehicle Management** is an enterprise-grade, multi-tenant SaaS platform designed to manage individual vehicles and commercial fleets seamlessly from a single unified ecosystem. 

Veltrics intentionally decouples fleet asset governance from hardware OBD-II telematics, focusing instead on **high-reliability maintenance scheduling, total cost of ownership (TCO) financial auditing, driver assignment, fuel logging, and offline-first operational synchronization**.

```mermaid
graph TD
    Consumer[Individual Consumer / Family] -->|Free Tier / Ad-Rewarded| CorePlatform[Veltrics Engine]
    SMB[SMB Fleet Manager] -->|Pro Subscription| CorePlatform
    Enterprise[Enterprise Fleet Director] -->|Enterprise Custom SaaS| CorePlatform

    CorePlatform --> International[International Operations\nStripe Payments + FCM]
    CorePlatform --> Pakistan[Pakistan Operations\nSafepay Payments + SMS / FCM Alerts]

    CorePlatform --> LocalTDD[Local Zero-Cloud TDD\nFastAPI + Uvicorn + SQLite]
    CorePlatform --> GCPCloud[GCP Cloud Infrastructure\nCloud Run + Cloud SQL PostgreSQL]
```

### 1.1 Strategic Highlights & Core Differentiators
1. **Enterprise Fleet & Asset Focus (Non-Telematics):** Solves vehicle upkeep, financial auditing, asset lifecycle status tracking, and compliance without requiring expensive or proprietary OBD-II GPS hardware.
2. **Dual-Market Regionalization:** Operates seamlessly across International markets (Stripe gateway billing, FCM push notifications) and Pakistan regional markets (Safepay payment gateway, SMS dispatch/alert support, PKR/USD currency localization).
3. **Offline-First Resilience:** Equips mobile drivers and field managers with offline transactional queues that automatically batch sync with topological integrity upon network re-connection.
4. **Zero-Cloud Local TDD Architecture:** Guarantees 100% database dialect parity across SQLite local development (`sqlite:///./dev.db`) and GCP Cloud SQL PostgreSQL in staging and production, strictly capping monthly non-production GCP costs (<$15/mo).

---

## 2. Multi-Platform System Architecture & Tech Stack

Veltrics enforces absolute separation between the client presentation layer and backend database models, routing 100% of data traffic through strongly-typed REST API endpoints governed by Pydantic payloads.

```mermaid
graph TB
    subgraph Clients["Presentation Layer (Flutter 3.x)"]
        MobileApp["Android Mobile App\n(Offline-First Sync Engine)"]
        WebApp["Chrome Desktop Web App\n(Fleet Ops Dashboard)"]
    end

    subgraph Gateway["API & Security Layer (FastAPI)"]
        AuthMiddleware["Firebase Auth Emulator / Identity Engine"]
        RESTAPI["FastAPI REST Router\n(Pydantic Payload Validation)"]
        BatchSyncEngine["Topological Batch Sync Processor\nPOST /api/v1/sync/batch"]
    end

    subgraph DataLayer["Persistence Layer (SQLAlchemy 2.0 ORM)"]
        TypeWrappers["Dialect-Agnostic Type Handlers\n(UUIDString & JSON Native/Text)"]
        LocalDB[("Local Dev DB\nSQLite (dev.db)")]
        CloudDB[("GCP Staging / Prod DB\nCloud SQL (PostgreSQL 15)")]
    end

    MobileApp -->|HTTPS / REST| RESTAPI
    WebApp -->|HTTPS / REST| RESTAPI
    RESTAPI --> AuthMiddleware
    RESTAPI --> BatchSyncEngine
    BatchSyncEngine --> TypeWrappers
    TypeWrappers -->|Local Env| LocalDB
    TypeWrappers -->|Staging & Prod Envs| CloudDB
```

### 2.1 Approved Technology Stack Summary

| Infrastructure Layer | Standardized Technology | Purpose & Environment Execution |
| :--- | :--- | :--- |
| **Frontend Framework** | Flutter 3.x (Dart 3.x) | Single codebase for Android Mobile App and Chrome Desktop Web App. |
| **State Management** | Flutter Riverpod 3.x | Reactive state management with offline persistence providers. |
| **Backend Framework** | FastAPI (Python 3.11+) | Asynchronous REST API service with automated OpenAPI specification generation. |
| **Data Validation** | Pydantic v2 | Strict request/response payload validation and schema enforcement. |
| **ORM & Database** | SQLAlchemy 2.0 + SQLite / PostgreSQL | Dialect-agnostic database access supporting SQLite locally and PostgreSQL on GCP. |
| **Authentication** | Firebase Auth (Local Emulator / Cloud) | JWT Bearer token authentication supporting email/password and phone OTP. |
| **Payment Gateways** | Stripe (Intl) & Safepay (PK) | Webhook-driven multi-currency subscription processing and quota management. |
| **Cloud Hosting** | GCP Cloud Run & GCP Cloud SQL | Serverless API execution paired with managed PostgreSQL (Staging/Production). |

---

## 3. Target User Personas & Journey Specifications

Veltrics caters to three primary user tiers with tailored user journeys and permission levels.

```mermaid
journey
    title Veltrics User Journey Lifecycle
    section Consumer Onboarding
      Download App & Login: 5: Consumer
      Add First Vehicle & Set Reminders: 5: Consumer
      Log Fuel Entry: 4: Consumer
    section SMB Fleet Operations
      Register Organization & Invite Drivers: 5: SMB Manager
      Assign Drivers to Vehicles: 5: SMB Manager
      Log Maintenance & Track Expenses: 4: SMB Manager, Driver
      Review TCO Summary & Export CSV: 5: SMB Manager
    section Enterprise Governance
      Multi-Tenant Branch Configuration: 5: Enterprise Director
      Custom RBAC Role Assignment: 5: Enterprise Director
      Audit Log Compliance Verification: 5: Enterprise Director
```

### 3.1 Persona Profiles & Feature Matrix

| Persona Class | Operational Focus | Primary Interface | Key Permissions & Limits |
| :--- | :--- | :--- | :--- |
| **Consumer (Free)** | Individual Vehicle Owners & Families | Android Mobile App | - Max 3 Vehicles (+2 via ad rewards = 5 max)<br>- Max 3 Drivers (+2 via ad rewards = 5 max)<br>- Maintenance alerts, fuel logging, basic expense recording. |
| **SMB Fleet Manager (Pro)** | Rental Operators, Logistics SMBs | Chrome Desktop Web + Android Mobile | - Up to 25 Vehicles & 25 Drivers<br>- Ad-free experience, PDF/CSV financial exports.<br>- Driver assignment, maintenance status updates. |
| **Enterprise Fleet Director** | Multi-Branch Logistics & Rental | Chrome Desktop Web App | - Unlimited Vehicles & Custom Driver Quotas<br>- Role-based access control (RBAC), immutable audit logs.<br>- Dedicated reporting and enterprise support SLAs. |

---

## 4. Complete Feature Matrix & Acceptance Criteria

All user stories are prioritized across P0 (Critical MVP), P1 (High Priority), and P2 (Enhancement).

### 4.1 Feature Stories & Testable Criteria (P0 / P1 / P2)

| Story ID | Epic | Feature Description | Priority | Testable Acceptance Criteria |
| :--- | :--- | :--- | :--- | :--- |
| **US-001** | Identity | Organization Registration & Multi-Tenant Setup | P0 | Given a new admin, when registering an organization, then create the tenant with free quota limits and initialize default roles. |
| **US-002** | Identity | User Authentication & JWT Session Management | P0 | Given valid credentials, when authenticating via Firebase Auth, then return a signed JWT bearer token containing `org_id` and `role`. |
| **US-003** | Assets | Vehicle Lifecycle Registration & Profile Management | P0 | Given vehicle specifications (VIN, License, Make, Model, Odometer), when created, default status to `ACTIVE` and enforce organization limits. |
| **US-004** | Operations | Maintenance Scheduling & Alert Generation | P0 | Given date or odometer thresholds, when maintenance is due, trigger alert status (`SCHEDULED` → `OVERDUE`) and send notification. |
| **US-005** | Operations | Granular Service Logging | P0 | Given a completed service item (e.g. Engine Oil, Brake Pads), when logged, update vehicle current odometer and record cost in financial audit. |
| **US-006** | Operations | Fuel Entry Logging & Consumption Analysis | P0 | Given fuel volume, cost, and odometer reading, calculate distance traveled and MPG / km-per-liter efficiency metrics. |
| **US-007** | Operations | General Expense & Cost Recording | P0 | Given non-maintenance costs (tolls, parking, repairs), assign expenses to vehicle records and attribute category tags. |
| **US-008** | Offline Engine| Topological Batch Sync Endpoint | P0 | Given an offline device re-connecting, process `POST /api/v1/sync/batch` in strict topological order (`orgs` → `users` → `vehicles` → `drivers` → `logs`). |
| **US-009** | Monetization| Ad-Rewarded Asset Quota Expansion | P1 | Given a Free tier user watching an in-app reward ad, permanently attach +1 vehicle/driver slot up to the hard cap of 5 total assets. |
| **US-010** | Monetization| Stripe Payment Gateway Subscription Sync | P1 | Given international checkout completion, process Stripe webhook to elevate organization status to `ACTIVE` Pro tier. |
| **US-011** | Monetization| Safepay Payment Gateway Webhook Handler | P1 | Given Pakistan Safepay checkout success, normalize transaction status and persist raw webhook JSON in `subscriptions.gateway_payload`. |
| **US-012** | Analytics | Fleet Financial TCO Summary Dashboard | P1 | Given selected date ranges, compute total fleet expenditure per vehicle, per driver, and cost per kilometer. |
| **US-013** | Compliance | Immutable System Audit Logging | P2 | Given sensitive operations (role elevation, asset deletion), record immutable audit log entries with user ID, IP address, and payload delta. |

### 4.2 Explicitly Descoped MVP Scope (Phase 1 Non-Goals)
- **OBD-II Hardware / Live Telematics Streaming:** Zero reliance on physical vehicle tracking hardware.
- **AI-Powered Predictive Maintenance Scoring:** Machine learning failure analysis deferred to Phase 2.
- **OCR Automated Receipt Scanning:** Optical character recognition for fuel/service receipts deferred to Phase 2.
- **Native iOS Application:** Native iOS binary build deferred until Phase 2 rollout.

---

## 5. Data Model, State Lifecycles & Dialect Parity

To ensure seamless execution across local zero-cloud development (`SQLite`) and production GCP infrastructure (`PostgreSQL`), all database schemas utilize custom SQLAlchemy type wrappers: `UUIDString` (maps to `CHAR(36)` on SQLite and native `UUID` on PostgreSQL) and `JSON` (maps to `JSON` / `TEXT` on SQLite and native `JSONB` on PostgreSQL).

```mermaid
erDiagram
    ORGANIZATIONS ||--o{ USERS : employs
    ORGANIZATIONS ||--o{ VEHICLES : owns
    ORGANIZATIONS ||--o{ SUBSCRIPTIONS : billed_via
    VEHICLES ||--o{ DRIVERS : assigned_to
    VEHICLES ||--o{ MAINTENANCE_LOGS : requires
    VEHICLES ||--o{ FUEL_LOGS : consumes
    VEHICLES ||--o{ EXPENSES : incurs
    USERS ||--o{ AUDIT_LOGS : executes

    ORGANIZATIONS {
        string id PK
        string name
        string tier
        int bonus_vehicle_slots
        datetime created_at
    }

    VEHICLES {
        string id PK
        string org_id FK
        string vin
        string license_plate
        string status
        int current_odometer
    }

    MAINTENANCE_LOGS {
        string id PK
        string vehicle_id FK
        string service_category
        string status
        float total_cost
        datetime performed_at
    }

    FUEL_LOGS {
        string id PK
        string vehicle_id FK
        float fuel_amount
        float total_cost
        int odometer_reading
    }
```

### 5.1 Primary Entity Lifecycles & State Transitions

```mermaid
stateDiagram-v2
    [*] --> VehicleActive : Register Asset
    VehicleActive --> MaintenanceDue : Trigger Date/Odometer Threshold
    MaintenanceDue --> UnderMaintenance : Schedule Service Entry
    UnderMaintenance --> VehicleActive : Complete Maintenance Log
    VehicleActive --> Decommissioned : Retire Asset
    Decommissioned --> [*]

    note right of MaintenanceDue
        Triggers FCM Push Notification
        or SMS Alert (Pakistan Region)
    end note
```

```mermaid
stateDiagram-v2
    [*] --> SubscribedActive : Webhook Checkout Success
    SubscribedActive --> PastDue : Payment Failed (Retry Period)
    PastDue --> SubscribedActive : Recovery Payment Success
    PastDue --> Cancelled : Grace Period Expired
    SubscribedActive --> Cancelled : User Cancelled Subscription
    Cancelled --> [*] : Revert Org to Free Tier Quotas
```

---

## 6. Design System & UI Components

Veltrics implements a dark-mode first design system tailored for high readability in automotive field conditions and desktop fleet operations.

### 6.1 Color Palette & Visual Tokens

| Design Token | Color Hex Code | Application Purpose |
| :--- | :--- | :--- |
| **Primary Brand Blue** | `#1E88E5` | Primary buttons, active tab indicators, key navigation links. |
| **Accent Electric Cyan** | `#00E5FF` | Highlight badges, metric callouts, interactive toggles. |
| **Background Charcoal** | `#121212` | Main application background (Dark Mode default). |
| **Surface Dark Slate** | `#1E1E1E` | Card containers, modal popups, table background surfaces. |
| **Status Warning Gold** | `#FFB300` | Maintenance scheduled alerts, upcoming inspection warnings. |
| **Status Critical Red** | `#E53935` | Overdue maintenance, payment past-due alerts, vehicle out-of-service. |
| **Status Success Green** | `#43A047` | Active vehicle status, completed maintenance logs, sync complete. |

---

## 7. Development Roadmap, Release Gates & Cost Governance

Development is structured into **10 Sprints across 3 Isolated Environment Tiers**, culminating in the target production release on **January 1, 2027**.

```mermaid
gantt
    title Veltrics 10-Sprint Execution Timeline (Jan 1, 2027 Production Launch)
    dateFormat  YYYY-MM-DD
    section Foundation & Data
    Sprint 01 (Auth & Multi-Tenant Setup)    :a1, 2026-08-01, 14d
    Sprint 02 (Vehicle & Driver Schema)      :a2, after a1, 14d
    section Core Operations
    Sprint 03 (Maintenance Alert Engine)     :a3, after a2, 14d
    Sprint 04 (Fuel & Expense Auditing)       :a4, after a3, 14d
    Sprint 05 (Offline Topological Sync)     :a5, after a4, 14d
    section Desktop & Client
    Sprint 06 (Chrome Desktop Dashboard)     :a6, after a5, 14d
    Sprint 07 (Android Mobile UI Refinement) :a7, after a6, 14d
    section Monetization & Staging
    Sprint 08 (Stripe & Safepay Gateways)    :a8, after a7, 14d
    Sprint 09 (GCP Staging & Dialect Audit)  :a9, after a8, 14d
    section Launch & Release Gate
    Sprint 10 (Production Release & Polish)  :a10, after a9, 14d
```

### 7.1 Mandatory Production Release Gate KPIs

Before merging the final `dev` branch into `main` for production release, 100% of the following Release Gate KPIs must be empirically validated:

1. **100% Dialect Parity & Zero Sync Data Loss:** 100% automated pass rate across both local SQLite unit/integration test suites and GCP Cloud SQL PostgreSQL staging test suites. Topological offline batch processing (`POST /api/v1/sync/batch`) must execute zero-data-loss recovery.
2. **Sub-200ms API Latency under 3G Mobile Simulation:** All core REST API endpoints (vehicle list, maintenance log entry, fuel record submit) must achieve `<200ms` response times under simulated high-latency 3G mobile network conditions.
3. **Strict Non-Production GCP Cost Limit (<$15/mo):** GCP Cloud SQL staging instances must be automatically managed via `.\scripts\gcp_cloud_control.ps1 -Action start/stop` to guarantee zero redundant cloud charges during non-coding windows.

---

## 8. Specification Integrity Review Resolutions

The following structural conflicts identified during the Stage 7b Integrity Review (`product-specs/07b-integrity-review.md`) have been fully resolved in this Master PRD:

1. **Dialect Parity Standard:** Enforced `UUIDString` and `JSON` ORM type wrappers so SQLite local development matches GCP PostgreSQL staging without Docker overhead.
2. **Topological Batch Ingestion Order:** Enforced strict entity ingestion order in `POST /api/v1/sync/batch`: `organizations` → `users` → `vehicles` → `drivers` → `fuel_logs` / `maintenance_logs` / `expenses` to prevent foreign key dependency violations.
3. **Multi-Gateway Payment Status Normalization:** Standardized subscription status mappings (`ACTIVE`, `PAST_DUE`, `CANCELLED`) for Stripe and Safepay webhooks, retaining full raw payloads in `gateway_payload` JSON fields.
4. **Ad-Rewarded Quota Lifecycle:** Standardized Free Tier ad rewards to attach directly to `organization` records, hard-capping total free slots at 5 vehicles and 5 drivers.

---

## 9. PRD Change Control & Governance

Any post-approval modifications to this Master PRD during Sprint implementation must be explicitly recorded in the version log below with engineering rationale and approval sign-offs.

| Version | Sprint ID | Date | Author / Role | Section Updated | Description & Rationale | Approver Sign-Off |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **1.0.0** | Baseline | 2026-07-29 | Chief of Product | All Sections | Baseline Master PRD synthesized from approved Stage 01–07b specs. | Lead Architect & TPM |
