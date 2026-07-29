# Veltrics — GCP Cost Minimization & AI Skill Plan

> **Reads from:** [01b-tech-stack.md](file:///e:/Non_Office/Dev_Space/vibe_skool/veltrics/product-specs/01b-tech-stack.md), [02-architecture.md](file:///e:/Non_Office/Dev_Space/vibe_skool/veltrics/product-specs/02-architecture.md), [07-roadmap.md](file:///e:/Non_Office/Dev_Space/vibe_skool/veltrics/product-specs/07-roadmap.md)  
> **Status:** ⏳ Pending User Approval  
> **Author:** Senior Software Architect & Engineering Programme Manager  

---

## 1. Zero-Dollar Development Architecture

To keep GCP cloud infrastructure bills near **$0/month** during active daily development, Veltrics enforces a strict local-first execution baseline:

1. **Docker-Free Local Database (`SQLite` / Local Postgres):** Daily feature coding relies on Python FastAPI connected to a local SQLite database (`sqlite:///./dev.db`). SQLite requires zero container overhead, zero cloud provisioning, and uses negligible disk space.
2. **Local Firebase Auth Emulation:** Authentication during development uses a lightweight JWT mock middleware or Firebase CLI local auth emulator, eliminating paid GCP Identity Platform API calls.
3. **Single-Command Launcher:** All backend services, database migrations, and local environment variables are initialized with a single command via `./scripts/start_backend.ps1`.

---

## 2. GCP Cloud Cost Minimization & Control Controls

When deploying to GCP Staging and Production:

### 2.1 Cloud Run (FastAPI Backend) — Auto-Scaling to Zero
- **Cost Profile:** $0 when idle.
- **Behavior:** Cloud Run automatically scales down to 0 instances when no HTTP traffic is detected. The moment you start coding or push to staging, incoming HTTP requests auto-wake the service within 1–2 seconds. No manual intervention required.

### 2.2 Cloud SQL (PostgreSQL Database) — On-Demand Instance Control
- **Cost Profile:** Billed per hour while active (~$7–$15/month for db-f1-micro if left running continuously).
- **Control Script (`./scripts/gcp_cloud_control.ps1`):** Since development occurs on a flexible schedule (days, nights, weekends), Cloud SQL is managed via an explicit on-demand start/stop script:
  - `.\scripts\gcp_cloud_control.ps1 -Action start` → Enables Cloud SQL instance for staging/integration testing.
  - `.\scripts\gcp_cloud_control.ps1 -Action stop` → Instantly stops Cloud SQL instance when coding session finishes.

---

## 3. AI TDD Skill Plan & Execution Strategy

Designed for a **solo full-stack developer paired with AI coding assistance**, this workflow maximizes speed while maintaining test coverage:

1. **Sprint Startup & Test Suite Generation:** At the start of each sprint, the AI agent inspects `product-specs/06-data-model.md` and generates API contract unit/integration tests in `./tests/` before implementation code is written.
2. **FastAPI Endpoint Construction:** AI agent constructs Pydantic schemas, SQLAlchemy models, and FastAPI router endpoints to pass the newly written test suites.
3. **Test Execution Logging:** Test suite names and execution status (Pass/Fail, execution time) are logged in the respective sprint tracker (`trackers/stage-01/sprints/07.01.XX-tracker.md`).
4. **CI/CD Quality Gate:** Pushes to `sprint/sprint-XX` require all local tests to pass before creating a Pull Request to `dev`.
