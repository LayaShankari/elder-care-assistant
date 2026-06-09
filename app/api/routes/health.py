from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.db import get_db
from app.models.models import User
from app.middleware.auth import get_current_user
from app.schemas.schemas import HealthReadingCreate, HealthReadingResponse
from app.services.services import HealthService

router = APIRouter()

@router.post("/readings", response_model=HealthReadingResponse)
async def add_health_reading(
    reading_data: HealthReadingCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Add a new health reading"""
    reading = HealthService.add_health_reading(db, current_user.id, reading_data)
    return reading

@router.get("/readings")
async def get_health_readings(
    days: int = 30,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get health reading history"""
    readings = HealthService.get_health_readings(db, current_user.id, days)
    return {
        "readings": readings,
        "count": len(readings),
        "period_days": days
    }

@router.get("/summary")
async def get_health_summary(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get health summary"""
    readings = HealthService.get_health_readings(db, current_user.id, days=7)

    # Group by type
    by_type = {}
    for reading in readings:
        if reading.reading_type not in by_type:
            by_type[reading.reading_type] = []
        by_type[reading.reading_type].append(reading)

    return {
        "user_name": f"{current_user.first_name} {current_user.last_name}",
        "readings_count": len(readings),
        "readings_by_type": {k: len(v) for k, v in by_type.items()},
        "last_7_days": [
            {
                "type": r.reading_type,
                "value": float(r.value),
                "status": r.status,
                "date": r.created_at.isoformat()
            } for r in readings
        ]
    }
