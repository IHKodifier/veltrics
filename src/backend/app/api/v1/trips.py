from typing import List, Optional, Union
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.organization import Organization
from app.schemas.trip import TripStart, TripStop, TripCreate, TripResponse, TripPaginatedResponse, TripSummaryResponse, TripUpdate, QuickTripCreate, MileageSummaryResponse
from app.services import trip_service

router = APIRouter(prefix="/trips", tags=["Trips"])

def resolve_organization(db: Session, org_id: Optional[str] = None) -> str:
    if org_id:
        org = db.query(Organization).filter(Organization.id == org_id, Organization.deleted_at == None).first()
        if org:
            return org.id
    first_org = db.query(Organization).filter(Organization.deleted_at == None).first()
    if first_org:
        return first_org.id
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No active organization found.")

@router.get("/summary", response_model=TripSummaryResponse)
def get_trip_summary(
    vehicle_id: Optional[str] = Query(None, description="Filter summary by vehicle ID"),
    organization_id: Optional[str] = Query(None, description="Active Organization ID"),
    tax_rate: float = Query(0.65, description="Tax deduction rate per km"),
    db: Session = Depends(get_db)
):
    """
    UC-053: Get Trip Summary & Tax Deduction Metrics.
    """
    org_id = resolve_organization(db, organization_id)
    return trip_service.get_trip_summary(
        db=db, organization_id=org_id, vehicle_id=vehicle_id, tax_rate_per_km=tax_rate
    )

@router.post("/start", response_model=TripResponse, status_code=status.HTTP_201_CREATED)
def start_trip(
    payload: TripStart,
    organization_id: Optional[str] = Query(None, description="Active Organization ID"),
    db: Session = Depends(get_db)
):
    """
    UC-052: Start GPS Trip Tracking session.
    """
    org_id = resolve_organization(db, organization_id)
    return trip_service.start_trip(db=db, organization_id=org_id, payload=payload)

@router.post("/{trip_id}/stop", response_model=TripResponse)
def stop_trip(
    trip_id: str,
    payload: TripStop,
    organization_id: Optional[str] = Query(None, description="Active Organization ID"),
    db: Session = Depends(get_db)
):
    """
    UC-052: Stop active GPS Trip Tracking session and calculate distance.
    """
    org_id = resolve_organization(db, organization_id)
    return trip_service.stop_trip(db=db, organization_id=org_id, trip_id=trip_id, payload=payload)

@router.post("", response_model=TripResponse, status_code=status.HTTP_201_CREATED)
@router.post("/", response_model=TripResponse, status_code=status.HTTP_201_CREATED, include_in_schema=False)
def create_trip(
    payload: TripCreate,
    organization_id: Optional[str] = Query(None, description="Active Organization ID"),
    db: Session = Depends(get_db)
):
    """
    UC-052 / UC-053: Create trip entry (Manual or completed GPS trip).
    """
    org_id = resolve_organization(db, organization_id)
    return trip_service.create_trip(db=db, organization_id=org_id, payload=payload)

@router.get("", response_model=Union[List[TripResponse], TripPaginatedResponse])
@router.get("/", include_in_schema=False)
def list_trips(
    vehicle_id: Optional[str] = Query(None, description="Filter trips by vehicle ID"),
    trip_purpose: Optional[str] = Query(None, description="Filter trips by purpose (BUSINESS/PERSONAL)"),
    organization_id: Optional[str] = Query(None, description="Active Organization ID"),
    page: Optional[int] = Query(None, description="Page number for pagination"),
    limit: Optional[int] = Query(None, description="Items per page"),
    paginated: bool = Query(False, description="Set to true for paginated wrapper format"),
    db: Session = Depends(get_db)
):
    """
    UC-053: View Trip History.
    """
    org_id = resolve_organization(db, organization_id)
    if paginated or (page is not None and limit is not None):
        p_page = page or 1
        p_limit = limit or 20
        items, total = trip_service.get_trips(
            db=db, organization_id=org_id, vehicle_id=vehicle_id, trip_purpose=trip_purpose, page=p_page, limit=p_limit
        )
        pages = (total + p_limit - 1) // p_limit if p_limit > 0 else 1
        if paginated:
            return {
                "items": items,
                "total": total,
                "page": p_page,
                "limit": p_limit,
                "pages": pages
            }
        return items
    items, _ = trip_service.get_trips(db=db, organization_id=org_id, vehicle_id=vehicle_id, trip_purpose=trip_purpose)
    return items

@router.patch("/{trip_id}", response_model=TripResponse)
def update_trip(
    trip_id: str,
    payload: TripUpdate,
    organization_id: Optional[str] = Query(None, description="Active Organization ID"),
    db: Session = Depends(get_db)
):
    """
    UC-054: Edit Trip Entry & Classification.
    """
    org_id = resolve_organization(db, organization_id)
    return trip_service.update_trip(
        db=db, organization_id=org_id, trip_id=trip_id, payload=payload
    )

@router.delete("/{trip_id}")
def delete_trip(
    trip_id: str,
    organization_id: Optional[str] = Query(None, description="Active Organization ID"),
    db: Session = Depends(get_db)
):
    """
    UC-055: Soft Delete Trip Entry.
    """
    org_id = resolve_organization(db, organization_id)
    return trip_service.delete_trip(
        db=db, organization_id=org_id, trip_id=trip_id
    )

@router.post("/quick", response_model=TripResponse, status_code=status.HTTP_201_CREATED)
def quick_create_trip(
    payload: QuickTripCreate,
    organization_id: Optional[str] = Query(None, description="Active Organization ID"),
    db: Session = Depends(get_db)
):
    """
    UC-056: Quick-Log Trip from Dashboard.
    """
    org_id = resolve_organization(db, organization_id)
    return trip_service.quick_log_trip(
        db=db, organization_id=org_id, payload=payload
    )

@router.get("/mileage-summary", response_model=MileageSummaryResponse)
def get_mileage_summary(
    vehicle_id: Optional[str] = Query(None, description="Filter trips by vehicle ID"),
    start_date: Optional[datetime] = Query(None, description="Start date filter"),
    end_date: Optional[datetime] = Query(None, description="End date filter"),
    organization_id: Optional[str] = Query(None, description="Active Organization ID"),
    db: Session = Depends(get_db)
):
    """
    UC-057: View Distance & Mileage Summary Analytics.
    """
    org_id = resolve_organization(db, organization_id)
    return trip_service.get_mileage_summary(
        db=db,
        organization_id=org_id,
        vehicle_id=vehicle_id,
        start_date=start_date,
        end_date=end_date
    )



