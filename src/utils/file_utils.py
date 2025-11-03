"""File utilities for handling uploads and file operations."""
from pathlib import Path
from typing import List, Union
import mimetypes


def get_file_mimetype(file_path: Union[str, Path]) -> str:
    """Get the MIME type of a file.
    
    Args:
        file_path: Path to the file
        
    Returns:
        str: MIME type of the file
    """
    mime_type, _ = mimetypes.guess_type(str(file_path))
    return mime_type or 'application/octet-stream'


def prepare_file_upload(file_path: Union[str, Path]) -> dict:
    """Prepare a file for upload.
    
    Args:
        file_path: Path to the file
        
    Returns:
        dict: File information for upload
    """
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")
        
    return {
        'file': (
            path.name,
            path.open('rb'),
            get_file_mimetype(path)
        )
    }