import os
import logging
from typing import Any, Dict, Optional
from .handler import (
    Encryption, DatabaseOperations, DataManipulation
)
from .modules import (
    CSVExporter, search_data, BackupToTelegram
)
from .utility import (
    convert_to_datetime, get_or_default, key_exists_or_add, normalize_keys,
    flatten_json, filter_data, sort_data, hash_password, check_password,
    sanitize_output, pretty_print
)

DATABASE_DIR = 'database'
if not os.path.exists(DATABASE_DIR):
    try:
        os.makedirs(DATABASE_DIR)
    except OSError as e:
        print(f"\033[90m#bugs\033[0m Couldn't make the database dir, permissions gone? Details: {e}")
        raise

def setup_logging(enable_log):
    if enable_log:
        logging.basicConfig(filename=os.path.join(DATABASE_DIR, 'LiteJsonDb.log'), level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class JsonDB(Encryption, DatabaseOperations, DataManipulation):
    """
    A lightweight JSON database with encryption, backup, and utility functions.

    This class combines functionalities for handling JSON database operations,
    including encryption, data manipulation, and utility functions.

    Args:
        filename (str): The name of the JSON database file. Defaults to "db.json".
        backup_filename (str): The name of the backup JSON database file. Defaults to "db_backup.json".
        enable_log (bool): Enables logging if set to True. Defaults to False.
        auto_backup (bool): Enables automatic backups after each write operation if True. Defaults to False.
        crypted (bool): Enables encryption for the database if set to True. Defaults to False.
        encryption_method (str): The encryption method to use ('base64' or 'fernet'). Defaults to 'base64'.
        encryption_key (Optional[str]): The encryption key to use (required for fernet). Defaults to None.

    """
    def __init__(self, filename="db.json", backup_filename="db_backup.json", 
                 enable_log=False, auto_backup=False, crypted=False, encryption_method='base64', encryption_key: Optional[str] = None):
        if encryption_method not in ['base64', 'fernet']:
            raise ValueError(f"\033[90m#bugs\033[0m Unknown encryption method: '{encryption_method}'!")

        self.filename = os.path.join(DATABASE_DIR, filename)
        self.backup_filename = os.path.join(DATABASE_DIR, backup_filename)
        self.enable_log = enable_log
        self.auto_backup = auto_backup
        self.crypted = crypted
        self.encryption_method = encryption_method
        self.db = {}
        self.observers = {}
        self.csv_exporter = CSVExporter(DATABASE_DIR)
        setup_logging(self.enable_log)
        Encryption.__init__(self, encryption_method, encryption_key) 
        DatabaseOperations.__init__(self, enable_log, auto_backup)
        DataManipulation.__init__(self)
        self._load_db()

    def backup_to_telegram(self, token: str, chat_id: str):
        """
         Sends the database backup to a specified Telegram chat.

         Args:
             token (str): The Telegram bot token.
             chat_id (str): The Telegram chat ID.
        """
        self._save_db()
        telegram_bot = BackupToTelegram(token=token, chat_id=chat_id)
        try:
            telegram_bot.backup_to_telegram(self.filename)
        except Exception as e:
            print(f"\033[90m#bugs\033[0m Telegram backup took a wrong turn! Error: {e}")
            if self.enable_log:
                logging.error(f"Error sending backup to Telegram: {e}")

    def export_to_csv(self, data_key: Optional[str] = None):
        """
         Exports the database or a specified collection to a CSV file.

         Args:
              data_key (Optional[str]): If provided, exports only the data under this key. If None, exports the full database.
        """
        if data_key:
            if data_key in self.db:
                data = self.db[data_key]
                csv_path = self.csv_exporter.export(data, f"{data_key}_export.csv")
                if csv_path:
                    print(f"🎉 Hooray! CSV exported to: {csv_path}")
                else:
                    print(f"\033[90m#bugs\033[0m Could not export '{data_key}' to CSV!")
            else:
                 print(f"\033[90m#bugs\033[0m Key '{data_key}' not found, is it hiding? Tip: Double-check it!")
        else:
            if self.db:
                csv_path = self.csv_exporter.export(self.db, "full_database_export.csv")
                if csv_path:
                    print(f"🎉 Full database exported to: {csv_path}")
                else:
                    print("\033[90m#bugs\033[0m Database export failed. It's shy!")
            else:
                print("\033[90m#bugs\033[0m Database is empty, ghost town vibes!")

    def search_data(self, value: Any, key: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """
        Searches for a value within the database.

         Args:
             value (Any): The value to search for.
             key (Optional[str]): If provided, searches only within the values associated with this key.
            Returns:
                Optional[Dict[str, Any]]: Returns the matching dictionary or None if not found.
        """
        try:
            result = search_data(self.db, value, key)
            if result:
                return result
            else:
                print("\033[90m#info\033[0m  Not found! Try another quest?")
                return None
        except Exception as e:
            print(f"\033[90m#bugs\033[0m Search party got lost! Error: {e}")
            return None

    @staticmethod
    def call_utility_function(func_name, *args, **kwargs):
        """
         Dynamically calls utility functions based on func_name.

         Args:
             func_name (str): The name of the utility function to call.
             *args: Positional arguments to pass to the function.
             **kwargs: Keyword arguments to pass to the function.
           Returns:
                Any: Result of the called utility function
            Raises:
                ValueError: If the specified function is not found.
        """
        functions = {
            'convert_to_datetime': convert_to_datetime,
            'get_or_default': get_or_default,
            'key_exists_or_add': key_exists_or_add,
            'normalize_keys': normalize_keys,
            'flatten_json': flatten_json,
            'filter_data': filter_data,
            'sort_data': sort_data,
            'hash_password': hash_password,
            'check_password': check_password,
            'sanitize_output': sanitize_output,
            'pretty_print': pretty_print
        }
        if func_name in functions:
            return functions[func_name](*args, **kwargs)
        #BUGS: Utility function not found.
        raise ValueError(f"\033[90m#bugs\033[0m  Utility function '{func_name}' not found!")

    @staticmethod
    def convert_to_datetime(date_str):
        """
        Wrapper for the utility function convert_to_datetime
        Args:
            date_str (str): The date string to convert.
        Returns:
            Any: Result of convert_to_datetime utility function
        """
        return JsonDB.call_utility_function('convert_to_datetime', date_str)

    @staticmethod
    def get_or_default(data, key, default=None):
        """
        Wrapper for the utility function get_or_default
        Args:
            data(Any): The data to search
            key (str): The key to search
            default (Any, optional): Value to return if key isn't present.
        Returns:
            Any: Result of get_or_default utility function
        """
        return JsonDB.call_utility_function('get_or_default', data, key, default)

    @staticmethod
    def key_exists_or_add(data, key, default):
        """
        Wrapper for the utility function key_exists_or_add
        Args:
            data(Any): The data to modify
            key (str): The key to check
            default (Any): Value to set if key doesn't exist.
        Returns:
            Any: Result of key_exists_or_add utility function
        """
        return JsonDB.call_utility_function('key_exists_or_add', data, key, default)

    @staticmethod
    def normalize_keys(data):
        """
        Wrapper for the utility function normalize_keys
        Args:
            data(Any): The data to normalize
        Returns:
            Any: Result of normalize_keys utility function
        """
        return JsonDB.call_utility_function('normalize_keys', data)

    @staticmethod
    def flatten_json(data):
        """
        Wrapper for the utility function flatten_json
        Args:
            data(Any): The json data to flatten
        Returns:
            Any: Result of flatten_json utility function
        """
        return JsonDB.call_utility_function('flatten_json', data)

    @staticmethod
    def filter_data(data, condition):
        """
        Wrapper for the utility function filter_data
        Args:
            data (Any): The data to filter.
            condition (callable): The filtering condition (a function).
        Returns:
            Any: Result of filter_data utility function
        """
        return JsonDB.call_utility_function('filter_data', data, condition)

    @staticmethod
    def sort_data(data, key, reverse=False):
        """
        Wrapper for the utility function sort_data
        Args:
            data (Any): The data to sort.
            key (str): The key to sort by.
            reverse (bool): if True sorts in reverse
        Returns:
            Any: Result of sort_data utility function
        """
        return JsonDB.call_utility_function('sort_data', data, key, reverse)

    @staticmethod
    def hash_password(password):
        """
        Wrapper for the utility function hash_password
        Args:
            password(str): the password to hash
        Returns:
            Any: Result of hash_password utility function
        """
        return JsonDB.call_utility_function('hash_password', password)

    @staticmethod
    def check_password(stored_hash, password):
        """
        Wrapper for the utility function check_password
        Args:
            stored_hash (str): The stored password hash.
            password (str): The password to check.
        Returns:
            Any: Result of check_password utility function
        """
        return JsonDB.call_utility_function('check_password', stored_hash, password)

    @staticmethod
    def sanitize_output(data):
        """
        Wrapper for the utility function sanitize_output
        Args:
            data(Any): The data to sanitize
        Returns:
            Any: Result of sanitize_output utility function
        """
        return JsonDB.call_utility_function('sanitize_output', data)

    @staticmethod
    def pretty_print(data):
        """
        Wrapper for the utility function pretty_print
        Args:
            data(Any): The data to print pretty
        Returns:
            Any: Result of pretty_print utility function
        """
        return JsonDB.call_utility_function('pretty_print', data)