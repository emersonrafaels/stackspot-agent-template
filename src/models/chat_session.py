"""Chat session management module.

The module uses dataclasses for efficient model representation:
- @dataclass decorator automatically generates special methods like __init__, __repr__, and __eq__
- field() function provides fine-grained control over default values and field properties
- default_factory allows lazy initialization of mutable defaults
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any
from datetime import datetime
import uuid


@dataclass
class Message:
    """Represents a chat message.
    
    Attributes:
        role (str): Role of the message sender (e.g., "user", "assistant")
        content (str): The actual message content
        timestamp (datetime): When the message was created, auto-generated
    
    Notes:
        Uses dataclass for automatic __init__ and other special methods
        timestamp uses default_factory to ensure unique datetime for each instance
    """
    role: str
    content: str
    timestamp: datetime = field(
        default_factory=datetime.now,
        metadata={"description": "Message creation time"}
    )


@dataclass
class ChatSession:
    """Manages chat session and message history.
    
    Attributes:
        conversation_id (str): Unique identifier for the session using UUID4
        messages (List[Message]): List of messages in the conversation
        metadata (Dict[str, Any]): Additional session data
        
    Notes:
        Uses dataclass for automatic __init__ and other special methods
        All collections (messages, metadata) use default_factory to avoid mutable default issues
        UUID4 ensures globally unique identifiers for sessions
    """
    conversation_id: str = field(
        default_factory=lambda: str(uuid.uuid4()),
        metadata={"description": "Unique session identifier"}
    )
    messages: List[Message] = field(
        default_factory=list,
        metadata={"description": "List of conversation messages"}
    )
    metadata: Dict[str, Any] = field(
        default_factory=dict,
        metadata={"description": "Additional session metadata"}
    )

    def add_message(self, role: str, content: str) -> None:
        """Add a message to the session history.
        
        Args:
            role (str): The role of the message sender (e.g., "user", "assistant")
            content (str): The content of the message
            
        Note:
            Creates a new Message instance with current timestamp automatically
        """
        self.messages.append(Message(role=role, content=content))

    def get_context(self) -> List[Dict[str, str]]:
        """Get formatted conversation context for the API.
        
        Returns:
            List[Dict[str, str]]: List of messages in API format
            
        Note:
            Formats messages as {"role": "...", "content": "..."} for API compatibility
            Preserves message order which is important for conversation context
        """
        return [
            {"role": msg.role, "content": msg.content}
            for msg in self.messages
        ]

    def clear(self) -> None:
        """Clear session history.
        
        Note:
            Maintains the same session ID but removes all messages
            Useful for starting a new conversation in the same session
        """
        self.messages.clear()