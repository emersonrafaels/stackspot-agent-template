import sys
from pathlib import Path

# Adjust import path for data functions
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.agents.stackspot_agent import StackSpotAgent
from src.config.config_dynaconf import get_settings
from src.models.llm import LLMConfig
from src.models.prompt import PromptConfig

# Retrieve settings instance
settings = get_settings()


def run_example():
    """Example of creating and using a StackSpot agent."""
    # Create configurations
    llm_config = LLMConfig(provider="openai", model="gpt-4o-mini")
    system_prompt_config = PromptConfig(content="Hello, I am a StackSpot agent!")

    # Create agent
    agent = StackSpotAgent(
        name="Example Agent",
        description="A simple example agent",
        llm_config=llm_config,
        prompt_config=system_prompt_config,
        client_id=settings.get("stackspot_client_id"),
        client_secret=settings.get("stackspot_client_secret"),
        realm=settings.get("stackspot_realm"),
    )

    # Create and execute
    agent.create()
    response = agent.execute("Tell me about yourself")
    print(response)


if __name__ == "__main__":
    run_example()
