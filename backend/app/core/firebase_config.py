import os
import tomllib
import pyrebase
import firebase_admin
from firebase_admin import credentials, firestore

def get_secrets():
    possible_paths = [
        ".streamlit/secrets.toml",
        "../../.streamlit/secrets.toml"
    ]
    for path in possible_paths:
        if os.path.exists(path):
            with open(path, "rb") as f:
                return tomllib.load(f)
    raise FileNotFoundError("Không tìm thấy file secrets.toml, hãy kiểm tra lại!")

def get_pyrebase_auth():
    secrets = get_secrets()
    firebase_cfg = secrets["firebase_client"]
    firebase_app = pyrebase.initialize_app(firebase_cfg)
    return firebase_app.auth()

def init_firebase_admin():
    if not firebase_admin._apps:
        secrets = get_secrets()
        cred_dict = dict(secrets["firebase_admin"])
        cred = credentials.Certificate(cred_dict)
        firebase_admin.initialize_app(cred)

def get_firestore():
    init_firebase_admin()
    return firestore.client()