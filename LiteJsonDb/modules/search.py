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

    :param data: The dictionary to search within.
    :param search_value: The value to search for.
    :param key: Optional. If provided, search within this specific key.
    :return: A dictionary containing matching results.
    """
    results = {}

    def search_recursive(d: Any, value: Any, current_key: str = ''):
        """
        Recursively search through the dictionary.

        :param d: The dictionary to search through.
        :param value: The value to search for.
        :param current_key: The current path of keys being traversed.
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
            print(f"🐛 \033[91mWhoops! Key '{key}' went on a vacation and we can't find it for search!\033[0m")
        else:
            search_recursive(data[key], search_value)
    else:
        search_recursive(data, search_value)

    if not results:
         print(f"🔍 \033[93mLooks like '{search_value}' is playing hide-and-seek and we couldn't find it!\033[0m")
    return results