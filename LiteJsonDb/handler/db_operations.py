import os
import json
import shutil
import logging
from typing import Any, Dict, Optional

class DatabaseOperations:
    """
    Handles database operations such as loading, saving, backing up, and restoring.

    This class provides methods to manage the database file, including loading data from the file,
    saving data to the file, creating backups, and restoring from backups.
    """
    def __init__(self, enable_log: bool = False, auto_backup: bool = False):
        """
        Initializes the DatabaseOperations class.

        Args:
            enable_log (bool, optional): Whether to enable logging. Defaults to False.
            auto_backup (bool, optional): Whether to enable automatic backups. Defaults to False.
        """
        self.enable_log = enable_log
        self.auto_backup = auto_backup

    def _load_db(self) -> None:
        """
        Loads the database from the JSON file, or creates a new one if it doesn't exist.
        """
        if not os.path.exists(self.filename):
            try:
                with open(self.filename, 'w') as file:
                    json.dump({}, file)
                if self.enable_log:
                    logging.info(f"Database file created: {self.filename}")
            except OSError as e:
                print(f"\033[91m#bugs\033[0m Unable to create database file: {e}")
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
            print(f"\033[91m#bugs\033[0m Unable to load database file: {e}")
            raise

    def _save_db(self) -> None:
        """
        Saves the database to the JSON file.
        """
        try:
            data = self.db if not self.crypted else self._encrypt(self.db)
            with open(self.filename, 'w') as file:
                json.dump(data, file, indent=4)
            if self.enable_log:
                logging.info(f"Database saved to {self.filename}")
        except OSError as e:
            print(f"\033[91m#bugs\033[0m Could not save database: {e}")
            raise
    
    def _backup_db(self) -> None:
        """
        Creates a backup of the database.
        """
        if self.auto_backup:
            try:
                shutil.copy(self.filename, self.backup_filename)
                if self.enable_log:
                    logging.info(f"Backup created: {self.backup_filename}")
            except OSError as e:
                print(f"\033[91m#bugs\033[0m Unable to create backup: {e}")
                raise

    def _restore_db(self) -> None:
        """
        Restores the database from backup.
        """
        if os.path.exists(self.backup_filename):
            try:
                shutil.copy(self.backup_filename, self.filename)
                self._load_db()
                if self.enable_log:
                    logging.info(f"Database restored from backup: {self.backup_filename}")
            except OSError as e:
                print(f"\033[91m#bugs\033[0m Unable to restore database: {e}")
                raise
        else:
            print("\033[91m#bugs\033[0m No backup file found.")
            if self.enable_log:
                logging.error("No backup file found to restore.")