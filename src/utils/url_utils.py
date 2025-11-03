"""URL utilities for handling API endpoints."""

import urllib.parse as urlparse
from typing import List, Optional, Tuple


def parse_url(url: str) -> Tuple[str, str, str, str, str, str]:
    """Parse URL into its components.
    
    Args:
        url (str): URL to parse
        
    Returns:
        Tuple[str, str, str, str, str, str]: URL components
            (scheme, netloc, path, params, query, fragment)
    """
    return urlparse.urlparse(url)


def clean_url_parts(*parts: str) -> List[str]:
    """Clean URL path parts by removing empty strings and leading/trailing slashes.
    
    Args:
        *parts: URL path parts to clean
        
    Returns:
        List[str]: List of cleaned URL parts
    """
    return [str(part).strip("/") for part in parts if part]


def build_url(base_url: str, *parts: str, query: Optional[dict] = None) -> str:
    """Build complete URL from base and path parts.
    
    Args:
        base_url (str): Base URL including scheme and domain
        *parts: Path parts to append
        query (dict, optional): Query parameters to add
        
    Returns:
        str: Complete URL with path and query
    """
    # Parse base URL
    parsed = parse_url(base_url)
    
    # Clean and join path parts
    clean_parts = clean_url_parts(*parts)
    
    # Add base path if it exists
    if parsed.path:
        base_path = parsed.path.strip("/")
        if base_path:
            clean_parts.insert(0, base_path)
            
    # Join parts with slashes
    path = "/".join(clean_parts)
    
    # Add query parameters if provided
    query_string = ""
    if query:
        query_string = urlparse.urlencode(query)
        
    # Rebuild URL
    return urlparse.urlunparse((
        parsed.scheme,
        parsed.netloc,
        f"/{path}",
        parsed.params,
        query_string,
        parsed.fragment
    ))


def join_url_parts(*parts: str) -> str:
    """Join URL parts with proper handling of slashes.
    
    Args:
        *parts: URL parts to join
        
    Returns:
        str: Joined URL parts
    """
    clean_parts = clean_url_parts(*parts)
    return "/".join(clean_parts)