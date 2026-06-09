from sqlalchemy.orm import Session
from app.models.models import User, HealthReading, NormalRange
from app.schemas.schemas import HealthReadingCreate
from app.utils.security import hash_password, verify_password
from app.schemas.schemas import UserCreate
import logging

logger = logging.getLogger(__name__)

class UserService:
    @staticmethod
    def create_user(db: Session, user_data: UserCreate) -> User:
        """Create a new user"""
        hashed_password = hash_password(user_data.password)
        db_user = User(
            email=user_data.email,
            password_hash=hashed_password,
            first_name=user_data.first_name,
            last_name=user_data.last_name,
            date_of_birth=user_data.date_of_birth,
            phone_number=user_data.phone_number,
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)

        # Create default normal ranges
        normal_ranges = NormalRange(user_id=db_user.id)
        db.add(normal_ranges)
        db.commit()

        return db_user

    @staticmethod
    def get_user_by_email(db: Session, email: str) -> User:
        """Get user by email"""
        return db.query(User).filter(User.email == email).first()

    @staticmethod
    def verify_user_password(db: Session, email: str, password: str) -> User:
        """Verify user credentials"""
        user = UserService.get_user_by_email(db, email)
        if not user or not verify_password(password, user.password_hash):
            return None
        return user


class HealthService:
    @staticmethod
    def add_health_reading(db: Session, user_id, reading_data: HealthReadingCreate) -> HealthReading:
        """Add a health reading"""
        db_reading = HealthReading(
            user_id=user_id,
            reading_type=reading_data.reading_type,
            value=reading_data.value,
            secondary_value=reading_data.secondary_value,
            unit=reading_data.unit,
            notes=reading_data.notes,
        )

        # Analyze reading
        status = HealthService.analyze_reading(db, user_id, reading_data)
        db_reading.status = status

        db.add(db_reading)
        db.commit()
        db.refresh(db_reading)
        return db_reading

    @staticmethod
    def analyze_reading(db: Session, user_id, reading_data: HealthReadingCreate) -> str:
        """Analyze health reading and return status"""
        normal_ranges = db.query(NormalRange).filter(NormalRange.user_id == user_id).first()

        if reading_data.reading_type == "blood_pressure":
            systolic = int(reading_data.value)
            diastolic = int(reading_data.secondary_value) if reading_data.secondary_value else 0

            if systolic > 180 or diastolic > 120:
                return "critical"
            elif systolic >= 140 or diastolic >= 90:
                return "warning"
            else:
                return "normal"

        elif reading_data.reading_type == "glucose":
            value = int(reading_data.value)
            if value < 54 or value > 400:
                return "critical"
            elif value < 70 or value > 200:
                return "warning"
            else:
                return "normal"

        elif reading_data.reading_type == "temperature":
            value = float(reading_data.value)
            if value > 104:
                return "critical"
            elif value > 100.4:
                return "warning"
            else:
                return "normal"

        return "normal"

    @staticmethod
    def get_health_readings(db: Session, user_id, days: int = 30):
        """Get health readings for user"""
        from datetime import datetime, timedelta

        start_date = datetime.utcnow() - timedelta(days=days)
        readings = db.query(HealthReading).filter(
            HealthReading.user_id == user_id,
            HealthReading.created_at >= start_date
        ).all()

        return readings
