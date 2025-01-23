from typing import Any, Dict, Optional, Union

class DataManipulation:
    """
    Data manipulation class.  Handles validating, setting, getting, editing, and removing data.

    The database (db) is treated as an instance variable of this class.
    """
    def __init__(self):
        """
        Initialization method.  No specific initialization is done.
        """
        self.db = {}  # Initialize the database
        self.observers = {}  # Initialize observers
        self.crypted = False # Initialize crypted flag
        # self._load_db()  # Load the database (commented out)
        # self._load_config() # Load config (commented out)

    def validate_data(self, data: Any) -> bool:
        """
        Validates data, ensuring it's a dictionary and that keys/values have consistent and allowed types.

        Args:
            data (Any): The data to validate.

        Returns:
            bool: True if the data is valid, False otherwise.
        """
        if isinstance(data, dict):
            types = {}
            for key, value in data.items():
                if not isinstance(key, str):
                    print(f"\033[91m#bugs\033[0m Key '{key}' must be a string. Did we stumble upon a non-string key?")
                    return False
                if key in types and types[key] != type(value):
                    print(f"\033[91m#bugs\033[0m Conflicting types for key '{key}'.")
                    return False
                types[key] = type(value)
            return all(isinstance(value, (str, int, float, list, dict, bool, None)) for value in data.values())
        print(f"\033[91m#bugs\033[0m Data must be a dictionary.")
        return False

    def _set_child(self, parent: Dict[str, Any], child_key: str, value: Any) -> None:
        """
        Helper method to set data in a nested dictionary.

        Args:
            parent (Dict[str, Any]): The parent dictionary.
            child_key (str): The key to set (path separated by "/").
            value (Any): The value to set.
        """
        keys = child_key.split('/')
        for key in keys[:-1]:
            parent = parent.setdefault(key, {})
        parent[keys[-1]] = value

    def _merge_dicts(self, dict1, dict2):
        """
        Helper method to merge dict2 into dict1.

        Args:
            dict1 (dict): The dictionary to merge into.
            dict2 (dict): The dictionary to merge from.

        Returns:
            dict: The merged dictionary (dict1).
        """
        for key, value in dict2.items():
            if isinstance(value, dict) and key in dict1 and isinstance(dict1[key], dict):
                self._merge_dicts(dict1[key], value)
            else:
                dict1[key] = value
        return dict1

    def key_exists(self, key: str) -> bool:
        """
        Checks if a key exists in the database.

        Args:
            key (str): The key to check (path separated by "/").

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
        """
        Gets data from the database by key.

        Args:
            key (str): The key to get (path separated by "/").

        Returns:
            Optional[Any]: The data if it exists, None otherwise.
        """
        keys = key.split('/')
        data = self.db
        for k in keys:
            if k in data:
                data = data[k]
            else:
                print(f"\033[91m#bugs\033[0m No data found at key '{key}'. Double-check the key or try a different path.")
                return None
        return data

    def set_data(self, key: str, value: Optional[Any] = None) -> None:
        """
        Sets data in the database.  Raises an error if the key already exists.

        Args:
            key (str): The key to set (path separated by "/").
            value (Optional[Any], optional): The value to set. Defaults to None, initializing with an empty dictionary.
        """
        if value is None:
            value = {}

        if not self.validate_data(value):
            print(f"\033[91m#bugs\033[0m Invalid data format. Ensure your data is a dictionary with consistent types.")
            return

        if self.key_exists(key):
            print(f"\033[91m#bugs\033[0m Key '{key}' already exists.  Use db.edit_data('{key}', new_value) to update or add new data.")
            return

        self._set_child(self.db, key, value)
        self.notify_observers("set_data", key, value)
        self._backup_db()  # Backup (mock implementation)
        self._save_db()  # Save (mock implementation)

    def edit_data(self, key: str, value: Any) -> None:
        """
        Edits data in the database.  Raises an error if the key doesn't exist.

        Args:
            key (str): The key to edit (path separated by "/").
            value (Any): The new value.
        """
        if not self.key_exists(key):
            print(f"\033[91m#bugs\033[0m Key '{key}' doesn't exist, cannot edit. Use 'set_data' to add new data.")
            return

        if not self.validate_data(value):
            print(f"\033[91m#bugs\033[0m Invalid data format. Ensure your data is a dictionary with consistent types.")
            return

        keys = key.split('/')
        data = self.db
        for k in keys[:-1]:
            data = data.setdefault(k, {})

        current_data = data.get(keys[-1], {})

        if isinstance(value, dict) and "increment" in value:
            for field, increment_value in value["increment"].items():
                if field in current_data:
                    if isinstance(current_data[field], (int, float)):
                        if isinstance(increment_value, (int, float)):
                            current_data[field] += increment_value
                        else:
                            print(f"\033[91m#bugs\033[0m Increment value for '{field}' is not a number. Provide a numeric value for incrementing (e.g., db.edit_data('users/1', {{'increment': {{'score': 5}}}})).")
                            return
                    else:
                        print(f"\033[91m#bugs\033[0m Field '{field}' is not a number. Ensure the field exists and is a number before incrementing.")
                        return
                else:
                    print(f"\033[91m#bugs\033[0m Field '{field}' doesn't exist. Make sure the field exists in the data structure; use db.edit_data to set initial values.")
                    return
        else:
            if isinstance(current_data, dict):
                value = self._merge_dicts(current_data, value)
            data[keys[-1]] = value

        self._backup_db()
        self._save_db()

    # ==================================================
    #                DATA OBSERVERS
    # --------------------------------------------------
    # ==================================================

    def add_observer(self, key: str, observer_func) -> None:
        """
        Adds an observer for a specific key.

        Args:
            key (str): The key to observe (path separated by "/").
            observer_func: The observer function.
        """
        if key not in self.observers:
            self.observers[key] = []
        self.observers[key].append(observer_func)

    def remove_observer(self, key: str, observer_func) -> None:
        """
        Removes an observer for a specific key.

        Args:
            key (str): The key being observed (path separated by "/").
            observer_func: The observer function to remove.
        """
        if key in self.observers:
            self.observers[key].remove(observer_func)
            if not self.observers[key]:
                del self.observers[key]

    def notify_observers(self, action: str, key: str, value: Any) -> None:
        """
        Notifies all observers about a change.

        Args:
            action (str): The type of action ("set_data", "edit_data", etc.).
            key (str): The key that was changed (path separated by "/").
            value (Any): The new value.
        """
        for observer_key, observers in self.observers.items():
            if key.startswith(observer_key):
                for observer in observers:
                    observer(action, key, value)

    def remove_data(self, key: str) -> None:
        """
        Removes data from the database by key.

        Args:
            key (str): The key to remove (path separated by "/").
        """
        keys = key.split('/')
        data = self.db
        for k in keys[:-1]:
            if k in data:
                data = data[k]
            else:
                print(f"\033[91m#bugs\033[0m Key '{key}' doesn't exist, cannot remove. Make sure the key path is correct.")
                return
        if keys[-1] in data:
            del data[keys[-1]]
            self._backup_db()
            self._save_db()
        else:
            print(f"\033[91m#bugs\033[0m Key '{key}' doesn't exist, cannot remove. Make sure the key path is correct.")

    # ==================================================
    #                WHOLE DATABASE
    # --------------------------------------------------
    # ==================================================

    def get_db(self, raw: bool = False) -> Union[Dict[str, Any], str]:
        """
        Gets the entire database, optionally in raw format.

        Args:
            raw (bool, optional):  Whether to get the raw data. Defaults to False.

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
        """
        Gets a specific subcollection, or an item within a subcollection.

        Args:
            collection_name (str): The subcollection name.
            item_id (Optional[str], optional): The item ID. Defaults to None.

        Returns:
            Optional[Any]: The subcollection, or the item. None if it doesn't exist.
        """
        collection = self.db.get(collection_name, {})
        if item_id is not None:
            if item_id in collection:
                return collection[item_id]
            else:
                print(f"\033[91m#bugs\033[0m ID '{item_id}' not found in collection '{collection_name}'. Check if the ID is correct; use get_subcollection('{collection_name}') to see all items.")
                return None
        return collection

    def set_subcollection(self, collection_name: str, item_id: str, value: Any) -> None:
        """
        Sets an item in a specific subcollection.

        Args:
            collection_name (str): The subcollection name.
            item_id (str): The item ID.
            value (Any): The value to set.
        """
        if not self.validate_data(value):
            print(f"\033[91m#bugs\033[0m Invalid data format.  Your data should look like this: {{'name': 'Aliou', 'age': 30}}.")
            return

        if collection_name not in self.db:
            self.db[collection_name] = {}

        if item_id in self.db[collection_name]:
            print(f"\033[91m#bugs\033[0m ID '{item_id}' already exists in collection '{collection_name}'. Use db.edit_subcollection('{collection_name}', '{item_id}', new_value) to update or add new data.")
            return

        self.db[collection_name][item_id] = value
        self._backup_db()
        self._save_db()

    def edit_subcollection(self, collection_name: str, item_id: str, value: Any) -> None:
        """
        Edits an item in a specific subcollection.

        Args:
            collection_name (str): The subcollection name.
            item_id (str): The item ID.
            value (Any): The new value.
        """
        if not self.validate_data(value):
            print(f"\033[91m#bugs\033[0m Invalid data format. Your data should look like this: {{'name': 'Aliou', 'age': 30}}.")
            return

        if collection_name in self.db and item_id in self.db[collection_name]:
            current_data = self.db[collection_name][item_id]
            if isinstance(current_data, dict):
                value = self._merge_dicts(current_data, value)
            self.db[collection_name][item_id] = value
            self._backup_db()
            self._save_db()
        else:
            print(f"\033[91m#bugs\033[0m ID '{item_id}' not found in collection '{collection_name}', cannot edit. Use 'set_subcollection' to create a new item.")

    def remove_subcollection(self, collection_name: str, item_id: Optional[str] = None) -> None:
        """
        Removes a subcollection or an item within it.

        Args:
            collection_name (str): The subcollection name.
            item_id (Optional[str], optional): The item ID. Defaults to None.
        """
        if item_id is None:
            if collection_name in self.db:
                del self.db[collection_name]
                self._backup_db()
                self._save_db()
            else:
                print(f"\033[91m#bugs\033[0m Collection '{collection_name}' not found, cannot remove. Make sure the collection name is correct.")
                return
        else:
            if collection_name in self.db and item_id in self.db[collection_name]:
                del self.db[collection_name][item_id]
                self._backup_db()
                self._save_db()
            else:
                print(f"\033[91m#bugs\033[0m ID '{item_id}' not found in collection '{collection_name}', cannot remove. Check the ID and collection name; use get_subcollection('{collection_name}') to see all items.")
                return