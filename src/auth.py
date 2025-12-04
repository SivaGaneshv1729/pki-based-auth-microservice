# src/auth.py
import pyotp
import base64
import time

class Authenticator:
    def __init__(self, hex_secret: str):
        self.secret = hex_secret.strip()
        self.base32_secret = self._to_base32()
        self.totp = pyotp.TOTP(self.base32_secret)

    def _to_base32(self):
        # Convert hex string -> bytes -> base32 string
        raw_bytes = bytes.fromhex(self.secret)
        return base64.b32encode(raw_bytes).decode('utf-8')

    def get_code_details(self):
        now = time.time()
        # Calculate remaining time in 30s window
        remaining = int(self.totp.interval - (now % self.totp.interval))
        return self.totp.now(), remaining

    def validate(self, input_code: str):
        # Allow +/- 1 interval (30 seconds)
        return self.totp.verify(input_code, valid_window=1)