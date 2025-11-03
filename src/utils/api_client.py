from typing import Any, Dict

import requests

from src.config.config_logger import logger
from src.utils.url_utils import build_url


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
        if not self.realm:
            raise ValueError("Account realm is required for authentication")

    def _create_auth_header(self, access_token: str) -> Dict[str, str]:
        """Create authorization header with access token."""
        return {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
        }

    def get_oauth_token(self, url, client_id: str, client_secret: str) -> str:
        """Get OAuth token from StackSpot."""
        try:
            # Use form data as specified in documentation
            payload = {
                "client_id": client_id,
                "grant_type": "client_credentials",
                "client_secret": client_secret,
            }

            headers = {"Content-Type": "application/x-www-form-urlencoded"}

            logger.debug(f"Getting OAuth token from: {url}")
            response = requests.post(url, headers=headers, data=payload)
            response.raise_for_status()

            token_data = response.json()
            access_token = token_data.get("access_token")

            if not access_token:
                raise ValueError("No access token in response")

            return access_token

        except Exception as e:
            logger.error(f"Authentication failed: {str(e)}")
            raise

    def get(self, endpoint: str, access_token: str) -> Dict[str, Any]:
        """Make GET request to StackSpot API."""
        try:
            url = build_url(self.base_url, endpoint)
            headers = self._create_auth_header(access_token)

            logger.debug(f"Making GET request to: {url}")
            response = requests.get(url, headers=headers)
            response.raise_for_status()

            return response.json()

        except Exception as e:
            logger.error(f"API request failed: {str(e)}")
            raise

    def post(self, endpoint: str, data: dict, access_token: str, files: dict = None) -> Dict[str, Any]:
        """Make POST request to StackSpot API.
        
        Args:
            endpoint (str): API endpoint
            data (dict): Request data
            access_token (str): OAuth access token
            files (dict, optional): Files to upload. Format: {'file': (filename, file_object, mimetype)}
            
        Returns:
            Dict[str, Any]: API response
        """
        try:
            url = build_url(self.base_url, endpoint)
            headers = self._create_auth_header(access_token)

            if files:
                # Remove Content-Type for multipart upload
                headers.pop('Content-Type', None)
                # Convert data to form fields
                form_data = {k: str(v) for k, v in data.items()}
                response = requests.post(url, headers=headers, data=form_data, files=files)
            else:
                response = requests.post(url, headers=headers, json=data)

            logger.debug(f"Making POST request to: {url}")
            response.raise_for_status()

            return response.json()

        except Exception as e:
            logger.error(f"API request failed: {str(e)}")
            raise

    def put(self, endpoint: str, data: dict, access_token: str) -> Dict[str, Any]:
        """Make PUT request to StackSpot API."""
        try:
            url = build_url(self.base_url, endpoint)
            headers = self._create_auth_header(access_token)

            logger.debug(f"Making PUT request to: {url}")
            response = requests.put(url, headers=headers, json=data)
            response.raise_for_status()

            return response.json()

        except Exception as e:
            logger.error(f"API request failed: {str(e)}")
            raise

    def delete(self, endpoint: str, access_token: str) -> Dict[str, Any]:
        """Make DELETE request to StackSpot API."""
        try:
            url = build_url(self.base_url, endpoint)
            headers = self._create_auth_header(access_token)

            logger.debug(f"Making DELETE request to: {url}")
            response = requests.delete(url, headers=headers)
            response.raise_for_status()

            return response.json()

        except Exception as e:
            logger.error(f"API request failed: {str(e)}")
            raise
