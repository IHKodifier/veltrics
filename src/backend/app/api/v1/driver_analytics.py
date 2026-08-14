from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.models.user_organization import UserOrganization
from app.schemas.driver_analytics import (
    DriverPerformanceDetailResponse,
    DriverAnomalyScanResponse,
    DriverSafetyCertificateResponse,
    DriverLeaderboardResponse,
)
from app.services import driver_analytics_service

router = APIRouter()


def get_user_org_id(db: Session, user: User) -> str:
    membership = db.query(UserOrganization).filter(
        UserOrganization.user_id == user.id
    ).first()
    if not membership:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User does not belong to any active organization",
        )
    return membership.organization_id


@router.get("/drivers/{driver_id}/performance", response_model=DriverPerformanceDetailResponse)
def get_driver_performance(
    driver_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    org_id = get_user_org_id(db, current_user)
    return driver_analytics_service.get_driver_performance_detail(db, driver_id, org_id)


@router.post("/detect-anomalies", response_model=DriverAnomalyScanResponse)
def detect_anomalies(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    org_id = get_user_org_id(db, current_user)
    return driver_analytics_service.detect_driver_anomalies(db, org_id)


@router.get("/drivers/{driver_id}/certificate", response_model=DriverSafetyCertificateResponse)
def get_driver_certificate(
    driver_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    org_id = get_user_org_id(db, current_user)
    return driver_analytics_service.generate_safety_certificate(db, driver_id, org_id)


@router.get("/leaderboard", response_model=DriverLeaderboardResponse)
def get_driver_leaderboard(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    org_id = get_user_org_id(db, current_user)
    return driver_analytics_service.get_organization_driver_leaderboard(db, org_id)
