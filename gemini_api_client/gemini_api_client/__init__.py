"""
Gemini API Client
=================

A simple and reliable client for interacting with a local Gemini API endpoint.
"""

__version__ = "0.1.0"

# Import the core functions and constants to make them easily accessible
# from the top-level package.
# e.g., `import gemini_api_client`
# `gemini_api_client.query_api_with_retries(...)`
from .client import (
    query_api_with_retries,
    format_list_as_indexed_string,
    extract_json_from_text,
    MODEL_LITE,
    MODEL_FLASH,
    API_URL
)
