"""Module for handling file uploads to StackSpot S3."""
from typing import Dict, List
from pathlib import Path
import json

import requests

from src.config.config_logger import logger
from src.config.config_dynaconf import get_settings
from src.config.stackspot_config import get_stackspot_config
from src.utils.url_utils import build_url

# Get configuration
settings = get_settings()
stackspot_config = get_stackspot_config()


class FileUploader:
    """Handle file uploads to StackSpot S3 storage."""

    def __init__(self, access_token: str, account_id: str = None):
        """Initialize uploader.
        
        Args:
            access_token (str): Bearer token for authentication
            account_id (str, optional): Optional account ID
        """
        self.access_token = access_token
        self.account_id = account_id
        
        # Build upload API URL from settings
        base_url = settings.get("stackspot.upload.base_url")
        api_version = settings.get("stackspot.upload.api_version")
        file_upload_resource = settings.get("stackspot.upload.file_upload_resource")
        form_endpoint = settings.get("stackspot.upload.form_endpoint")
        
        self.upload_api = build_url(
            base_url,
            api_version,
            file_upload_resource,
            form_endpoint
        )

    def _create_headers(self) -> Dict[str, str]:
        """Create request headers with authentication."""
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }
        if self.account_id:
            headers["x-account-id"] = self.account_id
        return headers

    def get_upload_form(self, file_name: str, expiration: int = 60) -> Dict:
        """Get S3 upload form data.
        
        Args:
            file_name (str): Name of file to upload
            expiration (int, optional): Form expiration in minutes. Defaults to 60.
            
        Returns:
            Dict: Upload form data including URL and S3 fields
        """
        try:
            payload = {
                "file_name": file_name,
                "target_type": "CONTEXT",
                "expiration": expiration
            }

            response = requests.post(
                self.upload_api,
                headers=self._create_headers(),
                data=json.dumps(payload)
            )
            response.raise_for_status()
            return response.json()

        except Exception as e:
            logger.error(f"Failed to get upload form: {str(e)}")
            raise

    def upload_to_s3(self, upload_data: Dict, file_path: Path) -> None:
        """Upload file to S3 using pre-signed form data.
        
        Args:
            upload_data (Dict): Form data from get_upload_form()
            file_path (Path): Path to file to upload
        """
        try:
            s3_url = upload_data["url"]
            form = upload_data["form"]

            # Prepare multipart form data
            files = {
                "file": file_path.open("rb")
            }
            
            data = {
                "key": form["key"],
                "x-amz-algorithm": form["x-amz-algorithm"],
                "x-amz-credential": form["x-amz-credential"],
                "x-amz-date": form["x-amz-date"],
                "policy": form["policy"],
                "x-amz-signature": form["x-amz-signature"],
            }
            
            # Add security token if present
            if "x-amz-security-token" in form:
                data["x-amz-security-token"] = form["x-amz-security-token"]

            # Upload to S3
            response = requests.post(s3_url, data=data, files=files)
            response.raise_for_status()

        except Exception as e:
            logger.error(f"Failed to upload to S3: {str(e)}")
            raise
        finally:
            # Ensure file is closed
            if "files" in locals():
                files["file"].close()

    def upload_files(self, file_paths: List[Path]) -> List[str]:
        """Upload multiple files and return their upload IDs.
        
        Args:
            file_paths (List[Path]): List of files to upload
            
        Returns:
            List[str]: List of upload IDs
        """
        upload_ids = []
        
        for file_path in file_paths:
            try:
                # Get upload form
                form = self.get_upload_form(file_path.name)
                
                # Upload file
                self.upload_to_s3(form, file_path)
                
                # Collect upload ID
                upload_ids.append(form["id"])
                
                logger.info(f"Successfully uploaded {file_path.name}")
                
            except Exception as e:
                logger.error(f"Failed to upload {file_path.name}: {str(e)}")
                raise

        return upload_ids