# Handoff: Begin Phase 0 Foundation & Sprint 1 Setup

> Paste this into your new chat session:
> *"Resume app-architect — Ticket Dispatch & Execution Mode. All 11 planning stages are approved. Read `handoff-prompts/sprints/stage-01/handoff-phase-0-to-sprint-01.md` for full context and execute Phase 0 Foundation & Setup Sequence."*

---

## Context & Approval Status

- **Status:** All 11 planning stages complete (`00-carry-forward-flags.md` through `08-master-prd.md` approved on disk).
- **Canonical Engineering Rules:** [`.agents/AGENTS.md`](file:///e:/Non_Office/Dev_Space/vibe_skool/veltrics/.agents/AGENTS.md)
- **Master PRD:** [`product-specs/08-master-prd.md`](file:///e:/Non_Office/Dev_Space/vibe_skool/veltrics/product-specs/08-master-prd.md)
- **Roadmap & Phase 0 Plan:** [`product-specs/07-roadmap.md`](file:///e:/Non_Office/Dev_Space/vibe_skool/veltrics/product-specs/07-roadmap.md)
- **Sprint 1 Tracker:** [`trackers/stage-01/sprints/07.01.01-tracker.md`](file:///e:/Non_Office/Dev_Space/vibe_skool/veltrics/trackers/stage-01/sprints/07.01.01-tracker.md)
- **Code Container Directory:** `src/` (`src/backend`, `src/mobile_frontend`, `src/tests`)

---

## Action Plan for the New Chat Session (Option A Execution)

### Step 1: Git Branch Checkout Sequence
1. Confirm working directory on `main` is clean.
2. Checkout protected staging branch `dev`: `git checkout -b dev`.
3. Checkout active Sprint 1 branch `sprint/sprint-01` from `dev`: `git checkout -b sprint/sprint-01`.

### Step 2: Phase 0 Flutter & Firebase Scaffolding
1. Create Flutter mobile client boilerplate inside `/src`(the src folder might not exist and you will have to create one):
   ```bash
   cd src
   flutter create mobile_frontend
   ```
2. Configure Flutter package dependencies (`firebase_core`, `firebase_auth`, `provider`/`flutter_bloc`, `sqflite`, `http`).
3. Link Firebase environments (`flutterfire configure`):
   - **Dev:** Local auth emulator / `veltrics-dev` project bindings.
   - **Staging:** `veltrics-staging` project bindings.
   - **Prod:** `veltrics-prod` project bindings.
4. Copy theme tokens from [`product-specs/05b-flutter-theme.dart`](file:///e:/Non_Office/Dev_Space/vibe_skool/veltrics/product-specs/05b-flutter-theme.dart) to `src/mobile_frontend/lib/theme/app_theme.dart`.
5. Verify "Hello World" app compilation.

### Step 3: Local Backend & DB Seeding Verification
1. Verify backend structure in `src/backend/` and local runner script `.\scripts\start_backend.ps1`.
2. Confirm SQLite DB (`sqlite:///./dev.db`) seeds properly.

### Step 4: First Ticket Handoff & Implementation
1. Dispatch **`UC-118`** (DB Migration & Schema Seeding Infrastructure) or **`UC-001`** (Sign Up with Google One-Tap) on branch `sprint/sprint-01`. 
2. Update [`trackers/stage-01/sprints/07.01.01-tracker.md`](file:///e:/Non_Office/Dev_Space/vibe_skool/veltrics/trackers/stage-01/sprints/07.01.01-tracker.md) as tickets complete.
