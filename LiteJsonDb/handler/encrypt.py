import base64
import json
import logging
from typing import Any, Dict, Optional
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

class Encryption:
    def __init__(self, encryption_method: str = 'base64', encryption_key: Optional[str] = None):
        self.encryption_method = encryption_method
        self.encryption_key = encryption_key

        if self.encryption_method == 'fernet':
            if not self.encryption_key:
                raise ValueError("Encryption key must be defined for 'fernet' method.")

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
        if self.encryption_method == 'base64':
            return self._base64_encrypt(data)
        elif self.encryption_method == 'fernet':
            return self._fernet_encrypt(data)
        else:
            raise ValueError("Unsupported encryption method.")

    def _decrypt(self, encoded_data: str) -> Dict[str, Any]:
        if self.encryption_method == 'base64':
            return self._base64_decrypt(encoded_data)
        elif self.encryption_method == 'fernet':
            return self._fernet_decrypt(encoded_data)
        else:
            raise ValueError("Unsupported encryption method.")

    def _base64_encrypt(self, data: Dict[str, Any]) -> str:
        json_data = json.dumps(data).encode('utf-8')
        return base64.b64encode(json_data).decode('utf-8')

    def _base64_decrypt(self, encoded_data: str) -> Dict[str, Any]:
        decoded_data = base64.b64decode(encoded_data.encode('utf-8')).decode('utf-8')
        return json.loads(decoded_data)

    def _fernet_encrypt(self, data: Dict[str, Any]) -> str:
        json_data = json.dumps(data).encode('utf-8')
        return self.fernet.encrypt(json_data).decode('utf-8')

    def _fernet_decrypt(self, encoded_data: str) -> Dict[str, Any]:
        try:
            decoded_data = self.fernet.decrypt(encoded_data.encode('utf-8'))
            return json.loads(decoded_data)
        except Exception as e:
            print("🐛 Error: Unable to decrypt the data. Ensure that the encryption key is correct.")
            raise ValueError("Decryption failed. Please check the provided key and data.")
