from sqlalchemy import Column, String, DateTime, Boolean, Integer, Numeric, Text, ForeignKey, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

from app.database.base import Base

class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(255), unique=True, nullable=False, index=True)
    phone_number = Column(String(20))
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    date_of_birth = Column(String(10), nullable=False)  # YYYY-MM-DD
    address = Column(Text)
    password_hash = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    preferred_language = Column(String(10), default="en")
    text_size = Column(String(20), default="normal")
    dark_mode = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    health_readings = relationship("HealthReading", back_populates="user", cascade="all, delete-orphan")
    reminders = relationship("Reminder", back_populates="user", cascade="all, delete-orphan")
    family_members = relationship("FamilyMember", back_populates="user", cascade="all, delete-orphan")
    chat_messages = relationship("ChatMessage", back_populates="user", cascade="all, delete-orphan")
    normal_ranges = relationship("NormalRange", back_populates="user", uselist=False, cascade="all, delete-orphan")

class HealthReading(Base):
    __tablename__ = "health_readings"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    reading_type = Column(String(50), nullable=False)  # blood_pressure, glucose, temperature, weight, heart_rate
    value = Column(Numeric(10, 2), nullable=False)
    secondary_value = Column(Numeric(10, 2))  # For BP diastolic
    unit = Column(String(20), nullable=False)
    status = Column(String(20))  # normal, warning, critical
    notes = Column(Text)
    device_id = Column(String(255))
    created_at = Column(DateTime, default=datetime.utcnow, index=True)

    # Relationships
    user = relationship("User", back_populates="health_readings")

class Reminder(Base):
    __tablename__ = "reminders"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    reminder_type = Column(String(50), nullable=False)  # medication, meal, appointment, exercise
    title = Column(String(255), nullable=False)
    description = Column(Text)
    schedule_type = Column(String(50), nullable=False)  # once, daily, weekly, monthly
    schedule_time = Column(String(5))  # HH:MM format
    days_of_week = Column(JSON)  # ["monday", "tuesday", ...]
    reminder_minutes_before = Column(Integer, default=10)
    status = Column(String(50), default="active")  # active, paused, completed, cancelled
    last_completed = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="reminders")

class NormalRange(Base):
    __tablename__ = "normal_ranges"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), unique=True, nullable=False)
    bp_systolic_min = Column(Integer, default=90)
    bp_systolic_max = Column(Integer, default=130)
    bp_diastolic_min = Column(Integer, default=60)
    bp_diastolic_max = Column(Integer, default=90)
    glucose_min = Column(Integer, default=70)
    glucose_max = Column(Integer, default=130)
    heart_rate_min = Column(Integer, default=60)
    heart_rate_max = Column(Integer, default=100)
    temperature_min = Column(Numeric(4, 2), default=97.0)
    temperature_max = Column(Numeric(4, 2), default=99.0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="normal_ranges")

class FamilyMember(Base):
    __tablename__ = "family_members"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    family_email = Column(String(255), nullable=False)
    family_phone = Column(String(20))
    relationship = Column(String(50))  # spouse, child, sibling, friend, caregiver
    can_view_health = Column(Boolean, default=True)
    can_view_reminders = Column(Boolean, default=True)
    can_edit_reminders = Column(Boolean, default=False)
    can_initiate_emergency = Column(Boolean, default=False)
    joined_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="family_members")

class ChatMessage(Base):
    __tablename__ = "chat_messages"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    conversation_id = Column(UUID(as_uuid=True))
    role = Column(String(50))  # user, assistant
    content = Column(Text, nullable=False)
    emotional_tone = Column(String(50))  # positive, neutral, concerning
    created_at = Column(DateTime, default=datetime.utcnow, index=True)

    # Relationships
    user = relationship("User", back_populates="chat_messages")
