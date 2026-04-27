from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class NoteCreate(BaseModel):
    content: str

class NoteResponse(BaseModel):
    id: str
    content: str
    ts: Optional[datetime] = None