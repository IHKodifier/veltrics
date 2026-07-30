# Antigravity Agent Rules — Veltrics Project Directives

## 1. Git Branch Protection & Workflow
- **`main` / `master` (Production):** NEVER commit or push code directly to `main`. This branch is strictly for production releases merged from `dev`.
- **`dev` (Staging):** Protected staging branch. All feature work must take place on dedicated `sprint/sprint-XX` or `feature/` branches checked out from `dev`.
- **Merging Protocol:** Only propose or execute a PR/merge from `sprint/sprint-XX` into `dev` when **100% of automated tests pass locally**.

## 2. Local-First & Zero-Cloud Execution
- **No Docker Required:** Local development MUST use `.\scripts\start_backend.ps1` (FastAPI + Uvicorn + SQLite `sqlite:///./dev.db` + Local Auth Emulator).
- **GCP Cost Protection:** Do NOT spin up GCP Cloud SQL instances during routine feature development. Use `.\scripts\gcp_cloud_control.ps1 -Action start/stop` strictly for staging deployment verification.

## 3. TDD & API-First Mandate
- **Test-First Development:** Before writing any implementation code or feature logic, create or update automated test files in `./tests/unit/` or `./tests/integration/`.
- **100% API Decoupling:** The frontend must NEVER interact directly with database models. All data requests must route through FastAPI REST endpoints governed by Pydantic payload models.

## 4. Automatic Hierarchical Tracker Maintenance
- Whenever a task, feature, or test suite is completed or updated:
  1. Record test names and Pass/Fail results in the active sprint tracker (`trackers/stage-XX/sprints/07.XX.YY-tracker.md`).
  2. Update the task status in the stage tracker (`trackers/stage-XX/07.XX-tracker.md`).
  3. Update the overall sprint completion percentage in the master tracker (`trackers/07-big-picture-tracker.md`).

## 5. Sprint Handoff Prompt Generation
- **End-of-Sprint Protocol:** At the end of every sprint (once 100% of DoD criteria and local tests pass), the agent MUST automatically generate a structured Handoff Prompt file indicating both the completed sprint and the upcoming sprint (e.g. `handoff-sprint-01-to-02.md`) and save it in the stage's sprint handoff directory (e.g. `handoff-prompts/sprints/stage-01/handoff-sprint-01-to-02.md`).
- **Handoff Content:** The sprint handoff prompt must include a summary of completed user stories/tasks, test results, branch merge status, updated tracker links, and initial prompts/goals for the subsequent sprint.
