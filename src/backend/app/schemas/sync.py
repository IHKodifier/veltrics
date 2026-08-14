from typing import Optional, List, Dict, Any
from datetime import datetime
from pydantic import BaseModel, ConfigDict

class SyncOperationEnvelope(BaseModel):
    op_id: str
    entity_type: str  # organizations, users, vehicles, drivers, fuel_logs, maintenance_schedules, service_records, trips, expenses
    action: str  # CREATE, UPDATE, DELETE
    payload: Dict[str, Any]
    base_updated_at: Optional[Any] = None
    client_timestamp: Optional[Any] = None

class SyncBatchRequest(BaseModel):
    organization_id: str
    operations: List[SyncOperationEnvelope]

class SyncOperationResult(BaseModel):
    op_id: str
    status: str  # SUCCESS, CONFLICT, REJECTED
    entity_id: Optional[str] = None
    server_entity: Optional[Dict[str, Any]] = None
    message: Optional[str] = None

class SyncBatchResponse(BaseModel):
    processed_count: int
    results: List[SyncOperationResult]

class DeltaSyncResponse(BaseModel):
    vehicles: List[Dict[str, Any]] = []
    drivers: List[Dict[str, Any]] = []
    fuel_logs: List[Dict[str, Any]] = []
    maintenance_schedules: List[Dict[str, Any]] = []
    service_records: List[Dict[str, Any]] = []
    trips: List[Dict[str, Any]] = []
    expenses: List[Dict[str, Any]] = []
    deleted_ids: Dict[str, List[str]] = {}
    sync_timestamp: Any
