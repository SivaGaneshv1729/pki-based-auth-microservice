import requests
import json
import sys

# --- CONFIGURATION ---
MY_ID = "23A91A6164"
MY_REPO = "https://github.com/SivaGaneshv1729/pki-based-auth-microservice"
API_ENDPOINT = "https://eajeyq4r3zljoq4rpovy2nthda0vtjqf.lambda-url.ap-south-1.on.aws/"
# ---------------------

def run():
    try:
        with open("student_public.pem", "r") as f:
            pub_key_data = f.read()

        req_body = {
            "student_id": MY_ID,
            "github_repo_url": MY_REPO,
            "public_key": pub_key_data
        }

        print(f"Contacting API for {MY_ID}...")
        resp = requests.post(API_ENDPOINT, json=req_body)
        
        if resp.status_code == 200:
            payload = resp.json()
            if "encrypted_seed" in payload:
                with open("encrypted_seed.txt", "w") as out:
                    out.write(payload["encrypted_seed"])
                print(">> Encrypted seed saved to 'encrypted_seed.txt'")
            else:
                print("!! API Error:", payload)
        else:
            print(f"!! HTTP Error {resp.status_code}: {resp.text}")

    except Exception as e:
        print(f"!! Critical Failure: {e}")

if _name_ == "_main_":
    run()