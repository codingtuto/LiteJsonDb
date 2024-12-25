import os
import json
import shutil
import logging
from typing import Any, Dict, Optional

class DatabaseOperations:
    def __init__(self, enable_log: bool = False, auto_backup: bool = False):
        self.enable_log = enable_log
        self.auto_backup = auto_backup

    def _load_db(self) -> None:
        """Load the database from the JSON file, or create a new one if it doesn't exist."""
        if not os.path.exists(self.filename):
            try:
                with open(self.filename, 'w') as file:
                    json.dump({}, file)
                if self.enable_log:
                    logging.info(f"Database file created: {self.filename}")
            except OSError as e:
                print("🐛 Error: Unable to create the database file. Perhaps it got trapped in a recursive loop?")
                print(f"Details: {e}")
                raise
        try:
            with open(self.filename, 'r') as file:
                data = json.load(file)
                if self.crypted and data:
                    self.db = self._decrypt(data)
                else:
                    self.db = data
            if self.enable_log:
                logging.info(f"Database loaded from: {self.filename}")
        except (OSError, json.JSONDecodeError) as e:
            print("🐛 Error: Unable to load the database file. Maybe it wandered off into the void?")
            print(f"Details: {e}")
            raise

    def _save_db(self) -> None:
        """Save the database to the JSON file."""
        try:
            data = self.db if not self.crypted else self._encrypt(self.db)
            with open(self.filename, 'w') as file:
                json.dump(data, file, indent=4)
            if self.enable_log:
                logging.info(f"Database saved to {self.filename}")
        except OSError as e:
            print("🐛 Error: Could not save the database. Did the save operation go on a coffee break?")
            print(f"Details: {e}")
            raise
    
    def _backup_db(self) -> None:
        """Create a backup of the database."""
        if self.auto_backup:
            try:
                shutil.copy(self.filename, self.backup_filename)
                if self.enable_log:
                    logging.info(f"Backup created: {self.backup_filename}")
            except OSError as e:
                print("🐛 Error: Unable to create the backup. Did it encounter an unexpected detour?")
                print(f"Details: {e}")
                raise

    def _restore_db(self) -> None:
        """Restore the database from backup."""
        if os.path.exists(self.backup_filename):
            try:
                shutil.copy(self.backup_filename, self.filename)
                self._load_db()
                if self.enable_log:
                    logging.info(f"Database restored from backup: {self.backup_filename}")
            except OSError as e:
                print("🐛 Error: Unable to restore the database. Was the backup file accidentally sent to another dimension?")
                print(f"Details: {e}")
                raise
        else:
            print("🐛 Error: No backup file found. It's like searching for your keys in a parallel universe.")
            if self.enable_log:
                logging.error("No backup file found to restore.")
