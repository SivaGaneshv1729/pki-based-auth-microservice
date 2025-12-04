# src/security.py
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import serialization, hashes
import base64

class CryptoHandler:
    @staticmethod
    def load_priv_key(path: str):
        with open(path, "rb") as f:
            return serialization.load_pem_private_key(f.read(), password=None)

    @staticmethod
    def unlock_data(b64_cipher: str, priv_key) -> str:
        try:
            raw_cipher = base64.b64decode(b64_cipher)
            
            decrypted_bytes = priv_key.decrypt(
                raw_cipher,
                padding.OAEP(
                    mgf=padding.MGF1(algorithm=hashes.SHA256()),
                    algorithm=hashes.SHA256(),
                    label=None
                )
            )
            return decrypted_bytes.decode('utf-8')
        except Exception as e:
            raise RuntimeError(f"Decryption failed: {e}")