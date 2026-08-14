from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Header, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.user import User
from app.models.organization import Organization
from app.models.driver import Driver
from app.api.deps import get_current_user
from app.schemas.driver import DriverCreateRequest, DriverResponse

router = APIRouter(prefix="/drivers", tags=["Drivers"])


@router.post("", response_model=DriverResponse, status_code=status.HTTP_201_CREATED)
def create_driver(
    payload: DriverCreateRequest,
    current_user: User = Depends(get_current_user),
    x_organization_id: Optional[str] = Header(None, alias="X-Organization-ID"),
    db: Session = Depends(get_db),
):
    """
    UC-087 & UC-018: Register Driver with organization driver quota enforcement.
    """
    if not x_organization_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="X-Organization-ID header is required.")

    org = db.query(Organization).filter(Organization.id == x_organization_id, Organization.deleted_at.is_(None)).first()
    if not org:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Organization not found.")

    # 1. Driver Quota Enforcement (UC-087)
    active_drivers = db.query(Driver).filter(
        Driver.organization_id == org.id,
        Driver.deleted_at.is_(None),
    ).count()

    if active_drivers >= org.max_drivers:
        raise HTTPException(
            status_code=status.HTTP_402_PAYMENT_REQUIRED,
            detail=f"DRIVER_QUOTA_EXCEEDED: Maximum driver limit reached for organization ({org.max_drivers} max).",
        )

    phone = payload.phone or payload.phone_number
    driver = Driver(
        organization_id=org.id,
        full_name=payload.full_name,
        phone_number=phone,
        license_number=payload.license_number,
        license_expiry_date=payload.license_expiry_date,
        status="ACTIVE",
    )
    db.add(driver)
    db.commit()
    db.refresh(driver)

    return driver


@router.get("", response_model=List[DriverResponse])
def list_drivers(
    current_user: User = Depends(get_current_user),
    x_organization_id: Optional[str] = Header(None, alias="X-Organization-ID"),
    db: Session = Depends(get_db),
):
    if not x_organization_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="X-Organization-ID header is required.")

    return db.query(Driver).filter(
        Driver.organization_id == x_organization_id,
        Driver.deleted_at.is_(None),
    ).all()
