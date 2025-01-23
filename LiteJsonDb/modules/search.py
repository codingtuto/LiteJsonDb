"""
░██████╗███████╗░█████╗░██████╗░░█████╗░██╗░░██╗░░░██████╗░██╗░░░██╗
██╔════╝██╔════╝██╔══██╗██╔══██╗██╔══██╗██║░░██║░░░██╔══██╗╚██╗░██╔╝
╚█████╗░█████╗░░███████║██████╔╝██║░░╚═╝███████║░░░██████╔╝░╚████╔╝░
░╚═══██╗██╔══╝░░██╔══██║██╔══██╗██║░░██╗██╔══██║░░░██╔═══╝░░░╚██╔╝░░
██████╔╝███████╗██║░░██║██║░░██║╚█████╔╝██║░░██║██╗██║░░░░░░░░██║░░░
╚═════╝░╚══════╝╚═╝░░╚═╝╚═╝░░╚═╝░╚════╝░╚═╝░░╚═╝╚═╝╚═╝░░░░░░░░╚═╝░░░
"""
from typing import Any, Dict, Optional

def search_data(data: Dict[str, Any], search_value: Any, key: Optional[str] = None) -> Dict[str, Any]:
    """
    Search for a value in a nested dictionary or within a specific key.

    Args:
        data (Dict[str, Any]): The dictionary to search within.
        search_value (Any): The value to search for.
        key (Optional[str]): If provided, search within this specific key.

    Returns:
        Dict[str, Any]: A dictionary containing matching results.
    """
    results = {}

    def search_recursive(d: Any, value: Any, current_key: str = ''):
        """
        Recursively search through the dictionary.

        Args:
            d (Any): The dictionary to search through.
            value (Any): The value to search for.
            current_key (str): The current path of keys being traversed.
        """
        if isinstance(d, dict):
            for k, v in d.items():
                new_key = f"{current_key}/{k}" if current_key else k
                if isinstance(v, dict):
                    search_recursive(v, value, new_key)
                elif value in (v, str(v)):
                    results[new_key] = v
        elif isinstance(d, list):
            for index, item in enumerate(d):
                search_recursive(item, value, f"{current_key}/{index}")

    if key:
        if key not in data:
            print(f"\033[91m#bugs\033[0m Key '{key}' not found for search.")
        else:
            search_recursive(data[key], search_value)
    else:
        search_recursive(data, search_value)

    if not results:
         print(f"\033[90m#info\033[0m Value '{search_value}' not found.")

    return results