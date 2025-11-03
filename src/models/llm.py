from dataclasses import dataclass
from typing import Dict, Any


@dataclass
class LLMConfig:
    """Configuration for the Language Model.
    
    Args:
        provider (str): The LLM provider name
        model (str): The model name/identifier
        temperature (float, optional): Controls randomness in responses. Defaults to 0.7.
            - Higher values (0.7-1.0) make output more random and creative
            - Lower values (0.0-0.3) make output more focused and deterministic
        top_p (float, optional): Controls diversity via nucleus sampling. Defaults to 1.0.
            - 1.0 considers all tokens in distribution
            - Lower values (e.g. 0.1) consider only highest probability tokens
        frequency_penalty (float, optional): Penalizes repeated tokens. Defaults to 0.1.
            - Higher values (0.5-1.0) decrease likelihood of repetition
            - 0.0 applies no penalty
        presence_penalty (float, optional): Penalizes repeated topics. Defaults to 0.0.
            - Higher values (0.5-1.0) encourage topic diversity
            - 0.0 applies no penalty
    """

    provider: str
    model: str
    temperature: float = 0.7
    top_p: float = 1.0
    frequency_penalty: float = 0.1
    presence_penalty: float = 0.0

    def to_dict(self) -> Dict[str, Any]:
        """Convert config to dictionary format."""
        return {
            "provider": self.provider,
            "model": self.model,
            "temperature": self.temperature,
            "top_p": self.top_p,
            "frequency_penalty": self.frequency_penalty,
            "presence_penalty": self.presence_penalty
        }
