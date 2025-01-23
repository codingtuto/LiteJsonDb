import requests
import os
from datetime import datetime
import platform

class BackupToTelegram:
    """
    A class to automate sending database backups to a Telegram chat.

    This class provides a simple way to send backups of your database files
    to a Telegram chat for safekeeping. It handles connection to the Telegram
    API, file handling, and error reporting.
    """
    def __init__(self, token: str, chat_id: str):
        """
        Initializes the BackupToTelegram class with necessary credentials.

        Args:
            token (str): The access token for your Telegram bot. This token is
                         provided by BotFather when you create a new bot on Telegram.
                         Ensure this token is kept secure.
            chat_id (str): The Telegram chat ID where the backup file will be sent.
                          This can be the ID of a group, channel, or individual chat.
                          To find the chat ID, you can use a bot that retrieves chat information.
        """
        self.token = token
        self.chat_id = chat_id
        self.api_url = f"https://api.telegram.org/bot{self.token}/sendDocument"

    def _send_request(self, files, caption: str) -> bool:
        """
        Internal helper function to send the backup file to the Telegram chat.

        This function handles the actual sending of the file to Telegram, including
        setting the chat ID, caption, and parse mode.

        Args:
            files (dict): A dictionary containing the file to be sent, in the format
                          expected by the `requests` library (i.e., `{'document': ('filename', file_object)}`).
            caption (str): A message to accompany the file, in HTML format. This can include
                           information about the backup, such as the filename and creation date.

        Returns:
            bool: True if the file was successfully sent, False otherwise.
        """
        try:
            response = requests.post(self.api_url, data={'chat_id': self.chat_id, 'caption': caption, 'parse_mode': 'HTML'}, files=files)
            response_data = response.json()

            if response.status_code == 401:
                print(f"\033[91m#bugs\033[0m Invalid Telegram token.")
                return False
            elif response_data.get("error_code") == 400 and "chat not found" in response_data.get("description", "").lower():
                print(f"\033[91m#bugs\033[0m Invalid chat ID: '{self.chat_id}'.")
                return False
            elif not response_data.get("ok"):
                 print(f"\033[91m#bugs\033[0m Telegram API error: {response_data.get('description', 'Unknown')}.")
                 return False

            return True
        except requests.exceptions.RequestException as e:
            print(f"\033[91m#bugs\033[0m Could not connect to Telegram API: {e}.")
            return False

    def backup_to_telegram(self, backup_filepath: str) -> None:
        """
        Backs up a file by sending it to a Telegram chat.

        This function takes the path to a file, checks if it exists and is within
        the size limits for Telegram, then sends it to the specified chat.

        Args:
            backup_filepath (str): The path to the backup file you want to send.
                                  This should be a valid path to a file on your system.
        """
        if not os.path.exists(backup_filepath):
            print(f"\033[91m#bugs\033[0m Backup file '{backup_filepath}' not found.")
            return

        file_size_mb = os.path.getsize(backup_filepath) / (1024 * 1024)  # File size in MB
        if file_size_mb > 50:
            print(f"\033[91m#bugs\033[0m File size ({file_size_mb:.2f} MB) exceeds Telegram limit.")
            return

        try:
            with open(backup_filepath, 'rb') as backup_file:
                filename = os.path.basename(backup_filepath)
                file_size = os.path.getsize(backup_filepath) / 1024  # File size in KB
                date_str = datetime.now().strftime("%-d/%-m/%Y at %H:%M")
                
                try:
                    os_info = platform.system() + " " + platform.release()
                except Exception:
                    os_info = "Unknown"
            
                caption = (f"<b>🔄 Backup created on {date_str}</b>\n"
                           f"<b>Filename:</b> {filename}\n"
                           f"<b>File size:</b> {file_size:.2f} KB\n"
                           f"<b>System:</b> {os_info}\n\n"
                           "<blockquote>How to restore 🤷‍♂️? Open this file in a text editor, copy its content, and paste it into your project inside the <code>database/db.json</code> file.</blockquote>")

                files = {'document': (filename, backup_file)}
                success = self._send_request(files, caption)

                if success:
                     print(f"🎉 \033[92mHooray! Backup file '{filename}' (Size: {file_size:.2f} KB) was successfully beamed to Telegram! System: {os_info}. All systems go!\033[0m")
                else:
                     print(f"\033[91m#bugs\033[0m Sending backup to Telegram failed.")
        
        except Exception as e:
            print(f"\033[91m#bugs\033[0m Unexpected error occurred: {e}.")