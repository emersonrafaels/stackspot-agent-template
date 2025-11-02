"""Configuration management for StackSpot settings."""

import sys
from functools import lru_cache
from pathlib import Path
from typing import Optional

# Adjust import path for data functions 
sys.path.insert(0, str(Path(__file__).parents[2]))

from src.config.config_dynaconf import settings


@lru_cache()
def get_stackspot_config() -> dict:
    """Get StackSpot configuration from settings.

    Returns:
        dict: Dictionary with StackSpot configuration
    """

    return {
        "realm": settings.stackspot.realm,
        "client_id": settings.stackspot.client_id,
        "client_secret": settings.stackspot.client_secret,
        "auth_url": settings.stackspot.auth.base_url,
        "base_url": f"{settings.stackspot.inference.base_url}/{settings.stackspot.inference.api_version}",
    }
