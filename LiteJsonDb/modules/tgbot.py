"""

████████╗░██████╗░██████╗░░█████╗░████████╗░░░██████╗░██╗░░░██╗
╚══██╔══╝██╔════╝░██╔══██╗██╔══██╗╚══██╔══╝░░░██╔══██╗╚██╗░██╔╝
░░░██║░░░██║░░██╗░██████╦╝██║░░██║░░░██║░░░░░░██████╔╝░╚████╔╝░
░░░██║░░░██║░░╚██╗██╔══██╗██║░░██║░░░██║░░░░░░██╔═══╝░░░╚██╔╝░░
░░░██║░░░╚██████╔╝██████╦╝╚█████╔╝░░░██║░░░██╗██║░░░░░░░░██║░░░
░░░╚═╝░░░░╚═════╝░╚═════╝░░╚════╝░░░░╚═╝░░░╚═╝╚═╝░░░░░░░░╚═╝░░░
"""
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
                print(f"\033[91mOops! Invalid token. Please check the bot token. If this were a movie, it’d be called: 'The Token is Not Enough'...\033[0m")
                return False
            elif response_data.get("error_code") == 400 and "chat not found" in response_data.get("description", "").lower():
                print(f"\033[91mOops! Invalid chat ID '{self.chat_id}'.\033[0m")
                print(f"\033[93mTip: Make sure you've started a conversation with the bot using `/start` in the Telegram chat. It’s like saying 'hi' before asking for a favor!\033[0m")
                return False
            elif not response_data.get("ok"):
                print(f"\033[91mOops! Something went wrong: {response_data.get('description', 'Unknown error')}. Like a mystery novel without the ending.\033[0m")
                return False

            return True
        except requests.exceptions.RequestException as e:
            print(f"\033[91mOops! Could not connect to Telegram API: {e}.\033[0m")
            print(f"\033[93mTip: Check your internet connection or see if the Telegram API decided to take a coffee break.\033[0m")
            return False

    def backup_to_telegram(self, backup_filepath: str) -> None:
        """
        Back up a file by sending it to a Telegram chat.

        Parameters:
        - backup_filepath (str): The path to the backup file you want to send.
        """
        if not os.path.exists(backup_filepath):
            print(f"\033[91mOops! The backup file '{backup_filepath}' does not exist. It's like trying to teleport without a destination!\033[0m")
            print(f"\033[93mTip: Double-check the file path to ensure the file is there. Maybe it took a vacation?\033[0m")
            return

        try:
            with open(backup_filepath, 'rb') as backup_file:
                filename = os.path.basename(backup_filepath)
                file_size = os.path.getsize(backup_filepath) / 1024  # File size in KB
                date_str = datetime.now().strftime("%-d/%-m/%Y at %H:%M")
            
                # Handle system information, default to "Unknown" if not found
                os_info = platform.system() + " " + platform.release() if platform.system() and platform.release() else "Unknown"

                caption = (f"<b>🔄 Backup created on {date_str}</b>\n"
                           f"<b>Filename:</b> {filename}\n"
                           f"<b>File size:</b> {file_size:.2f} KB\n"
                           f"<b>System:</b> {os_info}\n\n"
                           "<blockquote>How to restore 🤷‍♂️? Open this file in a text editor, copy its content, and paste it into your project inside the <code>database/db.json</code> file.</blockquote>")

                files = {'document': (filename, backup_file)}
                success = self._send_request(files, caption)

                if success:
                    print(f"\033[92mSuccess! Backup file '{filename}' (Size: {file_size:.2f} KB) was successfully sent to Telegram chat ID {self.chat_id}. Your system: {os_info}. Everything is safe and sound.\033[0m")
                else:
                    print(f"\033[91mFailed to send the backup file to Telegram. Something went sideways.\033[0m")
        
        except Exception as e:
            print(f"\033[91mOops! An unexpected error occurred: {e}. Maybe it’s time to check under the hood?\033[0m")
            print(f"\033[93mTip: Make sure the file is accessible, and there are no permission issues. Computers can be a bit picky with permissions!\033[0m")
