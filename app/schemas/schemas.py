from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional, List, UUID4

# User Schemas
class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8)
    first_name: str
    last_name: str
    date_of_birth: str  # YYYY-MM-DD
    phone_number: Optional[str] = None

class UserResponse(BaseModel):
    id: UUID4
    email: str
    first_name: str
    last_name: str
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True

class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    expires_in: int

# Health Schemas
class HealthReadingCreate(BaseModel):
    reading_type: str
    value: float
    secondary_value: Optional[float] = None
    unit: str
    notes: Optional[str] = None

class HealthReadingResponse(BaseModel):
    id: UUID4
    reading_type: str
    value: float
    secondary_value: Optional[float]
    unit: str
    status: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True

# Reminder Schemas
class ReminderCreate(BaseModel):
    reminder_type: str
    title: str
    description: Optional[str] = None
    schedule_type: str
    schedule_time: str
    days_of_week: Optional[List[str]] = None
    reminder_minutes_before: int = 10

class ReminderResponse(BaseModel):
    id: UUID4
    reminder_type: str
    title: str
    schedule_type: str
    status: str
    created_at: datetime

    class Config:
        from_attributes = True

# Chat Schemas
class ChatMessageCreate(BaseModel):
    message: str
    context: str = "general"

class ChatMessageResponse(BaseModel):
    response: str
    confidence: float
    emotional_tone: Optional[str]

    class Config:
        from_attributes = True

# Family Schemas
class FamilyMemberCreate(BaseModel):
    family_email: EmailStr
    relationship: str
    can_view_health: bool = True
    can_edit_reminders: bool = False

class FamilyMemberResponse(BaseModel):
    id: UUID4
    family_email: str
    relationship: str
    joined_at: datetime

    class Config:
        from_attributes = True

# Health Summary
class HealthSummaryResponse(BaseModel):
    user_name: str
    date: str
    health_status: str
    readings: dict
    reminders_completed: int
    reminders_total: int
    alerts: List[str]
