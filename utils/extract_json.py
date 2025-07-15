import json
import re

from fastapi import HTTPException


def extract_json_from_ia_response(response_text: str) -> list:
    """
    Extracts JSON content from a response text that contains a code block with JSON data.

    Args:
        response_text (str): The response text containing the JSON data in a code block.

    Returns:
        list: A list of dictionaries parsed from the JSON content.

    Raises:
        HTTPException: If the response does not contain valid JSON or if no match is found.
    """
    match = re.search(r"```json\s*(\[.*?\])\s*```", response_text, re.DOTALL)
    if not match:
        raise HTTPException(status_code=400, detail="Invalid response format")

    json_content = match.group(1)
    return json.loads(json_content)
