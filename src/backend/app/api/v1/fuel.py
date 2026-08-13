from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.organization import Organization
from app.schemas.fuel_log import FuelLogCreate, FuelLogResponse
from app.services import fuel_service

router = APIRouter(prefix="/fuel", tags=["Fuel Logs"])

def resolve_organization(db: Session, org_id: Optional[str] = None) -> str:
    if org_id:
        org = db.query(Organization).filter(Organization.id == org_id, Organization.deleted_at == None).first()
        if org:
            return org.id
    first_org = db.query(Organization).filter(Organization.deleted_at == None).first()
    if first_org:
        return first_org.id
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No active organization found.")

@router.post("", response_model=FuelLogResponse, status_code=status.HTTP_201_CREATED)
@router.post("/", response_model=FuelLogResponse, status_code=status.HTTP_201_CREATED, include_in_schema=False)
def create_fuel_log(
    payload: FuelLogCreate,
    organization_id: Optional[str] = Query(None, description="Active Organization ID"),
    db: Session = Depends(get_db)
):
    """
    UC-046: Log Fuel Fill-Up Entry.
    Automatically updates vehicle current odometer reading and generates a linked ExpenseLog under category 'FUEL'.
    """
    org_id = resolve_organization(db, organization_id)
    return fuel_service.log_fuel_entry(db=db, organization_id=org_id, payload=payload)

@router.get("", response_model=List[FuelLogResponse])
@router.get("/", response_model=List[FuelLogResponse], include_in_schema=False)
def list_fuel_logs(
    vehicle_id: Optional[str] = Query(None, description="Filter fuel logs by vehicle ID"),
    organization_id: Optional[str] = Query(None, description="Active Organization ID"),
    db: Session = Depends(get_db)
):
    """
    UC-047: View Fuel Log History.
    """
    org_id = resolve_organization(db, organization_id)
    return fuel_service.get_fuel_logs(db=db, organization_id=org_id, vehicle_id=vehicle_id)
