# Database Seeding Guide (`dev.db`) — Veltrics Platform

> **Target File:** `src/backend/dev.db` (Local SQLite Development Database)  
> **Backend Service:** FastAPI Uvicorn (`http://127.0.0.1:8000`)  
> **Source Module:** `src/backend/app/db/seed.py`

---

## 1. Overview & Seeded Datasets

The Veltrics Database Seeding engine pre-populates your local development database (`dev.db`) with production-grade master catalogues and OEM maintenance templates, enabling full offline/online UI testing without manual data entry.

### Seeded Catalogues:
1. **Vehicle Master Catalogue (`vehicle_types`)**:
   - **Sedans:** Toyota Corolla, Honda Civic, Honda City
   - **Hatchbacks:** Suzuki Alto, Suzuki Cultus
   - **SUVs & Crossovers:** Hyundai Tucson, Kia Sportage, BYD Atto 3 (EV)
   - **Pickups:** Toyota Hilux Revo
2. **OEM Maintenance Schedule Templates**:
   - **Engine Oil & Filter Change:** Every 5,000 km / 180 days (6 months)
   - **Air Filter Replacement:** Every 10,000 km / 365 days (12 months)
   - **Tire Rotation & Wheel Alignment:** Every 10,000 km / 180 days (6 months)
   - **Spark Plugs Replacement:** Every 30,000 km / 540 days (18 months)
   - **Brake Inspection & Fluid Flush:** Every 40,000 km / 730 days (24 months)
   - **Transmission Fluid Change:** Every 60,000 km / 1,095 days (36 months)

---

## 2. How to Seed the Database

### Option A: Via HTTP API (Recommended when server is running)

When the backend server is running (`.\scripts\start_backend.ps1`), you can trigger database seeding via REST API:

#### 1. Via PowerShell Terminal:
```powershell
Invoke-RestMethod -Method Post -Uri "http://127.0.0.1:8000/api/v1/admin/seed"
```

#### 2. Via Interactive Swagger UI:
1. Open your browser to [`http://127.0.0.1:8000/api/v1/docs`](http://127.0.0.1:8000/api/v1/docs).
2. Expand the **`POST /api/v1/admin/seed`** endpoint.
3. Click **Try it out**, then **Execute**.

---

### Option B: Via Python CLI Command

If the FastAPI server is stopped, run the Python seeding script directly from your terminal:

```powershell
cd src/backend
python -m app.db.seed
```

**Expected Output:**
```json
{
  "status": "success",
  "vehicle_types_added": 9,
  "vehicle_types_updated": 0,
  "templates_available": 6
}
```

---

## 3. Key Technical Properties

- **Idempotent Execution:** Running the seeding script multiple times will update existing master templates without creating duplicate database rows or corrupting user data.
- **Dialect-Agnostic:** Operates identically on local SQLite (`sqlite:///./dev.db`) and staging GCP Cloud SQL (PostgreSQL).
- **Multi-Tenant Safe:** Master vehicle types are stored in shared global tables (`vehicle_types`), while organization vehicles and schedules remain strictly isolated by `organization_id`.
