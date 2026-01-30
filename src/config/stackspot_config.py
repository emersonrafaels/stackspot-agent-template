"""Configuration management for StackSpot settings."""

from functools import lru_cache

from .config_dynaconf import get_settings
from ..utils.url_utils import build_url


@lru_cache()
def get_stackspot_config(
    agent_id: str = None, realm: str = None, client_id: str = None, client_secret: str = None
) -> dict:
    """Get StackSpot configuration from settings.

    # Args:
        agent_id (str, optional): Specific agent ID. Defaults to None.
        client_id (str, optional): Specific client ID. Defaults to None.
        client_secret (str, optional): Specific client secret. Defaults to None.
        realm (str, optional): Specific realm. Defaults to None.

    Returns:
        dict: Dictionary with StackSpot configuration
    """
    # Retrieve settings instance
    settings = get_settings()

    # Build auth URL with full path
    auth_url = build_url(
        settings.get("stackspot.auth.base_url", "https://idm.stackspot.com"),
        settings.get("stackspot.realm"),
        settings.get("stackspot.auth.oidc_resource", "oidc"),
        settings.get("stackspot.auth.oauth_resource", "oauth"),
        settings.get("stackspot.auth.token_resource", "token"),
    )

    # Build inference URL
    inference_url = build_url(
        settings.get("stackspot.inference.base_url", "https://genai-inference-app.stackspot.com"),
        settings.get("stackspot.inference.api_version", "v1"),
        settings.get("stackspot.inference.agent_resource", "agent"),
        agent_id,
    )

    # Build upload url
    upload_api = build_url(
        settings.get("stackspot.upload.base_url", "https://genai-inference-app.stackspot.com"),
        settings.get("stackspot.upload.api_version", "v2"),
        settings.get("stackspot.upload.file_upload_resource", "file-upload"),
        settings.get("stackspot.upload.form_endpoint", ""),
    )

    # Get credentials with validation
    realm = realm if realm else settings.get("stackspot.realm")

    return {
        "agent_id": agent_id,
        "realm": realm,
        "client_id": client_id,
        "client_secret": client_secret,
        "auth_url": auth_url,  # Ex: https://idm.stackspot.com/your_realm/oidc/oauth/token
        "inference_url": inference_url,  # Ex: https://genai-inference-app.stackspot.com/v1/agent/id/chat
        "upload_url": upload_api,  # Ex: https://genai-inference-app.stackspot.com/v2/file-upload/form
    }
