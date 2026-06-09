from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import datetime

from app.database.db import get_db
from app.models.models import User, Reminder
from app.middleware.auth import get_current_user
from app.schemas.schemas import ReminderCreate, ReminderResponse

router = APIRouter()

@router.post("/", response_model=ReminderResponse)
async def create_reminder(
    reminder_data: ReminderCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new reminder"""
    db_reminder = Reminder(
        user_id=current_user.id,
        reminder_type=reminder_data.reminder_type,
        title=reminder_data.title,
        description=reminder_data.description,
        schedule_type=reminder_data.schedule_type,
        schedule_time=reminder_data.schedule_time,
        days_of_week=reminder_data.days_of_week,
        reminder_minutes_before=reminder_data.reminder_minutes_before,
    )
    db.add(db_reminder)
    db.commit()
    db.refresh(db_reminder)
    return db_reminder

@router.get("/")
async def list_reminders(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all reminders for user"""
    reminders = db.query(Reminder).filter(
        Reminder.user_id == current_user.id,
        Reminder.status == "active"
    ).all()
    return {"reminders": reminders, "count": len(reminders)}

@router.get("/upcoming")
async def get_upcoming_reminders(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get upcoming reminders"""
    reminders = db.query(Reminder).filter(
        Reminder.user_id == current_user.id,
        Reminder.status == "active"
    ).all()

    return {
        "upcoming": [
            {
                "id": str(r.id),
                "title": r.title,
                "type": r.reminder_type,
                "time": r.schedule_time,
                "next_reminder": r.schedule_time  # Simplified
            }
            for r in reminders
        ]
    }

@router.patch("/{reminder_id}/complete")
async def mark_reminder_complete(
    reminder_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Mark reminder as complete"""
    reminder = db.query(Reminder).filter(
        Reminder.id == reminder_id,
        Reminder.user_id == current_user.id
    ).first()

    if not reminder:
        return {"error": "Reminder not found"}

    reminder.last_completed = datetime.utcnow()
    db.commit()

    return {
        "status": "completed",
        "reminder_id": str(reminder.id),
        "completed_at": datetime.utcnow().isoformat()
    }

@router.delete("/{reminder_id}")
async def delete_reminder(
    reminder_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete a reminder"""
    reminder = db.query(Reminder).filter(
        Reminder.id == reminder_id,
        Reminder.user_id == current_user.id
    ).first()

    if not reminder:
        return {"error": "Reminder not found"}

    db.delete(reminder)
    db.commit()

    return {"status": "deleted", "reminder_id": str(reminder.id)}
