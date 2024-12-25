from typing import Any, Dict, Optional, Union
class DataManipulation:
    def __init__(self):
        pass

    def validate_data(self, data: Any) -> bool:
        """Validate data before insertion."""
        if isinstance(data, dict):
            # Check for duplicate keys with different types
            types = {}
            for key, value in data.items():
                if not isinstance(key, str):
                   print(f"🐛 \033[91mWhoops! Keys in data should be strings. Did we stumble upon a non-string key '{key}'?\033[0m")
                   return False
                if key in types and types[key] != type(value):
                   print(f"🐛 \033[91mWhoops! Key '{key}' has conflicting types in data. It's like mixing oil and water!\033[0m")
                   return False
                types[key] = type(value)
            # Ensure values are of allowed types
            return all(isinstance(value, (str, int, float, list, dict, bool, None)) for value in data.values())
        print("🐛 \033[91mWhoops! Data should be a dictionary. Did it morph into something else?\033[0m")
        return False

    def _set_child(self, parent: Dict[str, Any], child_key: str, value: Any) -> None:
        """Helper to set data in a nested dictionary."""
        keys = child_key.split('/')
        for key in keys[:-1]:
            parent = parent.setdefault(key, {})
        parent[keys[-1]] = value

    def _merge_dicts(self, dict1, dict2):
        """Merge dict2 into dict1."""
        for key, value in dict2.items():
            if isinstance(value, dict) and key in dict1 and isinstance(dict1[key], dict):
                self._merge_dicts(dict1[key], value)
            else:
                dict1[key] = value
        return dict1

    def key_exists(self, key: str) -> bool:
        """Check if a key exists in the database."""
        keys = key.split('/')
        data = self.db
        for k in keys:
            if k in data:
                data = data[k]
            else:
                return False
        return True

    def get_data(self, key: str) -> Optional[Any]:
        """Get data from the database by key."""
        keys = key.split('/')
        data = self.db
        for k in keys:
            if k in data:
                data = data[k]
            else:
                print(f"🐛 \033[91mWhoops! The key '{key}' doesn't exist in our database. Did it take a wrong turn?\033[0m")
                print(f"\033[93m💡 Tip: Double-check the key or try a different path.\033[0m")
                return None
        return data

    def set_data(self, key: str, value: Optional[Any] = None) -> None:
        """Set data in the database and notify observers.
    
        If `value` is not provided, initialize the key with an empty dictionary.
        """
        if value is None:
            value = {}

        if not self.validate_data(value):
            print("🐛 \033[91mWhoops! The provided data is not in a valid format. Did it get tangled in the wrong format?\033[0m")
            print(f"\033[93m💡 Tip: Make sure your data is a dictionary with consistent types.\033[0m")
            return
        if self.key_exists(key):
            print(f"🐛 \033[91mWhoops! The key '{key}' already exists. It's like trying to park two cars in the same spot!\033[0m")
            print(f"\033[93m💡 Tip: If you want to update or add new key, use db.edit_data('{key}', new_value).\033[0m")
            return
        self._set_child(self.db, key, value)
        self.notify_observers("set_data", key, value)
        self._backup_db()
        self._save_db()

    def edit_data(self, key: str, value: Any) -> None:
        """Edit data in the database and notify observers."""
        if not self.key_exists(key):
            print(f"🐛 \033[91mWhoops! The key '{key}' doesn't exist. We can't edit a ghost!\033[0m")
            print(f"\033[93m💡 Tip: Use 'set_data' to add new data if needed.\033[0m")
            return
        if not self.validate_data(value):
            print("🐛 \033[91mWhoops! The provided data is not in a valid format. Did it get caught in a format warp?\033[0m")
            print(f"\033[93m💡 Tip: Make sure your data is a dictionary with consistent types.\033[0m")
            return

        keys = key.split('/')
        data = self.db
        for k in keys[:-1]:
            data = data.setdefault(k, {})
    
        current_data = data.get(keys[-1], {})
    
        """
        Adding the increment because we're all about making coding a little bit easier. 
        (Plus, who doesn't love a good shortcut?)
        """
        if isinstance(value, dict) and "increment" in value:
            for field, increment_value in value["increment"].items():
                if field in current_data:
                    if isinstance(current_data[field], (int, float)):
                        if isinstance(increment_value, (int, float)):
                            current_data[field] += increment_value
                        else:
                            print(f"🐛 \033[91mWhoops! The increment value for '{field}' is not a number. Did we try to add letters to numbers?\033[0m")
                            print(f"\033[93m💡 Tip: Make sure to provide a numeric value for incrementing. Example: db.edit_data('users/1', {{'increment': {{'score': 5}}}})\033[0m")
                            return
                    else:
                        print(f"🐛 \033[91mWhoops! The field '{field}' is not a number. We can't add like that!\033[0m")
                        print(f"\033[93m💡 Tip: Ensure that the field '{field}' exists and is a number before incrementing.\033[0m")
                        return
                else:
                    print(f"🐛 \033[91mWhoops! The field '{field}' doesn't exist. It's like trying to find a key that isn't there!\033[0m")
                    print(f"\033[93m💡 Tip: Make sure the field exists in the data structure. You can use db.edit_data to set initial values.\033[0m")
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
        """Add an observer for a specific key."""
        if key not in self.observers:
            self.observers[key] = []
        self.observers[key].append(observer_func)

    def remove_observer(self, key: str, observer_func) -> None:
        """Remove an observer for a specific key."""
        if key in self.observers:
            self.observers[key].remove(observer_func)
            if not self.observers[key]:
                del self.observers[key]

    def notify_observers(self, action: str, key: str, value: Any) -> None:
        """Notify all observers about a change."""
        for observer_key, observers in self.observers.items():
            if key.startswith(observer_key):
                for observer in observers:
                    observer(action, key, value)

    def remove_data(self, key: str) -> None:
        """Remove data from the database by key."""
        keys = key.split('/')
        data = self.db
        for k in keys[:-1]:
            if k in data:
                data = data[k]
            else:
                print(f"🐛 \033[91mWhoops! The key '{key}' doesn't exist. It's like trying to delete a ghost!\033[0m")
                print(f"\033[93m💡 Tip: Make sure the key path is correct and exists.\033[0m")
                return
        if keys[-1] in data:
            del data[keys[-1]]
            self._backup_db()
            self._save_db()
        else:
            print(f"🐛 \033[91mWhoops! The key '{key}' doesn't exist. It's like trying to delete something that's already gone!\033[0m")
            print(f"\033[93m💡 Tip: Make sure the key path is correct and exists.\033[0m")

    # ==================================================
    #                WHOLE DATABASE
    # --------------------------------------------------
    # ==================================================

    def get_db(self, raw: bool = False) -> Union[Dict[str, Any], str]:
        """Get the entire database, optionally in raw format."""
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
        """Get a specific subcollection or an item within a subcollection."""
        collection = self.db.get(collection_name, {})
        if item_id is not None:
            if item_id in collection:
                return collection[item_id]
            else:
                print(f"🐛 \033[91mWhoops! The ID '{item_id}' doesn't exist in the collection '{collection_name}'. It's like looking for a star in the daylight!\033[0m")
                print(f"\033[93m💡 Tip: Check if the ID is correct. Use get_subcollection('{collection_name}') to see all items.\033[0m")
                return None
        return collection

    def set_subcollection(self, collection_name: str, item_id: str, value: Any) -> None:
        """Set an item in a specific subcollection."""
        if not self.validate_data(value):
            print("🐛 \033[91mWhoops! The provided data is not in a valid format. It seems to have lost its form!\033[0m")
            print(f"\033[93m💡 Tip: Your data should look like this: {{'name': 'Aliou', 'age': 30}}\033[0m")
            return
        if collection_name not in self.db:
            self.db[collection_name] = {}
        if item_id in self.db[collection_name]:
            print(f"🐛 \033[91mWhoops! The ID '{item_id}' already exists in the collection '{collection_name}'. It's like trying to fit two keys into one lock!\033[0m")
            print(f"\033[93m💡 Tip: If you want to update or add new item, use db.edit_subcollection('{collection_name}', '{item_id}', new_value).\033[0m")
            return
        self.db[collection_name][item_id] = value
        self._backup_db()
        self._save_db()

    def edit_subcollection(self, collection_name: str, item_id: str, value: Any) -> None:
        """Edit an item in a specific subcollection."""
        if not self.validate_data(value):
            print("🐛 \033[91mWhoops! The provided data is not in a valid format. It's gone a bit haywire!\033[0m")
            print(f"\033[93m💡 Tip: Your data should look like this: {{'name': 'Aliou', 'age': 30}}\033[0m")
            return
        if collection_name in self.db and item_id in self.db[collection_name]:
            current_data = self.db[collection_name][item_id]
            if isinstance(current_data, dict):
                value = self._merge_dicts(current_data, value)
            self.db[collection_name][item_id] = value
            self._backup_db()
            self._save_db()
        else:
            print(f"🐛 \033[91mWhoops! The ID '{item_id}' doesn't exist in the collection '{collection_name}'. It's like editing a ghost!\033[0m")
            print(f"\033[93m💡 Tip: Use 'set_subcollection' to create a new item if needed.\033[0m")

    def remove_subcollection(self, collection_name: str, item_id: Optional[str] = None) -> None:
        """Remove an entire subcollection or a specific item within it."""
        if item_id is None:
            if collection_name in self.db:
                del self.db[collection_name]
                self._backup_db()
                self._save_db()
            else:
                print(f"🐛 \033[91mWhoops! The collection '{collection_name}' doesn't exist. It seems to have vanished!\033[0m")
                print(f"\033[93m💡 Tip: Make sure the collection name is correct.\033[0m")
                return
        else:
            if collection_name in self.db and item_id in self.db[collection_name]:
                del self.db[collection_name][item_id]
                self._backup_db()
                self._save_db()
            else:
                print(f"🐛 \033[91mWhoops! The ID '{item_id}' doesn't exist in the collection '{collection_name}'. It's like trying to remove something that isn't there!\033[0m")
                print(f"\033[93m💡 Tip: Check the ID and collection name. Use get_subcollection('{collection_name}') to see all items.\033[0m")
                return