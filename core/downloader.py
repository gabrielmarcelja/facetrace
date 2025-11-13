"""
FaceTrace CLI - Image Downloader
Download images from URLs for searching
"""

import requests
from typing import Optional
from urllib.parse import urlparse


def is_url(path: str) -> bool:
    """
    Check if path is a URL

    Args:
        path: String to check

    Returns:
        True if path is URL, False if file path
    """
    try:
        result = urlparse(path)
        return all([result.scheme, result.netloc])
    except:
        return False


def download_image(url: str, timeout: int = 30) -> Optional[bytes]:
    """
    Download image from URL

    Args:
        url: Image URL
        timeout: Request timeout in seconds

    Returns:
        Image bytes or None if download fails
    """
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

        response = requests.get(
            url,
            headers=headers,
            timeout=timeout,
            allow_redirects=True
        )

        if response.status_code == 200:
            return response.content

        return None

    except requests.exceptions.Timeout:
        print(f"Error: Download timeout for {url}")
        return None
    except requests.exceptions.RequestException as e:
        print(f"Error: Failed to download image: {str(e)}")
        return None


def extract_instagram_image(url: str) -> Optional[bytes]:
    """
    Extract image from Instagram post URL

    Args:
        url: Instagram post URL

    Returns:
        Image bytes or None if extraction fails

    Note: This is a simplified version. Instagram scraping
    may require more sophisticated methods in production.
    """
    # For now, just try to download directly
    # In production, you might need to use Instagram's API
    # or scraping libraries like instaloader

    return download_image(url)


def get_image_from_url(url: str) -> Optional[bytes]:
    """
    Get image bytes from URL (with platform-specific handling)

    Args:
        url: Image or post URL

    Returns:
        Image bytes or None if failed
    """
    url_lower = url.lower()

    # Instagram-specific handling
    if 'instagram.com' in url_lower:
        return extract_instagram_image(url)

    # Twitter/X-specific handling
    elif 'twitter.com' in url_lower or 'x.com' in url_lower:
        # Twitter images usually have direct URL
        # If it's a post URL, we might need to extract the image URL
        return download_image(url)

    # Default: try direct download
    else:
        return download_image(url)


def validate_image_size(image_bytes: bytes, max_size_mb: int = 10) -> bool:
    """
    Validate image size

    Args:
        image_bytes: Image data
        max_size_mb: Maximum size in megabytes

    Returns:
        True if size is valid, False otherwise
    """
    size_mb = len(image_bytes) / (1024 * 1024)
    return size_mb <= max_size_mb
