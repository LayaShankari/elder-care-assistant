from typing import Dict, Any
from app.agents.base import BaseAgent
import random

class CompanionAgent(BaseAgent):
    """Agent for providing conversational support and companionship"""

    def __init__(self):
        super().__init__("companion-001", "Companion")

    async def validate_input(self, input_data: Dict[str, Any]) -> bool:
        """Validate companion input"""
        return "message" in input_data

    async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process user message and generate response"""
        if not await self.validate_input(input_data):
            return {"error": "Invalid input data"}

        user_message = input_data.get("message", "").lower()
        context = input_data.get("context", "general")

        response = await self._generate_response(user_message, context)
        emotional_tone = self._detect_tone(user_message)
        confidence = self._calculate_confidence(user_message)

        return {
            "response": response,
            "confidence": confidence,
            "emotional_tone": emotional_tone,
            "requires_human_review": confidence < 0.7
        }

    async def _generate_response(self, message: str, context: str) -> str:
        """Generate companion response"""
        # Check for help requests
        if "help" in message or "how do i" in message:
            return self._get_help_response(message)

        # Check for jokes
        if "joke" in message:
            return self._get_joke()

        # Check for emotional support
        if any(word in message for word in ["sad", "lonely", "depressed", "feel bad"]):
            return self._get_emotional_support()

        # Check for health questions
        if any(word in message for word in ["blood pressure", "sugar", "medication", "medicine"]):
            return "I'm not a doctor, but that's a great question for your physician. Would you like help with something else?"

        # General conversation
        return "That's interesting! Tell me more about that. How can I help you today?"

    def _get_help_response(self, message: str) -> str:
        """Get help response"""
        if "reminder" in message:
            return "To add a reminder: Tap 'Activity Reminders' → 'Add Reminder' → Choose type → Set details → Save. Would you like help with anything else?"
        elif "health" in message:
            return "You can log health readings in 'Health Monitor'. Tap it, enter your reading, and the system will analyze it for you."
        elif "family" in message:
            return "To add family members: Go to 'Family Updates' → 'Add Member' → Enter their email → Choose permissions. Easy as that!"
        else:
            return "I'm happy to help! What would you like to know about?"

    def _get_joke(self) -> str:
        """Get a joke"""
        jokes = [
            "Why did the elderly person bring a ladder to the doctor? Because they heard laughter is the best medicine! 😄",
            "What did one wrinkle say to the other? 'You're looking good for your age!' 😊",
            "Why do senior citizens play golf? It's one of the only sports where you can actually hear the ball hit! ⛳",
            "A man tells his doctor 'I want to improve my health. Should I start with exercise or diet?' The doctor replies, 'Start by paying my bill.' 💰",
        ]
        return random.choice(jokes)

    def _get_emotional_support(self) -> str:
        """Get emotional support response"""
        responses = [
            "I understand how you feel. You're not alone. Would you like to talk about it, or would you prefer to do something fun together?",
            "It's okay to feel that way sometimes. Remember, you have people who care about you. Would it help to connect with family?",
            "I'm sorry you're going through this. Want to hear a funny story or would you like to chat about what's on your mind?",
            "Your feelings are valid. Let's try to focus on the positive things. What's something you enjoyed recently?",
        ]
        return random.choice(responses)

    def _detect_tone(self, message: str) -> str:
        """Detect emotional tone"""
        sad_words = ["sad", "lonely", "depressed", "miss", "cry", "unhappy"]
        happy_words = ["happy", "great", "wonderful", "love", "excited"]
        worried_words = ["worried", "nervous", "anxious", "scared", "afraid"]

        if any(word in message for word in sad_words):
            return "concerning"
        elif any(word in message for word in happy_words):
            return "positive"
        elif any(word in message for word in worried_words):
            return "concerning"

        return "neutral"

    def _calculate_confidence(self, message: str) -> float:
        """Calculate response confidence"""
        # Higher confidence for specific requests
        if any(word in message for word in ["help", "how", "joke", "tell"]):
            return 0.95
        else:
            return 0.80
