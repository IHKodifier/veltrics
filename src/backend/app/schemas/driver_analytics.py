from typing import List, Optional
from datetime import date, datetime
from pydantic import BaseModel

class DriverSafetyScoreResponse(BaseModel):
    driver_id: str
    full_name: str
    safety_score: int
    badge_tier: str  # PLATINUM, GOLD, SILVER, BRONZE
    completed_trips: int
    total_distance_km: float
    harsh_events_count: int

class DriverPerformanceDetailResponse(BaseModel):
    driver_id: str
    full_name: str
    license_number: Optional[str] = None
    status: str
    safety_score: int
    badge_tier: str
    completed_trips: int
    total_distance_km: float
    harsh_events_count: int
    efficiency_rating: str  # OPTIMAL, STANDARD, POOR
    monthly_score_history: List[dict]

class DriverAnomalyItem(BaseModel):
    driver_id: str
    driver_name: str
    anomaly_type: str  # IDLE_DRIVER, EXPIRING_LICENSE, UNCLOSED_TRIP
    severity: str      # HIGH, MEDIUM, LOW
    description: str

class DriverAnomalyScanResponse(BaseModel):
    organization_id: str
    scan_timestamp: datetime
    anomalies_count: int
    anomalies: List[DriverAnomalyItem]

class DriverSafetyCertificateResponse(BaseModel):
    certificate_id: str
    driver_id: str
    driver_name: str
    organization_name: str
    badge_tier: str
    safety_score: int
    issue_date: str
    verification_hash: str

class DriverLeaderboardEntry(BaseModel):
    rank: int
    driver_id: str
    driver_name: str
    badge_tier: str
    safety_score: int
    completed_trips: int
    total_distance_km: float

class DriverLeaderboardResponse(BaseModel):
    organization_id: str
    total_drivers: int
    leaderboard: List[DriverLeaderboardEntry]
