# tools/gen_proof.py
import base64
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding

# === UPDATE THIS AFTER COMMITTING ===
GIT_HASH = "PASTE_HASH_HERE"
# ====================================

def main():
    try:
        # Load My Key
        with open("student_private.pem", "rb") as f:
            priv = serialization.load_pem_private_key(f.read(), password=None)

        # Sign Hash
        sig = priv.sign(
            GIT_HASH.encode('utf-8'),
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )

        # Load Instructor Key
        with open("instructor_public.pem", "rb") as f:
            pub = serialization.load_pem_public_key(f.read())

        # Encrypt Signature
        enc_sig = pub.encrypt(
            sig,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )

        print("\n[Encrypted Signature]:")
        print(base64.b64encode(enc_sig).decode('utf-8'))
        print("")

    except Exception as e:
        print("Error:", e)

if _name_ == "_main_":
    main()