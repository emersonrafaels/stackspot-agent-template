from typing import Any, Dict

import requests

from src.config.config_logger import logger


class StackSpotAPIClient:
    """Handle all API communications with StackSpot."""

    def __init__(self, base_url: str = None, auth_url: str = None, realm: str = None):
        """Initialize API client.
        
        Args:
            base_url (str, optional): Base URL for agent API. Defaults to genai-inference-app URL.
            auth_url (str, optional): Auth URL for token. Defaults to idm URL.
            realm (str, optional): Account realm for authentication. Required for auth.
        """
        self.base_url = base_url or "https://genai-inference-app.stackspot.com/v1"
        self.auth_url = auth_url or "https://idm.stackspot.com"
        self.realm = realm
        self._headers = {
            "Content-Type": "application/json",
        }

    def _create_auth_header(self, access_token: str) -> Dict[str, str]:
        """Create authorization header with access token."""
        return {"Authorization": f"Bearer {access_token}"}

    def get_oauth_token(self, client_id: str, client_secret: str) -> str:
        """Get OAuth token from StackSpot API."""
        try:
            if not self.realm:
                raise ValueError("Account realm is required for authentication")

            url = f"{self.auth_url}/{self.realm}/oidc/oauth/token"
            logger.debug(f"Getting OAuth token from: {url}")

            # Use form data instead of JSON for token request
            payload = {
                "grant_type": "client_credentials",
                "client_id": client_id,
                "client_secret": client_secret
            }
            headers = {
                "Content-Type": "application/x-www-form-urlencoded"
            }

            response = requests.post(url, headers=headers, data=payload)
            response.raise_for_status()
            return response.json()["access_token"]

        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to get OAuth token: {str(e)}")
            raise

    def get(self, endpoint: str, access_token: str) -> Dict[str, Any]:
        """Make GET request to StackSpot API."""
        try:
            url = f"{self.base_url}/{endpoint}"
            logger.debug(f"Making GET request to: {url}")

            headers = {**self._headers, **self._create_auth_header(access_token)}
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            return response.json()

        except requests.exceptions.RequestException as e:
            logger.error(f"API request failed: {str(e)}")
            raise

    def post(self, endpoint: str, data: dict, access_token: str) -> Dict[str, Any]:
        """Make POST request to StackSpot API."""
        try:
            url = f"{self.base_url}/{endpoint}"
            logger.debug(f"Making POST request to: {url}")

            headers = {**self._headers, **self._create_auth_header(access_token)}
            response = requests.post(url, headers=headers, json=data)
            response.raise_for_status()
            return response.json()

        except requests.exceptions.RequestException as e:
            logger.error(f"API request failed: {str(e)}")
            raise

    def put(self, endpoint: str, data: dict, access_token: str) -> Dict[str, Any]:
        """Make PUT request to StackSpot API."""
        try:
            url = f"{self.base_url}/{endpoint}"
            logger.debug(f"Making PUT request to: {url}")

            headers = {**self._headers, **self._create_auth_header(access_token)}
            response = requests.put(url, headers=headers, json=data)
            response.raise_for_status()
            return response.json()

        except requests.exceptions.RequestException as e:
            logger.error(f"API request failed: {str(e)}")
            raise

    def delete(self, endpoint: str, access_token: str) -> Dict[str, Any]:
        """Make DELETE request to StackSpot API."""
        try:
            url = f"{self.base_url}/{endpoint}"
            logger.debug(f"Making DELETE request to: {url}")

            headers = {**self._headers, **self._create_auth_header(access_token)}
            response = requests.delete(url, headers=headers)
            response.raise_for_status()
            return response.json()

        except requests.exceptions.RequestException as e:
            logger.error(f"API request failed: {str(e)}")
            raise
