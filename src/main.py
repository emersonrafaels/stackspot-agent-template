import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Optional

import requests

from src.config import logger


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

    def execute_prompt(self, prompt: str) -> Dict[str, Any]:
        """
        Execute a prompt with the agent.

        Args:
            prompt (str): The prompt to execute

        Returns:
            Dict[str, Any]: Response from the API
        """
        try:
            logger.info(f"Executing prompt: {prompt[:50]}...")
            response = requests.post(
                f"{self.base_url}/agents/execute",
                headers=self._headers,
                json={"prompt": prompt},
            )
            response.raise_for_status()

            result = response.json()
            logger.success("Prompt executed successfully")
            return result

        except requests.exceptions.RequestException as e:
            logger.error(f"Error executing prompt: {str(e)}")
            raise


def main():
    """Main execution function."""
    try:
        # Create agent configuration
        llm_config = LLMConfig(provider="openai", model="gpt-4o-mini")

        prompt_config = PromptConfig(
            content="Você é um especialista em dados do Itaú, com foco em IBS360, Scorefy e Radar Imobiliário."
        )

        # Initialize agent
        agent = StackSpotAgent(
            api_key="SUA_CHAVE_STACKSPOT",
            name="Agente IBS360",
            description="Especialista em dados imobiliários e performance de agências.",
            llm_config=llm_config,
            prompt_config=prompt_config,
        )

        # Create the agent
        result = agent.create_agent()
        print(json.dumps(result, indent=2))

    except Exception as e:
        logger.error(f"Error in main execution: {str(e)}")
        raise


if __name__ == "__main__":
    main()
