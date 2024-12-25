"""
██╗░░░██╗████████╗██╗██╗░░░░░░██████╗░░░██████╗░██╗░░░██╗
██║░░░██║╚══██╔══╝██║██║░░░░░██╔════╝░░░██╔══██╗╚██╗░██╔╝
██║░░░██║░░░██║░░░██║██║░░░░░╚█████╗░░░░██████╔╝░╚████╔╝░
██║░░░██║░░░██║░░░██║██║░░░░░░╚═══██╗░░░██╔═══╝░░░╚██╔╝░░
╚██████╔╝░░░██║░░░██║███████╗██████╔╝██╗██║░░░░░░░░██║░░░
░╚═════╝░░░░╚═╝░░░╚═╝╚══════╝╚═════╝░╚═╝╚═╝░░░░░░░░╚═╝░░░

Just a bunch of handy-dandy functions to make rewriting and coding extra functionalities a breeze.
No need to thank me, but you can send cookies. 🍪 by submitting a PR( Pull Requests 🙃)
"""

import json
import hashlib
import datetime
import itertools
from functools import wraps
from typing import Any, Callable, Dict, Optional, List

def convert_to_datetime(date_str: str) -> datetime.datetime:
    """Turn that boring string into a fancy datetime object! Time travel not included."""
    return datetime.datetime.fromisoformat(date_str)

def get_or_default(data: Dict[str, Any], key: str, default: Any = None) -> Any:
    """Can't find what you're looking for? Here's your fallback! Retrieves a value or serves a default one if the key is missing in action."""
    return data.get(key, default)

def key_exists_or_add(data: Dict[str, Any], key: str, default: Any) -> bool:
    """Check if a key exists, and if not, sneakily add it with a default value. It's like a secret ingredient!"""
    if key in data:
        return True
    data[key] = default
    return False

def normalize_keys(data: Dict[str, Any]) -> Dict[str, Any]:
    """Normalize those wild keys (like all lowercase). Because case sensitivity is sooo last season."""
    return {key.lower(): value for key, value in data.items()}

def flatten_json(data: Dict[str, Any], parent_key: str = '', sep: str = '.') -> Dict[str, Any]:
    """Squish that nested JSON into a flat dictionary. Like a JSON pancake! 🥞"""
    items = []
    for k, v in data.items():
        new_key = parent_key + sep + k if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten_json(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)

def filter_data(data: List[Dict[str, Any]], condition: Callable[[Dict[str, Any]], bool]) -> List[Dict[str, Any]]:
    """Filter out the riffraff based on a condition. Only the finest data shall pass!"""
    return [item for item in data if condition(item)]

def sort_data(data: List[Dict[str, Any]], key: Callable[[Dict[str, Any]], Any], reverse: bool = False) -> List[Dict[str, Any]]:
    """Sort that data like a pro. Whether ascending or descending, we've got your back!"""
    return sorted(data, key=key, reverse=reverse)

def hash_password(password: str) -> str:
    """Turn your plain password into a cryptographic masterpiece using SHA-256. Hackers, beware!"""
    return hashlib.sha256(password.encode()).hexdigest()

def check_password(stored_hash: str, password: str) -> bool:
    """Verify if the password matches the stored hash. The ultimate password bouncer!"""
    return stored_hash == hash_password(password)

def sanitize_output(data: Dict[str, Any]) -> Dict[str, Any]:
    """Sanitize the output to avoid XSS vulnerabilities. Keep your app safe from those sneaky hackers! 
    You're probably thinking, 'XSS vulnerability in Python, huh?' Yeah, I discovered this on a LinkedIn post and thought, why not include it? Maybe...there are people who might use our tool as a database for their web apps🙃"""
    return {key: (str(value).replace('<', '&lt;').replace('>', '&gt;')) if isinstance(value, str) else value
            for key, value in data.items()}

def pretty_print(data: Any) -> None:
    """Make your data shine with beautifully formatted output. It's like a makeover for your JSON!"""
    print(json.dumps(data, indent=4, ensure_ascii=False))
