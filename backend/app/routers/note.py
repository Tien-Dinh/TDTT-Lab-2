from fastapi import APIRouter, Depends, HTTPException, Query
from dependencies.auth import get_current_user
from schemas.note import NoteCreate, NoteResponse
from services.firestore_service import save_note, load_notes, delete_note, update_note

router = APIRouter(prefix="/notes", tags=["notes"])

@router.get("", response_model=list[NoteResponse])
def get_notes(limit: int = Query(default=20, ge=1, le=50), user=Depends(get_current_user)):
    try:
        notes = load_notes(user["uid"], limit=limit)
        return notes
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("")
def create_note(payload: NoteCreate, user=Depends(get_current_user)):
    try:
        save_note(user["uid"], payload.content)
        return {"message": "Tạo ghi chú thành công"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{note_id}")
def delete_note_endpoint(note_id: str, user=Depends(get_current_user)):
    try:
        delete_note(user["uid"], note_id)
        return {"message": "Đã xóa ghi chú"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/{note_id}")
def update_note_endpoint(note_id: str, payload: NoteCreate, user=Depends(get_current_user)):
    try:
        update_note(user["uid"], note_id, payload.content)
        return {"message": "Cập nhật thành công"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))