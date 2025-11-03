"""Module for chatting with StackSpot agents."""
from typing import Any, Dict, List, Optional, Union
from pathlib import Path

from src.agents.stackspot_agent import StackSpotAgent
from src.config.config_logger import logger
from src.models.llm import LLMConfig
from src.models.prompt import PromptConfig


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
        auth_url: str = None,
        base_url: str = None,
        chat_endpoint: str = None
    ):
        """Initialize chat with an existing agent.

        Args:
            agent_id (str): ID of the existing agent
            realm (str, optional): StackSpot realm. Defaults from settings.
            client_id (str, optional): OAuth client ID. Defaults from settings.
            client_secret (str, optional): OAuth client secret. Defaults from settings.
            auth_url (str, optional): Auth URL. Defaults from settings.
            base_url (str, optional): Base API URL. Defaults from settings.
            chat_endpoint (str, optional): Chat endpoint. Defaults from settings.
        """
        # Create dummy configs since we're using an existing agent
        dummy_llm = LLMConfig(
            provider="openai",
            model="gpt-4o-mini",
            temperature=0,
        )
        dummy_prompt = PromptConfig(
            content="",
        )
        
        # Initialize parent class with existing agent ID as name
        super().__init__(
            name=agent_id,  # Use agent_id as name for API paths
            description="Existing agent",
            llm_config=dummy_llm,
            prompt_config=dummy_prompt,
            client_id=client_id,
            client_secret=client_secret,
            realm=realm,
            auth_url=auth_url,
            base_url=base_url,
            endpoint=chat_endpoint
        )

    def ask(
        self, 
        question: str,
        context: Optional[list] = None,
        streaming: bool = True,
        use_stackspot_docs: bool = True,
        return_ks_in_response: bool = True,
        files: List[Union[str, Path]] = None
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
                files=files
            )
            
            # Extract just the response text
            answer = response.get("message", "")
            return answer

        except Exception as e:
            logger.error(f"Failed to get response: {str(e)}")
            raise
