from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.db.session import engine, Base
from app.api.v1.auth import router as auth_router
from app.api.v1.seed import router as seed_router
from app.api.v1.vehicles import router as vehicles_router
from app.api.v1.maintenance import router as maintenance_router
from app.api.v1.dashboard import router as dashboard_router
from app.api.v1.organizations import router as organizations_router
from app.api.v1.users import router as users_router
from app.api.v1.fuel import router as fuel_router
from app.api.v1.trips import router as trips_router
from app.api.v1.expenses import router as expenses_router
from app.api.v1.uploads import router as uploads_router, UPLOAD_DIR
from app.api.v1.notifications import router as notifications_router
from app.api.v1.invitations import router as invitations_router
from app.api.v1.sync import router as sync_router
from fastapi.staticfiles import StaticFiles

from sqlalchemy import text


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Auto-create SQLite/DB tables on startup
    Base.metadata.create_all(bind=engine)

    with engine.connect() as conn:
        for statement in [
            "ALTER TABLE vehicles ADD COLUMN registration_province VARCHAR(50) DEFAULT 'Punjab'",
            "ALTER TABLE vehicles ADD COLUMN photo_url VARCHAR(1024)",
            "ALTER TABLE users ADD COLUMN phone_number VARCHAR(32)",
            "ALTER TABLE users ADD COLUMN city VARCHAR(128)",
            "ALTER TABLE users ADD COLUMN job_role VARCHAR(128)",
            "ALTER TABLE users ADD COLUMN avatar_url VARCHAR(1024)",
            "ALTER TABLE users ADD COLUMN is_super_admin BOOLEAN DEFAULT 0"
        ]:
            try:
                conn.execute(text(statement))
                conn.commit()
            except Exception:
                pass
    yield


app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    docs_url=f"{settings.API_V1_STR}/docs",
    lifespan=lifespan
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origin_regex=r"http://.*",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Router Mounts
app.include_router(auth_router, prefix=settings.API_V1_STR)
app.include_router(seed_router, prefix=settings.API_V1_STR)
app.include_router(vehicles_router, prefix=settings.API_V1_STR)
app.include_router(maintenance_router, prefix=settings.API_V1_STR)
app.include_router(dashboard_router, prefix=settings.API_V1_STR)
app.include_router(organizations_router, prefix=settings.API_V1_STR)
app.include_router(users_router, prefix=settings.API_V1_STR)
app.include_router(fuel_router, prefix=settings.API_V1_STR)
app.include_router(trips_router, prefix=settings.API_V1_STR)
app.include_router(expenses_router, prefix=settings.API_V1_STR)
app.include_router(uploads_router, prefix=settings.API_V1_STR)
app.include_router(notifications_router, prefix=settings.API_V1_STR)
app.include_router(invitations_router, prefix=settings.API_V1_STR)
app.include_router(sync_router, prefix=settings.API_V1_STR)

app.mount("/uploads/receipts", StaticFiles(directory=UPLOAD_DIR), name="receipts")



@app.get(f"{settings.API_V1_STR}/health", tags=["Health Check"])
def health_check():
    return {
        "status": "healthy",
        "service": settings.PROJECT_NAME,
        "environment": settings.ENVIRONMENT
    }

@app.get("/", tags=["Root"])
def root():
    return {"message": "Welcome to Veltrics Fleet Management API"}
