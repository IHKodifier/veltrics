# Handoff Prompt: Stage 6 (Data Model & State) Completed

> **Reads from:** [01-product-brief.md](file:///e:/Non_Office/Dev_Space/vibe_skool/veltrics/product-specs/01-product-brief.md), [01b-tech-stack.md](file:///e:/Non_Office/Dev_Space/vibe_skool/veltrics/product-specs/01b-tech-stack.md), [02-architecture.md](file:///e:/Non_Office/Dev_Space/vibe_skool/veltrics/product-specs/02-architecture.md), [03-user-journeys.md](file:///e:/Non_Office/Dev_Space/vibe_skool/veltrics/product-specs/03-user-journeys.md), [04-feature-stories.md](file:///e:/Non_Office/Dev_Space/vibe_skool/veltrics/product-specs/04-feature-stories.md), [04b-mvp-scope.md](file:///e:/Non_Office/Dev_Space/vibe_skool/veltrics/product-specs/04b-mvp-scope.md), [05-style-guide.md](file:///e:/Non_Office/Dev_Space/vibe_skool/veltrics/product-specs/05-style-guide.md), [05b-flutter-theme.dart](file:///e:/Non_Office/Dev_Space/vibe_skool/veltrics/product-specs/05b-flutter-theme.dart), [06-data-model.md](file:///e:/Non_Office/Dev_Space/vibe_skool/veltrics/product-specs/06-data-model.md)  
> **Target Stage:** `★ DEVELOPMENT ROADMAP` (resulting in `07-roadmap.md`)  
> **Status:** Approved & Ready for Handoff

---

## 1. Project State & Key Decisions Summary

The **Veltrics Fleet & Vehicle Management** platform has completed Stage 6 (Data Model & State). All 9 core product specification artifacts are approved and fully consistent.

- **Data Architecture:** PostgreSQL 15+ (Cloud SQL) with 14 core tables. Every tenant table includes an `organization_id` tenant key and `sharding_key` column for horizontal Citus/partitioning readiness.
- **Identity & Auth Providers:** 4 supported Firebase Auth sign-in methods: Email/Password, Google Sign-In, Facebook Login, and Phone OTP. `auth_provider` and `linked_providers` JSONB fields stored on `users` entity.
- **Primary Keys:** UUID v4 (`gen_random_uuid()`) for all API-exposed domain entities.
- **Soft Deletes:** `deleted_at TIMESTAMP WITH TIME ZONE NULL` implemented across all domain entities with partial B-Tree indexes (`WHERE deleted_at IS NULL`).
- **Offline Sync:** Flutter Hive local boxes (`hive_vehicles`, `hive_fuel_queue`, `hive_maintenance_queue`, `hive_trip_queue`, `hive_sync_meta`) with timestamped sync flags and server-wins conflict resolution.
- **JSONB Schemas:** Formal Pydantic/JSON schemas for vehicle custom specs, multi-point maintenance checklists, and billing gateway metadata.
- **Audit Logging:** System-wide immutable `audit_logs` table tracking all mutations.

---

## 2. Approved Artifacts

- [01-product-brief.md](file:///e:/Non_Office/Dev_Space/vibe_skool/veltrics/product-specs/01-product-brief.md) — ✅ Approved
- [01b-tech-stack.md](file:///e:/Non_Office/Dev_Space/vibe_skool/veltrics/product-specs/01b-tech-stack.md) — ✅ Approved (Updated with Facebook Auth)
- [02-architecture.md](file:///e:/Non_Office/Dev_Space/vibe_skool/veltrics/product-specs/02-architecture.md) — ✅ Approved (Updated with Facebook Auth)
- [03-user-journeys.md](file:///e:/Non_Office/Dev_Space/vibe_skool/veltrics/product-specs/03-user-journeys.md) — ✅ Approved (Updated with Facebook Auth)
- [04-feature-stories.md](file:///e:/Non_Office/Dev_Space/vibe_skool/veltrics/product-specs/04-feature-stories.md) — ✅ Approved (Updated with Facebook Auth)
- [04b-mvp-scope.md](file:///e:/Non_Office/Dev_Space/vibe_skool/veltrics/product-specs/04b-mvp-scope.md) — ✅ Approved
- [05-style-guide.md](file:///e:/Non_Office/Dev_Space/vibe_skool/veltrics/product-specs/05-style-guide.md) — ✅ Approved
- [05b-flutter-theme.dart](file:///e:/Non_Office/Dev_Space/vibe_skool/veltrics/product-specs/05b-flutter-theme.dart) — ✅ Approved
- [06-data-model.md](file:///e:/Non_Office/Dev_Space/vibe_skool/veltrics/product-specs/06-data-model.md) — ✅ Approved

---

## 3. Next Stage: STAGE 7 — DEVELOPMENT ROADMAP

- **Next Persona:** Engineering Programme Manager
- **Output:** `product-specs/07-roadmap.md`
- **Focus:** 90-day execution roadmap divided into 6 two-week sprints (Sprints 1–6), task dependency graph, critical path analysis, risk mitigation strategies, and Definition of Done (DoD).

---

## 4. Decision Record Summary (SDS-001 to SDS-016)

| ID | Decision | Summary |
|:---|:---|:---|
| SDS-001 | 3 Candidate Palettes | Slate Teal, Amber, Forest Green tokenized & implemented in Dart |
| SDS-002 | Typeface | Inter as sole UI typeface, Roboto Mono for numbers/codes |
| SDS-003 | Dark Mode Baseline | Deep charcoal (`#121212`) |
| SDS-004 | Ad Components | De-emphasized card blend (90% opacity, muted border) |
| SDS-005 | No-Ad Zones | SCR-FUEL-001, SCR-MNT-002, SCR-TRIP-001, SCR-EXP-001 |
| SDS-006 | Button Shape | Pill-shaped primary buttons (`radius-full`) |
| SDS-007 | Input Style | Outlined input fields (6px radius) |
| SDS-008 | Dashboard Density | Balanced (48px table rows, 16px padding) |
| SDS-009 | Navigation | Collapsible sidebar on desktop Chrome, 4-item bottom nav on Android |
| SDS-010 | Quota Wall Tone | Avoid error-red; keep tone motivating |
| SDS-011 | Multi-Tenant Isolation | Shared database with `organization_id` on all tables + sharding key readiness |
| SDS-012 | Primary Keys | UUID v4 (`gen_random_uuid()`) for all API domain entities |
| SDS-013 | Soft Delete Policy | Soft deletes via `deleted_at TIMESTAMPTZ NULL` on all domain entities |
| SDS-014 | Offline Sync Protocol | Client-generated UUIDs + Timestamped Sync Flag in Flutter Hive (Server-Wins) |
| SDS-015 | JSONB Usage Boundary | Strict relational columns for core metrics; JSONB for dynamic checklists & custom specs |
| SDS-016 | Auth Providers | 4 supported providers: Email/password, Google Sign-In, Facebook Login, Phone OTP |
