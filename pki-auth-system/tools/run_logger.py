import sys
import os
from datetime import datetime, timezone

# Fix path to allow importing from src
# We need to go up one level from 'tools' to the root '/app'
current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(current_dir)
sys.path.append(root_dir)

from src.auth import Authenticator

STORAGE = "/data/seed.txt"
LOG_FILE = "/cron/last_code.txt"

def execute_log():
    if not os.path.exists(STORAGE):
        return

    try:
        with open(STORAGE, "r") as f:
            seed_data = f.read().strip()

        # Generate Code
        auth = Authenticator(seed_data)
        current_otp, _ = auth.get_code_details()
        
        # UTC Timestamp
        now_utc = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
        
        # Print to stdout (captured by cron redirect)
        print(f"{now_utc} - 2FA Code: {current_otp}")

    except Exception as e:
        print(f"Cron Error: {e}")

if __name__ == "__main__":
    execute_log()