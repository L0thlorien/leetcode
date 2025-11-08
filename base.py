"""
Base utilities for LeetCode solutions.
Common functions for testing and running solutions.
"""

import json
from typing import Any, Dict


def parse_json_input(raw: str) -> Dict[str, Any]:
    """Parse JSON string into input arguments.

    Args:
        raw: JSON string with input data

    Returns:
        Dictionary of arguments for solution methods

    Raises:
        ValueError: If invalid JSON
    """
    try:
        data = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Invalid JSON input: {exc}") from exc
    if not isinstance(data, dict):
        raise ValueError("Top-level JSON must be an object with named fields.")
    return data


def pretty_dump(obj: Any) -> str:
    """Pretty print JSON output."""
    return json.dumps(obj, ensure_ascii=False, indent=2)
