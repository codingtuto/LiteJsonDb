from typing import Any, Dict, Optional, Union
import re

class DataManipulation:
    def __init__(self):
        """Initializes the DataManipulation class.
        
        This class provides methods for manipulating data within a dictionary-based database, including validation, setting, editing, retrieving, and removing data, as well as managing observers for data changes.
        """
        pass

    def validate_data(self, data: Any) -> bool:
        """Validates data before insertion.

        Args:
            data (Any): The data to validate.

        Returns:
            bool: True if the data is valid, False otherwise.
        """
        if isinstance(data, dict):
            # Check for duplicate keys with different types
            types = {}
            for key, value in data.items():
                if not isinstance(key, str):
                   print(f"\033[91m#bugs\033[0m Keys in data should be strings. Non-string key '{key}' found.")
                   return False
                if key in types and types[key] != type(value):
                   print(f"\033[91m#bugs\033[0m Key '{key}' has conflicting types in data.")
                   return False
                types[key] = type(value)
            # Ensure values are of allowed types
            return all(isinstance(value, (str, int, float, list, dict, bool, None)) for value in data.values())
        print("\033[91m#bugs\033[0m Data should be a dictionary.")
        return False

    def _set_child(self, parent: Dict[str, Any], child_key: str, value: Any) -> None:
        """Helper to set data in a nested dictionary.

        Args:
            parent (Dict[str, Any]): The parent dictionary.
            child_key (str): The key to set, can be a path like 'a/b/c'.
            value (Any): The value to set.
        """
        keys = child_key.split('/')
        for key in keys[:-1]:
            parent = parent.setdefault(key, {})
        parent[keys[-1]] = value

    def _merge_dicts(self, dict1, dict2):
        """Merges dict2 into dict1.

        Args:
            dict1 (dict): The dictionary to merge into.
            dict2 (dict): The dictionary to merge from.

        Returns:
            dict: dict1 after merging dict2 into it.
        """
        for key, value in dict2.items():
            if isinstance(value, dict) and key in dict1 and isinstance(dict1[key], dict):
                self._merge_dicts(dict1[key], value)
            else:
                dict1[key] = value
        return dict1

    def key_exists(self, key: str) -> bool:
        """Checks if a key exists in the database.

        Args:
            key (str): The key to check.

        Returns:
            bool: True if the key exists, False otherwise.
        """
        keys = key.split('/')
        data = self.db
        for k in keys:
            if k in data:
                data = data[k]
            else:
                return False
        return True

    def get_data(self, key: str) -> Optional[Any]:
        """Gets data from the database by key.

        Args:
            key (str): The key to retrieve data from.

        Returns:
            Optional[Any]: The data associated with the key, or None if the key doesn't exist.
        """
        keys = key.split('/')
        data = self.db
        for k in keys:
            if k in data:
                data = data[k]
            else:
                print(f"\033[91m#bugs\033[0m The key '{key}' doesn't exist in our database.")
                return None
        return data

    def set_data(self, key: str, value: Optional[Any] = None) -> None:
        """Sets data in the database.

        Args:
            key (str): The key to set data at.
            value (Optional[Any]): The value to set. If None, initializes the key with an empty dictionary.
        """
        if value is None:
            value = {}

        if not self.validate_data(value):
            print("\033[91m#bugs\033[0m The provided data is not in a valid format.")
            return
        if self.key_exists(key):
            print(f"\033[91m#bugs\033[0m The key '{key}' already exists. Use 'edit_data' to modify existing data.")
            return
        self._set_child(self.db, key, value)
        self.notify_observers("set_data", key, value)
        self._backup_db()
        self._save_db()

    def edit_data(self, key: str, value: Any) -> None:
        """Edits data in the database.
        Args:
            key (str): The key to edit data at.
            value (Any): The value to edit the data with, can include "+X" or "-X" for increment/decrement operations.
        """
        if not self.key_exists(key):
            print(f"\033[91m#bugs\033[0m The key '{key}' doesn't exist. Use 'set_data' to create new data.")
            return

        keys = key.split('/')
        data = self.db
        for k in keys[:-1]:
            data = data.setdefault(k, {})
        target_key = keys[-1]

        # Use get_data to retrieve the *actual* value from the database
        current_data = self.get_data(key)

        if current_data is None:
            print(f"\033[91m#bugs\033[0m No data found at key '{key}'.")
            return

        if isinstance(current_data, dict) and isinstance(value, dict):
            for field, new_value in value.items():
                if field in current_data and isinstance(new_value, str):
                    match = re.match(r"([+-])(\d+(\.\d*)?)", new_value)
                    if match and isinstance(current_data[field], (int, float)):
                        sign, num, _ = match.groups()
                        num = float(num)
                        old_value = current_data[field]

                        if sign == "+":
                            data[target_key][field] = old_value + num
                        elif sign == "-":
                            data[target_key][field] = old_value - num

                        else:
                            print(f"\033[91m#bugs\033[0m Invalid sign in increment string for field '{field}'.")
                            return


                    elif field in current_data:
                        print(f"\033[91m#bugs\033[0m Field '{field}' cannot be incremented as current data is not a number or increment value is not valid.")
                        return
                else:
                    print(f"\033[91m#bugs\033[0m Field '{field}' not found in current data or new value is not a string.")
                    return

            #data[target_key] = current_data #Remove the whole data to add in his field only the modified value
            print("\033[93m#info\033[0m Using '+X' or '-X' to increment/decrement value is now the preferred method.")
            self._backup_db()
            self._save_db()

        else:
            print(f"\033[91m#bugs\033[0m Invalid value format. Use {{'field': '+X'}} to increment or a dictionary to replace the value.")
            return

    # ==================================================
    #                DATA OBSERVERS
    # --------------------------------------------------
    # ==================================================

    def add_observer(self, key: str, observer_func) -> None:
        """Adds an observer for a specific key.

        Args:
            key (str): The key to observe.
            observer_func (function): The function to call when the key's data changes.
        """
        if key not in self.observers:
            self.observers[key] = []
        self.observers[key].append(observer_func)

    def remove_observer(self, key: str, observer_func) -> None:
        """Removes an observer for a specific key.

        Args:
            key (str): The key being observed.
            observer_func (function): The function to remove from the list of observers.
        """
        if key in self.observers:
            self.observers[key].remove(observer_func)
            if not self.observers[key]:
                del self.observers[key]

    def notify_observers(self, action: str, key: str, value: Any) -> None:
        """Notifies all observers about a change.

        Args:
            action (str): The action that occurred (e.g., 'set_data').
            key (str): The key that was changed.
            value (Any): The new value of the key.
        """
        for observer_key, observers in self.observers.items():
            if key.startswith(observer_key):
                for observer in observers:
                    observer(action, key, value)

    def remove_data(self, key: str) -> None:
        """Removes data from the database by key.

        Args:
            key (str): The key to remove.
        """
        if not self.key_exists(key):
            print(f"\033[91m#bugs\033[0m The key '{key}' doesn't exist.")
            return
        keys = key.split('/')
        data = self.db
        for k in keys[:-1]:
            if k in data:
                data = data[k]
            else:
                print(f"\033[91m#bugs\033[0m The key '{key}' doesn't exist.")
                return
        if keys[-1] in data:
            del data[keys[-1]]
            self._backup_db()
            self._save_db()
        else:
            print(f"\033[91m#bugs\033[0m The key '{key}' doesn't exist.")

    # ==================================================
    #                WHOLE DATABASE
    # --------------------------------------------------
    # ==================================================

    def get_db(self, raw: bool = False) -> Union[Dict[str, Any], str]:
        """Gets the entire database, optionally in raw format.

        Args:
            raw (bool): If True, returns the database as is. Otherwise, returns a decrypted version if encryption is enabled.

        Returns:
            Union[Dict[str, Any], str]: The entire database.
        """
        if raw:
            return self.db
        if self.crypted:
            return self._decrypt(self._encrypt(self.db))
        return self.db

    # ==================================================
    #            SUBCOLLECTION VALIDATION
    # --------------------------------------------------
    # ==================================================

    def get_subcollection(self, collection_name: str, item_id: Optional[str] = None) -> Optional[Any]:
        """Gets a specific subcollection or an item within a subcollection.

        Args:
            collection_name (str): The name of the subcollection.
            item_id (Optional[str]): The ID of the item to retrieve within the subcollection. If None, returns the entire subcollection.

        Returns:
            Optional[Any]: The subcollection or item, or None if not found.
        """
        collection = self.db.get(collection_name, {})
        if item_id is not None:
            if item_id in collection:
                return collection[item_id]
            else:
                print(f"\033[91m#bugs\033[0m The ID '{item_id}' doesn't exist in the collection '{collection_name}'.")
                return None
        return collection

    def set_subcollection(self, collection_name: str, item_id: str, value: Any) -> None:
        """Sets an item in a specific subcollection.

        Args:
            collection_name (str): The name of the subcollection.
            item_id (str): The ID of the item to set.
            value (Any): The value to set for the item.
        """
        if not self.validate_data(value):
            print("\033[91m#bugs\033[0m The provided data is not in a valid format.")
            return
        if collection_name not in self.db:
            self.db[collection_name] = {}
        if item_id in self.db[collection_name]:
            print(f"\033[91m#bugs\033[0m The ID '{item_id}' already exists in the collection '{collection_name}'. Use 'edit_subcollection' to modify existing data.")
            return
        self.db[collection_name][item_id] = value
        self._backup_db()
        self._save_db()

    def edit_subcollection(self, collection_name: str, item_id: str, value: Any) -> None:
        """Edits an item in a specific subcollection.

        Args:
            collection_name (str): The name of the subcollection.
            item_id (str): The ID of the item to edit.
            value (Any): The new value for the item.
        """
        if not self.validate_data(value):
            print("\033[91m#bugs\033[0m The provided data is not in a valid format.")
            return
        if collection_name not in self.db or item_id not in self.db[collection_name]:
            print(f"\033[91m#bugs\033[0m The ID '{item_id}' doesn't exist in the collection '{collection_name}'. Use 'set_subcollection' to create new data.")
            return
        current_data = self.db[collection_name][item_id]
        if isinstance(current_data, dict):
            value = self._merge_dicts(current_data, value)
        self.db[collection_name][item_id] = value
        self._backup_db()
        self._save_db()