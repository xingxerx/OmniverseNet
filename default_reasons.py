# Example of loading from JSON (conceptual)
import json
from typing import List, Dict, Optional

DEFAULT_REASONS_FILE = 'reasons_data.json' # Example filename

def load_reasons_from_file(filepath: str) -> Dict[str, List[str]]:
    """Loads reasons data from a JSON file."""
    try:
        with open(filepath, 'r') as f:
            data = json.load(f)
            # Basic validation (ensure it's a dict with list values)
            if isinstance(data, dict) and all(isinstance(v, list) for v in data.values()):
                return data
            else:
                print(f"Warning: Invalid format in {filepath}")
                return {}
    except FileNotFoundError:
        print(f"Warning: Reasons file not found at {filepath}")
        return {}
    except json.JSONDecodeError:
        print(f"Warning: Could not decode JSON from {filepath}")
        return {}

# You would initialize this once, perhaps outside the function or in a class
REASONS_DATA = load_reasons_from_file(DEFAULT_REASONS_FILE)

def suggest_reasons_from_file(
    situation_keyword: str,
    default_reasons: Optional[List[str]] = None
) -> List[str]:
    """Suggests possible reasons loaded from an external source."""
    default_to_use = default_reasons if default_reasons is not None else ["Unknown situation"]
    return REASONS_DATA.get(situation_keyword.lower(), default_to_use)

# Example usage:
# print(suggest_reasons_from_file("delay"))
