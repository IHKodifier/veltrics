# Engineering Charter: Veltrics Fleet & Vehicle Management Platform

> **Stage:** Stage 07a — Engineering Charter Interlude  
> **Persona:** Founding Engineer  
> **Status:** ✅ Approved  
> **Reads from:** [01b-tech-stack.md](file:///e:/Non_Office/Dev_Space/vibe_skool/veltrics/product-specs/01b-tech-stack.md) · [06a-use-case-tickets.md](file:///e:/Non_Office/Dev_Space/vibe_skool/veltrics/product-specs/06a-use-case-tickets.md) · [07-roadmap.md](file:///e:/Non_Office/Dev_Space/vibe_skool/veltrics/product-specs/07-roadmap.md) · [07c-gcp-cost-minimization-and-skill-plan.md](file:///e:/Non_Office/Dev_Space/vibe_skool/veltrics/product-specs/07c-gcp-cost-minimization-and-skill-plan.md)  
> **Canonical Location:** Repo root [`/AGENTS.md`](file:///e:/Non_Office/Dev_Space/vibe_skool/veltrics/AGENTS.md)  

---

## Executive Summary & Engineering Governance

The Engineering Charter establishes project-specific engineering rules, execution boundaries, and automated tracker maintenance structures for the Veltrics platform. It integrates local-first zero-cloud development rules, TDD mandates, and git workflow protection directly into the agent runtime environment.

### Core Directives Summary
1. **Canonical Governance File:** Canonical rules live exclusively at `/AGENTS.md` at the repository root.
2. **Local-First Baseline:** Zero Docker overhead during routine coding. Local development uses `.\scripts\start_backend.ps1` with SQLite (`sqlite:///./dev.db`) and local JWT auth emulator.
3. **GCP Cost Protection:** GCP Cloud SQL instances are strictly controlled via `.\scripts\gcp_cloud_control.ps1 -Action start|stop` for staging verification only.
4. **Git Branching Protocol:** `main` is protected production. Staging is `dev`. All feature tickets execute on `sprint/sprint-XX` or `feature/` branches. Merge into `dev` requires 100% test pass.
5. **Tracker Rollup Structure:** Three-tier tracker system (`07-big-picture-tracker.md` → `07.01-tracker.md` → `07.01.XX-tracker.md`).

---

## Tracker Infrastructure Map

The complete ticket backlog from `06a-use-case-tickets.md` (UC-001 through UC-122) is populated into the project tracker hierarchy:

```
trackers/
├── 07-big-picture-tracker.md          # Master Tracker (Rollup of all phases & sprints)
└── stage-01/
    ├── 07.01-tracker.md               # Stage 01 Stage Tracker
    └── sprints/
        ├── 07.01.01-tracker.md        # Sprint 1 Tracker (Auth, Org, Vehicle, Mnt Core, DB Seed)
        ├── 07.01.02-tracker.md        # Sprint 2 Tracker (Fuel, Trip, Expense, Push Notif)
        ├── 07.01.03-tracker.md        # Sprint 3 Tracker (Offline Sync Engine, Org Admin, Drivers)
        ├── 07.01.04-tracker.md        # Sprint 4 Tracker (Payments, Ads, Quota Walls, Ad-Gate)
        ├── 07.01.05-tracker.md        # Sprint 5 Tracker (Fleet Dashboard, Scoring, PDF/CSV Export)
        └── 07.01.06-tracker.md        # Sprint 6 Tracker (Theme, Settings, Urdu RTL, Hardening)
```

---

## Enforcement Checklist

- [x] Canonical `/AGENTS.md` written to repo root.
- [x] Hierarchical trackers created and populated with all 122 UC tickets (`trackers/`).
- [ ] Git branch protection configured on remote repository for `main` and `dev`.
- [ ] Pre-push test runner configured to execute `pytest tests/ -v` prior to `git push`.
