import os
import json
import shutil
import logging
import tempfile
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
        self._db_signature = None

    def _current_signature(self):
        """
        Cheap fingerprint of the database file on disk (modification time + size).

        A single ``os.stat`` call (microseconds) is enough to tell whether the
        file was changed by something other than this instance, without reading
        or parsing its contents.
        """
        try:
            st = os.stat(self.filename)
            return (st.st_mtime_ns, st.st_size)
        except OSError:
            return None

    def _sync_if_changed(self) -> None:
        """
        Reload the database from disk if the file changed outside this instance.

        This makes external edits (e.g. someone editing ``database/db.json`` in a
        text editor while the program runs) visible to reads, and prevents writes
        from clobbering those edits. It is intentionally lightweight (one stat per
        call), silent (no log/print spam) and tolerant of partial writes: if the
        file is momentarily unreadable (an editor mid-save), the in-memory state
        is kept and the reload is retried on the next access.
        """
        if getattr(self, '_batch_mode', False):
            # Inside a batch() we deliberately work from the in-memory snapshot.
            return
        signature = self._current_signature()
        if signature == self._db_signature:
            return
        try:
            with open(self.filename, 'r') as file:
                data = json.load(file)
        except (OSError, ValueError):
            # File missing or partially written; keep current state, retry later.
            return
        if self.crypted and data:
            try:
                self.db = self._decrypt(data) if isinstance(data, str) else data
            except Exception:
                return
        else:
            self.db = data
        self._db_signature = signature

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
                # Encrypted payloads are stored as a string. A dict here means the
                # file was written as plain text (e.g. by an older version where
                # encryption was inactive); load it as-is for backward compatibility.
                self.db = self._decrypt(data) if isinstance(data, str) else data
            else:
                self.db = data
            self._db_signature = self._current_signature()
            if self.enable_log:
                logging.info(f"Database loaded from: {self.filename}")
        except (OSError, json.JSONDecodeError) as e:
            print(f"\033[91m#bugs\033[0m Unable to load database file: {e}")
            raise

    def _save_db(self) -> None:
        """
        Saves the database to the JSON file.
        """
        if getattr(self, '_batch_mode', False):
            # Inside a batch() block: defer the write until the block exits.
            return
        try:
            data = self.db if not self.crypted else self._encrypt(self.db)
            # Write to a temp file then atomically replace, so an interrupted
            # write can never leave a half-written / corrupted database on disk.
            target_dir = os.path.dirname(self.filename) or '.'
            fd, tmp_path = tempfile.mkstemp(dir=target_dir, suffix='.tmp')
            try:
                with os.fdopen(fd, 'w') as file:
                    indent = getattr(self, 'json_indent', None)
                    if indent is None:
                        # Compact output: ~5x faster to serialize and far smaller on disk.
                        json.dump(data, file, separators=(',', ':'))
                    else:
                        json.dump(data, file, indent=indent)
                os.replace(tmp_path, self.filename)
            except BaseException:
                try:
                    os.remove(tmp_path)
                except OSError:
                    pass
                raise
            # Record our own write so it is not mistaken for an external change.
            self._db_signature = self._current_signature()
            if self.enable_log:
                logging.info(f"Database saved to {self.filename}")
        except OSError as e:
            print(f"\033[91m#bugs\033[0m Could not save database: {e}")
            raise
    
    def _backup_db(self) -> None:
        """
        Creates a backup of the database.
        """
        if getattr(self, '_batch_mode', False):
            # Inside a batch() block: defer the backup until the block exits.
            return
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