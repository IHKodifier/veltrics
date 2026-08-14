from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Header, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.models.user_organization import UserOrganization
from app.models.maintenance import Vendor
from app.schemas.vendor import VendorCreateRequest, VendorResponse

router = APIRouter(prefix="/vendors", tags=["Vendors"])


def get_user_org_id(db: Session, user: User, header_org_id: Optional[str] = None) -> str:
    if header_org_id:
        return header_org_id
    membership = db.query(UserOrganization).filter(
        UserOrganization.user_id == user.id
    ).first()
    if not membership:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User does not belong to an organization",
        )
    return membership.organization_id


@router.post("", response_model=VendorResponse, status_code=status.HTTP_201_CREATED)
def create_vendor(
    payload: VendorCreateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    x_organization_id: Optional[str] = Header(None, alias="X-Organization-ID"),
):
    """
    UC-043: Create Maintenance Vendor.
    """
    org_id = get_user_org_id(db, current_user, x_organization_id)

    vendor = Vendor(
        organization_id=org_id,
        name=payload.name,
        contact_person=payload.contact_person,
        phone_number=payload.phone_number,
        address=payload.address,
        rating=payload.rating,
    )
    db.add(vendor)
    db.commit()
    db.refresh(vendor)
    return vendor


@router.get("", response_model=List[VendorResponse])
def get_vendors(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    x_organization_id: Optional[str] = Header(None, alias="X-Organization-ID"),
):
    """
    UC-043: List Maintenance Vendors.
    """
    org_id = get_user_org_id(db, current_user, x_organization_id)
    return db.query(Vendor).filter(Vendor.organization_id == org_id).all()
