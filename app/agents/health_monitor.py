from typing import Dict, Any
from app.agents.base import BaseAgent
from app.services.services import HealthService
from sqlalchemy.orm import Session

class HealthMonitorAgent(BaseAgent):
    """Agent for monitoring health readings and detecting anomalies"""

    def __init__(self):
        super().__init__("health-monitor-001", "Health Monitor")

    async def validate_input(self, input_data: Dict[str, Any]) -> bool:
        """Validate health input"""
        required_fields = ["reading_type", "value", "unit"]
        return all(field in input_data for field in required_fields)

    async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process health reading"""
        if not await self.validate_input(input_data):
            return {"error": "Invalid input data"}

        reading_type = input_data.get("reading_type")
        value = float(input_data.get("value"))
        secondary_value = input_data.get("secondary_value")

        # Analyze reading
        status = self._analyze_reading(reading_type, value, secondary_value)
        recommendation = self._get_recommendation(reading_type, value, status)
        alert_family = status in ["warning", "critical"]

        return {
            "status": status,
            "message": self._get_message(reading_type, status),
            "recommendation": recommendation,
            "alert_family": alert_family,
            "trend": "stable"
        }

    def _analyze_reading(self, reading_type: str, value: float, secondary_value: float = None) -> str:
        """Analyze reading and return status"""
        if reading_type == "blood_pressure":
            systolic = int(value)
            diastolic = int(secondary_value) if secondary_value else 0

            if systolic > 180 or diastolic > 120:
                return "critical"
            elif systolic >= 140 or diastolic >= 90:
                return "warning"
            else:
                return "normal"

        elif reading_type == "glucose":
            val = int(value)
            if val < 54 or val > 400:
                return "critical"
            elif val < 70 or val > 200:
                return "warning"
            else:
                return "normal"

        elif reading_type == "temperature":
            if value > 104:
                return "critical"
            elif value > 100.4:
                return "warning"
            else:
                return "normal"

        elif reading_type == "heart_rate":
            val = int(value)
            if val < 40 or val > 130:
                return "warning"
            else:
                return "normal"

        return "normal"

    def _get_message(self, reading_type: str, status: str) -> str:
        """Get user-friendly message"""
        messages = {
            ("blood_pressure", "normal"): "✓ Great! Your blood pressure is in the healthy range.",
            ("blood_pressure", "warning"): "⚠️ Your blood pressure is elevated. Please rest and hydrate.",
            ("blood_pressure", "critical"): "🚨 Your blood pressure is dangerously high. Please seek immediate medical attention.",
            ("glucose", "normal"): "✓ Your blood sugar is at a healthy level.",
            ("glucose", "warning"): "⚠️ Your blood sugar is higher than normal. Monitor closely.",
            ("glucose", "critical"): "🚨 Your blood sugar is critically high. Seek medical help.",
            ("temperature", "normal"): "✓ Your temperature is normal.",
            ("temperature", "warning"): "⚠️ You have a fever. Rest and monitor.",
            ("temperature", "critical"): "🚨 You have a high fever. Seek medical attention.",
            ("heart_rate", "normal"): "✓ Your heart rate is normal.",
            ("heart_rate", "warning"): "⚠️ Your heart rate is unusual. Monitor closely.",
        }

        return messages.get((reading_type, status), f"Your {reading_type} reading has been recorded.")

    def _get_recommendation(self, reading_type: str, value: float, status: str) -> str:
        """Get health recommendation"""
        if status == "critical":
            return "Please call your doctor or emergency services immediately."
        elif status == "warning":
            return "Monitor your reading closely and contact your doctor if it persists."
        else:
            return "Keep maintaining your healthy habits!"
