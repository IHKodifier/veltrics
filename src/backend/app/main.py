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


from sqlalchemy import text

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



app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    docs_url=f"{settings.API_V1_STR}/docs"
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
