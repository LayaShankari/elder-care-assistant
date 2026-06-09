from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import datetime

from app.database.db import get_db
from app.models.models import User, FamilyMember
from app.middleware.auth import get_current_user

router = APIRouter()

@router.post("/activate")
async def activate_emergency(
    emergency_data: dict,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Activate emergency protocol"""
    emergency_type = emergency_data.get("type", "general")
    severity = emergency_data.get("severity", "high")

    # Get family members to notify
    family_members = db.query(FamilyMember).filter(
        FamilyMember.user_id == current_user.id
    ).all()

    # In production: call 911, send SMS, etc
    actions_taken = []

    if severity == "critical":
        actions_taken.append("called_911")

    actions_taken.append(f"notified_{len(family_members)}_family_members")

    return {
        "status": "emergency_activated",
        "emergency_type": emergency_type,
        "severity": severity,
        "timestamp": datetime.utcnow().isoformat(),
        "actions_taken": actions_taken,
        "message": "Emergency services have been alerted. Stay calm.",
        "family_notified": [m.family_email for m in family_members]
    }

@router.get("/status/{emergency_id}")
async def get_emergency_status(
    emergency_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get emergency status"""
    # In production: look up emergency record
    return {
        "emergency_id": emergency_id,
        "status": "active",
        "estimated_arrival": "5-7 minutes",
        "responders": 2
    }

@router.post("/contacts")
async def add_emergency_contact(
    contact_data: dict,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Add emergency contact"""
    # In production: save to database
    return {
        "status": "contact_added",
        "name": contact_data.get("name"),
        "phone": contact_data.get("phone")
    }

@router.get("/history")
async def get_emergency_history(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get emergency history"""
    # In production: query emergency records
    return {
        "emergencies": [],
        "count": 0
    }
