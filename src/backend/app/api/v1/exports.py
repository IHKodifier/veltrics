from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Header, Response, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.schemas.export import ExportEmailRequest, ExportEmailResponse
from app.services import export_service

router = APIRouter(prefix="/exports", tags=["Exports"])


def verify_org_header(x_organization_id: Optional[str] = Header(None, alias="X-Organization-ID")) -> str:
    if not x_organization_id:
        raise HTTPException(status_code=400, detail="X-Organization-ID header required")
    return x_organization_id


@router.get("/maintenance/pdf")
def export_maintenance_pdf(
    org_id: str = Depends(verify_org_header),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    UC-110: Export Maintenance History to PDF.
    """
    pdf_bytes = export_service.generate_maintenance_pdf(db, org_id)
    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename=maintenance_history_{org_id}.pdf"}
    )


@router.get("/fuel-expenses/csv")
def export_fuel_expenses_csv(
    org_id: str = Depends(verify_org_header),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    UC-111: Export Fuel & Expense Logs to CSV.
    """
    csv_str = export_service.generate_fuel_expenses_csv(db, org_id)
    return Response(
        content=csv_str,
        media_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename=fuel_expenses_{org_id}.csv"}
    )


@router.post("/monthly-summary/email", response_model=ExportEmailResponse)
def email_monthly_summary(
    payload: ExportEmailRequest,
    org_id: str = Depends(verify_org_header),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    UC-112: Generate & Email Monthly Fleet Summary PDF.
    """
    return export_service.email_monthly_summary(db, org_id, payload.target_email)
