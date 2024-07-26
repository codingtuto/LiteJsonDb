"""
██╗░░░░░██╗████████╗███████╗░░░░░██╗░██████╗░█████╗░███╗░░██╗██████╗░██████╗░░░░██████╗░██╗░░░██╗
██║░░░░░██║╚══██╔══╝██╔════╝░░░░░██║██╔════╝██╔══██╗████╗░██║██╔══██╗██╔══██╗░░░██╔══██╗╚██╗░██╔╝
██║░░░░░██║░░░██║░░░█████╗░░░░░░░██║╚█████╗░██║░░██║██╔██╗██║██║░░██║██████╦╝░░░██████╔╝░╚████╔╝░
██║░░░░░██║░░░██║░░░██╔══╝░░██╗░░██║░╚═══██╗██║░░██║██║╚████║██║░░██║██╔══██╗░░░██╔═══╝░░░╚██╔╝░░
███████╗██║░░░██║░░░███████╗╚█████╔╝██████╔╝╚█████╔╝██║░╚███║██████╔╝██████╦╝██╗██║░░░░░░░░██║░░░
╚══════╝╚═╝░░░╚═╝░░░╚══════╝░╚════╝░╚═════╝░░╚════╝░╚═╝░░╚══╝╚═════╝░╚═════╝░╚═╝╚═╝░░░░░░░░╚═╝░░░
"""

import json
import os
import base64
import logging
import shutil
from typing import Any, Dict, Optional, Union

# LET'S CREATE THE DATABASE FILE
DATABASE_DIR = 'database'
if not os.path.exists(DATABASE_DIR):
    try:
        os.makedirs(DATABASE_DIR)
    except OSError as e:
        print(f"\033[91mOops! Unable to create the database directory. Make sure you have the correct permissions.\033[0m")
        print(f"\033[93mError details: {e}\033[0m")
        raise

