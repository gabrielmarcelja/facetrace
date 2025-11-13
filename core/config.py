"""
FaceTrace CLI - Configuration Management
Manages ~/.facetrace/config.json for storing API key and settings
"""

import json
import os
from pathlib import Path
from typing import Optional, Dict


CONFIG_DIR = Path.home() / ".facetrace"
CONFIG_FILE = CONFIG_DIR / "config.json"

# Default API base URL
DEFAULT_API_URL = "https://bisque-echidna-708046.hostingersite.com"


def ensure_config_dir():
    """Create config directory if it doesn't exist"""
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)


def load_config() -> Dict:
    """
    Load configuration from file

    Returns:
        Dict with config data, or empty dict if file doesn't exist
    """
    if not CONFIG_FILE.exists():
        return {}

    try:
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"Warning: Failed to load config: {e}")
        return {}


def save_config(config: Dict):
    """
    Save configuration to file

    Args:
        config: Configuration dictionary to save
    """
    ensure_config_dir()

    try:
        with open(CONFIG_FILE, 'w') as f:
            json.dump(config, f, indent=2)
    except Exception as e:
        print(f"Error: Failed to save config: {e}")


def get_api_key() -> Optional[str]:
    """
    Get API key from config

    Returns:
        API key string or None if not found
    """
    config = load_config()
    return config.get('api_key')


def set_api_key(api_key: str, email: str = None):
    """
    Save API key to config

    Args:
        api_key: API key to save
        email: Optional email to save
    """
    config = load_config()
    config['api_key'] = api_key

    if email:
        config['email'] = email

    save_config(config)


def get_api_url() -> str:
    """
    Get API base URL from config

    Returns:
        API URL string
    """
    config = load_config()
    return config.get('api_url', DEFAULT_API_URL)


def set_api_url(api_url: str):
    """
    Save custom API URL to config

    Args:
        api_url: API URL to save
    """
    config = load_config()
    config['api_url'] = api_url
    save_config(config)


def get_email() -> Optional[str]:
    """
    Get email from config

    Returns:
        Email string or None if not found
    """
    config = load_config()
    return config.get('email')


def clear_config():
    """
    Delete config file (logout)
    """
    if CONFIG_FILE.exists():
        try:
            CONFIG_FILE.unlink()
        except Exception as e:
            print(f"Error: Failed to clear config: {e}")


def is_authenticated() -> bool:
    """
    Check if user is authenticated (has API key)

    Returns:
        True if API key exists, False otherwise
    """
    api_key = get_api_key()
    return api_key is not None and len(api_key) > 0


def get_config_path() -> Path:
    """
    Get path to config file

    Returns:
        Path object for config file
    """
    return CONFIG_FILE
