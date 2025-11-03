"""Chat session management module."""

from dataclasses import dataclass, field
from typing import List, Dict, Any
from datetime import datetime


@dataclass
class Message:
    """Represents a chat message."""
    role: str
    content: str
    timestamp: datetime = field(default_factory=datetime.now)


@dataclass
class ChatSession:
    """Manages chat session and message history."""
    conversation_id: str = field(default_factory=lambda: str(datetime.now().timestamp()))
    messages: List[Message] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def add_message(self, role: str, content: str) -> None:
        """Add a message to the session history."""
        self.messages.append(Message(role=role, content=content))

    def get_context(self) -> List[Dict[str, str]]:
        """Get formatted conversation context for the API."""
        return [
            {"role": msg.role, "content": msg.content}
            for msg in self.messages
        ]

    def clear(self) -> None:
        """Clear session history."""
        self.messages.clear()