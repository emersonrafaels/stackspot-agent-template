from typing import Any, Dict

from src.agents.base_agent import BaseAgent
from src.config.config_logger import logger
from src.models.llm import LLMConfig
from src.models.prompt import PromptConfig
from src.utils.api_client import StackSpotAPIClient


class StackSpotAgent(BaseAgent):
    """Implementation of StackSpot AI agent."""

    def __init__(
        self,
        name: str,
        description: str,
        llm_config: LLMConfig,
        prompt_config: PromptConfig,
        client_secret: str,
        realm: str,
        base_url: str = None,
        auth_url: str = None,
    ):
        """Initialize StackSpot Agent.
        
        Args:
            client_secret (str): OAuth client secret
            name (str): Agent name/client ID
            description (str): Agent description
            llm_config (LLMConfig): LLM configuration
            prompt_config (PromptConfig): Prompt configuration 
            realm (str): Account realm for authentication
            base_url (str, optional): Base URL for agent API. Defaults to None.
            auth_url (str, optional): Auth URL for token. Defaults to None.
        """
        self.name = name
        self.description = description
        self.llm = llm_config
        self.prompt = prompt_config
        
        # Initialize API client and get OAuth token
        self.api_client = StackSpotAPIClient(
            base_url=base_url,
            auth_url=auth_url,
            realm=realm
        )
        self.access_token = self.api_client.get_oauth_token(
            client_id=self.name,
            client_secret=client_secret
        )

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
                endpoint="agents",
                data=payload,
                access_token=self.access_token
            )
            logger.success(f"Agent created successfully: {result.get('id', 'No ID')}")
            return result
        except Exception as e:
            logger.error(f"Error creating agent: {str(e)}")
            raise

    def execute(
        self, 
        prompt: str,
        streaming: bool = True,
        use_stackspot_knowledge: bool = True,
        return_ks_in_response: bool = False
    ) -> Dict[str, Any]:
        """Execute a prompt with the agent.
        
        Args:
            prompt (str): The user prompt to send to the agent
            streaming (bool, optional): Whether to stream responses. Defaults to True.
            use_stackspot_knowledge (bool, optional): Use StackSpot knowledge. Defaults to True.
            return_ks_in_response (bool, optional): Return knowledge source in response. Defaults to False.
        """
        try:
            logger.info(f"Executing prompt: {prompt[:50]}...")
            payload = {
                "user_prompt": prompt,
                "streaming": streaming,
                "stackspot_knowledge": use_stackspot_knowledge,
                "return_ks_in_response": return_ks_in_response
            }
            result = self.api_client.post(
                endpoint=f"agent/{self.name}/chat",
                data=payload,
                access_token=self.access_token
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
                endpoint="agents",
                access_token=self.access_token
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
                endpoint=f"agents/{self.name}",
                access_token=self.access_token
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
                access_token=self.access_token
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
                endpoint=f"agents/{self.name}",
                access_token=self.access_token
            )
            logger.success("Agent deleted successfully")
            return result
        except Exception as e:
            logger.error(f"Error deleting agent: {str(e)}")
            raise
