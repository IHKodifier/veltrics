import json
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Header, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.models.user_organization import UserOrganization
from app.models.maintenance import VehicleInspection
from app.schemas.inspection import InspectionCreateRequest, InspectionResponse

router = APIRouter(prefix="/inspections", tags=["Inspections"])


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


@router.post("", response_model=InspectionResponse, status_code=status.HTTP_201_CREATED)
def create_inspection(
    payload: InspectionCreateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    x_organization_id: Optional[str] = Header(None, alias="X-Organization-ID"),
):
    """
    UC-044: Log Vehicle Safety Inspection Checklist.
    """
    org_id = get_user_org_id(db, current_user, x_organization_id)

    items_str = json.dumps(payload.items_json) if payload.items_json else None

    inspection = VehicleInspection(
        organization_id=org_id,
        vehicle_id=payload.vehicle_id,
        inspector_id=current_user.id,
        inspection_type=payload.inspection_type,
        overall_status=payload.overall_status,
        items_json=items_str,
        notes=payload.notes,
    )
    db.add(inspection)
    db.commit()
    db.refresh(inspection)
    return inspection


@router.get("/vehicle/{vehicle_id}", response_model=List[InspectionResponse])
def get_vehicle_inspections(
    vehicle_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    x_organization_id: Optional[str] = Header(None, alias="X-Organization-ID"),
):
    """
    UC-044: Fetch Vehicle Safety Inspections.
    """
    org_id = get_user_org_id(db, current_user, x_organization_id)
    return db.query(VehicleInspection).filter(
        VehicleInspection.organization_id == org_id,
        VehicleInspection.vehicle_id == vehicle_id
    ).order_by(VehicleInspection.created_at.desc()).all()
