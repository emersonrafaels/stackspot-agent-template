"""Module for chatting with StackSpot agents."""

from typing import Any, Dict, Optional

from src.config.config_logger import logger
from src.config.stackspot_config import get_stackspot_config
from src.utils.api_client import StackSpotAPIClient


class AgentChat:
    """Simple interface for chatting with StackSpot agents."""

    def __init__(
        self,
        agent_id: str,
        realm: str = None,
        client_id: str = None,
        client_secret: str = None,
        base_url: str = "https://genai-inference-app.stackspot.com/v1",
        auth_url: str = "https://idm.stackspot.com",
    ):
        """Initialize chat with an agent.

        Args:
            agent_id (str): ID of the existing agent
            realm (str, optional): StackSpot realm. Defaults to None.
            client_id (str, optional): OAuth client ID. Defaults to None.
            client_secret (str, optional): OAuth client secret. Defaults to None.
            base_url (str, optional): Base API URL. Defaults to None.
            auth_url (str, optional): Auth URL. Defaults to None.
        """
        # Get configuration, overriding with provided values
        config = get_stackspot_config()

        self.agent_id = agent_id
        self.api_client = StackSpotAPIClient(
            base_url=base_url or config["base_url"],
            auth_url=auth_url or config["auth_url"],
            realm=realm or config["realm"],
        )
        self.access_token = self.api_client.get_oauth_token(
            client_id=client_id or config["client_id"],
            client_secret=client_secret or config["client_secret"],
        )

    def ask(self, question: str, use_stackspot_docs: bool = True) -> str:
        """Send a question to the agent.

        Args:
            question (str): The question to ask
            use_stackspot_docs (bool, optional): Use StackSpot documentation. Defaults to True.

        Returns:
            str: Agent's response
        """
        try:
            logger.info(f"Asking agent: {question[:50]}...")

            response = self.api_client.post(
                endpoint=f"agent/{self.agent_id}/chat",
                data={
                    "user_prompt": question,
                    "streaming": True,
                    "stackspot_knowledge": use_stackspot_docs,
                    "return_ks_in_response": False,
                },
                access_token=self.access_token,
            )

            # Extract just the response text
            answer = response.get("response", "")
            logger.success("Got response from agent")
            return answer

        except Exception as e:
            logger.error(f"Failed to get response: {str(e)}")
            raise
