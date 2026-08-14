from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.db.seed import seed_database

router = APIRouter(prefix="/admin", tags=["Database Administration"])

@router.post("/seed", status_code=status.HTTP_200_OK)
def trigger_seed_database(db: Session = Depends(get_db)):
    """
    UC-118: Trigger Database Migration & Master Seeding Infrastructure.
    Pre-populates Vehicle Types Catalogue and Maintenance Schedule Templates.
    """
    return seed_database(db)
