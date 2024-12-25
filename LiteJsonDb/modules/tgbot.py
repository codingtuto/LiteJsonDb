import requests
import os
from datetime import datetime
import platform

class BackupToTelegram:
    def __init__(self, token: str, chat_id: str):
        """
        Initialize the BackupToTelegram class.

        Parameters:
        - token (str): The access token for your Telegram bot.
        - chat_id (str): The Telegram chat ID where the file will be sent.
        """
        self.token = token
        self.chat_id = chat_id
        self.api_url = f"https://api.telegram.org/bot{self.token}/sendDocument"

    def _send_request(self, files, caption: str) -> bool:
        """
        Internal helper function to send the backup file to the Telegram chat.

        Parameters:
        - files (dict): The backup file to be sent.
        - caption (str): A message to accompany the file, in HTML format.

        Returns:
        - bool: True if the file was successfully sent, False otherwise.
        """
        try:
            response = requests.post(self.api_url, data={'chat_id': self.chat_id, 'caption': caption, 'parse_mode': 'HTML'}, files=files)
            response_data = response.json()

            if response.status_code == 401:
                print(f"🐛 \033[91mWhoops! Invalid token. Like trying to use the wrong key on a treasure chest!\033[0m")
                return False
            elif response_data.get("error_code") == 400 and "chat not found" in response_data.get("description", "").lower():
                print(f"🐛 \033[91mWhoops! Invalid chat ID '{self.chat_id}'. Maybe the bot is in another dimension!\033[0m")
                return False
            elif not response_data.get("ok"):
                 print(f"🐛 \033[91mWhoops! Something went wrong: {response_data.get('description', 'Unknown error')}. Like a plot twist no one saw coming!\033[0m")
                 return False

            return True
        except requests.exceptions.RequestException as e:
            print(f"🐛 \033[91mWhoops! Could not connect to Telegram API. Is the internet taking a break?: {e}\033[0m")
            return False

    def backup_to_telegram(self, backup_filepath: str) -> None:
        """
        Back up a file by sending it to a Telegram chat.

        Parameters:
        - backup_filepath (str): The path to the backup file you want to send.
        """
        if not os.path.exists(backup_filepath):
            print(f"🐛 \033[91mWhoops! Backup file '{backup_filepath}' does not exist. It’s like trying to find a unicorn!\033[0m")
            return

        file_size_mb = os.path.getsize(backup_filepath) / (1024 * 1024)  # File size in MB
        if file_size_mb > 50:
            print(f"🐛 \033[91mWhoops! File size ({file_size_mb:.2f} MB) exceeds Telegram's limit (50 MB). Time to go on a diet!\033[0m")
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
                     print(f"🐛 \033[91mWhoops! Sending the backup file to Telegram went sideways! Looks like it missed the flight.\033[0m")
        
        except Exception as e:
            print(f"🐛 \033[91mWhoops! An unexpected error occurred: {e}. Time to investigate this anomaly!\033[0m")