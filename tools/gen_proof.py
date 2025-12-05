# tools/gen_proof.py
import sys

print(">> Script started...")

try:
    import base64
    print(">> Imported base64")
    from cryptography.hazmat.primitives import hashes, serialization
    from cryptography.hazmat.primitives.asymmetric import padding
    print(">> Imported cryptography")
except ImportError as e:
    print(f"!! ERROR: Missing libraries. Run 'pip install cryptography'. Details: {e}")
    sys.exit(1)

# === UPDATE THIS AFTER COMMITTING ===
GIT_HASH = "3561811cfced36123af91e7046b8fb61cc871cf1"  # <--- Make sure he pasted the hash here!
# ====================================

def main():
    print(f">> using GIT_HASH: {GIT_HASH}")
    
    try:
        # Load My Key
        print(">> Attempting to load 'student_private.pem'...")
        with open("student_private.pem", "rb") as f:
            priv = serialization.load_pem_private_key(f.read(), password=None)
        print(">> Private key loaded.")

        # Sign Hash
        print(">> Signing hash...")
        sig = priv.sign(
            GIT_HASH.encode('utf-8'),
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        print(">> Hash signed.")

        # Load Instructor Key
        print(">> Attempting to load 'instructor_public.pem'...")
        with open("instructor_public.pem", "rb") as f:
            pub = serialization.load_pem_public_key(f.read())
        print(">> Instructor public key loaded.")

        # Encrypt Signature
        print(">> Encrypting signature...")
        enc_sig = pub.encrypt(
            sig,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )

        print("\n[Encrypted Signature] (COPY THIS BELOW):")
        print("---------------------------------------------------")
        print(base64.b64encode(enc_sig).decode('utf-8'))
        print("---------------------------------------------------")

    except FileNotFoundError as e:
        print(f"\n!! FILE ERROR: Could not find a key file.")
        print(f"!! Details: {e}")
        print("!! HINT: Are you running this from the ROOT folder?")
        print("!! Try running: python tools/gen_proof.py")
    except Exception as e:
        print(f"\n!! UNEXPECTED ERROR: {e}")

if __name__ == "__main__":
    main()