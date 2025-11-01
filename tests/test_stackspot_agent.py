import pytest

from src.agents.stackspot_agent import StackSpotAgent
from src.models.llm import LLMConfig
from src.models.prompt import PromptConfig


def test_agent_creation():
    """Test agent creation with basic configuration."""
    # Arrange
    llm_config = LLMConfig(provider="openai", model="gpt-4o-mini")
    prompt_config = PromptConfig(content="Test prompt")

    # Act
    agent = StackSpotAgent(
        api_key="test_key",
        name="Test Agent",
        description="Test Description",
        llm_config=llm_config,
        prompt_config=prompt_config,
    )

    # Assert
    assert agent.name == "Test Agent"
    assert agent.description == "Test Description"
    assert agent.llm == llm_config
    assert agent.prompt == prompt_config


def test_llm_config_to_dict():
    """Test LLMConfig to_dict method."""
    # Arrange
    config = LLMConfig(provider="test_provider", model="test_model")

    # Act
    result = config.to_dict()

    # Assert
    assert result == {"provider": "test_provider", "model": "test_model"}


def test_prompt_config_to_dict():
    """Test PromptConfig to_dict method."""
    # Arrange
    config = PromptConfig(content="test content")

    # Act
    result = config.to_dict()

    # Assert
    assert result == {"content": "test content"}
