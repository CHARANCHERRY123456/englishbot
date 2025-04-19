import os
import pickle
from datetime import datetime
from typing import List

from conversation.schemas import ConversationCreate, MessageCreate, ConversationOut, MessageOut
from conversation.models import ConversationModel as Conversation, MessageModel as Message
from google.generativeai import GenerativeModel, configure

# 🌐 Gemini Configuration
configure(api_key=os.getenv("GEMINI_API_KEY"))
model = GenerativeModel("gemini-1.5-flash")

# Path helper
def get_pickle_path(convo_id: str) -> str:
    return f"chat_history/{convo_id}.pkl"

class ConversationService:
    def __init__(self):
        os.makedirs("chat_history", exist_ok=True)
        # Simulated storage for now (replace with DB if needed)
        self.conversations = {}
        self.messages = {}

    def load_history(self, conversation_id: str):
        path = get_pickle_path(conversation_id)
        if os.path.exists(path):
            with open(path, "rb") as f:
                return pickle.load(f)
        return []

    def save_history(self, conversation_id: str, history):
        path = get_pickle_path(conversation_id)
        with open(path, "wb") as f:
            pickle.dump(history, f)

    async def create_conversation(self, data: ConversationCreate) -> ConversationOut:
        convo_id = f"convo_{len(self.conversations)+1}"
        convo = ConversationModel(
            title=data.title or "Untitled",
            description=data.description,
            image=data.image,
            user_id=data.user_id,
            created_at=datetime.utcnow()
        )
        self.conversations[convo_id] = convo
        return ConversationOut(id=convo_id, **convo.dict())

    async def add_message(self, conversation_id: str, msg: MessageCreate) -> MessageOut:
        # Save user message
        user_msg = MessageModel(
            content=msg.content,
            sender_id=msg.sender_id,
            conversation_id=conversation_id,
            timestamp=datetime.utcnow()
        )
        self.messages.setdefault(conversation_id, []).append(user_msg)

        # Chat logic
        history = self.load_history(conversation_id)
        chat = model.start_chat(history=history)
        response = chat.send_message(msg.content).text
        self.save_history(conversation_id, chat.history)

        # Save Gemini response
        assistant_msg = MessageModel(
            content=response,
            sender_id="ai",
            conversation_id=conversation_id,
            timestamp=datetime.utcnow()
        )
        self.messages[conversation_id].append(assistant_msg)

        return MessageOut(**assistant_msg.dict())

    async def get_conversation_history(self, conversation_id: str, limit: int = 20, offset: int = 0) -> List[MessageOut]:
        msgs = self.messages.get(conversation_id, [])[offset:offset+limit]
        return [MessageOut(**msg.dict()) for msg in msgs]

# Singleton instance + DI
conversation_service_instance = ConversationService()

def get_conversation_service():
    return conversation_service_instance
