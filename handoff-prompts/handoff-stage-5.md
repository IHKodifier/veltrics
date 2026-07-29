# Handoff Prompt: Stage 5 (Style Guide) Completed

> **Reads from:** [01-product-brief.md](file:///e:/Non_Office/Dev_Space/vibe_skool/veltrics/product-specs/01-product-brief.md), [01b-tech-stack.md](file:///e:/Non_Office/Dev_Space/vibe_skool/veltrics/product-specs/01b-tech-stack.md), [02-architecture.md](file:///e:/Non_Office/Dev_Space/vibe_skool/veltrics/product-specs/02-architecture.md), [03-user-journeys.md](file:///e:/Non_Office/Dev_Space/vibe_skool/veltrics/product-specs/03-user-journeys.md), [04-feature-stories.md](file:///e:/Non_Office/Dev_Space/vibe_skool/veltrics/product-specs/04-feature-stories.md), [04b-mvp-scope.md](file:///e:/Non_Office/Dev_Space/vibe_skool/veltrics/product-specs/04b-mvp-scope.md), [05-style-guide.md](file:///e:/Non_Office/Dev_Space/vibe_skool/veltrics/product-specs/05-style-guide.md), [05b-flutter-theme.dart](file:///e:/Non_Office/Dev_Space/vibe_skool/veltrics/product-specs/05b-flutter-theme.dart)  
> **Target Stage:** `★ DATA MODEL` (resulting in `06-data-model.md`)  
> **Status:** Approved & Ready for Handoff

---

## 1. Project State & Key Decisions Summary

The **Veltrics Fleet & Vehicle Management** platform has completed all foundational product definition and design system stages. All 8 core specification artifacts are approved.

- **Brand Personality:** Professional & Trustworthy + Friendly & Efficient dual-axis.
- **Design System:** Inter typeface, 12-token type scale, 4px spacing grid, pill-shaped primary buttons, outlined fields, Material Symbols Outlined icons.
- **Color System:** Three production-ready candidate palettes (Slate Teal, Amber/Orange, Forest Green/Emerald) fully specified with light/dark tokens. Swap via single `VeltricsPalette` enum in `05b-flutter-theme.dart`.
- **Dark Mode:** Deep charcoal (`#121212`) baseline with subtle per-palette undertone card surfaces.
- **Ad Styling:** De-emphasized card blend (90% opacity, muted border). Explicit no-ad zones on all 4 data entry forms (`SCR-FUEL-001`, `SCR-MNT-002`, `SCR-TRIP-001`, `SCR-EXP-001`).
- **Motion:** Staggered card reveal animation for Aha Moment maintenance schedule (350ms spring).

---

## 2. Approved Artifacts

- [01-product-brief.md](file:///e:/Non_Office/Dev_Space/vibe_skool/veltrics/product-specs/01-product-brief.md) — ✅ Approved
- [01b-tech-stack.md](file:///e:/Non_Office/Dev_Space/vibe_skool/veltrics/product-specs/01b-tech-stack.md) — ✅ Approved
- [02-architecture.md](file:///e:/Non_Office/Dev_Space/vibe_skool/veltrics/product-specs/02-architecture.md) — ✅ Approved
- [03-user-journeys.md](file:///e:/Non_Office/Dev_Space/vibe_skool/veltrics/product-specs/03-user-journeys.md) — ✅ Approved
- [04-feature-stories.md](file:///e:/Non_Office/Dev_Space/vibe_skool/veltrics/product-specs/04-feature-stories.md) — ✅ Approved
- [04b-mvp-scope.md](file:///e:/Non_Office/Dev_Space/vibe_skool/veltrics/product-specs/04b-mvp-scope.md) — ✅ Approved
- [05-style-guide.md](file:///e:/Non_Office/Dev_Space/vibe_skool/veltrics/product-specs/05-style-guide.md) — ✅ Approved
- [05b-flutter-theme.dart](file:///e:/Non_Office/Dev_Space/vibe_skool/veltrics/product-specs/05b-flutter-theme.dart) — ✅ Approved

---

## 3. Next Stage: ★ DATA MODEL

- **Next Persona:** Database Architect
- **Output:** `product-specs/06-data-model.md`
- **Focus:** Relational schema design (PostgreSQL 15+), entity-relationship diagram (ERD), table definitions, foreign keys, indexes, JSONB schemas, multi-tenant isolation via RLS, data access patterns, and offline Hive local database schemas.

---

## 4. Decision Record Summary (SDS-001 to SDS-010)

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
