import requests
import json
import time
import re
import logging
from typing import List, Dict, Any, Optional

# --- Configuration ---

# Configure basic logging to print informational messages and errors.
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# --- Constants ---
# It's good practice to define constants at the top of the script.
API_URL = 'http://localhost:5200/poso'
MODEL_LITE = "gemini-2.5-flash-lite-preview-09-2025"
MODEL_FLASH = "gemini-2.5-flash-preview-09-2025"

# --- Helper Functions ---

def format_list_as_indexed_string(items: List[str]) -> str:
    """
    Efficiently formats a list of strings into a single, newline-separated
    string with each line numbered.

    Args:
        items: A list of strings to format.

    Returns:
        A single formatted string.
    """
    return "\n".join(f"{i}. {info}" for i, info in enumerate(items))

def extract_json_from_text(text: str):
    """
    Reliably extracts a JSON object from a string that might contain markdown
    code blocks or other surrounding text. It handles cases where JSON is
    embedded within other text.

    Args:
        text: The raw string response from the API.

    Returns:
        A dictionary representing the parsed JSON, or None if parsing fails.
    """
    # 1. First, try to find a JSON object within a markdown code block
    match = re.search(r"```json\s*([\s\S]*?)\s*```", text, re.DOTALL)
    if match:
        json_str = match.group(1)
        try:
            return json.loads(json_str)
        except json.JSONDecodeError as e:
            logging.error(f"JSON in markdown block failed to parse: {e}")
            # Don't return yet; the fallback might still find a valid JSON object.

    # 2. If no markdown block is found, or if it failed to parse, search for the
    #    first valid JSON object in the entire string.
    decoder = json.JSONDecoder()
    idx = 0
    while idx < len(text):
        # Find the start of a potential JSON object ('{' or '[')
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
            # No more JSON starting characters left in the string.
            break

        try:
            # Try to decode from this starting position
            result, _ = decoder.raw_decode(text, obj_start)
            # logging.info("Successfully")
            # logging.info(text)
            # logging.info(result)
            return result
        except json.JSONDecodeError:
            # This was not the start of a valid JSON object; move the search
            # position forward and try again.
            idx = obj_start + 1

    logging.warning("Could not find any valid JSON object in the response text.")
    return None

# --- Core API Interaction ---

def query_api_with_retries(
    prompt: str,
    model: str,
    max_retries: int = 5,
    initial_backoff: float = 1.0,
    timeout: int = 90,
    image= None,
    outjson= True
) -> Optional[Dict[str, Any]]:
    """
    Posts a prompt to the API and handles retries with exponential backoff.

    Args:
        prompt: The prompt to send to the model.
        model: The model name to use (e.g., MODEL_PRO or MODEL_FLASH).
        max_retries: Maximum number of times to retry the request.
        initial_backoff: Initial wait time in seconds before the first retry.
        timeout: How many seconds to wait for the server to send data.

    Returns:
        The parsed JSON response as a dictionary, or None if all retries fail.
    """
    headers = {'Content-Type': 'application/json'}
    if image:
        payload = {"prompt": prompt, "model": model, "image": image}
    else:
        payload = {"prompt": prompt, "model": model}
    backoff = initial_backoff

    for attempt in range(max_retries):
        logging.info(f"Attempt {attempt + 1}/{max_retries} to query API for model {model}...")
        try:
            response = requests.post(
                API_URL,
                headers=headers,
                json=payload,
                timeout=timeout
            )
            response.raise_for_status()
            if outjson:
                parsed_data = extract_json_from_text(response.text)
            else:
                parsed_data = response.text

            if parsed_data:
                logging.info("Successfully received and parsed JSON response.")
                return parsed_data
            else:
                raise ValueError("Response did not contain valid, extractable JSON.")

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

