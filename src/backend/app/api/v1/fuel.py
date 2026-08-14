from typing import List, Optional, Union
from fastapi import APIRouter, Depends, HTTPException, Query, status, File, UploadFile
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.organization import Organization
from app.schemas.fuel_log import FuelLogCreate, FuelLogResponse, FuelLogUpdate, FuelPaginatedResponse, FuelTrendsResponse
from app.schemas.ocr_receipt import ReceiptOcrResponse
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

@router.get("/trends", response_model=FuelTrendsResponse)
def get_fuel_trends(
    vehicle_id: Optional[str] = Query(None, description="Filter trends by vehicle ID"),
    organization_id: Optional[str] = Query(None, description="Active Organization ID"),
    db: Session = Depends(get_db)
):
    """
    UC-048: View Fuel Efficiency Trends & Aggregate Metrics.
    """
    org_id = resolve_organization(db, organization_id)
    return fuel_service.get_fuel_efficiency_trends(db=db, organization_id=org_id, vehicle_id=vehicle_id)

@router.get("/anomalies", response_model=List[FuelLogResponse])
def list_fuel_anomalies(
    organization_id: Optional[str] = Query(None, description="Active Organization ID"),
    unverified_only: bool = Query(True, description="Filter unverified anomalies only"),
    db: Session = Depends(get_db)
):
    """
    UC-050: Detect Fuel Anomaly & Theft Alerts - Fetch anomaly logs.
    """
    org_id = resolve_organization(db, organization_id)
    return fuel_service.get_fuel_anomalies(db=db, organization_id=org_id, unverified_only=unverified_only)

@router.patch("/{fuel_log_id}/verify-anomaly", response_model=FuelLogResponse)
def verify_fuel_anomaly(
    fuel_log_id: str,
    db: Session = Depends(get_db)
):
    """
    UC-050 (A1): Manager clears fuel anomaly flag.
    """
    return fuel_service.verify_fuel_anomaly(db=db, fuel_log_id=fuel_log_id)

@router.post("/ocr-scan", response_model=ReceiptOcrResponse)
async def ocr_scan_receipt(
    file: UploadFile = File(...)
):
    """
    UC-049: Fuel Receipt OCR Auto-Fill (Pro).
    """
    content = await file.read()
    return fuel_service.parse_receipt_ocr(file_bytes=content, filename=file.filename or "receipt.jpg")



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

@router.get("", response_model=Union[List[FuelLogResponse], FuelPaginatedResponse])
@router.get("/", include_in_schema=False)
def list_fuel_logs(
    vehicle_id: Optional[str] = Query(None, description="Filter fuel logs by vehicle ID"),
    organization_id: Optional[str] = Query(None, description="Active Organization ID"),
    page: Optional[int] = Query(None, description="Page number for pagination"),
    limit: Optional[int] = Query(None, description="Items per page"),
    paginated: bool = Query(False, description="Set to true for paginated wrapper format"),
    db: Session = Depends(get_db)
):
    """
    UC-047 / UC-048: View Fuel Log History with optional pagination.
    """
    org_id = resolve_organization(db, organization_id)
    if paginated or (page is not None and limit is not None):
        p_page = page or 1
        p_limit = limit or 20
        items, total = fuel_service.get_fuel_logs(
            db=db, organization_id=org_id, vehicle_id=vehicle_id, page=p_page, limit=p_limit
        )
        pages = (total + p_limit - 1) // p_limit if p_limit > 0 else 1
        fleet_avg = fuel_service.get_fleet_average_efficiency(db, org_id)
        if paginated:
            return {
                "items": items,
                "total": total,
                "page": p_page,
                "limit": p_limit,
                "pages": pages,
                "fleet_avg_efficiency_kpl": fleet_avg
            }
        return items
    return fuel_service.get_fuel_logs(db=db, organization_id=org_id, vehicle_id=vehicle_id)

@router.patch("/{fuel_log_id}", response_model=FuelLogResponse)
def update_fuel_log(
    fuel_log_id: str,
    payload: FuelLogUpdate,
    organization_id: Optional[str] = Query(None, description="Active Organization ID"),
    db: Session = Depends(get_db)
):
    """
    UC-051: Edit Fuel Log Entry.
    Updates entry, syncs linked ExpenseLog, and recalculates vehicle fuel efficiency chain.
    """
    org_id = resolve_organization(db, organization_id)
    return fuel_service.update_fuel_entry(
        db=db, organization_id=org_id, fuel_log_id=fuel_log_id, payload=payload
    )

@router.delete("/{fuel_log_id}")
def delete_fuel_log(
    fuel_log_id: str,
    organization_id: Optional[str] = Query(None, description="Active Organization ID"),
    db: Session = Depends(get_db)
):
    """
    UC-051: Soft Delete Fuel Log Entry.
    Soft-deletes entry and linked ExpenseLog, and heals vehicle fuel efficiency chain.
    """
    org_id = resolve_organization(db, organization_id)
    return fuel_service.delete_fuel_entry(
        db=db, organization_id=org_id, fuel_log_id=fuel_log_id
    )