# LOGGING
logging.basicConfig(filename=os.path.join(DATABASE_DIR, 'LiteJsonDb.log'), level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class JsonDB:
    def __init__(self, filename="db.json", backup_filename="db_backup.json", crypted=True):
        self.filename = os.path.join(DATABASE_DIR, filename)
        self.backup_filename = os.path.join(DATABASE_DIR, backup_filename)
        self.crypted = crypted
        self.db = {}
        self.observers = {}
        self._load_db()

    def _encrypt(self, data: Dict[str, Any]) -> str:
        """Encode data to base64 for fun. Just a playful way to 'encrypt' our data!"""
        json_data = json.dumps(data).encode('utf-8')
        encoded_data = base64.b64encode(json_data).decode('utf-8')
        return encoded_data

    def _decrypt(self, encoded_data: str) -> Dict[str, Any]:
        """Decode data from base64 for fun. Decoding our playful 'encryption'!"""
        decoded_data = base64.b64decode(encoded_data.encode('utf-8')).decode('utf-8')
        return json.loads(decoded_data)

    def _load_db(self) -> None:
        """Load the database from the JSON file, or create a new one if it doesn't exist."""
        if not os.path.exists(self.filename):
            try:
                with open(self.filename, 'w') as file:
                    json.dump({}, file)
            except OSError as e:
                print(f"\033[91mOops! Unable to create the database file. Make sure you have the correct permissions.\033[0m")
                print(f"\033[93mError details: {e}\033[0m")
                raise
        try:
            with open(self.filename, 'r') as file:
                data = json.load(file)
                if self.crypted and data:
                    self.db = self._decrypt(data)  # Removed extra parameter `data`
                else:
                    self.db = data
        except (OSError, json.JSONDecodeError) as e:
            print(f"\033[91mOops! Unable to load the database file. Make sure the file is accessible and contains valid JSON.\033[0m")
            print(f"\033[93mError details: {e}\033[0m")
            raise

    def _save_db(self) -> None:
        """Save the database to the JSON file."""
        try:
            data = self.db if not self.crypted else self._encrypt(self.db)
            with open(self.filename, 'w') as file:
                json.dump(data, file, indent=4)
            logging.info(f"Database saved to {self.filename}")
        except OSError as e:
            print(f"\033[91mOops! Unable to save the database file. Make sure you have the correct permissions.\033[0m")
            print(f"\033[93mError details: {e}\033[0m")
            raise

    def _backup_db(self) -> None:
        """Create a backup of the database."""
        try:
            shutil.copy(self.filename, self.backup_filename)
            logging.info(f"Backup created: {self.backup_filename}")
        except OSError as e:
            print(f"\033[91mOops! Unable to create the backup file. Make sure you have the correct permissions.\033[0m")
            print(f"\033[93mError details: {e}\033[0m")
            raise

    def _restore_db(self) -> None:
        """Restore the database from backup."""
        if os.path.exists(self.backup_filename):
            try:
                shutil.copy(self.backup_filename, self.filename)
                self._load_db()
                logging.info(f"Database restored from backup: {self.backup_filename}")
            except OSError as e:
                print(f"\033[91mOops! Unable to restore the database from backup. Make sure the backup file is accessible.\033[0m")
                print(f"\033[93mError details: {e}\033[0m")
                raise
        else:
            print(f"\033[91mOops! No backup file found to restore.\033[0m")
            logging.error("No backup file found to restore.")

    def validate_data(self, data: Any) -> bool:
        """Validate data before insertion."""
        if isinstance(data, dict):
            # Check for duplicate keys with different types
            types = {}
            for key, value in data.items():
                if not isinstance(key, str):
                    print(f"\033[91mOops! Keys in data should be strings. Found non-string key '{key}'.\033[0m")
                    return False
                if key in types and types[key] != type(value):
                    print(f"\033[91mOops! Key '{key}' has conflicting types in data. Found types: {types[key]} and {type(value)}.\033[0m")
                    return False
                types[key] = type(value)
            # Ensure values are of allowed types
            return all(isinstance(value, (str, int, float, list, dict, bool, None)) for value in data.values())
        print(f"\033[91mOops! Data should be a dictionary.\033[0m")
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
                print(f"\033[91mOops! The key '{key}' does not exist. Make sure the key is correct.\033[0m")
                print(f"\033[93mTip: Use a valid key path like 'users/1' to get specific user data.\033[0m")
                return None
        return data

    def set_data(self, key: str, value: Optional[Any] = None) -> None:
        """Set data in the database and notify observers.
    
        If `value` is not provided, initialize the key with an empty dictionary.
        """
        if value is None:
            value = {}

        if not self.validate_data(value):
            print("\033[91mOops! The provided data is not in a valid format. Use a dictionary with consistent types.\033[0m")
            print(f"\033[93mTip: Ensure keys have consistent types and values are of allowed types.\033[0m")
            return
        if self.key_exists(key):
            print(f"\033[91mOops! The key '{key}' already exists. Use 'edit_data' to modify the existing key.\033[0m")
            print(f"\033[93mTip: If you want to update or add new key, use db.edit_data('{key}', new_value).\033[0m")
            return
        self._set_child(self.db, key, value)
        self._backup_db()
        self._save_db()


    def edit_data(self, key: str, value: Any) -> None:
        """Edit data in the database and notify observers."""
        if not self.key_exists(key):
            print(f"\033[91mOops! The key '{key}' does not exist. Unable to edit non-existent data.\033[0m")
            print(f"\033[93mTip: Use 'set_data' to add new data if needed.\033[0m")
            return
        if not self.validate_data(value):
            print("\033[91mOops! The provided data is not in a valid format. Use a dictionary with consistent types.\033[0m")
            print(f"\033[93mTip: Ensure keys have consistent types and values are of allowed types.\033[0m")
            return
        keys = key.split('/')
        data = self.db
        for k in keys[:-1]:
            data = data.setdefault(k, {})
        current_data = data.get(keys[-1], {})
        if isinstance(current_data, dict):
            value = self._merge_dicts(current_data, value)
        data[keys[-1]] = value
        self._backup_db()
        self._save_db()

    def remove_data(self, key: str) -> None:
        """Remove data from the database by key."""
        keys = key.split('/')
        data = self.db
        for k in keys[:-1]:
            if k in data:
                data = data[k]
            else:
                print(f"\033[91mOops! The key '{key}' does not exist. Cannot delete.\033[0m")
                print(f"\033[93mTip: Make sure the key path is correct and exists.\033[0m")
                return
        if keys[-1] in data:
            del data[keys[-1]]
            self._backup_db()
            self._save_db()
        else:
            print(f"\033[91mOops! The key '{key}' does not exist. Cannot delete.\033[0m")
            print(f"\033[93mTip: Make sure the key path is correct and exists.\033[0m")

    def get_db(self, raw: bool = False) -> Union[Dict[str, Any], str]:
        """Get the entire database, optionally in raw format."""
        if raw:
            return self.db
        if self.crypted:
            return self._decrypt(self._encrypt(self.db))
        return self.db


    def get_subcollection(self, collection_name: str, item_id: Optional[str] = None) -> Optional[Any]:
        """Get a specific subcollection or an item within a subcollection."""
        collection = self.db.get(collection_name, {})
        if item_id is not None:
            if item_id in collection:
                return collection[item_id]
            else:
                print(f"\033[91mOops! The ID '{item_id}' does not exist in the collection '{collection_name}'.\033[0m")
                print(f"\033[93mTip: Check if the ID is correct. Use get_subcollection('{collection_name}') to see all items.\033[0m")
                return None
        return collection

    def set_subcollection(self, collection_name: str, item_id: str, value: Any) -> None:
        """Set an item in a specific subcollection."""
        if not self.validate_data(value):
            print("\033[91mOops! The provided data is not in a valid format. Use a dictionary.\033[0m")
            print(f"\033[93mTip: Your data should look like this: {{'name': 'Aliou', 'age': 30}}\033[0m")
            return
        if collection_name not in self.db:
            self.db[collection_name] = {}
        if item_id in self.db[collection_name]:
            print(f"\033[91mOops! The ID '{item_id}' already exists in the collection '{collection_name}'. Use 'edit_subcollection' to modify the existing item.\033[0m")
            print(f"\033[93mTip: If you want to update or add new item, use db.edit_subcollection('{collection_name}', '{item_id}', new_value).\033[0m")
            return
        self.db[collection_name][item_id] = value
        self._backup_db()
        self._save_db()

    def edit_subcollection(self, collection_name: str, item_id: str, value: Any) -> None:
        """Edit an item in a specific subcollection."""
        if not self.validate_data(value):
            print("\033[91mOops! The provided data is not in a valid format. Use a dictionary.\033[0m")
            print(f"\033[93mTip: Your data should look like this: {{'name': 'Aliou', 'age': 30}}\033[0m")
            return
        if collection_name in self.db and item_id in self.db[collection_name]:
            current_data = self.db[collection_name][item_id]
            if isinstance(current_data, dict):
                value = self._merge_dicts(current_data, value)
            self.db[collection_name][item_id] = value
            self._backup_db()
            self._save_db()
        else:
            print(f"\033[91mOops! The ID '{item_id}' does not exist in the collection '{collection_name}'. Unable to edit non-existent item.\033[0m")
            print(f"\033[93mTip: Use 'set_subcollection' to create a new item if needed.\033[0m")

    def remove_subcollection(self, collection_name: str, item_id: Optional[str] = None) -> None:
        """Remove an entire subcollection or a specific item within it."""
        if item_id is None:
            if collection_name in self.db:
                del self.db[collection_name]
                self._backup_db()
                self._save_db()
            else:
                print(f"\033[91mOops! The collection '{collection_name}' does not exist. Cannot delete.\033[0m")
                print(f"\033[93mTip: Make sure the collection name is correct.\033[0m")
                return
        else:
            if collection_name in self.db and item_id in self.db[collection_name]:
                del self.db[collection_name][item_id]
                self._backup_db()
                self._save_db()
            else:
                print(f"\033[91mOops! The ID '{item_id}' does not exist in the collection '{collection_name}'. Cannot delete.\033[0m")
                print(f"\033[93mTip: Check the ID and collection name. Use get_subcollection('{collection_name}') to see all items.\033[0m")
                return
