from datetime import datetime, timedelta
from typing import Optional, Dict, List
from sqlalchemy.orm import Session

from app.models.fuel_log import FuelLog
from app.models.maintenance import ServiceRecord
from app.models.expense_log import ExpenseLog

def get_cost_breakdown(
    db: Session,
    organization_id: str,
    vehicle_id: Optional[str] = None,
    timeframe: str = "6m"
) -> Dict:
    timeframe_map = {
        "1m": 30,
        "30d": 30,
        "3m": 90,
        "90d": 90,
        "6m": 180,
        "1y": 365
    }
    days = timeframe_map.get(timeframe.lower(), 180)
    cutoff = datetime.utcnow() - timedelta(days=days)

    fuel_query = db.query(FuelLog).filter(
        FuelLog.organization_id == organization_id,
        FuelLog.deleted_at == None,
        FuelLog.log_date >= cutoff
    )
    if vehicle_id:
        fuel_query = fuel_query.filter(FuelLog.vehicle_id == vehicle_id)
    fuel_logs = fuel_query.all()

    mnt_query = db.query(ServiceRecord).filter(
        ServiceRecord.organization_id == organization_id,
        ServiceRecord.deleted_at == None,
        ServiceRecord.service_date >= cutoff.date()
    )
    if vehicle_id:
        mnt_query = mnt_query.filter(ServiceRecord.vehicle_id == vehicle_id)
    mnt_logs = mnt_query.all()

    exp_query = db.query(ExpenseLog).filter(
        ExpenseLog.organization_id == organization_id,
        ExpenseLog.deleted_at == None,
        ExpenseLog.expense_date >= cutoff
    )
    if vehicle_id:
        exp_query = exp_query.filter(ExpenseLog.vehicle_id == vehicle_id)
    exp_logs = exp_query.all()

    total_fuel = sum(fl.total_cost or 0.0 for fl in fuel_logs)
    total_mnt = sum(ml.total_cost or 0.0 for ml in mnt_logs)
    total_exp = sum(el.amount or 0.0 for el in exp_logs)
    grand_total = total_fuel + total_mnt + total_exp

    monthly_data: Dict[str, Dict[str, float]] = {}

    for fl in fuel_logs:
        period = fl.log_date.strftime("%Y-%m")
        if period not in monthly_data:
            monthly_data[period] = {"fuel": 0.0, "mnt": 0.0, "exp": 0.0}
        monthly_data[period]["fuel"] += fl.total_cost or 0.0

    for ml in mnt_logs:
        period = ml.service_date.strftime("%Y-%m")
        if period not in monthly_data:
            monthly_data[period] = {"fuel": 0.0, "mnt": 0.0, "exp": 0.0}
        monthly_data[period]["mnt"] += ml.total_cost or 0.0


    for el in exp_logs:
        period = el.expense_date.strftime("%Y-%m")
        if period not in monthly_data:
            monthly_data[period] = {"fuel": 0.0, "mnt": 0.0, "exp": 0.0}
        monthly_data[period]["exp"] += el.amount or 0.0

    items = []
    for period in sorted(monthly_data.keys()):
        p_data = monthly_data[period]
        f_cost = round(p_data["fuel"], 2)
        m_cost = round(p_data["mnt"], 2)
        e_cost = round(p_data["exp"], 2)
        t_cost = round(f_cost + m_cost + e_cost, 2)

        items.append({
            "period": period,
            "fuel_cost": f_cost,
            "maintenance_cost": m_cost,
            "other_expense_cost": e_cost,
            "total_cost": t_cost
        })

    return {
        "timeframe": timeframe,
        "vehicle_id": vehicle_id,
        "total_fuel_cost": round(total_fuel, 2),
        "total_maintenance_cost": round(total_mnt, 2),
        "total_other_expense_cost": round(total_exp, 2),
        "grand_total_cost": round(grand_total, 2),
        "items": items
    }
