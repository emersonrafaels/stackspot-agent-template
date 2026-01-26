import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Optional

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


class StackSpotAgent:
    """
    Class to manage StackSpot AI agents.

    Attributes:
        api_key (str): StackSpot API key
        base_url (str): Base URL for StackSpot API
        name (str): Name of the agent
        description (str): Description of the agent
        llm (LLMConfig): Language model configuration
        prompt (PromptConfig): Prompt configuration
    """

    def __init__(
        self,
        api_key: str,
        name: str,
        description: str,
        llm_config: LLMConfig,
        prompt_config: PromptConfig,
        base_url: str = "https://api.stackspot.ai/v1",
    ):
        self.api_key = api_key
        self.base_url = base_url
        self.name = name
        self.description = description
        self.llm = llm_config
        self.prompt = prompt_config
        self._headers = self._create_headers()

    def _create_headers(self) -> Dict[str, str]:
        """Create headers for API requests."""
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

    def _create_agent_payload(self) -> Dict[str, Any]:
        """Create the payload for agent creation."""
        return {
            "name": self.name,
            "description": self.description,
            "llm": {"provider": self.llm.provider, "model": self.llm.model},
            "prompt": {"content": self.prompt.content},
        }

    def create_agent(self) -> Dict[str, Any]:
        """
        Create a new agent in StackSpot.

        Returns:
            Dict[str, Any]: Response from the API

        Raises:
            requests.exceptions.RequestException: If the API request fails
        """
        try:
            logger.info(f"Creating agent: {self.name}")
            payload = self._create_agent_payload()

            response = requests.post(
                f"{self.base_url}/agents", headers=self._headers, json=payload
            )
            response.raise_for_status()

            result = response.json()
            logger.success(f"Agent created successfully: {result.get('id', 'No ID')}")
            return result
        except requests.exceptions.RequestException as e:
            logger.error(f"Error creating agent: {str(e)}")
            raise

    def execute_prompt(
        self, prompt: str, context: Optional[list] = None
    ) -> Dict[str, Any]:
        """
        Execute a prompt with the agent, always sending conversation context.

        Args:
            prompt (str): The prompt to execute
            context (Optional[list]): Conversation context as a list of dicts

        Returns:
            Dict[str, Any]: Response from the API
        """
        try:
            logger.info(f"Executing prompt: {prompt[:50]}...")
            payload = {"prompt": prompt, "context": context or []}
            response = requests.post(
                f"{self.base_url}/agents/execute",
                headers=self._headers,
                json=payload,
            )
            response.raise_for_status()

            result = response.json()
            logger.success("Prompt executed successfully")
            return result

        except requests.exceptions.RequestException as e:
            logger.error(f"Error executing prompt: {str(e)}")
            raise


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


# Example usage
# settings = get_settings()
# stackspot_config = get_stackspot_config()
# handler = ChatWithFilesHandler(
#     agent_id=stackspot_config.get("agent_id"),
#     realm=stackspot_config.get("realm"),
#     client_id=stackspot_config.get("client_id"),
#     client_secret=stackspot_config.get("client_secret"),
#     auth_url=stackspot_config.get("auth_url"),
#     base_url=stackspot_config.get("inference_url"),
#     chat_endpoint=settings.get("stackspot.inference.chat_endpoint"),
# )
# handler.initialize_chat()


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


def create_agent():
    """
    Function to create an agent.
    """
    settings = get_settings()
    llm_config = LLMConfig(provider="openai", model="gpt-4o-mini")
    prompt_config = PromptConfig(content="Hello, I am a StackSpot agent!")
    agent = StackSpotAgent(
        name="Example Agent",
        description="A simple example agent",
        llm_config=llm_config,
        prompt_config=prompt_config,
        client_id=settings.get("stackspot_client_id"),
        client_secret=settings.get("stackspot_client_secret"),
        realm=settings.get("stackspot_realm"),
    )
    agent.create()
    print("Agent created.")


# Expose the functions for external calls
__all__ = ["chat_with_files", "chat", "create_agent"]
