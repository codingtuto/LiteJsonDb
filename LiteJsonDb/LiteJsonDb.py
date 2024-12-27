"""
██╗░░░░░██╗████████╗███████╗░░░░░██╗░██████╗░█████╗░███╗░░██╗██████╗░██████╗░░░░██████╗░██╗░░░██╗
██║░░░░░██║╚══██╔══╝██╔════╝░░░░░██║██╔════╝██╔══██╗████╗░██║██╔══██╗██╔══██╗░░░██╔══██╗╚██╗░██╔╝
██║░░░░░██║░░░██║░░░█████╗░░░░░░░██║╚█████╗░██║░░██║██╔██╗██║██║░░██║██████╦╝░░░██████╔╝░╚████╔╝░
██║░░░░░██║░░░██║░░░██╔══╝░░██╗░░██║░╚═══██╗██║░░██║██║╚████║██║░░██║██╔══██╗░░░██╔═══╝░░░╚██╔╝░░
███████╗██║░░░██║░░░███████╗╚█████╔╝██████╔╝╚█████╔╝██║░╚███║██████╔╝██████╦╝██╗██║░░░░░░░░██║░░░
╚══════╝╚═╝░░░╚═╝░░░╚══════╝░╚════╝░╚═════╝░░╚════╝░╚═╝░░╚══╝╚═════╝░╚═════╝░╚═╝╚═╝░░░░░░░░╚═╝░░░
"""

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
        print(f"🐛 Whoops! Couldn't create the database dir. Are the permissions on vacation? 😅")
        print(f"Details: {e}")
        raise

# LOGGING (Conditional)
def setup_logging(enable_log):
    if enable_log:
        logging.basicConfig(filename=os.path.join(DATABASE_DIR, 'LiteJsonDb.log'), level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class JsonDB(Encryption, DatabaseOperations, DataManipulation):
    def __init__(self, filename="db.json", backup_filename="db_backup.json", 
                 enable_log=False, auto_backup=False, crypted=False, encryption_method='base64', encryption_key: Optional[str] = None):
        """Initialize the database connection and encryption setup."""
        if encryption_method not in ['base64', 'fernet']:
            raise ValueError(f"🐛 Oops! I don't know '{encryption_method}' encryption!")

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
        """Send the db backup to Telegram."""
        self._save_db()
        telegram_bot = BackupToTelegram(token=token, chat_id=chat_id)
        try:
            telegram_bot.backup_to_telegram(self.filename)
        except Exception as e:
            print(f"🐛 Whoops! Telegram backup failed! Looks like it took a wrong turn!")
            if self.enable_log:
                logging.error(f"Error sending backup to Telegram: {e}")

    def export_to_csv(self, data_key: Optional[str] = None):
        """Export the database or a specified collection to CSV."""
        if data_key:
            if data_key in self.db:
                data = self.db[data_key]
                csv_path = self.csv_exporter.export(data, f"{data_key}_export.csv")
                if csv_path:
                    print(f"🎉 Hooray! CSV exported to: {csv_path}")
                else:
                    print(f"🐛 Whoops! Could not export '{data_key}' to CSV. Something went wrong. 😵")
            else:
                print(f"🐛 Whoops! Key '{data_key}' doesn't exist. Is it hiding? 🤔")
                print("💡 Tip: Double-check the key or try a different one!")
        else:
            if self.db:
                csv_path = self.csv_exporter.export(self.db, "full_database_export.csv")
                if csv_path:
                    print(f"🎉 Full database exported to: {csv_path}")
                else:
                    print("🐛 Whoops! The database is camera-shy and won't export. 🤨")
            else:
                print("🐛 Whoops! The database is empty. Ghost town vibes! 👻")

    def search_data(self, value: Any, key: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """Search for a value in the database."""
        try:
            result = search_data(self.db, value, key)
            if result:
                return result
            else:
                print("🐛 Whoops! The treasure you're looking for isn't here. Try another quest?")
                return None
        except Exception as e:
            print(f"🐛 Whoops! Something went wrong while searching. The search party got lost!")
            print(f"Details: {e}")
            return None

    @staticmethod
    def call_utility_function(func_name, *args, **kwargs):
        """Call utility functions dynamically."""
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
        raise ValueError(f"Oops! {func_name} not found! Looks like it ran away!")

    @staticmethod
    def convert_to_datetime(date_str):
        return JsonDB.call_utility_function('convert_to_datetime', date_str)

    @staticmethod
    def get_or_default(data, key, default=None):
        return JsonDB.call_utility_function('get_or_default', data, key, default)

    @staticmethod
    def key_exists_or_add(data, key, default):
        return JsonDB.call_utility_function('key_exists_or_add', data, key, default)

    @staticmethod
    def normalize_keys(data):
        return JsonDB.call_utility_function('normalize_keys', data)

    @staticmethod
    def flatten_json(data):
        return JsonDB.call_utility_function('flatten_json', data)

    @staticmethod
    def filter_data(data, condition):
        return JsonDB.call_utility_function('filter_data', data, condition)

    @staticmethod
    def sort_data(data, key, reverse=False):
        return JsonDB.call_utility_function('sort_data', data, key, reverse)

    @staticmethod
    def hash_password(password):
        return JsonDB.call_utility_function('hash_password', password)

    @staticmethod
    def check_password(stored_hash, password):
        return JsonDB.call_utility_function('check_password', stored_hash, password)

    @staticmethod
    def sanitize_output(data):
        return JsonDB.call_utility_function('sanitize_output', data)

    @staticmethod
    def pretty_print(data):
        return JsonDB.call_utility_function('pretty_print', data)