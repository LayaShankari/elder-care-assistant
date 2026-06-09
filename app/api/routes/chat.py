from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import uuid

from app.database.db import get_db
from app.models.models import User, ChatMessage
from app.middleware.auth import get_current_user
from app.schemas.schemas import ChatMessageCreate, ChatMessageResponse

router = APIRouter()

@router.post("/message", response_model=ChatMessageResponse)
async def send_chat_message(
    chat_data: ChatMessageCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Send message to companion"""
    # Store user message
    user_message = ChatMessage(
        user_id=current_user.id,
        conversation_id=uuid.uuid4(),
        role="user",
        content=chat_data.message
    )
    db.add(user_message)
    db.commit()

    # Generate response (simplified - would use Claude API in production)
    response_text = generate_companion_response(chat_data.message)
    emotional_tone = detect_emotional_tone(chat_data.message)

    # Store assistant message
    assistant_message = ChatMessage(
        user_id=current_user.id,
        conversation_id=user_message.conversation_id,
        role="assistant",
        content=response_text,
        emotional_tone=emotional_tone
    )
    db.add(assistant_message)
    db.commit()

    return {
        "response": response_text,
        "confidence": 0.85,
        "emotional_tone": emotional_tone
    }

@router.get("/history")
async def get_chat_history(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get chat history"""
    messages = db.query(ChatMessage).filter(
        ChatMessage.user_id == current_user.id
    ).order_by(ChatMessage.created_at.desc()).limit(50).all()

    return {
        "messages": [
            {
                "role": m.role,
                "content": m.content,
                "created_at": m.created_at.isoformat()
            }
            for m in reversed(messages)
        ],
        "count": len(messages)
    }

def generate_companion_response(user_message: str) -> str:
    """Generate companion response (simplified)"""
    lower_msg = user_message.lower()

    if "joke" in lower_msg:
        return "Why did the elderly person bring a ladder to the doctor? Because they heard laughter is the best medicine! 😄"
    elif "help" in lower_msg or "how do i" in lower_msg:
        return "I'd be happy to help! What would you like assistance with?"
    elif "reminder" in lower_msg:
        return "You can create reminders by going to 'Activity Reminders' and tapping 'Add Reminder'. What would you like to be reminded about?"
    elif "lonely" in lower_msg or "sad" in lower_msg:
        return "I understand. I'm here for you. Would you like to talk, or would you prefer to do something together?"
    else:
        return f"That's interesting! I'm here to help. Is there anything specific I can assist you with?"

def detect_emotional_tone(message: str) -> str:
    """Detect emotional tone (simplified)"""
    lower_msg = message.lower()

    sad_keywords = ["sad", "lonely", "depressed", "miss", "cry"]
    happy_keywords = ["happy", "great", "wonderful", "love", "excited"]
    worried_keywords = ["worried", "nervous", "anxious", "scared", "afraid"]

    if any(kw in lower_msg for kw in sad_keywords):
        return "concerning"
    elif any(kw in lower_msg for kw in happy_keywords):
        return "positive"
    elif any(kw in lower_msg for kw in worried_keywords):
        return "concerning"

    return "neutral"
