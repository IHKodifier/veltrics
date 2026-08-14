import logging
from sqlalchemy.orm import Session
from app.db.session import SessionLocal, engine, Base
from app.models.vehicle import VehicleType

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

DEFAULT_VEHICLE_CATALOGUE = [
    {"make": "Toyota", "model": "Corolla", "category": "Sedan", "default_fuel_type": "Petrol", "recommended_oil_interval_km": 5000, "recommended_oil_interval_days": 180},
    {"make": "Honda", "model": "Civic", "category": "Sedan", "default_fuel_type": "Petrol", "recommended_oil_interval_km": 5000, "recommended_oil_interval_days": 180},
    {"make": "Suzuki", "model": "Alto", "category": "Hatchback", "default_fuel_type": "Petrol", "recommended_oil_interval_km": 5000, "recommended_oil_interval_days": 180},
    {"make": "Suzuki", "model": "Cultus", "category": "Hatchback", "default_fuel_type": "Petrol", "recommended_oil_interval_km": 5000, "recommended_oil_interval_days": 180},
    {"make": "Honda", "model": "City", "category": "Sedan", "default_fuel_type": "Petrol", "recommended_oil_interval_km": 5000, "recommended_oil_interval_days": 180},
    {"make": "Toyota", "model": "Hilux Revo", "category": "Pickup", "default_fuel_type": "Diesel", "recommended_oil_interval_km": 5000, "recommended_oil_interval_days": 180},
    {"make": "Hyundai", "model": "Tucson", "category": "SUV", "default_fuel_type": "Petrol", "recommended_oil_interval_km": 5000, "recommended_oil_interval_days": 180},
    {"make": "Kia", "model": "Sportage", "category": "SUV", "default_fuel_type": "Petrol", "recommended_oil_interval_km": 5000, "recommended_oil_interval_days": 180},
    {"make": "BYD", "model": "Atto 3", "category": "SUV", "default_fuel_type": "EV", "recommended_oil_interval_km": 10000, "recommended_oil_interval_days": 365},
]

DEFAULT_MAINTENANCE_TEMPLATES = [
    {"task_name": "Engine Oil & Filter Change", "interval_km": 5000, "interval_days": 180},
    {"task_name": "Air Filter Replacement", "interval_km": 10000, "interval_days": 365},
    {"task_name": "Tire Rotation & Wheel Alignment", "interval_km": 10000, "interval_days": 180},
    {"task_name": "Brake Inspection & Fluid Flush", "interval_km": 40000, "interval_days": 730},
    {"task_name": "Transmission Fluid Change", "interval_km": 60000, "interval_days": 1095},
    {"task_name": "Spark Plugs Replacement", "interval_km": 30000, "interval_days": 540},
]

def seed_database(db: Session) -> dict:
    """
    Idempotent seeding script for Vehicle Master Catalogue and Default Maintenance Templates.
    """
    # Ensure tables are created
    Base.metadata.create_all(bind=db.get_bind())

    seeded_types = 0
    updated_types = 0

    for item in DEFAULT_VEHICLE_CATALOGUE:
        existing = db.query(VehicleType).filter(
            VehicleType.make == item["make"],
            VehicleType.model == item["model"]
        ).first()

        if existing:
            existing.category = item["category"]
            existing.default_fuel_type = item["default_fuel_type"]
            existing.recommended_oil_interval_km = item["recommended_oil_interval_km"]
            existing.recommended_oil_interval_days = item["recommended_oil_interval_days"]
            updated_types += 1
        else:
            vtype = VehicleType(**item)
            db.add(vtype)
            seeded_types += 1

    db.commit()
    logger.info(f"Database Seeding Complete. Added: {seeded_types}, Updated: {updated_types}")

    return {
        "status": "success",
        "vehicle_types_added": seeded_types,
        "vehicle_types_updated": updated_types,
        "templates_available": len(DEFAULT_MAINTENANCE_TEMPLATES)
    }

if __name__ == "__main__":
    db = SessionLocal()
    try:
        res = seed_database(db)
        print("Seeding Result:", res)
    finally:
        db.close()
