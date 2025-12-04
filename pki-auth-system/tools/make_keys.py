# tools/make_keys.py
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization

# Configuration
EXPONENT = 65537
BITS = 4096

print(f"Generating {BITS}-bit RSA keypair...")

key_pair = rsa.generate_private_key(
    public_exponent=EXPONENT,
    key_size=BITS
)

# Export Private
with open("student_private.pem", "wb") as priv_file:
    priv_file.write(key_pair.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    ))

# Export Public
with open("student_public.pem", "wb") as pub_file:
    pub_file.write(key_pair.public_key().public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    ))

print("Keys created successfully.")