from typing import List, Optional, Dict, Any
from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from app.db.session import get_db
from app.models.user import User, utc_now
from app.models.organization import Organization
from app.models.vehicle import Vehicle
from app.models.driver import Driver
from app.models.fuel_log import FuelLog
from app.models.maintenance import MaintenanceSchedule, ServiceRecord
from app.models.trip import Trip
from app.models.expense_log import ExpenseLog
from app.models.audit_log import AuditLog
from app.schemas.sync import (
    SyncBatchRequest,
    SyncBatchResponse,
    SyncOperationResult,
    DeltaSyncResponse,
)

router = APIRouter(prefix="/sync", tags=["Sync Engine"])

TOPOLOGICAL_ORDER = {
    "organization": 1,
    "organizations": 1,
    "user": 2,
    "users": 2,
    "vehicle": 3,
    "vehicles": 3,
    "driver": 4,
    "drivers": 4,
    "fuel_log": 5,
    "fuel_logs": 5,
    "maintenanceschedule": 5,
    "maintenance_schedule": 5,
    "maintenance_schedules": 5,
    "servicerecord": 6,
    "service_record": 6,
    "service_records": 6,
    "trip": 5,
    "trips": 5,
    "expenselog": 5,
    "expense_log": 5,
    "expenses": 5,
}

MODEL_MAP = {
    "organization": Organization,
    "organizations": Organization,
    "user": User,
    "users": User,
    "vehicle": Vehicle,
    "vehicles": Vehicle,
    "driver": Driver,
    "drivers": Driver,
    "fuel_log": FuelLog,
    "fuel_logs": FuelLog,
    "maintenanceschedule": MaintenanceSchedule,
    "maintenance_schedule": MaintenanceSchedule,
    "maintenance_schedules": MaintenanceSchedule,
    "servicerecord": ServiceRecord,
    "service_record": ServiceRecord,
    "service_records": ServiceRecord,
    "trip": Trip,
    "trips": Trip,
    "expenselog": ExpenseLog,
    "expense_log": ExpenseLog,
    "expenses": ExpenseLog,
}

def parse_iso_datetime(val: Any) -> Optional[datetime]:
    if not val:
        return None
    if isinstance(val, datetime):
        return val
    if isinstance(val, str):
        s = val.replace("Z", "+00:00").strip()
        # Handle HTTP query param URL decoding where '+' becomes ' '
        if " " in s:
            s = s.replace(" 00:00", "+00:00").replace(" 05:00", "+05:00").replace(" ", "T")
        try:
            return datetime.fromisoformat(s)
        except ValueError:
            try:
                clean_s = s[:19].replace("T", " ")
                return datetime.strptime(clean_s, "%Y-%m-%d %H:%M:%S")
            except Exception:
                return None
    return None

def serialize_model(instance: Any) -> Dict[str, Any]:
    """Helper to convert SQLAlchemy model instance to dict."""
    d = {}
    for column in instance.__table__.columns:
        val = getattr(instance, column.name)
        if isinstance(val, datetime):
            val = val.isoformat()
        d[column.name] = val
    return d

