# src/server.py
from fastapi import FastAPI
from pydantic import BaseModel
import os
from src.security import CryptoHandler
from src.auth import Authenticator

api = FastAPI()

# Paths & Config
DATA_STORE = "/data/seed.txt"
KEY_LOC = "/app/student_private.pem"

# Request Models
class PayloadIn(BaseModel):
    encrypted_seed: str

class CodeIn(BaseModel):
    code: str

# Helper to read data
def _read_seed():
    if not os.path.exists(DATA_STORE):
        return None
    with open(DATA_STORE, "r") as f:
        return f.read().strip()

@api.post("/decrypt-seed")
def handle_decryption(payload: PayloadIn):
    try:
        pk = CryptoHandler.load_priv_key(KEY_LOC)
        plain_seed = CryptoHandler.unlock_data(payload.encrypted_seed, pk)
        
        # Persist to volume
        with open(DATA_STORE, "w") as f:
            f.write(plain_seed)
        return {"status": "ok"}
    except Exception as e:
        return {"error": str(e)}, 500

@api.get("/generate-2fa")
def handle_generation():
    seed = _read_seed()
    if not seed:
        return {"error": "Seed not decrypted yet"}, 500
    
    auth = Authenticator(seed)
    otp, ttl = auth.get_code_details()
    return {"code": otp, "valid_for": ttl}

@api.post("/verify-2fa")
def handle_verification(payload: CodeIn):
    seed = _read_seed()
    if not seed:
        return {"error": "Seed not decrypted yet"}, 500
        
    auth = Authenticator(seed)
    is_valid = auth.validate(payload.code)
    return {"valid": is_valid}