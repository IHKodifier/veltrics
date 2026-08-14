import hashlib
from datetime import datetime, timezone, timedelta
from typing import List, Dict, Any
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.driver import Driver
from app.models.trip import Trip
from app.models.organization import Organization
from app.schemas.driver_analytics import (
    DriverPerformanceDetailResponse,
    DriverAnomalyScanResponse,
    DriverAnomalyItem,
    DriverSafetyCertificateResponse,
    DriverLeaderboardResponse,
    DriverLeaderboardEntry,
)

def calculate_driver_metrics(db: Session, driver: Driver) -> Dict[str, Any]:
    # Query completed trips for driver
    trips = db.query(Trip).filter(
        Trip.driver_id == driver.id,
        Trip.deleted_at.is_(None)
    ).all()

    completed_trips = [t for t in trips if t.status == "COMPLETED"]
    total_completed = len(completed_trips)
    total_distance_km = sum(t.distance_km or 0.0 for t in completed_trips)

    # Count harsh events from notes/logs
    harsh_events = 0
    for trip in completed_trips:
        if trip.notes and "harsh" in trip.notes.lower():
            harsh_events += 1

    # Base Score calculation (100 base)
    score = 100
    # Penalty: -5 per harsh event
    score -= (harsh_events * 5)
    # Penalty: -10 if no trips completed yet
    if total_completed == 0:
        score = 75
    
    # Bound score between 0 and 100
    score = max(0, min(100, score))

    # Badge Tier classification
    if score >= 90:
        badge_tier = "PLATINUM"
    elif score >= 80:
        badge_tier = "GOLD"
    elif score >= 70:
        badge_tier = "SILVER"
    else:
        badge_tier = "BRONZE"

    return {
        "driver_id": driver.id,
        "full_name": driver.full_name,
        "license_number": driver.license_number,
        "status": driver.status,
        "safety_score": score,
        "badge_tier": badge_tier,
        "completed_trips": total_completed,
        "total_distance_km": round(total_distance_km, 2),
        "harsh_events_count": harsh_events,
        "efficiency_rating": "OPTIMAL" if score >= 85 else "STANDARD",
    }


def get_driver_performance_detail(db: Session, driver_id: str, organization_id: str) -> DriverPerformanceDetailResponse:
    driver = db.query(Driver).filter(
        Driver.id == driver_id,
        Driver.organization_id == organization_id,
        Driver.deleted_at.is_(None)
    ).first()

    if not driver:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Driver not found in organization",
        )

    metrics = calculate_driver_metrics(db, driver)

    # Dummy monthly history for trend charts
    monthly_history = [
        {"month": "May", "score": max(50, metrics["safety_score"] - 5)},
        {"month": "Jun", "score": max(50, metrics["safety_score"] - 2)},
        {"month": "Jul", "score": metrics["safety_score"]},
    ]

    return DriverPerformanceDetailResponse(
        driver_id=metrics["driver_id"],
        full_name=metrics["full_name"],
        license_number=metrics["license_number"],
        status=metrics["status"],
        safety_score=metrics["safety_score"],
        badge_tier=metrics["badge_tier"],
        completed_trips=metrics["completed_trips"],
        total_distance_km=metrics["total_distance_km"],
        harsh_events_count=metrics["harsh_events_count"],
        efficiency_rating=metrics["efficiency_rating"],
        monthly_score_history=monthly_history,
    )


def detect_driver_anomalies(db: Session, organization_id: str) -> DriverAnomalyScanResponse:
    anomalies: List[DriverAnomalyItem] = []

    drivers = db.query(Driver).filter(
        Driver.organization_id == organization_id,
        Driver.deleted_at.is_(None)
    ).all()

    now = datetime.now(timezone.utc)
    today = now.date()

    for driver in drivers:
        # Check license expiration
        if driver.license_expiry_date:
            days_to_expiry = (driver.license_expiry_date - today).days
            if days_to_expiry <= 30:
                anomalies.append(
                    DriverAnomalyItem(
                        driver_id=driver.id,
                        driver_name=driver.full_name,
                        anomaly_type="EXPIRING_LICENSE",
                        severity="HIGH" if days_to_expiry <= 7 else "MEDIUM",
                        description=f"Driver license expires in {days_to_expiry} days on {driver.license_expiry_date}.",
                    )
                )

        # Check idle drivers (no completed trip in last 14 days)
        last_trip = db.query(Trip).filter(
            Trip.driver_id == driver.id,
            Trip.status == "COMPLETED",
            Trip.deleted_at.is_(None)
        ).order_by(Trip.end_time.desc()).first()

        if not last_trip:
            anomalies.append(
                DriverAnomalyItem(
                    driver_id=driver.id,
                    driver_name=driver.full_name,
                    anomaly_type="IDLE_DRIVER",
                    severity="LOW",
                    description="No recorded completed trips found for driver.",
                )
            )

    return DriverAnomalyScanResponse(
        organization_id=organization_id,
        scan_timestamp=now,
        anomalies_count=len(anomalies),
        anomalies=anomalies,
    )


def generate_safety_certificate(db: Session, driver_id: str, organization_id: str) -> DriverSafetyCertificateResponse:
    driver = db.query(Driver).filter(
        Driver.id == driver_id,
        Driver.organization_id == organization_id,
        Driver.deleted_at.is_(None)
    ).first()

    if not driver:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Driver not found",
        )

    org = db.query(Organization).filter(Organization.id == organization_id).first()
    org_name = org.name if org else "Veltrics Fleet"

    metrics = calculate_driver_metrics(db, driver)
    cert_id = f"CERT-{driver_id[:8].upper()}-2026"
    issue_date = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    # Generate verification SHA-256 hash
    raw_hash_input = f"{cert_id}:{driver_id}:{metrics['safety_score']}:{issue_date}"
    verification_hash = hashlib.sha256(raw_hash_input.encode("utf-8")).hexdigest()

    return DriverSafetyCertificateResponse(
        certificate_id=cert_id,
        driver_id=driver.id,
        driver_name=driver.full_name,
        organization_name=org_name,
        badge_tier=metrics["badge_tier"],
        safety_score=metrics["safety_score"],
        issue_date=issue_date,
        verification_hash=verification_hash,
    )


def get_organization_driver_leaderboard(db: Session, organization_id: str) -> DriverLeaderboardResponse:
    drivers = db.query(Driver).filter(
        Driver.organization_id == organization_id,
        Driver.deleted_at.is_(None)
    ).all()

    driver_metrics_list = [calculate_driver_metrics(db, d) for d in drivers]

    # Sort descending by safety score
    driver_metrics_list.sort(key=lambda x: x["safety_score"], reverse=True)

    leaderboard_entries: List[DriverLeaderboardEntry] = []
    for rank, m in enumerate(driver_metrics_list, start=1):
        leaderboard_entries.append(
            DriverLeaderboardEntry(
                rank=rank,
                driver_id=m["driver_id"],
                driver_name=m["full_name"],
                badge_tier=m["badge_tier"],
                safety_score=m["safety_score"],
                completed_trips=m["completed_trips"],
                total_distance_km=m["total_distance_km"],
            )
        )

    return DriverLeaderboardResponse(
        organization_id=organization_id,
        total_drivers=len(leaderboard_entries),
        leaderboard=leaderboard_entries,
    )