@router.post("/batch", response_model=SyncBatchResponse)
def execute_sync_batch(req: SyncBatchRequest, db: Session = Depends(get_db)):
    """
    UC-119: Offline Sync Batch Transaction Engine.
    Processes operation envelopes inside a single database transaction in strict topological order.
    UC-094: Enforces Server-Wins baseline conflict resolution protocol.
    """
    # 1. Sort operations topologically by entity dependency order
    sorted_ops = sorted(
        req.operations,
        key=lambda op: TOPOLOGICAL_ORDER.get(op.entity_type.lower(), 99)
    )

    results: List[SyncOperationResult] = []

    try:
        for op in sorted_ops:
            entity_key = op.entity_type.lower()
            model_cls = MODEL_MAP.get(entity_key)

            if not model_cls:
                results.append(SyncOperationResult(
                    op_id=op.op_id,
                    status="REJECTED",
                    message=f"Unknown entity_type '{op.entity_type}'"
                ))
                continue

            action = op.action.upper()
            payload = dict(op.payload or {})
            payload_id = payload.get("id") or op.op_id

            if action == "CREATE":
                # Check if entity already exists
                existing = db.query(model_cls).filter_by(id=payload_id).first()
                if existing:
                    # Idempotent skip or update existing
                    results.append(SyncOperationResult(
                        op_id=op.op_id,
                        status="SUCCESS",
                        entity_id=payload_id
                    ))
                    continue

                # Ensure organization_id is set if model requires it
                if hasattr(model_cls, "organization_id") and "organization_id" not in payload:
                    payload["organization_id"] = req.organization_id

                # Parse date/datetime fields in payload
                for k, v in list(payload.items()):
                    if k.endswith("_at") or k.endswith("_date"):
                        parsed_dt = parse_iso_datetime(v)
                        if parsed_dt:
                            payload[k] = parsed_dt

                # Filter valid model columns
                valid_cols = {c.name for c in model_cls.__table__.columns}
                filtered_payload = {k: v for k, v in payload.items() if k in valid_cols}
                if "id" not in filtered_payload:
                    filtered_payload["id"] = payload_id

                instance = model_cls(**filtered_payload)
                db.add(instance)
                db.flush()

                results.append(SyncOperationResult(
                    op_id=op.op_id,
                    status="SUCCESS",
                    entity_id=payload_id
                ))

            elif action == "UPDATE":
                existing = db.query(model_cls).filter_by(id=payload_id).first()
                if not existing:
                    results.append(SyncOperationResult(
                        op_id=op.op_id,
                        status="REJECTED",
                        message=f"Entity '{payload_id}' not found for update"
                    ))
                    continue

                # UC-094: Conflict check (Server-Wins Baseline)
                base_updated_at = parse_iso_datetime(op.base_updated_at)
                if base_updated_at and hasattr(existing, "updated_at") and existing.updated_at:
                    db_updated_at = existing.updated_at
                    # Make naive for safe comparison if needed
                    if db_updated_at.tzinfo is not None and base_updated_at.tzinfo is None:
                        base_updated_at = base_updated_at.replace(tzinfo=timezone.utc)
                    elif db_updated_at.tzinfo is None and base_updated_at.tzinfo is not None:
                        base_updated_at = base_updated_at.replace(tzinfo=None)

                    if db_updated_at > base_updated_at:
                        # Conflict! Server wins baseline.
                        results.append(SyncOperationResult(
                            op_id=op.op_id,
                            status="CONFLICT",
                            entity_id=payload_id,
                            server_entity=serialize_model(existing),
                            message="Server state is newer than client base edit."
                        ))
                        continue

                # Apply non-null fields
                valid_cols = {c.name for c in model_cls.__table__.columns}
                for k, v in payload.items():
                    if k in valid_cols and k != "id":
                        if k.endswith("_at") or k.endswith("_date"):
                            parsed_dt = parse_iso_datetime(v)
                            if parsed_dt:
                                setattr(existing, k, parsed_dt)
                        else:
                            setattr(existing, k, v)

                if hasattr(existing, "updated_at"):
                    existing.updated_at = utc_now()

                db.flush()
                results.append(SyncOperationResult(
                    op_id=op.op_id,
                    status="SUCCESS",
                    entity_id=payload_id
                ))

            elif action == "DELETE":
                existing = db.query(model_cls).filter_by(id=payload_id).first()
                if existing:
                    if hasattr(existing, "deleted_at"):
                        existing.deleted_at = utc_now()
                    else:
                        db.delete(existing)
                    db.flush()

                results.append(SyncOperationResult(
                    op_id=op.op_id,
                    status="SUCCESS",
                    entity_id=payload_id
                ))

        audit = AuditLog(
            organization_id=req.organization_id,
            action="EXECUTE_SYNC_BATCH",
            payload={"batch_count": len(sorted_ops), "success_count": sum(1 for r in results if r.status == "SUCCESS")}
        )
        db.add(audit)
        db.commit()

        return SyncBatchResponse(
            processed_count=len(results),
            results=results
        )

    except Exception as err:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Sync batch transaction failed: {str(err)}"
        )

@router.get("/delta", response_model=DeltaSyncResponse)
def get_delta_sync(
    organization_id: str = Query(..., description="Organization ID"),
    since: Optional[str] = Query(None, description="ISO timestamp string to filter updates since"),
    db: Session = Depends(get_db)
):
    """
    UC-096: Delta Sync Payload Fetching (Incremental Catch-up).
    Returns active entities modified since timestamp along with soft-deleted entity IDs.
    """
    since_dt = parse_iso_datetime(since)
    since_dt_naive = since_dt.replace(tzinfo=None) if (since_dt and since_dt.tzinfo) else since_dt

    delta_tables = {
        "vehicles": Vehicle,
        "drivers": Driver,
        "fuel_logs": FuelLog,
        "maintenance_schedules": MaintenanceSchedule,
        "service_records": ServiceRecord,
        "trips": Trip,
        "expenses": ExpenseLog,
    }

    response_data: Dict[str, Any] = {
        "vehicles": [],
        "drivers": [],
        "fuel_logs": [],
        "maintenance_schedules": [],
        "service_records": [],
        "trips": [],
        "expenses": [],
        "deleted_ids": {},
        "sync_timestamp": utc_now().isoformat()
    }

    for key, model_cls in delta_tables.items():
        all_records = db.query(model_cls).filter(model_cls.organization_id == organization_id).all()

        if since_dt_naive:
            active_list = []
            deleted_list = []
            for rec in all_records:
                rec_updated = getattr(rec, "updated_at", None)
                rec_deleted = getattr(rec, "deleted_at", None)
                
                # Normalize rec_updated for comparison
                if rec_updated and rec_updated.tzinfo is not None:
                    rec_updated = rec_updated.replace(tzinfo=None)
                if rec_deleted and rec_deleted.tzinfo is not None:
                    rec_deleted = rec_deleted.replace(tzinfo=None)

                if rec_deleted is None:
                    if rec_updated and rec_updated > since_dt_naive:
                        active_list.append(rec)
                else:
                    if rec_deleted and rec_deleted > since_dt_naive:
                        deleted_list.append(rec.id)

            response_data[key] = [serialize_model(rec) for rec in active_list]
            response_data["deleted_ids"][key] = deleted_list
        else:
            active_list = [rec for rec in all_records if getattr(rec, "deleted_at", None) is None]
            response_data[key] = [serialize_model(rec) for rec in active_list]
            response_data["deleted_ids"][key] = []

    return DeltaSyncResponse(**response_data)
