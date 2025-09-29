import requests
import json
import time
import re
import logging
from typing import List, Dict, Any, Optional

# --- Configuration (remains the same) ---
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# --- Constants (remains the same) ---
API_URL = 'http://localhost:5200/poso'
MODEL_LITE = "gemini-2.5-flash-lite-preview-09-2025"
MODEL_FLASH = "gemini-2.5-flash-preview-09-2025"

# --- Helper Functions (remains the same) ---
def format_list_as_indexed_string(items: List[str]) -> str:
    return "\n".join(f"{i}. {info}" for i, info in enumerate(items))

def extract_json_from_text(text: str):
    match = re.search(r"```json\s*([\s\S]*?)\s*```", text, re.DOTALL)
    if match:
        json_str = match.group(1)
        try:
            return json.loads(json_str)
        except json.JSONDecodeError as e:
            logging.error(f"JSON in markdown block failed to parse: {e}")
    decoder = json.JSONDecoder()
    idx = 0
    while idx < len(text):
        obj_start = -1
        brace_start = text.find('{', idx)
        bracket_start = text.find('[', idx)
        if brace_start != -1 and bracket_start != -1:
            obj_start = min(brace_start, bracket_start)
        elif brace_start != -1:
            obj_start = brace_start
        elif bracket_start != -1:
            obj_start = bracket_start
        else:
            break
        try:
            result, _ = decoder.raw_decode(text, obj_start)
            return result
        except json.JSONDecodeError:
            idx = obj_start + 1
    logging.warning("Could not find any valid JSON object in the response text.")
    return None

# --- Core API Interaction (MODIFIED) ---

def query_api_with_retries(
    prompt: str,
    model: str,
    image: Optional[bytes] = None, # Make sure 'image' is in bytes
    max_retries: int = 1,
    initial_backoff: float = 1.0,
    timeout: int = 90,
    outjson: bool = True
) -> Optional[Dict[str, Any]]:
    """
    Posts a prompt and an optional image to the API. It sends JSON if no
    image is provided, and multipart/form-data if an image is included.
    Handles retries with exponential backoff.

    Args:
        prompt: The prompt to send to the model.
        model: The model name to use.
        image: The raw bytes of the image file to send.
        max_retries: Maximum number of times to retry the request.
        initial_backoff: Initial wait time in seconds before the first retry.
        timeout: How many seconds to wait for the server to send data.
        outjson: Whether to parse the response as JSON.

    Returns:
        The parsed response as a dictionary or text, or None if all retries fail.
    """
    backoff = initial_backoff

    for attempt in range(max_retries):
        logging.info(f"Attempt {attempt + 1}/{max_retries} to query API for model {model}...")
        try:
            # Prepare the text-based payload
            payload = {"prompt": prompt, "model": model}

            if image:
                # --- If an image exists, send as multipart/form-data ---
                logging.info("Image detected, sending as multipart/form-data.")
                # The key 'image' here must match the key your Flask app expects in request.files
                files = {'image': ('image.jpg', image, 'image/jpeg')}

                # When using 'files', 'requests' automatically sets the correct
                # 'Content-Type' header. Do NOT set it manually.
                response = requests.post(
                    API_URL,
                    data=payload,   # Text fields go here
                    files=files,    # File data goes here
                    timeout=timeout
                )
            else:
                # --- If no image, send as JSON (original behavior) ---
                logging.info("No image, sending as application/json.")
                headers = {'Content-Type': 'application/json'}
                response = requests.post(
                    API_URL,
                    headers=headers,
                    json=payload,
                    timeout=timeout
                )

            response.raise_for_status()  # This will raise an HTTPError for bad responses (4xx or 5xx)

            if outjson:
                parsed_data = extract_json_from_text(response.text)
            else:
                parsed_data = response.text

            if parsed_data:
                logging.info("Successfully received and parsed API response.")
                return parsed_data
            else:
                raise ValueError("Response did not contain valid, extractable data.")

        except requests.exceptions.RequestException as e:
            logging.error(f"A network-related error occurred: {e}")
        except ValueError as e:
            logging.error(f"A data-related error occurred: {e}")

        if attempt < max_retries - 1:
            logging.info(f"Retrying in {backoff:.2f} seconds...")
            time.sleep(backoff)
            backoff *= 2
        else:
            logging.critical("All API query retries failed. Giving up.")

    return None