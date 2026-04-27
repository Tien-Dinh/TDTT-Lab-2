import requests

API_BASE = "http://localhost:8000"

def signup(email: str, password: str):
    r = requests.post(f"{API_BASE}/auth/signup", json={"email": email, "password": password})
    r.raise_for_status()
    return r.json()

def login(email: str, password: str):
    r = requests.post(f"{API_BASE}/auth/login", json={"email": email, "password": password})
    r.raise_for_status()
    return r.json()

def get_notes(id_token: str, limit: int = 20):
    r = requests.get(
        f"{API_BASE}/notes",
        params={"limit": limit},
        headers={"Authorization": f"Bearer {id_token}"}
    )
    r.raise_for_status()
    return r.json()

def create_note(id_token: str, content: str):
    r = requests.post(
        f"{API_BASE}/notes",
        json={"content": content},
        headers={"Authorization": f"Bearer {id_token}"}
    )
    r.raise_for_status()
    return r.json()

def delete_note_api(id_token: str, note_id: str):
    r = requests.delete(
        f"{API_BASE}/notes/{note_id}",
        headers={"Authorization": f"Bearer {id_token}"}
    )
    r.raise_for_status()
    return r.json()

def update_note_api(id_token: str, note_id: str, content: str):
    r = requests.put(
        f"{API_BASE}/notes/{note_id}",
        json={"content": content},
        headers={"Authorization": f"Bearer {id_token}"}
    )
    r.raise_for_status()
    return r.json()