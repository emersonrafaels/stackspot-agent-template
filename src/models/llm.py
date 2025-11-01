from dataclasses import dataclass
from typing import Dict


@dataclass
class LLMConfig:
    """Configuration for the Language Model."""

    provider: str
    model: str

    def to_dict(self) -> Dict[str, str]:
        """Convert config to dictionary format."""
        return {"provider": self.provider, "model": self.model}
