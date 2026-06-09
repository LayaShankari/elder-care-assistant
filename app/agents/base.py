from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)

class BaseAgent(ABC):
    """Base class for all Elder Care Assistant agents"""

    def __init__(self, agent_id: str, agent_name: str):
        self.agent_id = agent_id
        self.agent_name = agent_name
        self.logger = logging.getLogger(f"{__name__}.{agent_name}")

    @abstractmethod
    async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process input and return response"""
        pass

    @abstractmethod
    async def validate_input(self, input_data: Dict[str, Any]) -> bool:
        """Validate input data"""
        pass

    async def log_interaction(self, user_id: str, input_data: Dict, output_data: Dict):
        """Log agent interaction"""
        self.logger.info(
            f"Agent {self.agent_name} - User: {user_id}, Input: {input_data}, Output: {output_data}"
        )

    def get_agent_info(self) -> Dict[str, str]:
        """Get agent information"""
        return {
            "agent_id": self.agent_id,
            "agent_name": self.agent_name,
            "status": "active"
        }
