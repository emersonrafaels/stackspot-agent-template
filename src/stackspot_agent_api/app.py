import sys
from dataclasses import dataclass
from typing import Any, Dict, Optional
from pathlib import Path

import requests

# Adicionar src ao path
base_dir = Path(__file__).parents[1]
sys.path.insert(0, str(base_dir))

from src.agents.chat import AgentChat
from src.models.chat_session import ChatSession
from src.models.llm import LLMConfig
from src.models.prompt import PromptConfig
from src.config.stackspot_config import get_stackspot_config
from src.config.config_logger import logger
from src.config.config_dynaconf import get_settings


@dataclass
class LLMConfig:
    """Configuration for the Language Model."""

    provider: str
    model: str


@dataclass
class PromptConfig:
    """Configuration for the agent's prompt."""

    content: str


class ChatWithFilesHandler:
    def __init__(
        self,
        agent_id: str,
        realm: str,
        client_id: str,
        client_secret: str,
        auth_url: str,
        base_url: str,
        chat_endpoint: str,
    ):
        self.agent_id = agent_id
        self.realm = realm
        self.client_id = client_id
        self.client_secret = client_secret
        self.auth_url = auth_url
        self.base_url = base_url
        self.chat_endpoint = chat_endpoint

    def initialize_chat(self):
        """
        Initialize the chat with files.
        """
        session = ChatSession()
        chat = AgentChat(
            agent_id=self.agent_id,
            realm=self.realm,
            client_id=self.client_id,
            client_secret=self.client_secret,
            auth_url=self.auth_url,
            base_url=self.base_url,
            chat_endpoint=self.chat_endpoint,
        )
        print("Chat with files initialized.")


def chat():
    """
    Function to handle chat functionality.
    """
    settings = get_settings()
    stackspot_config = get_stackspot_config()
    session = ChatSession()
    chat = AgentChat(
        agent_id=stackspot_config.get("agent_id"),
        realm=stackspot_config.get("realm"),
        client_id=stackspot_config.get("client_id"),
        client_secret=stackspot_config.get("client_secret"),
        auth_url=stackspot_config.get("auth_url"),
        base_url=stackspot_config.get("inference_url"),
        chat_endpoint=settings.get("stackspot.inference.chat_endpoint"),
    )
    print("Chat initialized.")


# Expose the functions for external calls
__all__ = ["chat_with_files", "chat"]
