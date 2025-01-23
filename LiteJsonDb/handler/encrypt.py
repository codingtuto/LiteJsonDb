import base64
import json
import logging
from typing import Any, Dict, Optional
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

class Encryption:
    """
    Handles encryption and decryption of data using either base64 or Fernet.

    This class provides methods to encrypt and decrypt dictionaries using either
    base64 encoding or Fernet symmetric encryption. It supports key derivation
    for Fernet using PBKDF2HMAC.
    """
    def __init__(self, encryption_method: str = 'base64', encryption_key: Optional[str] = None):
        """
        Initializes the Encryption class.

        Args:
            encryption_method (str, optional): The encryption method to use ('base64' or 'fernet').
                Defaults to 'base64'.
            encryption_key (Optional[str], optional): The encryption key to use (required for 'fernet').
                Defaults to None.
        
        Raises:
            ValueError: If encryption_method is 'fernet' and encryption_key is not provided.
        """
        self.encryption_method = encryption_method
        self.encryption_key = encryption_key

        if self.encryption_method == 'fernet':
            if not self.encryption_key:
                raise ValueError("\033[91m#bugs\033[0m Encryption key required for 'fernet'.")

            salt = b"ThisIsASalt"
            kdf = PBKDF2HMAC(
                algorithm=hashes.SHA256(),
                length=32,
                salt=salt,
                iterations=480000,
            )
            key = base64.urlsafe_b64encode(kdf.derive(self.encryption_key.encode('utf-8')))
            self.fernet = Fernet(key)

    def _encrypt(self, data: Dict[str, Any]) -> str:
        """
        Encrypts the given data.

        Args:
            data (Dict[str, Any]): The data to encrypt.

        Returns:
            str: The encrypted data as a string.

        Raises:
            ValueError: If an unsupported encryption method is specified.
        """
        if self.encryption_method == 'base64':
            return self._base64_encrypt(data)
        elif self.encryption_method == 'fernet':
            return self._fernet_encrypt(data)
        else:
            raise ValueError("\033[91m#bugs\033[0m Unsupported encryption method.")

    def _decrypt(self, encoded_data: str) -> Dict[str, Any]:
        """
        Decrypts the given encoded data.

        Args:
            encoded_data (str): The data to decrypt.

        Returns:
            Dict[str, Any]: The decrypted data as a dictionary.

        Raises:
            ValueError: If an unsupported encryption method is specified.
        """
        if self.encryption_method == 'base64':
            return self._base64_decrypt(encoded_data)
        elif self.encryption_method == 'fernet':
            return self._fernet_decrypt(encoded_data)
        else:
            raise ValueError("\033[91m#bugs\033[0m Unsupported encryption method.")

    def _base64_encrypt(self, data: Dict[str, Any]) -> str:
        """
        Encrypts the given data using base64 encoding.

        Args:
            data (Dict[str, Any]): The data to encrypt.

        Returns:
            str: The base64 encoded string.
        """
        json_data = json.dumps(data).encode('utf-8')
        return base64.b64encode(json_data).decode('utf-8')

    def _base64_decrypt(self, encoded_data: str) -> Dict[str, Any]:
        """
        Decrypts the given base64 encoded data.

        Args:
            encoded_data (str): The base64 encoded string.

        Returns:
            Dict[str, Any]: The decrypted data as a dictionary.
        """
        decoded_data = base64.b64decode(encoded_data.encode('utf-8')).decode('utf-8')
        return json.loads(decoded_data)

    def _fernet_encrypt(self, data: Dict[str, Any]) -> str:
        """
        Encrypts the given data using Fernet.

        Args:
            data (Dict[str, Any]): The data to encrypt.

        Returns:
            str: The Fernet encrypted string.
        """
        json_data = json.dumps(data).encode('utf-8')
        return self.fernet.encrypt(json_data).decode('utf-8')

    def _fernet_decrypt(self, encoded_data: str) -> Dict[str, Any]:
        """
        Decrypts the given Fernet encrypted data.

        Args:
            encoded_data (str): The Fernet encrypted string.

        Returns:
            Dict[str, Any]: The decrypted data as a dictionary.

        Raises:
            ValueError: If the decryption fails due to an incorrect key or corrupted data.
        """
        try:
            decoded_data = self.fernet.decrypt(encoded_data.encode('utf-8'))
            return json.loads(decoded_data)
        except Exception as e:
            print("\033[91m#bugs\033[0m Fernet decryption failed.")
            raise ValueError("\033[91m#bugs\033[0m Decryption failed: invalid key or data.")