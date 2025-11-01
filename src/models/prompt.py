from dataclasses import dataclass
from typing import Dict


@dataclass
class PromptConfig:
    """Configuration for the agent's prompt."""

    content: str

    def to_dict(self) -> Dict[str, str]:
        """Convert config to dictionary format."""
        return {"content": self.content}
