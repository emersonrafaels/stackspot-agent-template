from pathlib import Path
from typing import Any, Dict, List

from src.agents.base_agent import BaseAgent
from src.config.config_dynaconf import get_settings
from src.config.config_logger import logger
from src.config.stackspot_config import get_stackspot_config
from src.models.llm import LLMConfig
from src.models.prompt import PromptConfig
from src.utils.api_client import StackSpotAPIClient

# Retrieve settings instance
settings = get_settings()

# Retrieve settings instance
stackspot_config = get_stackspot_config()


class StackSpotAgent(BaseAgent):
    """Implementation of StackSpot AI agent."""

    def __init__(
        self,
        name: str,
        description: str,
        llm_config: LLMConfig,
        prompt_config: PromptConfig,
        client_id: str,
        client_secret: str,
        realm: str,
        auth_url: str = None,
        base_url: str = None,
        endpoint: str = None,
    ):
        """Initialize StackSpot Agent.

        Args:
            name (str): Agent name
            description (str): Agent description
            llm_config (LLMConfig): LLM configuration
            prompt_config (PromptConfig): Prompt configuration
            client_id (str): OAuth client ID
            client_secret (str): OAuth client secret
            realm (str): Account realm for authentication
            auth_url (str, optional): Auth URL for token. Defaults from settings.
            base_url (str, optional): Base inference API URL. Defaults from settings.
            endpoint (str, optional): API endpoint for agent operations. Defaults to None.
        """
        self.name = name
        self.description = description
        self.llm = llm_config
        self.prompt = prompt_config

        # Get base URLs from settings if not provided
        inference_url = base_url or stackspot_config.get("inference_url")
        auth_url = auth_url or stackspot_config.get("auth_url")

        # Initialize API client and get OAuth token
        self.api_client = StackSpotAPIClient(
            base_url=inference_url,
            auth_url=auth_url,
            realm=realm
        )

        # Get OAuth token
        self.access_token = self.api_client.get_oauth_token(
            url=auth_url,
            client_id=client_id,
            client_secret=client_secret
        )
        
        # Set endpoint for agent operations
        self.endpoint = endpoint or "chat"

    def create(self) -> Dict[str, Any]:
        """Create a new agent in StackSpot."""
        try:
            logger.info(f"Creating agent: {self.name}")
            payload = {
                "name": self.name,
                "description": self.description,
                "llm": self.llm.to_dict(),
                "prompt": self.prompt.to_dict(),
            }
            result = self.api_client.post(
                endpoint="agents", data=payload, access_token=self.access_token
            )
            logger.success(f"Agent created successfully: {result.get('id', 'No ID')}")
            return result
        except Exception as e:
            logger.error(f"Error creating agent: {str(e)}")
            raise

    def execute(
        self,
        prompt: str,
        context: List[Dict[str, str]] = None,
        streaming: bool = True,
        use_stackspot_knowledge: bool = True,
        return_ks_in_response: bool = False,
        files: List[Path] = None
    ) -> Dict[str, Any]:
        """Execute a prompt with the agent.

        Args:
            prompt (str): The user prompt to send to the agent
            context (List[Dict[str, str]], optional): Previous conversation context. Defaults to None.
            streaming (bool, optional): Whether to stream responses. Defaults to True.
            use_stackspot_knowledge (bool, optional): Use StackSpot knowledge. Defaults to True.
            return_ks_in_response (bool, optional): Return knowledge source in response. Defaults to False.
            files (List[Path], optional): List of paths to files to upload and include in context.
        """
        try:
            logger.info(f"Executing prompt: {prompt[:50]}...")
            payload = {
                "user_prompt": prompt,
                "context": context or [],
                "streaming": streaming,
                "stackspot_knowledge": use_stackspot_knowledge,
                "return_ks_in_response": return_ks_in_response,
            }
            result = self.api_client.post(
                endpoint=self.endpoint,
                data=payload,
                access_token=self.access_token,
                files=files
            )
            logger.success("Prompt executed successfully")
            return result
        except Exception as e:
            logger.error(f"Error executing prompt: {str(e)}")
            raise

    def list(self) -> Dict[str, Any]:
        """List all agents."""
        try:
            logger.info("Listing all agents...")
            result = self.api_client.get(
                endpoint="agents", access_token=self.access_token
            )
            logger.success("Agents listed successfully")
            return result
        except Exception as e:
            logger.error(f"Error listing agents: {str(e)}")
            raise

    def get(self) -> Dict[str, Any]:
        """Get agent details."""
        try:
            logger.info(f"Getting agent details: {self.name}")
            result = self.api_client.get(
                endpoint=f"agents/{self.name}", access_token=self.access_token
            )
            logger.success("Agent details retrieved successfully")
            return result
        except Exception as e:
            logger.error(f"Error getting agent details: {str(e)}")
            raise

    def update(self) -> Dict[str, Any]:
        """Update agent details."""
        try:
            logger.info(f"Updating agent: {self.name}")
            payload = {
                "name": self.name,
                "description": self.description,
                "llm": self.llm.to_dict(),
                "prompt": self.prompt.to_dict(),
            }
            result = self.api_client.put(
                endpoint=f"agents/{self.name}",
                data=payload,
                access_token=self.access_token,
            )
            logger.success("Agent updated successfully")
            return result
        except Exception as e:
            logger.error(f"Error updating agent: {str(e)}")
            raise

    def delete(self) -> Dict[str, Any]:
        """Delete agent."""
        try:
            logger.info(f"Deleting agent: {self.name}")
            result = self.api_client.delete(
                endpoint=f"agents/{self.name}", access_token=self.access_token
            )
            logger.success("Agent deleted successfully")
            return result
        except Exception as e:
            logger.error(f"Error deleting agent: {str(e)}")
            raise
