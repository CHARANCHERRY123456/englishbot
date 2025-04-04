import json
import os
from typing import Dict, List, Any, Optional
import logging
from pathlib import Path

# Configure logging
logger = logging.getLogger(__name__)

class JsonDatabase:
    def __init__(self, db_path: str = "database/data.json"):
        """
        Initialize the JSON database
        
        Args:
            db_path: Path to the JSON database file
        """
        self.db_path = db_path
        self.data = self._load_data()
    
    def _load_data(self) -> Dict:
        """Load data from the JSON file"""
        try:
            if os.path.exists(self.db_path):
                with open(self.db_path, 'r') as f:
                    return json.load(f)
            return {"conversations": {}, "next_id": 1}
        except Exception as e:
            logger.error(f"Error loading database: {str(e)}")
            return {"conversations": {}, "next_id": 1}
    
    def _save_data(self) -> None:
        """Save data to the JSON file"""
        try:
            # Ensure directory exists
            os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
            
            with open(self.db_path, 'w') as f:
                json.dump(self.data, f, indent=2)
        except Exception as e:
            logger.error(f"Error saving database: {str(e)}")
    
    def create_conversation(self, conversation: Dict) -> str:
        """
        Create a new conversation
        
        Args:
            conversation: Conversation data
        
        Returns:
            The ID of the created conversation
        """
        conversation_id = str(self.data["next_id"])
        self.data["next_id"] += 1
        conversation["id"] = conversation_id
        self.data["conversations"][conversation_id] = conversation
        self._save_data()
        return conversation_id
    
    def get_conversation(self, conversation_id: str) -> Optional[Dict]:
        """
        Get a conversation by ID
        
        Args:
            conversation_id: The ID of the conversation
        
        Returns:
            The conversation data or None if not found
        """
        return self.data["conversations"].get(conversation_id)
    
    def get_conversations_by_user(self, user_id: str) -> List[Dict]:
        """
        Get all conversations for a user
        
        Args:
            user_id: The ID of the user
        
        Returns:
            A list of conversations
        """
        return [
            conv for conv in self.data["conversations"].values()
            if conv.get("user_id") == user_id
        ]
    
    def update_conversation(self, conversation_id: str, conversation: Dict) -> None:
        """
        Update a conversation
        
        Args:
            conversation_id: The ID of the conversation
            conversation: Updated conversation data
        """
        if conversation_id in self.data["conversations"]:
            self.data["conversations"][conversation_id] = conversation
            self._save_data()
    
    def delete_conversation(self, conversation_id: str) -> None:
        """
        Delete a conversation
        
        Args:
            conversation_id: The ID of the conversation
        """
        if conversation_id in self.data["conversations"]:
            del self.data["conversations"][conversation_id]
            self._save_data()
# Global database instance
_db_instance = None

def init_db():
    """Initialize the database"""
    global _db_instance
    _db_instance = JsonDatabase()

def get_db():
    """Get the database instance"""
    global _db_instance
    if _db_instance is None:
        init_db()
    return _db_instance