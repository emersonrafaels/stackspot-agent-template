"""Module for chatting with StackSpot agents."""

from pathlib import Path
from typing import List, Optional, Union

from .stackspot_agent_chat import StackSpotAgent
from ..config.config_logger import logger
from ..models.llm import LLMConfig
from ..models.prompt import PromptConfig


class AgentChat(StackSpotAgent):
    """Simple interface for chatting with StackSpot agents.

    Extends StackSpotAgent to provide a simpler interface focused on chat interactions.
    """

    def __init__(
        self,
        agent_id: str,
        realm: str = None,
        client_id: str = None,
        client_secret: str = None,
    ):
        """Initialize chat with an existing agent.

        Args:
            agent_id (str): ID of the existing agent
            realm (str, optional): StackSpot realm. Defaults from settings.
            client_id (str, optional): OAuth client ID.
            client_secret (str, optional): OAuth client secret.
        """

        # Initialize parent class with existing agent ID as name
        super().__init__(
            agent_id=agent_id,
            realm=realm,
            client_id=client_id,
            client_secret=client_secret,
            endpoint="chat",
        )

    def ask(
        self,
        question: str,
        context: Optional[list] = None,
        streaming: bool = True,
        use_stackspot_docs: bool = True,
        return_ks_in_response: bool = True,
        files: List[Union[str, Path]] = None,
    ) -> str:
        """Send a question to the agent.

        Args:
            question (str): The question to ask
            context (list, optional): Previous conversation context. Defaults to None.
            streaming (bool, optional): Enable streaming responses. Defaults to True.
            use_stackspot_docs (bool, optional): Use StackSpot documentation. Defaults to True.
            return_ks_in_response (bool, optional): Return knowledge sources in response. Defaults to True.
            files (List[Union[str, Path]], optional): List of file paths to include in context.

        Returns:
            str: Agent's response
        """
        try:
            # Convert any string paths to Path objects
            if files:
                files = [Path(f) if isinstance(f, str) else f for f in files]

            # Use parent's execute method with simplified interface
            response = self.execute(
                prompt=question,
                context=context,
                streaming=streaming,
                use_stackspot_knowledge=use_stackspot_docs,
                return_ks_in_response=return_ks_in_response,
                files=files,
            )

            # Return all response content as a string
            return response if isinstance(response, (dict)) else {}

        except Exception as e:
            logger.error(f"Failed to get response: {str(e)}")
            return {}
