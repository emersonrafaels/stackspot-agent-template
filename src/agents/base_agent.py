from abc import ABC, abstractmethod
from typing import Any, Dict


class BaseAgent(ABC):
    """Base class for all agents."""

    @abstractmethod
    def create(self) -> Dict[str, Any]:
        """Create a new agent."""
        pass

    @abstractmethod
    def execute(self, prompt: str) -> Dict[str, Any]:
        """Execute a prompt with the agent."""
        pass
