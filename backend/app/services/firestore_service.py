from datetime import datetime, timezone
from core.firebase_config import get_firestore
from firebase_admin import firestore

db = get_firestore()

def save_note(uid: str, content: str):
    doc = {
        "content": content,
        "ts": datetime.now(timezone.utc)
    }
    db.collection("users").document(uid).collection("notes").add(doc)

def load_notes(uid: str, limit: int = 20):
    q = (
        db.collection("users")
        .document(uid)
        .collection("notes")
        .order_by("ts", direction=firestore.Query.DESCENDING)
        .limit(limit)
    )

    docs = list(q.stream())
    
    return [
        {
            "id": d.id,
            "content": d.to_dict().get("content", ""),
            "ts": d.to_dict().get("ts")
        }
        for d in docs
    ]

def delete_note(uid: str, note_id: str):
    db.collection("users").document(uid).collection("notes").document(note_id).delete()

def update_note(uid: str, note_id: str, new_content: str):
    doc_ref = db.collection("users").document(uid).collection("notes").document(note_id)
    doc_ref.update({
        "content": new_content,
        "ts": datetime.now(timezone.utc)
    })